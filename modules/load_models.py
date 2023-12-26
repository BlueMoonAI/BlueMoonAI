import json


def get_download_choices():
    # Use the absolute path to model_links.json
    file_path = 'D:/bluemoon/models/downloads/model_links.json'

    with open(file_path, 'r') as file:
        data = json.load(file)

    return data['sdxl']
