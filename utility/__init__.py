import os
from platform import system as os_name

_path = os.path.split(os.path.split(__file__)[0])[0]
is_windows = True if os_name().lower() in ['windows', 'nt'] else False
CONFIG_PATH = os.path.join(os.getenv('LOCALAPPDATA'), "discord-guild-downloader",'config_file.json') if is_windows else os.path.join(os.getenv('HOME', _path), "discord-guild-downloader", 'config_file.json')

if not os.path.exists(CONFIG_PATH):
	os.makedirs(CONFIG_PATH, exist_ok=True)
