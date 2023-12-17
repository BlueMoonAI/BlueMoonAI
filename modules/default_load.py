import json
import os

file_names = [
    "models.json",
    "sd.json",
    "paint.json",
    "upscaler.json",
    "sdxl_lcm_lora.json",
    "controlnet.json",
    "ip_adapter.json",
]

def load_json_file(file_name):
    file_path = os.path.abspath(os.path.join("models/default", file_name))
    try:
        with open(file_path, "r", encoding="utf-8") as json_file:
            return json.load(json_file)
    except Exception as e:
        print(f'Failed to load models file "{file_path}". The reason is: {str(e)}')
        return None

model_links, sd_links, paint_links, upscaler_links, lcm_links, controlnet_links, ip_adapter_links = (
    load_json_file(name) for name in file_names
)
