# download_models.py
from modules.model_loader import load_file_from_url
from modules.shared_module import read_model_config_path

def download_models(url, selected):
    model_paths = read_model_config_path("./models/default/model_config_path.json")
    path = model_paths.get(selected)

    # Add your download logic here
    try:
        load_file_from_url(url, model_dir=path, progress=True, file_name=None)
        success_message = f"Download successful!"
    except Exception as e:
        success_message = f"Download failed! please check url or try again later."

    return success_message
