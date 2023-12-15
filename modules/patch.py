import os
import torch
import time
import math
import bluemoon.ldm_patched.modules.model_base
import bluemoon.ldm_patched.ldm.modules.diffusionmodules.openaimodel
import bluemoon.ldm_patched.modules.model_management
import modules.anisotropic as anisotropic
import bluemoon.ldm_patched.ldm.modules.attention
import bluemoon.ldm_patched.k_diffusion.sampling
import bluemoon.ldm_patched.modules.sd1_clip
import modules.inpaint_worker as inpaint_worker
import bluemoon.ldm_patched.ldm.modules.diffusionmodules.openaimodel
import bluemoon.ldm_patched.ldm.modules.diffusionmodules.model
import bluemoon.ldm_patched.modules.sd
import bluemoon.ldm_patched.controlnet.cldm
import bluemoon.ldm_patched.modules.model_patcher
import bluemoon.ldm_patched.modules.samplers
import bluemoon.ldm_patched.modules.args_parser
import modules.advanced_parameters as advanced_parameters
import warnings
import safetensors.torch
import modules.constants as constants

from bluemoon.ldm_patched.modules.samplers import calc_cond_uncond_batch
from bluemoon.ldm_patched.k_diffusion.sampling import BatchedBrownianTree
from bluemoon.ldm_patched.ldm.modules.diffusionmodules.openaimodel import forward_timestep_embed, apply_control


sharpness = 2.0

adm_scaler_end = 0.3
positive_adm_scale = 1.5
negative_adm_scale = 0.8

adaptive_cfg = 7.0
global_diffusion_progress = 0
eps_record = None


