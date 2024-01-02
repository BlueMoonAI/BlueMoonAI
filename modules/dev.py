from modules.shared_module import read_model_config_path


def bluemoon_type():
    json = read_model_config_path("./settings.json")
    value = json.get("DEBUG")
    return value