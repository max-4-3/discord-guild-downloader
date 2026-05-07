import os
from platform import system as os_name

is_windows = os_name().lower() in ["windows", "nt"]
is_android = not is_windows and (
    "ANDROID_ROOT" in os.environ or "ANDROID_DATA" in os.environ
)

ROOT = os.path.split(os.path.split(__file__)[0])[0]
CONFIG_PATH = os.path.join(
    os.getenv("HOME" if not is_windows else "LOCALAPPDATA", ROOT),
    "discord-guild-downloader",
    "config_file.json",
)
GUILD_RAPR = os.path.join(ROOT, "guild_rapr.txt")

os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