def calculate_weight_patched(self, patches, weight, key):
    for p in patches:
        alpha = p[0]
        v = p[1]
        strength_model = p[2]

        if strength_model != 1.0:
            weight *= strength_model

        if isinstance(v, list):
            v = (self.calculate_weight(v[1:], v[0].clone(), key),)

        if len(v) == 1:
            patch_type = "diff"
        elif len(v) == 2:
            patch_type = v[0]
            v = v[1]

        if patch_type == "diff":
            w1 = v[0]
            if alpha != 0.0:
                if w1.shape != weight.shape:
                    print("WARNING SHAPE MISMATCH {} WEIGHT NOT MERGED {} != {}".format(key, w1.shape, weight.shape))
                else:
                    weight += alpha * bluemoon.ldm_patched.modules.model_management.cast_to_device(w1, weight.device, weight.dtype)
        elif patch_type == "lora":
            mat1 = bluemoon.ldm_patched.modules.model_management.cast_to_device(v[0], weight.device, torch.float32)
            mat2 = bluemoon.ldm_patched.modules.model_management.cast_to_device(v[1], weight.device, torch.float32)
            if v[2] is not None:
                alpha *= v[2] / mat2.shape[0]
            if v[3] is not None:
                mat3 = bluemoon.ldm_patched.modules.model_management.cast_to_device(v[3], weight.device, torch.float32)
                final_shape = [mat2.shape[1], mat2.shape[0], mat3.shape[2], mat3.shape[3]]
                mat2 = torch.mm(mat2.transpose(0, 1).flatten(start_dim=1),
                                mat3.transpose(0, 1).flatten(start_dim=1)).reshape(final_shape).transpose(0, 1)
            try:
                weight += (alpha * torch.mm(mat1.flatten(start_dim=1), mat2.flatten(start_dim=1))).reshape(
                    weight.shape).type(weight.dtype)
            except Exception as e:
                print("ERROR", key, e)
        elif patch_type == "BlueMoon":
            w1 = bluemoon.ldm_patched.modules.model_management.cast_to_device(v[0], weight.device, torch.float32)
            w_min = bluemoon.ldm_patched.modules.model_management.cast_to_device(v[1], weight.device, torch.float32)
            w_max = bluemoon.ldm_patched.modules.model_management.cast_to_device(v[2], weight.device, torch.float32)
            w1 = (w1 / 255.0) * (w_max - w_min) + w_min
            if alpha != 0.0:
                if w1.shape != weight.shape:
                    print("WARNING SHAPE MISMATCH {} BlueMoon AI WEIGHT NOT MERGED {} != {}".format(key, w1.shape, weight.shape))
                else:
                    weight += alpha * bluemoon.ldm_patched.modules.model_management.cast_to_device(w1, weight.device, weight.dtype)
        elif patch_type == "lokr":
            w1 = v[0]
            w2 = v[1]
            w1_a = v[3]
            w1_b = v[4]
            w2_a = v[5]
            w2_b = v[6]
            t2 = v[7]
            dim = None

            if w1 is None:
                dim = w1_b.shape[0]
                w1 = torch.mm(bluemoon.ldm_patched.modules.model_management.cast_to_device(w1_a, weight.device, torch.float32),
                              bluemoon.ldm_patched.modules.model_management.cast_to_device(w1_b, weight.device, torch.float32))
            else:
                w1 = bluemoon.ldm_patched.modules.model_management.cast_to_device(w1, weight.device, torch.float32)

            if w2 is None:
                dim = w2_b.shape[0]
                if t2 is None:
                    w2 = torch.mm(bluemoon.ldm_patched.modules.model_management.cast_to_device(w2_a, weight.device, torch.float32),
                                  bluemoon.ldm_patched.modules.model_management.cast_to_device(w2_b, weight.device, torch.float32))
                else:
                    w2 = torch.einsum('i j k l, j r, i p -> p r k l',
                                      bluemoon.ldm_patched.modules.model_management.cast_to_device(t2, weight.device, torch.float32),
                                      bluemoon.ldm_patched.modules.model_management.cast_to_device(w2_b, weight.device, torch.float32),
                                      bluemoon.ldm_patched.modules.model_management.cast_to_device(w2_a, weight.device, torch.float32))
            else:
                w2 = bluemoon.ldm_patched.modules.model_management.cast_to_device(w2, weight.device, torch.float32)

            if len(w2.shape) == 4:
                w1 = w1.unsqueeze(2).unsqueeze(2)
            if v[2] is not None and dim is not None:
                alpha *= v[2] / dim

            try:
                weight += alpha * torch.kron(w1, w2).reshape(weight.shape).type(weight.dtype)
            except Exception as e:
                print("ERROR", key, e)
        elif patch_type == "loha":
            w1a = v[0]
            w1b = v[1]
            if v[2] is not None:
                alpha *= v[2] / w1b.shape[0]
            w2a = v[3]
            w2b = v[4]
            if v[5] is not None:  # cp decomposition
                t1 = v[5]
                t2 = v[6]
                m1 = torch.einsum('i j k l, j r, i p -> p r k l',
                                  bluemoon.ldm_patched.modules.model_management.cast_to_device(t1, weight.device, torch.float32),
                                  bluemoon.ldm_patched.modules.model_management.cast_to_device(w1b, weight.device, torch.float32),
                                  bluemoon.ldm_patched.modules.model_management.cast_to_device(w1a, weight.device, torch.float32))

                m2 = torch.einsum('i j k l, j r, i p -> p r k l',
                                  bluemoon.ldm_patched.modules.model_management.cast_to_device(t2, weight.device, torch.float32),
                                  bluemoon.ldm_patched.modules.model_management.cast_to_device(w2b, weight.device, torch.float32),
                                  bluemoon.ldm_patched.modules.model_management.cast_to_device(w2a, weight.device, torch.float32))
            else:
                m1 = torch.mm(bluemoon.ldm_patched.modules.model_management.cast_to_device(w1a, weight.device, torch.float32),
                              bluemoon.ldm_patched.modules.model_management.cast_to_device(w1b, weight.device, torch.float32))
                m2 = torch.mm(bluemoon.ldm_patched.modules.model_management.cast_to_device(w2a, weight.device, torch.float32),
                              bluemoon.ldm_patched.modules.model_management.cast_to_device(w2b, weight.device, torch.float32))

            try:
                weight += (alpha * m1 * m2).reshape(weight.shape).type(weight.dtype)
            except Exception as e:
                print("ERROR", key, e)
        elif patch_type == "glora":
            if v[4] is not None:
                alpha *= v[4] / v[0].shape[0]

            a1 = bluemoon.ldm_patched.modules.model_management.cast_to_device(v[0].flatten(start_dim=1), weight.device, torch.float32)
            a2 = bluemoon.ldm_patched.modules.model_management.cast_to_device(v[1].flatten(start_dim=1), weight.device, torch.float32)
            b1 = bluemoon.ldm_patched.modules.model_management.cast_to_device(v[2].flatten(start_dim=1), weight.device, torch.float32)
            b2 = bluemoon.ldm_patched.modules.model_management.cast_to_device(v[3].flatten(start_dim=1), weight.device, torch.float32)

            weight += ((torch.mm(b2, b1) + torch.mm(torch.mm(weight.flatten(start_dim=1), a2), a1)) * alpha).reshape(weight.shape).type(weight.dtype)
        else:
            print("patch type not recognized", patch_type, key)

    return weight


