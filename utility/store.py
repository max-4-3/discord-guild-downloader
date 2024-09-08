import json

from utility import CONFIG_PATH


def store_config(**kwargs):
    with open(CONFIG_PATH, 'w', encoding='utf- 8', errors='ignore') as file:
        data = {}
        if kwargs.get('token'):
            data['token'] = kwargs.get('token')
        if kwargs.get('path'):
            data['path'] = kwargs.get('path')

        json.dump(data, file, indent=2, ensure_ascii=False)


def read_config() -> dict:
    try:
        with open(CONFIG_PATH, 'r') as file:
            return json.load(file)
    except (FileExistsError, FileNotFoundError):
        return {}
