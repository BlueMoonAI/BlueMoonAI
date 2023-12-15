import json
import os
import json


def load_model_links(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as json_file:
            model_links = json.load(json_file)
        return model_links
    except FileNotFoundError:
        print(f'Error: File not found - "{file_path}"')
        raise
    except Exception as e:
        print(f'Error loading models file "{file_path}": {str(e)}')
        raise


# Rest of your code...

# Example usage:
models_path = os.path.abspath("../models/default/models.json")
model_links = load_model_links(models_path)
print(model_links.get('default', {}).get('default_value', None))