class BrownianTreeNoiseSamplerPatched:
    transform = None
    tree = None

    @staticmethod
    def global_init(x, sigma_min, sigma_max, seed=None, transform=lambda x: x, cpu=False):
        if bluemoon.ldm_patched.modules.model_management.directml_enabled:
            cpu = True

        t0, t1 = transform(torch.as_tensor(sigma_min)), transform(torch.as_tensor(sigma_max))

        BrownianTreeNoiseSamplerPatched.transform = transform
        BrownianTreeNoiseSamplerPatched.tree = BatchedBrownianTree(x, t0, t1, seed, cpu=cpu)

    def __init__(self, *args, **kwargs):
        pass

    @staticmethod
    def __call__(sigma, sigma_next):
        transform = BrownianTreeNoiseSamplerPatched.transform
        tree = BrownianTreeNoiseSamplerPatched.tree

        t0, t1 = transform(torch.as_tensor(sigma)), transform(torch.as_tensor(sigma_next))
        return tree(t0, t1) / (t1 - t0).abs().sqrt()


def compute_cfg(uncond, cond, cfg_scale, t):
    global adaptive_cfg

    mimic_cfg = float(adaptive_cfg)
    real_cfg = float(cfg_scale)

    real_eps = uncond + real_cfg * (cond - uncond)

    if cfg_scale > adaptive_cfg:
        mimicked_eps = uncond + mimic_cfg * (cond - uncond)
        return real_eps * t + mimicked_eps * (1 - t)
    else:
        return real_eps


def patched_sampling_function(model, x, timestep, uncond, cond, cond_scale, model_options=None, seed=None):
    global eps_record

    if math.isclose(cond_scale, 1.0):
        final_x0 = calc_cond_uncond_batch(model, cond, None, x, timestep, model_options)[0]
        if eps_record is not None:
            eps_record = ((x - final_x0) / timestep).cpu()

        return final_x0
    positive_x0, negative_x0 = calc_cond_uncond_batch(model, cond, uncond, x, timestep, model_options)

    positive_eps = x - positive_x0
    negative_eps = x - negative_x0
    sigma = timestep

    alpha = 0.001 * sharpness * global_diffusion_progress

    positive_eps_degraded = anisotropic.adaptive_anisotropic_filter(x=positive_eps, g=positive_x0)
    positive_eps_degraded_weighted = positive_eps_degraded * alpha + positive_eps * (1.0 - alpha)

    final_eps = compute_cfg(uncond=negative_eps, cond=positive_eps_degraded_weighted,
                            cfg_scale=cond_scale, t=global_diffusion_progress)

    if eps_record is not None:
        eps_record = (final_eps / timestep).cpu()

    return x - final_eps


def round_to_64(x):
    h = float(x)
    h = h / 64.0
    h = round(h)
    h = int(h)
    h = h * 64
    return h


