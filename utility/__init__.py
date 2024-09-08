import os
from platform import system as os_name

CONFIG_PATH = os.path.join(os.getenv('LOCALAPPDATA'), 'config_file.json') if os_name().lower() in ['windows', 'nt'] else os.path.join(os.getcwd(), 'config_file.json')
