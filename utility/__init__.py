import os
from platform import system as os_name

_path = os.path.split(os.path.split(__file__)[0])[0]
is_windows = os_name().lower() in ['windows', 'nt']
is_android = not is_windows and ('ANDROID_ROOT' in os.environ or 'ANDROID_DATA' in os.environ)
CONFIG_PATH = os.path.join(os.getenv('LOCALAPPDATA'), "discord-guild-downloader",'config_file.json') if is_windows else os.path.join(os.getenv('HOME', _path), "discord-guild-downloader", 'config_file.json')

if not os.path.exists(os.path.dirname(CONFIG_PATH)):
	os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