def sdxl_encode_adm_patched(self, **kwargs):
    global positive_adm_scale, negative_adm_scale

    clip_pooled = bluemoon.ldm_patched.modules.model_base.sdxl_pooled(kwargs, self.noise_augmentor)
    width = kwargs.get("width", 1024)
    height = kwargs.get("height", 1024)
    target_width = width
    target_height = height

    if kwargs.get("prompt_type", "") == "negative":
        width = float(width) * negative_adm_scale
        height = float(height) * negative_adm_scale
    elif kwargs.get("prompt_type", "") == "positive":
        width = float(width) * positive_adm_scale
        height = float(height) * positive_adm_scale

    def embedder(number_list):
        h = torch.tensor(number_list, dtype=torch.float32)
        h = self.embedder(h)
        h = torch.flatten(h).unsqueeze(dim=0).repeat(clip_pooled.shape[0], 1)
        return h

    width, height = round_to_64(width), round_to_64(height)
    target_width, target_height = round_to_64(target_width), round_to_64(target_height)

    adm_emphasized = embedder([height, width, 0, 0, target_height, target_width])
    adm_consistent = embedder([target_height, target_width, 0, 0, target_height, target_width])

    clip_pooled = clip_pooled.to(adm_emphasized)
    final_adm = torch.cat((clip_pooled, adm_emphasized, clip_pooled, adm_consistent), dim=1)

    return final_adm


def encode_token_weights_patched_with_a1111_method(self, token_weight_pairs):
    to_encode = list()
    max_token_len = 0
    has_weights = False
    for x in token_weight_pairs:
        tokens = list(map(lambda a: a[0], x))
        max_token_len = max(len(tokens), max_token_len)
        has_weights = has_weights or not all(map(lambda a: a[1] == 1.0, x))
        to_encode.append(tokens)

    sections = len(to_encode)
    if has_weights or sections == 0:
        to_encode.append(bluemoon.ldm_patched.modules.sd1_clip.gen_empty_tokens(self.special_tokens, max_token_len))

    out, pooled = self.encode(to_encode)
    if pooled is not None:
        first_pooled = pooled[0:1].to(bluemoon.ldm_patched.modules.model_management.intermediate_device())
    else:
        first_pooled = pooled

    output = []
    for k in range(0, sections):
        z = out[k:k + 1]
        if has_weights:
            original_mean = z.mean()
            z_empty = out[-1]
            for i in range(len(z)):
                for j in range(len(z[i])):
                    weight = token_weight_pairs[k][j][1]
                    if weight != 1.0:
                        z[i][j] = (z[i][j] - z_empty[j]) * weight + z_empty[j]
            new_mean = z.mean()
            z = z * (original_mean / new_mean)
        output.append(z)

    if len(output) == 0:
        return out[-1:].to(bluemoon.ldm_patched.modules.model_management.intermediate_device()), first_pooled
    return torch.cat(output, dim=-2).to(bluemoon.ldm_patched.modules.model_management.intermediate_device()), first_pooled


def patched_KSamplerX0Inpaint_forward(self, x, sigma, uncond, cond, cond_scale, denoise_mask, model_options={}, seed=None):
    if inpaint_worker.current_task is not None:
        latent_processor = self.inner_model.inner_model.process_latent_in
        inpaint_latent = latent_processor(inpaint_worker.current_task.latent).to(x)
        inpaint_mask = inpaint_worker.current_task.latent_mask.to(x)

        if getattr(self, 'energy_generator', None) is None:
            # avoid bad results by using different seeds.
            self.energy_generator = torch.Generator(device='cpu').manual_seed((seed + 1) % constants.MAX_SEED)

        energy_sigma = sigma.reshape([sigma.shape[0]] + [1] * (len(x.shape) - 1))
        current_energy = torch.randn(
            x.size(), dtype=x.dtype, generator=self.energy_generator, device="cpu").to(x) * energy_sigma
        x = x * inpaint_mask + (inpaint_latent + current_energy) * (1.0 - inpaint_mask)

        out = self.inner_model(x, sigma,
                               cond=cond,
                               uncond=uncond,
                               cond_scale=cond_scale,
                               model_options=model_options,
                               seed=seed)

        out = out * inpaint_mask + inpaint_latent * (1.0 - inpaint_mask)
    else:
        out = self.inner_model(x, sigma,
                               cond=cond,
                               uncond=uncond,
                               cond_scale=cond_scale,
                               model_options=model_options,
                               seed=seed)
    return out


