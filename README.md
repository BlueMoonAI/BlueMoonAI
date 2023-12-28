
![Web_Photo_Editor](https://github.com/BlueMoonAI/BlueMoonAI/assets/138202531/4af70b17-5349-478c-b3fb-956139e8ae75)

<div align="center">

# BlueMoonAI: Unleash Your Creative Potential

[![Python 3.8](https://img.shields.io/badge/Python-3.8-blue)](https://www.python.org/downloads/release/python-380/)
[![Python 3.9](https://img.shields.io/badge/Python-3.9-blue)](https://www.python.org/downloads/release/python-390/)
[![Python 3.10](https://img.shields.io/badge/Python-3.10-blue)](https://www.python.org/downloads/release/python-3100/)
[![Python 3.11](https://img.shields.io/badge/Python-3.11-blue)](https://www.python.org/downloads/release/python-3110/)
[![CodeQL](https://github.com/BlueMoonAI/BlueMoonAI/actions/workflows/github-code-scanning/codeql/badge.svg)](https://github.com/BlueMoonAI/BlueMoonAI/actions/workflows/github-code-scanning/codeql)
[![GitHub issues](https://img.shields.io/github/issues/BlueMoonAI/BlueMoonAI)](https://github.com/BlueMoonAI/BlueMoonAI/issues)
[![GitHub pull requests](https://img.shields.io/github/issues-pr/BlueMoonAI/BlueMoonAI)](https://github.com/BlueMoonAI/BlueMoonAI/pulls)
[![Stable Diffusion](https://img.shields.io/badge/Stable%20Diffusion-Yes-brightgreen)](https://www.bluemoonai.com/stable-diffusion/)
[![Powered by Gradio](https://img.shields.io/badge/Powered%20by-Gradio-blue)](https://www.gradio.app/)
[![Creativity Unleashed](https://img.shields.io/badge/Creativity-Unleashed-orange)](https://www.bluemoonai.com/)
[![Photorealistic Images](https://img.shields.io/badge/Images-Photorealistic-green)](https://www.bluemoonai.com/gallery/)
[![License](https://img.shields.io/github/license/BlueMoonAI/BlueMoonAI)](https://github.com/BlueMoonAI/BlueMoonAI/blob/main/LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/BlueMoonAI/BlueMoonAI)](https://github.com/BlueMoonAI/BlueMoonAI/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/BlueMoonAI/BlueMoonAI)](https://github.com/BlueMoonAI/BlueMoonAI/network/members)
[![GitHub watchers](https://img.shields.io/github/watchers/BlueMoonAI/BlueMoonAI)](https://github.com/BlueMoonAI/BlueMoonAI/watchers)
[![GitHub last commit](https://img.shields.io/github/last-commit/BlueMoonAI/BlueMoonAI)](https://github.com/BlueMoonAI/BlueMoonAI/commits/main)
[![GitHub contributors](https://img.shields.io/github/contributors/BlueMoonAI/BlueMoonAI)](https://github.com/BlueMoonAI/BlueMoonAI/graphs/contributors)
[![Popularity](https://komarev.com/ghpvc/?username=BlueMoonAI&label=Popularity)](https://github.com/BlueMoonAI/BlueMoonAI)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/BlueMoonAI/BlueMoonAI/blob/main/bluemoonai_colab.ipynb)
<a href="https://www.patreon.com/bluemoonai/membership" target="_blank">
  <img src="https://img.shields.io/badge/Support%20Us-Donate-%23FF424D.svg" alt="Donate to Bluemoon AI on Patreon">
</a>

</div>

BlueMoon AI stands at the forefront as a latent text-to-image diffusion model, skillfully crafting photo-realistic images from diverse textual inputs. It not only generates stunning imagery but also fosters autonomous creativity, empowering individuals worldwide to effortlessly create captivating art within moments. (Powered by [Gradio](https://www.gradio.app/))

Don't forget to give the project a star ⭐, if you find it useful! and fork this repository if you want to contribute!

- **Automated Optimization**: BlueMoonAI incorporates advanced inner optimizations and quality enhancements, eliminating the need for users to grapple with complex technical parameters.
- **Intuitive Interface**: The user-friendly interface allows users to generate images with a single click. The intuitive design enables users to create images with ease.
- **Unparalleled Quality**: BlueMoonAI produces high-quality images with a resolution of up to 1024x1024. The images are comparable to those produced by the state-of-the-art diffusion models.
- **Unlimited Creativity**: BlueMoonAI is capable of generating images from a wide range of textual inputs, including but not limited to single words, sentences, and paragraphs. The model can also generate images from a combination of text and images.
- **Unrestricted Access**: BlueMoonAI is free to use and open-source. The model is available to everyone, and the source code is available on GitHub.
- **Uncompromised Security**: BlueMoonAI is a client-side application. The model runs locally on your device, and your data will not be uploaded to any server.
- **Unparalleled Performance**: BlueMoonAI is optimized for performance. The model is capable of generating images at a rate of lightning speed.
- **Unparalleled Compatibility**: BlueMoonAI is compatible with a wide range of devices, including but not limited to Windows, Linux, and Mac with a wide range of devices with gpu
- **Simplified Installation**: Experience a streamlined installation process. From the moment you press "download" to generating the inaugural image, it demands fewer than three mouse clicks. The minimal GPU memory requirement stands at 4GB (Nvidia).

Create exquisite images effortlessly with our AI Image Generator (Text to Image) – all for free.

Let Your Creativity Flow.



## Table of Contents

- [BlueMoonAI: Unleash Your Creative Potential](#bluemoonai-unleash-your-creative-potential)
- [Installing BlueMoonAI](#installing-bluemoonai)
  - [Run in Colab](#run-in-colab)
  - [Linux (Using Anaconda)](#linux-using-anaconda)
  - [Linux (Using Python Venv)](#linux-using-python-venv)
  - [Linux (Using native system Python)](#linux-using-native-system-python)
  - [Linux (AMD GPUs)](#linux-amd-gpus)
  - [Windows(AMD GPUs)](#windowsamd-gpus)
  - [Mac](#mac)
  - [Docker](#docker)
- [Contributing](#contributing)
- [Code of Conduct](#code-of-conduct)
- [Minimal Requirement](#minimal-requirement)
- [Default Models](#default-models)
- [Customization](#customization)
  - [All CMD Flags](#all-cmd-flags)
  - [NSFW Blackout](#nsfw-blackout)
- [Update Log](#update-log)
- [Localization/Translation](#localizationtranslation)
- [Happy Creativity! ❤️](#happy-creativity-)


## [Installing BlueMoonAI](#download)

### Run in Colab

<a href="https://colab.research.google.com/github/BlueMoonAI/BlueMoonAI/blob/main/bluemoonai_colab.ipynb" target="_parent">
  <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab" style="width: 150px; height: 25px;">
</a>

***Tested and works!**

### Linux (Using Anaconda)
Note that the [minimal requirement](#minimal-requirement) for different platforms is different.

If you want to use Anaconda/Miniconda, you can

    git clone https://github.com/BlueMoonAI/BlueMoonAI.git
    cd BlueMoonAI
    conda env create -f environment.yaml
    conda activate BlueMoonAI
    pip install -r requirements.txt

Then download the models: download [default models](#models) to the folder "BlueMoonAI\models\checkpoints". **Or let BlueMoonAI automatically download the models** using the launcher:

    conda activate BlueMoonAI
    python launcher.py

Or if you want to open a remote port, use

    conda activate BlueMoonAI
    python launcher.py --listen

Use `python launcher.py --preset anime` or `python launcher.py --preset realistic` for BlueMoonAI Anime/Realistic Edition.

### Linux (Using Python Venv)
Note that the [minimal requirement](#minimal-requirement) for different platforms is different.

Your Linux needs to have **Python 3.10** installed, and lets say your Python can be called with command **python3** with your venv system working, you can

    git clone https://github.com/BlueMoonAI/BlueMoonAI.git
    cd BlueMoonAI
    python3 -m venv BlueMoonAI_env
    source BlueMoonAI_env/bin/activate
    pip install -r requirements.txt

See the above sections for model downloads. You can launch the software with:

    source BlueMoonAI_env/bin/activate
    python launcher.py

Or if you want to open a remote port, use

    source BlueMoonAI_env/bin/activate
    python launcher.py --listen

Use `python launcher.py --preset anime` or `python launcher.py --preset realistic` for BlueMoonAI Anime/Realistic Edition.

### Linux (Using native system Python)
Note that the [minimal requirement](#minimal-requirement) for different platforms is different.

If you know what you are doing, and your Linux already has **Python 3.10** installed, and your Python can be called with command **python3** (and Pip with **pip3**), you can

    git clone https://github.com/BlueMoonAI/BlueMoonAI.git
    cd BlueMoonAI
    pip3 install -r requirements.txt

See the above sections for model downloads. You can launch the software with:

    python3 launcher.py

Or if you want to open a remote port, use

    python3 launcher.py --listen

Use `python launcher.py --preset anime` or `python launcher.py --preset realistic` for BlueMoonAI Anime/Realistic Edition.

### Linux (AMD GPUs)
Note that the [minimal requirement](#minimal-requirement) for different platforms is different.

Same with the above instructions. You need to change torch to AMD version

    pip uninstall torch torchvision torchaudio torchtext functorch xformers 
    pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/rocm5.6

AMD is not intensively tested, however. The AMD support is in beta.

Use `python launcher.py --preset anime` or `python launcher.py --preset realistic` for BlueMoonAI Anime/Realistic Edition.

### Windows(AMD GPUs)
Note that the [minimal requirement](#minimal-requirement) for different platforms is different.

AMD is not intensively tested, however. The AMD support is in beta.

For AMD, use `python launcher.py --directml --preset anime` or `python launcher.py --directml --preset realistic` for BlueMoonAI Anime/Realistic Edition.

### Mac
Note that the [minimal requirement](#minimal-requirement) for different platforms is different.

Mac is not intensively tested. Below is an unofficial guideline for using Mac. You can discuss problems [here](https://github.com/BlueMoonAI/BlueMoonAI/).

You can install BlueMoonAI on Apple Mac silicon (M1 or M2) with macOS 'Catalina' or a newer version. BlueMoonAI runs on Apple silicon computers via [PyTorch](https://pytorch.org/get-started/locally/) MPS device acceleration. Mac Silicon computers don't come with a dedicated graphics card, resulting in significantly longer image processing times compared to computers with dedicated graphics cards.

1. Install the conda package manager and pytorch nightly. Read the [Accelerated PyTorch training on Mac](https://developer.apple.com/metal/pytorch/) Apple Developer guide for instructions. Make sure pytorch recognizes your MPS device.
1. Open the macOS Terminal app and clone this repository with `git clone https://github.com/BlueMoonAI/BlueMoonAI.git`.
1. Change to the new BlueMoonAI directory, `cd BlueMoonAI`.
1. Create a new conda environment, `conda env create -f environment.yaml`.
1. Activate your new conda environment, `conda activate BlueMoonAI`.
1. Install the packages required by BlueMoonAI, `pip install -r requirements.txt`.
1. Launch BlueMoonAI by running `python launcher.py`. (Some Mac M2 users may need `python launcher.py --disable-offload-from-vram` to speed up model loading/unloading.) The first time you run BlueMoonAI, it will automatically download the Stable Diffusion SDXL models and will take a significant time, depending on your internet connection.

Use `python launcher.py --preset anime` or `python launcher.py --preset realistic` for BlueMoonAI Anime/Realistic Edition.


### Docker

See [docker.md](docker.md)

## Contributing

If you want to contribute to this project, follow these steps:

1. Fork the repository.
2. Create a new branch: `git checkout -b feature-branch`.
3. Make your changes and commit them: `git commit -m 'Description of your changes'`.
4. Push to the branch: `git push origin feature-branch`.
5. Submit a pull request.

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on the code of conduct and the process for submitting pull requests.

## Code of Conduct

Please review our [Code of Conduct](CODE_OF_CONDUCT.md) to understand the behavior we expect from contributors.

## Minimal Requirement

Below is the minimal requirement for running BlueMoon AI locally. If your device capability is lower than this spec, you may not be able to use BlueMoon AI locally. (Please let us know, in any case, if your device capability is lower but BlueMoon AI still works.)

| Operating System  | GPU                          | Minimal GPU Memory | Minimal System Memory | Note                                                  |
|-------------------|------------------------------|--------------------|-----------------------|-------------------------------------------------------|
| Windows/Linux     | Nvidia RTX >2XXX             | 4GB                | 8GB                   | Offers superior performance compared to GTX 1XXX (on GPU)  |
| Windows/Linux     | Nvidia GTX >9XX              | 8GB                | 8GB                   | GPU performance may vary in comparison to CPU            |
| Windows/Linux     | Nvidia GTX < 9XX             | Not supported      | /                     | /                                                       |
| Windows           | AMD GPU                      | 16GB               | 8GB                   | Leverages DirectML for GPU acceleration                |
| Linux             | AMD GPU                      | 8GB                | 8GB                   | Accelerated via ROCm                                  |
| Windows           | &ast; AMD GPU ROCm (on hold) | 8GB      | 8GB       | ROCm support currently on hold                         |
| Mac               | M1/M2 MPS                    | Shared             | Shared                |  slower than Nvidia RTX 3XXX          |

&ast; AMD GPU ROCm (on hold): The AMD is still working on supporting ROCm on Windows.

&ast; Nvidia GTX 1XXX 6GB uncertain: Some people reports 6GB success on GTX 10XX but some other people reports failure cases.

*Note that BlueMoon AI is only for extremely high quality image generating. We will not support smaller models to reduce the requirement and sacrifice result quality.*


## Default Models
<a name="models"></a>

Given different goals, the default models and configs of BlueMoonAI is different:

| Task | Windows | Linux args | Main Model | Refiner | Config |
| - | - | - | - | - | - |
| General | run.bat |  | [juggernautXL v6_RunDiffusion](https://huggingface.co/BlueMoonAI/Models/resolve/main/juggernautXL_version6Rundiffusion.safetensors) | not used | [here](https://github.com/BlueMoonAI/BlueMoonAI/blob/main/modules/path.py) |
| Realistic | run_realistic.bat | --preset realistic | [realistic_stock_photo](https://huggingface.co/BlueMoonAI/Models/resolve/main/realisticStockPhoto_v10.safetensors) | not used | [here](https://github.com/BlueMoonAI/BlueMoonAI/blob/main/presets/realistic.json) |
| Anime | run_anime.bat | --preset anime | [bluepencil_v50](https://huggingface.co/BlueMoonAI/Models/resolve/main/bluePencilXL_v050.safetensors) | [dreamsharper_v8](https://huggingface.co/BlueMoonAI/Models/resolve/main/DreamShaper_8_pruned.safetensors) (SD1.5) | [here](https://github.com/BlueMoonAI/BlueMoonAI/blob/main/presets/anime.json) |

Note that the download is **automatic** - you do not need to do anything if the internet connection is okay. However, you can download them manually if you (or move them from somewhere else) have your own preparation.

The default models are downloaded to `BlueMoonAI\models\checkpoints` folder. You can also download them manually and put them in the folder.


## Customization

After the first time you run BlueMoonAI, a config file will be generated at `BlueMoonAI\config.txt`. This file can be edited for changing the model path or default parameters.

For example, an edited `BlueMoonAI\config.txt` (this file will be generated after the first launch) may look like this:

```json
{
    "path_checkpoints": "D:\\BlueMoonAI\\models\\checkpoints",
    "path_loras": "D:\\BlueMoonAI\\models\\loras",
    "path_embeddings": "D:\\BlueMoonAI\\models\\embeddings",
    "path_vae_approx": "D:\\BlueMoonAI\\models\\vae_approx",
    "path_upscale_models": "D:\\BlueMoonAI\\models\\upscale_models",
    "path_inpaint": "D:\\BlueMoonAI\\models\\inpaint",
    "path_controlnet": "D:\\BlueMoonAI\\models\\controlnet",
    "path_clip_vision": "D:\\BlueMoonAI\\models\\clip_vision",
    "path_BlueMoonAI_expansion": "D:\\BlueMoonAI\\models\\prompt_expansion\\BlueMoonAI_expansion",
    "path_outputs": "D:\\BlueMoonAI\\outputs",
    "default_model": "realisticStockPhoto_v10.safetensors",
    "default_refiner": "",
    "default_loras": [["lora_filename_1.safetensors", 0.5], ["lora_filename_2.safetensors", 0.5]],
    "default_cfg_scale": 3.0,
    "default_sampler": "dpmpp_2m",
    "default_scheduler": "karras",
    "default_negative_prompt": "low quality",
    "default_positive_prompt": "",
    "default_styles": [
        "BlueMoonAI V1",
        "BlueMoonAI Photograph",
        "BlueMoonAI Negative"
    ]
}
```

Many other keys, formats, and examples are in `BlueMoonAI\config_settings.txt` (this file will be generated after the first launch).

Consider twice before you really change the config. If you find yourself breaking things, just delete `BlueMoonAI\config.txt`. BlueMoonAI will go back to default.

### All CMD Flags

```
launcher.py  [-h] [--listen [IP]] [--port PORT]
                      [--disable-header-check [ORIGIN]]
                      [--web-upload-size WEB_UPLOAD_SIZE]
                      [--external-working-path PATH [PATH ...]]
                      [--output-path OUTPUT_PATH] [--temp-path TEMP_PATH]
                      [--cache-path CACHE_PATH] [--in-browser]
                      [--disable-in-browser] [--gpu-device-id DEVICE_ID]
                      [--async-cuda-allocation | --disable-async-cuda-allocation]
                      [--disable-attention-upcast] [--all-in-fp32 | --all-in-fp16]
                      [--unet-in-bf16 | --unet-in-fp16 | --unet-in-fp8-e4m3fn | --unet-in-fp8-e5m2]
                      [--vae-in-fp16 | --vae-in-fp32 | --vae-in-bf16]
                      [--clip-in-fp8-e4m3fn | --clip-in-fp8-e5m2 | --clip-in-fp16 | --clip-in-fp32]
                      [--directml [DIRECTML_DEVICE]] [--disable-ipex-hijack]
                      [--preview-option [none,auto,fast,taesd]]
                      [--attention-split | --attention-quad | --attention-pytorch]
                      [--disable-xformers]
                      [--always-gpu | --always-high-vram | --always-normal-vram | 
                       --always-low-vram | --always-no-vram | --always-cpu]
                      [--always-offload-from-vram] [--disable-server-log]
                      [--debug-mode] [--is-windows-embedded-python]
                      [--disable-server-info] [--share] [--preset PRESET]
                      [--language LANGUAGE] [--disable-offload-from-vram]
                      [--theme THEME] [--disable-image-log]
```

## Update Log

The log is [here](update_log.md).

## Localization/Translation

**We need your help!** Please help with translating BlueMoonAI to international languages.

You can put json files in the `language` folder to translate the user interface.

For example, below is the content of `BlueMoonAI/language/example.json`:

```json
{
  "Preview": "Prévisualisation",
  "Gallery": "Galerie",
  "Generate": "Générer",
  "Skip": "Passer",
  "Stop": "Arrêter",
  "Input Image": "Image d'entrée",
  "Advanced": "Avancé",
  "Upscale or Variation": "Agrandir ou Variante",
  "Image Prompt": "Incitation d'image",
  "Inpaint or Outpaint": "Retouche ou Extrapolation",
  "Drag above image to here": "Faites glisser l'image ci-dessus ici",
  "Upscale or Variation:": "Agrandir ou Variante:",
  "Disabled": "Désactivé",
  "Vary (Subtle)": "Variante (Subtile)",
  "Vary (Strong)": "Variante (Fort)",
  "Upscale (1.5x)": "Agrandir (1.5x)",
  "Upscale (2x)": "Agrandir (2x)",
  "Upscale (Fast 2x)": "Agrandir (Rapide 2x)",
  "\ud83d\udcd4 Document": "\uD83D\uDCD4 Document",
  "Image": "Image",
  "Outpaint Expansion Direction:": "Direction d'extension de la extrapolation:",
  "* Powered by BlueMoon AI Inpaint Engine": "* Propulsé par BlueMoon AI Inpaint Engine",
  "BlueMoon AI Enhance": "BlueMoon AI Améliorer",
  "BlueMoon AI Cinematic": "BlueMoon AI Cinématique",
  "BlueMoon AI Sharp": "BlueMoon AI Net"
}

```

If you add `--language example` arg, BlueMoonAI will read `BlueMoonAI/language/example.json` to translate the UI.

For practical translation, you may create your own file like `BlueMoonAI/language/jp.json` or `BlueMoonAI/language/cn.json` and then use flag `--language jp` or `--language cn`. Apparently, these files do not exist now. **We need your help to create these files!**



Note that if no `--language` is given and at the same time `BlueMoonAI/language/default.json` exists, BlueMoonAI will always load `BlueMoonAI/language/default.json` for translation. By default, the file `BlueMoonAI/language/default.json` does not exist.


## Happy Creativity! ❤️
