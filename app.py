import os
import sys
import ssl


import bluemoonai_version


import json
import os

from bluemoon.utils.logly import logly
from updater import Updater



logly.info('[System ARGV]', f"{str(sys.argv)}")

root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(root)
os.chdir(root)


# Load data from settings.json
with open('settings.json', 'r') as file:
    settings_data = json.load(file)

# Set environment variables with default values or values from the settings file
os.environ["REPO_URL"] = settings_data.get("REPO_URL", "https://github.com/BlueMoonAI/BlueMoonAI")
os.environ["BRANCH_NAME"] = settings_data.get("BRANCH_NAME", "main")
os.environ["LOCAL_VERSION"] = bluemoonai_version.get_version()
os.environ["AUTOUPDATE"] = settings_data.get("AUTOUPDATE", "True")
try:
    # Run the updater
    updater = Updater()
    updater.run_update()
except Exception as e:
    logly.error('[Updater]', f"{str(e)}")

# Set additional environment variables
os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = settings_data.get("PYTORCH_ENABLE_MPS_FALLBACK", "1")
os.environ["PYTORCH_MPS_HIGH_WATERMARK_RATIO"] = settings_data.get("PYTORCH_MPS_HIGH_WATERMARK_RATIO", "0.0")

import platform

from build import build_launcher
from modules.launch_util import is_installed, run, python, run_pip, requirements_met
from modules.model_loader import load_file_from_url
from modules.config import path_checkpoints, path_loras, path_vae_approx, path_bluemoon_expansion, \
    checkpoint_downloads, path_embeddings, embeddings_downloads, lora_downloads, model_downloads, path_download_models

REINSTALL_ALL = False
TRY_INSTALL_XFORMERS = False


def prepare_environment():
    torch_index_url = os.environ.get('TORCH_INDEX_URL', "https://download.pytorch.org/whl/cu121")
    torch_command = os.environ.get('TORCH_COMMAND',
                                   f"pip install torch==2.1.0 torchvision==0.16.0 --extra-index-url {torch_index_url}")
    requirements_file = os.environ.get('REQS_FILE', "requirements.txt")

    logly.info(f"Python", f"{sys.version}")
    logly.info(f"BlueMoon AI version:", f"v{bluemoonai_version.get_version()}")

    if REINSTALL_ALL or not is_installed("torch") or not is_installed("torchvision"):
        run(f'"{python}" -m {torch_command}', "Installing torch and torchvision", "Couldn't install torch", live=True)

    if TRY_INSTALL_XFORMERS:
        if REINSTALL_ALL or not is_installed("xformers"):
            xformers_package = os.environ.get('XFORMERS_PACKAGE', 'xformers==0.0.20')
            if platform.system() == "Windows":
                if platform.python_version().startswith("3.10"):
                    run_pip(f"install -U -I --no-deps {xformers_package}", "xformers", live=True)
                else:
                    logly.warn("Installation of xformers is not supported in this version of Python.")
                    logly.warn(
                        "You can also check this and build manually: https://github.com/AUTOMATIC1111/stable-diffusion-webui/wiki/Xformers#building-xformers-on-windows-by-duckness")
                    if not is_installed("xformers"):
                        exit(0)
            elif platform.system() == "Linux":
                run_pip(f"install -U -I --no-deps {xformers_package}", "xformers")

    if REINSTALL_ALL or not requirements_met(requirements_file):
        run_pip(f"install -r \"{requirements_file}\"", "requirements")

    return


vae_approx_filenames = [
    ('xlvaeapp.pth', 'https://huggingface.co/BlueMoonAI/misc/resolve/main/xlvaeapp.pth'),
    ('vaeapp_sd15.pth', 'https://huggingface.co/BlueMoonAI/misc/resolve/main/vaeapp_sd15.pt'),
    ('xl-to-v1_interposer-v3.1.safetensors',
     'https://huggingface.co/BlueMoonAI/misc/resolve/main/xl-to-v1_interposer-v3.1.safetensors')
]


def download_models():
    for file_name, url in model_downloads.items():
        load_file_from_url(url=url, model_dir=path_download_models, file_name=file_name)
    for file_name, url in checkpoint_downloads.items():
        load_file_from_url(url=url, model_dir=path_checkpoints, file_name=file_name)
    for file_name, url in embeddings_downloads.items():
        load_file_from_url(url=url, model_dir=path_embeddings, file_name=file_name)
    for file_name, url in lora_downloads.items():
        load_file_from_url(url=url, model_dir=path_loras, file_name=file_name)
    for file_name, url in vae_approx_filenames:
        load_file_from_url(url=url, model_dir=path_vae_approx, file_name=file_name)

    load_file_from_url(
        url='https://huggingface.co/BlueMoonAI/misc/resolve/main/bluemoon_expansion.bin',
        model_dir=path_bluemoon_expansion,
        file_name='pytorch_model.bin'
    )

    return


def ini_args():
    from args_manager import args
    return args


prepare_environment()
build_launcher()
args = ini_args()

if args.gpu_device_id is not None:
    os.environ['CUDA_VISIBLE_DEVICES'] = str(args.gpu_device_id)
    logly.info("Set device to:", args.gpu_device_id)

download_models()

from webui import *