def timed_adm(y, timesteps):
    if isinstance(y, torch.Tensor) and int(y.dim()) == 2 and int(y.shape[1]) == 5632:
        y_mask = (timesteps > 999.0 * (1.0 - float(adm_scaler_end))).to(y)[..., None]
        y_with_adm = y[..., :2816].clone()
        y_without_adm = y[..., 2816:].clone()
        return y_with_adm * y_mask + y_without_adm * (1.0 - y_mask)
    return y


def patched_cldm_forward(self, x, hint, timesteps, context, y=None, **kwargs):
    t_emb = bluemoon.ldm_patched.ldm.modules.diffusionmodules.openaimodel.timestep_embedding(timesteps, self.model_channels, repeat_only=False).to(x.dtype)
    emb = self.time_embed(t_emb)

    guided_hint = self.input_hint_block(hint, emb, context)

    y = timed_adm(y, timesteps)

    outs = []

    hs = []
    if self.num_classes is not None:
        assert y.shape[0] == x.shape[0]
        emb = emb + self.label_emb(y)

    h = x
    for module, zero_conv in zip(self.input_blocks, self.zero_convs):
        if guided_hint is not None:
            h = module(h, emb, context)
            h += guided_hint
            guided_hint = None
        else:
            h = module(h, emb, context)
        outs.append(zero_conv(h, emb, context))

    h = self.middle_block(h, emb, context)
    outs.append(self.middle_block_out(h, emb, context))

    if advanced_parameters.controlnet_softness > 0:
        for i in range(10):
            k = 1.0 - float(i) / 9.0
            outs[i] = outs[i] * (1.0 - advanced_parameters.controlnet_softness * k)

    return outs


def patched_unet_forward(self, x, timesteps=None, context=None, y=None, control=None, transformer_options={}, **kwargs):
    global global_diffusion_progress

    self.current_step = 1.0 - timesteps.to(x) / 999.0
    global_diffusion_progress = float(self.current_step.detach().cpu().numpy().tolist()[0])

    y = timed_adm(y, timesteps)

    transformer_options["original_shape"] = list(x.shape)
    transformer_options["transformer_index"] = 0
    transformer_patches = transformer_options.get("patches", {})

    num_video_frames = kwargs.get("num_video_frames", self.default_num_video_frames)
    image_only_indicator = kwargs.get("image_only_indicator", self.default_image_only_indicator)
    time_context = kwargs.get("time_context", None)

    assert (y is not None) == (
            self.num_classes is not None
    ), "must specify y if and only if the model is class-conditional"
    hs = []
    t_emb = bluemoon.ldm_patched.ldm.modules.diffusionmodules.openaimodel.timestep_embedding(timesteps, self.model_channels, repeat_only=False).to(x.dtype)
    emb = self.time_embed(t_emb)

    if self.num_classes is not None:
        assert y.shape[0] == x.shape[0]
        emb = emb + self.label_emb(y)

    h = x
    for id, module in enumerate(self.input_blocks):
        transformer_options["block"] = ("input", id)
        h = forward_timestep_embed(module, h, emb, context, transformer_options, time_context=time_context, num_video_frames=num_video_frames, image_only_indicator=image_only_indicator)
        h = apply_control(h, control, 'input')
        if "input_block_patch" in transformer_patches:
            patch = transformer_patches["input_block_patch"]
            for p in patch:
                h = p(h, transformer_options)

        hs.append(h)
        if "input_block_patch_after_skip" in transformer_patches:
            patch = transformer_patches["input_block_patch_after_skip"]
            for p in patch:
                h = p(h, transformer_options)

    transformer_options["block"] = ("middle", 0)
    h = forward_timestep_embed(self.middle_block, h, emb, context, transformer_options, time_context=time_context, num_video_frames=num_video_frames, image_only_indicator=image_only_indicator)
    h = apply_control(h, control, 'middle')

    for id, module in enumerate(self.output_blocks):
        transformer_options["block"] = ("output", id)
        hsp = hs.pop()
        hsp = apply_control(hsp, control, 'output')

        if "output_block_patch" in transformer_patches:
            patch = transformer_patches["output_block_patch"]
            for p in patch:
                h, hsp = p(h, hsp, transformer_options)

        h = torch.cat([h, hsp], dim=1)
        del hsp
        if len(hs) > 0:
            output_shape = hs[-1].shape
        else:
            output_shape = None
        h = forward_timestep_embed(module, h, emb, context, transformer_options, output_shape, time_context=time_context, num_video_frames=num_video_frames, image_only_indicator=image_only_indicator)
    h = h.type(x.dtype)
    if self.predict_codebook_ids:
        return self.id_predictor(h)
    else:
        return self.out(h)


