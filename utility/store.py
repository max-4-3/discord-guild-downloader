import json
import os

from utility import CONFIG_PATH


def read_config() -> dict:
    try:
        # Ensure the file exists before reading
        if os.path.exists(CONFIG_PATH):
            with open(CONFIG_PATH, 'r', encoding='utf-8', errors='ignore') as file:
                return json.load(file)
        else:
            return {}
    except (FileNotFoundError, json.JSONDecodeError):
        # Return an empty dictionary if the file doesn't exist or is empty
        return {}


def store_config(**kwargs):
    # Fetch the already existing config, if any
    already_config = read_config()

    # Prepare a dictionary to store updated config values
    data = {}

    # Store or update the token if it's different from the existing one
    if kwargs.get('token') and kwargs.get('token') != already_config.get('token'):
        data['token'] = kwargs.get('token')
    else:
        data['token'] = already_config.get('token')

    # Store or update the path if it's different from the existing one
    if kwargs.get('path') and kwargs.get('path') != already_config.get('path'):
        data['path'] = kwargs.get('path')
    else:
        data['path'] = already_config.get('path')

    # Write the updated config to the file
    with open(CONFIG_PATH, 'w', encoding='utf-8', errors='ignore') as file:
        json.dump(data, file, indent=2, ensure_ascii=False)
