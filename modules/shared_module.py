# shared_module.py
import json

def read_model_config_path(json_file_path):
    with open(json_file_path, 'r') as f:
        model_paths = json.load(f)
    return model_paths
