import os
import json

from bluemoon.utils.logly import logly

def get_folders_and_paths(root_folder):
    folder_data = {}

    for folder_name in os.listdir(root_folder):
        folder_path = os.path.join(root_folder, folder_name)
        if os.path.isdir(folder_path):
            folder_data[folder_name] = folder_path

            # Recursively get folders and paths inside subdirectories
            subfolder_data = get_folders_and_paths(folder_path)
            folder_data.update(subfolder_data)

    return folder_data

def save_to_json(data, json_file):
    with open(json_file, 'w') as f:
        json.dump(data, f, indent=4)

def get_model_paths():
    # Get the absolute path of the script's directory
    script_directory = os.path.dirname(os.path.abspath(__file__))

    root_folder = os.path.join(script_directory, "../models/")

    if not os.path.exists(root_folder):
        logly.error("Error: The specified folder does not exist.")
        return

    folder_data = get_folders_and_paths(root_folder)

    items_to_delete = []
    for folder_name, folder_path in folder_data.items():
        if os.path.sep in folder_name:
            parent_folder_name, subfolder_name = folder_name.split(os.path.sep, 1)
            parent_folder_path = folder_data[parent_folder_name]
            folder_data[subfolder_name] = os.path.join(parent_folder_path, folder_name)
            items_to_delete.append(folder_name)

    for item in items_to_delete:
        del folder_data[item]

    json_file_name = "model_config_path.json"
    json_file_path = os.path.join(root_folder, "default", json_file_name)

    save_to_json(folder_data, json_file_path)

    logly.info(f"Folder data has been saved to {json_file_path}.")


