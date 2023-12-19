# bluemoonai_version.py
import json
from os.path import abspath

from bluemoon.utils.logly import logly


def get_version_from_json(json_file_path):
    try:
        with open(json_file_path, "r") as f:
            data = json.load(f)
        return data.get("version", "0.0.1")  # Default to "0.0.1" if "version" key is not found
    except Exception as e:
        logly.error(f"Error reading version from JSON: {e}")
        return "0.0.1"  # Default to "0.0.1" in case of any error

def get_version():
    json_file_path = abspath("version.json")
    version_from_json = get_version_from_json(json_file_path)
    return version_from_json