def patched_load_models_gpu(*args, **kwargs):
    execution_start_time = time.perf_counter()
    y = bluemoon.ldm_patched.modules.model_management.load_models_gpu_origin(*args, **kwargs)
    moving_time = time.perf_counter() - execution_start_time
    if moving_time > 0.1:
        print(f'[BlueMoon AI Model Management] Moving model(s) has taken {moving_time:.2f} seconds')
    return y


def build_loaded(module, loader_name):
    original_loader_name = loader_name + '_origin'

    if not hasattr(module, original_loader_name):
        setattr(module, original_loader_name, getattr(module, loader_name))

    original_loader = getattr(module, original_loader_name)

    def loader(*args, **kwargs):
        result = None
        try:
            result = original_loader(*args, **kwargs)
        except Exception as e:
            result = None
            exp = str(e) + '\n'
            for path in list(args) + list(kwargs.values()):
                if isinstance(path, str):
                    if os.path.exists(path):
                        exp += f'File corrupted: {path} \n'
                        corrupted_backup_file = path + '.corrupted'
                        if os.path.exists(corrupted_backup_file):
                            os.remove(corrupted_backup_file)
                        os.replace(path, corrupted_backup_file)
                        if os.path.exists(path):
                            os.remove(path)
                        exp += f'BlueMoon AI has tried to move the corrupted file to {corrupted_backup_file} \n'
                        exp += f'You may try again now and BlueMoon AI will download models again. \n'
            raise ValueError(exp)
        return result

    setattr(module, loader_name, loader)
    return


def patch_all():
    if not hasattr(bluemoon.ldm_patched.modules.model_management, 'load_models_gpu_origin'):
        bluemoon.ldm_patched.modules.model_management.load_models_gpu_origin = bluemoon.ldm_patched.modules.model_management.load_models_gpu

    bluemoon.ldm_patched.modules.model_management.load_models_gpu = patched_load_models_gpu
    bluemoon.ldm_patched.modules.model_patcher.ModelPatcher.calculate_weight = calculate_weight_patched
    bluemoon.ldm_patched.controlnet.cldm.ControlNet.forward = patched_cldm_forward
    bluemoon.ldm_patched.ldm.modules.diffusionmodules.openaimodel.UNetModel.forward = patched_unet_forward
    bluemoon.ldm_patched.modules.model_base.SDXL.encode_adm = sdxl_encode_adm_patched
    bluemoon.ldm_patched.modules.sd1_clip.ClipTokenWeightEncoder.encode_token_weights = encode_token_weights_patched_with_a1111_method
    bluemoon.ldm_patched.modules.samplers.KSamplerX0Inpaint.forward = patched_KSamplerX0Inpaint_forward
    bluemoon.ldm_patched.k_diffusion.sampling.BrownianTreeNoiseSampler = BrownianTreeNoiseSamplerPatched
    bluemoon.ldm_patched.modules.samplers.sampling_function = patched_sampling_function

    warnings.filterwarnings(action='ignore', module='torchsde')

    build_loaded(safetensors.torch, 'load_file')
    build_loaded(torch, 'load')

    return
