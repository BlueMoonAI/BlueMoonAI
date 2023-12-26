import json
import os

from bluemoon.utils.logly import logly

file_names = [
    "models.json",
    "sd.json",
    "paint.json",
    "upscaler.json",
    "sdxl_lcm_lora.json",
    "controlnet.json",
    "ip_adapter.json",
    "model_settings.json",

]

def load_json_file(file_name):
    file_path = os.path.abspath(os.path.join("models/default", file_name))
    try:
        with open(file_path, "r", encoding="utf-8") as json_file:
            return json.load(json_file)
    except Exception as e:
        logly.error(f'Failed to load models file "{file_path}". The reason is: {str(e)}')
        return None

model_links, sd_links, paint_links, upscaler_links, lcm_links, controlnet_links, ip_adapter_links,download_models= (
    load_json_file(name) for name in file_names
)
