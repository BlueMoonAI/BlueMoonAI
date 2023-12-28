
import os
import json

from bluemoon.utils.logly import logly


def download_models(selected_models_sdxl, selected_models_sd, url_input):
    downloaded_models = load_downloaded_models()

    # Filter out already downloaded models
    selected_models_sdxl = [model for model in selected_models_sdxl if not is_model_downloaded(model, downloaded_models['sdxl'])]
    selected_models_sd = [model for model in selected_models_sd if not is_model_downloaded(model, downloaded_models['sd'])]

    for model in selected_models_sdxl:

        logly.info(f'Downloading {model}...')

        # Implement the download logic for sdxl models
        # ...
        downloaded_models['sdxl'].append(model)

    for model in selected_models_sd:

        logly.info(f'Downloading {model}...')

        # Implement the download logic for sd models
        # ...
        downloaded_models['sd'].append(model)

    if url_input:

        logly.info(f'Downloading from URL: {url_input}...')

        # Implement the download logic for URL
        # ...
        downloaded_models['url'].append(url_input)

    save_downloaded_models(downloaded_models)

def is_model_downloaded(model, downloaded_models):
    return model in downloaded_models

def get_downloaded_models():
    downloaded_models = load_downloaded_models()
    return downloaded_models

def load_downloaded_models():
    script_directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.abspath(os.path.join(script_directory, 'models/downloads/downloaded_models.json'))

    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            downloaded_models = json.load(file)
        return downloaded_models
    else:
        return {'sdxl': [], 'sd': [], 'url': []}

def save_downloaded_models(downloaded_models):
    script_directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.abspath(os.path.join(script_directory, 'models/downloads/downloaded_models.json'))

    existing_downloaded_models = load_downloaded_models()

    # Append newly downloaded models
    for key in downloaded_models:
        existing_downloaded_models[key].extend(downloaded_models[key])

    with open(file_path, 'w') as file:
        json.dump(existing_downloaded_models, file, indent=2)

