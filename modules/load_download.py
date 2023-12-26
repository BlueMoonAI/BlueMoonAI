import json
import os


def load_json_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as json_file:
            return json.load(json_file)
    except Exception as e:
        print(f'Failed to load models file "{file_path}". The reason is: {str(e)}')
        return None


def get_models_values(file_names):
    result = {}

    for file_name in file_names:
        file_path = os.path.join("../models/default", file_name)

        # Load JSON data from the current file
        model_settings_data = load_json_file(file_path)

        if model_settings_data:
            # Get the value associated with 'models.json' key
            models_value = model_settings_data.get('downloads', {}).get('models.json', None)

            # Store the value in the result dictionary
            result[file_name] = models_value
        else:
            print(f"Unable to load {file_name}.")

    return result


file_names = [
    "model_settings.json",
    # Add more file names if needed
]

