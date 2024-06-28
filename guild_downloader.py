from os import makedirs, path, system, getcwd, startfile
from platform import system as psys
from json import load, dump, dumps
from shutil import make_archive
from typing import Dict, Tuple, Optional
from time import sleep
from random import uniform
from asyncio import run

try:
    from init import *
except ModuleNotFoundError:
    BASE = "https://discord.com/api/v9"
    DISCORD_BASE = "https://discord.com"
    ASSET_BASE = "https://cdn.discordapp.com"
    ASSET_BASE_TWO = "https://media.discordapp.net"
try:
    from requests import get
except ModuleNotFoundError:
    print("[!] requests Module Not Found!, Downloading...")
    system("pip install requests")
    from requests import get
try:
    from aiohttp import ClientSession
except ModuleNotFoundError:
    print("[!] aiohttp Module Not Found!, Downloading...")
    system("pip install aiohttp")
    from aiohttp import ClientSession
try:
    from alive_progress import alive_bar
except ModuleNotFoundError:
    print("[!] alive_progress Module Not Found!, Downloading...")
    system("pip install alive_progress")
    from alive_progress import alive_bar
try:
    from colorama import Fore
except ModuleNotFoundError:
    print("[!] colorama Module Not Found!, Downloading...")
    system("pip install colorama")
    from colorama import Fore


def cls():
    os_name = psys().lower()
    art = r'''
               _____       _ _     _   _____                      _                 _           
              / ____|     (_) |   | | |  __ \                    | |               | |          
             | |  __ _   _ _| | __| | | |  | | _____      ___ __ | | ___   __ _  __| | ___ _ __ 
             | | |_ | | | | | |/ _` | | |  | |/ _ \ \ /\ / / '_ \| |/ _ \ / _` |/ _` |/ _ \ '__|
             | |__| | |_| | | | (_| | | |__| | (_) \ V  V /| | | | | (_) | (_| | (_| |  __/ |   
              \_____|\__,_|_|_|\__,_| |_____/ \___/ \_/\_/ |_| |_|_|\___/ \__,_|\__,_|\___|_|   
                '''
    if os_name in ["windows", "nt"]:
        system("cls")
        print(art)
    else:
        system("clear")
        print(art)

# Forgive my stupid variable naming
G_name = ""
G_json = {}


# Main Guild Class
class Guild:

    @staticmethod
    def emoji(guild_id) -> list[dict[int, dict[str, str | bool]]] | None:
        """
        Gives the emoji info of all emojis from a guild
        :param guild_id: The id of the guild.
        :return: A list of Dictionary.
        """

        def extract_emoji_info(emoji_json) -> list[dict[int, dict[str, str | bool]]]:
            emoji_url_list = []
            for emoji in emoji_json:
                # gather info
                name = emoji.get("name")
                e_id = emoji.get("id")
                anim = emoji.get("animated")
                fmt = ".gif" if anim else ".png"
                url = f"{ASSET_BASE}/emojis/{e_id}{fmt}?size=4096"

                # append the info to list
                emoji_url_list.append({
                    int(e_id): {
                        "name": name if name else e_id,
                        "url": url,
                        "animated": True if anim else False
                    }
                })
            return emoji_url_list

        try:
            url_emoji = BASE + f"/guilds/{guild_id}/emojis"
            data = get(url_emoji, headers=HEADERS).json()
            return extract_emoji_info(data)
        except Exception as emoji_exception:
            print(f"{Fore.RED}[!] Got an exception while getting emojis : {emoji_exception}{Fore.RESET}")
            return None

    @staticmethod
    def role(guild_id) -> list[dict[str, str]] | None:
        """
        Gives the role info of all roles from a guild.
        :param guild_id: The id of the guild.
        :return: A list of Dictionary.
        """

        def extract_role_info(guild_json) -> list[dict[str, str]]:
            roles = guild_json
            roles_info = [
                {
                    "Name": role.get("name"),
                    "ID": role.get("id"),
                    "Position": role.get("position"),
                    "Color": role.get("color"),
                    "Permissions": role.get("permissions"),
                    "Icon": role.get("icon", "No Icon!")
                }
                for role in roles
            ]
            return roles_info

        try:
            url_role = BASE + f"/guilds/{guild_id}/roles"
            data = get(url_role, headers=HEADERS).json()
            return extract_role_info(data)
        except Exception as roles_exception:
            print(f"{Fore.RED}[!] Got an exception while getting roles : {roles_exception}{Fore.RESET}")
            return None

    @staticmethod
    def channel(guild_id) -> list[dict[str, str | int | dict[str, str | int]]] | None:
        """
        Gives the channel info of all channels from a guild
        :param guild_id: The id of the guild.
        :return: A list of Dictionary. The "permission_overwrites" or "Permissions" contains a dictionary.
        """

        def extract_channel_info(channel_json) -> list[dict[str, str | int | dict[str, str | int]]]:
            guild_channels = channel_json
            channels_info = [
                {
                    "Name": channel.get("name"),
                    "ID": channel.get("id"),
                    "Topic": channel.get("topic"),
                    "Position": channel.get("position"),
                    "Permissions": channel.get("permission_overwrites"),
                    "Server ID": channel.get("guild_id")
                }
                for channel in guild_channels
            ]
            return channels_info

        try:
            url_role = BASE + f"/guilds/{guild_id}/channels"
            data = get(url_role, headers=HEADERS).json()
            return extract_channel_info(data)
        except Exception as channels_exception:
            print(f"{Fore.RED}[!] Got an exception while getting channels : {channels_exception}{Fore.RESET}")
            return None

    @staticmethod
    def sticker(guild_id) -> list[dict[int, dict[str, str | bool]]] | None:
        """
        Gives the sticker url of all stickers in a guild
        :param guild_id: The id of the guild.
        :return: A dictionary where sticker id is mapped to another dictionary
                containing the url and whether the sticker is apng or not and also the name.
        """

        def extract_sticker_info(sticker_json) -> list[dict[int, dict[str, str | bool]]]:
            stick_url_list = []
            for s in sticker_json:
                if s.get("format_type") == 1:
                    fmt = ".png"
                    name = s.get("name")
                    u = f"{ASSET_BASE}/stickers/{s.get('id')}{fmt}?size=4096"
                    animate = False
                    stick_url_list.append({
                        int(s.get("id")): {
                            "name": name,
                            "url": u,
                            "animated": animate
                        }
                    })
                elif s.get("format_type") == 2:
                    fmt = ".png"
                    u = f"{ASSET_BASE}/stickers/{s.get('id')}{fmt}?size=4096"
                    animate = True
                    name = s.get("name")
                    stick_url_list.append({
                        int(s.get("id")): {
                            "name": name,
                            "url": u,
                            "animated": animate
                        }
                    })
                elif s.get("format_type") == 3:
                    fmt = ".json"
                    u = f"{ASSET_BASE}/stickers/{s.get('id')}{fmt}?size=4096"
                    animate = False
                    name = s.get("name")
                    stick_url_list.append({
                        int(s.get("id")): {
                            "name": name,
                            "url": u,
                            "animated": animate
                        }
                    })
                elif s.get("format_type") == 4:
                    fmt = ".gif"
                    u = f"{ASSET_BASE_TWO}/stickers/{s.get('id')}{fmt}?size=4096"
                    animate = False
                    name = s.get("name")
                    stick_url_list.append({
                        int(s.get("id")): {
                            "name": name,
                            "url": u,
                            "animated": animate
                        }
                    })
                else:
                    print(f"{Fore.RED}[!] {s.get('name')} can't be downloaded!{Fore.RESET}")
            return stick_url_list

        try:
            url_stickers = BASE + f"/guilds/{guild_id}/stickers"
            data = get(url_stickers, headers=HEADERS).json()
            return extract_sticker_info(data)
        except Exception as sticker_exception:
            print(f"{Fore.RED}[!] Got an exception while getting channels : {sticker_exception}{Fore.RESET}")
            return None

    @staticmethod
    def icon(guild_json) -> None | str:
        """
        Gives the icon of the guild if it exists.
        :param guild_json: The Json Obj of the get request to Guild.
        :return: The url as a string if it exists otherwise None
        """
        icon_hash = guild_json.get("icon", None)
        if not icon_hash:
            print(f"{Fore.RED}[!] Server don't have any icon or is a new server? {Fore.RESET}")
            return
        fmt = ".gif" if icon_hash.startswith("a_") else ".png"
        return f"{ASSET_BASE}/icons/{guild_json.get("id")}/{icon_hash}.{fmt}?size=4096"

    @staticmethod
    def banner(guild_json) -> None | str:
        """
        Gives the banner of the guild if it exists.
        :param guild_json: The Json Obj of the get request to Guild.
        :return: The url as a string if it exists otherwise None
        """
        banner_hash = guild_json.get("banner", None)
        if not banner_hash:
            print(
                f"{Fore.RED}[!] Server don't have any banner or is a new server or haven't set any banner?{Fore.RESET}"
            )
            return
        fmt = ".gif" if banner_hash.startswith("a_") else ".png"
        return f"{ASSET_BASE}/banner/{guild_json.get("id")}/{banner_hash}.{fmt}?size=4096"

    @staticmethod
    def splash(guild_json) -> None | str:
        """
        Gives the splash of the guild if it exists.
        :param guild_json: The Json Obj of the get request to Guild.
        :return: The url as a string if it exists otherwise None
        """
        splash_hash = guild_json.get("splash", None)
        if not splash_hash:
            print(
                f"{Fore.RED}[!] Server don't have any splash or is a new server or haven't set any banner?{Fore.RESET}"
            )
            return
        fmt = ".gif" if splash_hash.startswith("a_") else ".png"
        return f"{ASSET_BASE}/splashes/{guild_json.get("id")}/{splash_hash}.{fmt}?size=4096"

    @staticmethod
    def discovery_splash(guild_json) -> None | str:
        """
        Gives the discovery_splash of the guild if it exists.
        :param guild_json: The Json Obj of the get request to Guild.
        :return: The url as a string if it exists otherwise None
        """
        discovery_splash_hash = guild_json.get("discovery_splash", None)
        if not discovery_splash_hash:
            print(
                f"{Fore.RED}[!] Server don't have any discovery splash or haven't set any banner?{Fore.RESET}"
            )
            return
        fmt = ".gif" if discovery_splash_hash.startswith("a_") else ".png"
        return f"{ASSET_BASE}/discovery-splashes/{guild_json.get("id")}/{discovery_splash_hash}.{fmt}?size=4096"

    @staticmethod
    def description(guild_json) -> None | str:
        """
        Gives the description of the guild if it exists.
        :param guild_json: The Json Obj of the get request to Guild.
        :return: The url as a string if it exists otherwise None
        """
        return guild_json.get("description", "No Description!")

    @staticmethod
    def name(guild_json) -> str:
        """
        Gives the name of the guild.
        :param guild_json: The Json Obj of the get request to Guild.
        :return: The url as a string.
        """
        return guild_json.get("name")


# Just A Collection of Functions Stored in a Class
class Utils:

    @staticmethod
    def retry():
        retry_prompt = input(f"{Fore.YELLOW}[?] Retry? (yes/no): {Fore.RESET}").lower()
        while retry_prompt not in ["yes", "no"]:
            retry_prompt = input(f"{Fore.YELLOW}[?] Retry? (yes/no): {Fore.RESET}").lower()
        if retry_prompt == "no":
            print(f"{Fore.GREEN}[#] Everything went smoothly and all emojis were downloaded!{Fore.RESET}")
            exit(0)
        else:
            cls()
            main()

    # i didn't used in this version
    @staticmethod
    def create_archive(name: str, mode: str, base_dir: str):
        try:
            make_archive(base_name=name, format=mode, base_dir=base_dir)
            print(f"{Fore.GREEN}[+] Archive Created! [{path.abspath(name + '.' + mode)}]{Fore.RESET}")
        except Exception as archive_exception:
            print(f"{Fore.RED}[!] Failed to create archive: {archive_exception}{Fore.RESET}")

    @staticmethod
    def validate() -> Optional[str]:
        try:
            file_name = "token.json"
            if not path.exists(file_name):
                return
            with open(file_name, 'r') as file:
                token = load(file).get("token")
            if not token or len(token.split(".")) != 3:
                return
            return token
        except Exception as token_exception:
            print(f"{Fore.RED}[!] Got An Exception While Opening {"token.json"} File, {token_exception}{Fore.RESET}")
            return

    @staticmethod
    def get_guild_id() -> str:
        prompt = f"{Fore.BLUE}[+] Enter The Guild ID: {Fore.RESET}"
        while True:
            guild_id = input(prompt)
            if not guild_id:
                print(f"{Fore.RED}[!] Please enter a Guild ID!{Fore.RESET}")
            elif guild_id == "exit":
                print(f"{Fore.BLUE}\n[#] Okay!{Fore.RESET}")
                exit(0)
            elif not guild_id.isdigit():
                print(f"{Fore.RED}[!] The Guild ID must be a number!{Fore.RESET}")
            elif not len(guild_id) > 8:
                print(f"{Fore.RED}[!] The Guild ID can't be so small!{Fore.RESET}")
            else:
                return guild_id

    @staticmethod
    def get_user_token() -> str:
        token = Utils.validate()
        prompt = f"{Fore.BLUE}[+] Enter Your Account Token: {Fore.RESET}"

        if token:
            choice = input(f"{Fore.YELLOW}[?] Load token from file? (yes/no): {Fore.RESET}").lower()
            while choice not in ["yes", "no"]:
                choice = input(f"{Fore.YELLOW}[?] Load token from file? (yes/no): {Fore.RESET}").lower()
            if choice == "yes":
                return token

        while True:
            token = input(prompt)
            if not token:
                print(f"{Fore.RED}[!] Please enter an account token!{Fore.RESET}")
                continue
            try:
                split_text = len(token.split("."))
                if split_text != 3:
                    print(f"{Fore.RED}[!] The account token is not valid!{Fore.RESET}")
                    continue
            except IndexError:
                print(f"{Fore.RED}[!] The account token is not valid!{Fore.RESET}")
                continue
            with open('/token.json', 'w') as file:
                dump({"token": token}, file)
            return token

    @staticmethod
    def generate_headers(auth: str) -> Dict[str, str]:
        return {
            "Authorization": auth,
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                           "(KHTML, like Gecko) Chrome/124.0.6367.233 Safari/537.36"),
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin"
        }

    @staticmethod
    def generate_url(guild_id: str) -> str:
        return BASE + f"/guilds/{guild_id}"

    @staticmethod
    def check_validity(response_code: int) -> bool:
        return response_code == 200

    @staticmethod
    async def get_user_and_guild(headers, guild_id):
        user = await Utils.get_user(headers)
        guild = await Utils.get_guild(guild_id, headers)
        return user, guild

    @staticmethod
    async def get_user(headers):
        async with ClientSession() as session:
            url = BASE + f"/users/@me"
            async with session.get(url, headers=headers) as response:
                if response.status != 200:
                    print(f"{Fore.RED}[!] Error getting user : {response.status}{Fore.RESET}")
                    return None
                info = await response.json()
                return info

    @staticmethod
    async def get_guild(guild_id, headers):
        async with ClientSession() as session:
            url = BASE + f"/guilds/{guild_id}"
            async with session.get(url, headers=headers) as response:
                if response.status != 200:
                    print(f"{Fore.RED}[!] Error getting server : {response.status}{Fore.RESET}")
                    return None
                info = await response.json()
                return info

    @staticmethod
    def set_globals(guild_json):
        global G_name, G_json
        G_name, G_json = guild_json.get("name"), guild_json

    @staticmethod
    def confirmation(user, guild):
        print(f"{Fore.YELLOW}[?] Are These Info Correct?:{Fore.RESET}")
        print(f"\n{Fore.WHITE}Your Information:{Fore.RESET}")
        print(f"\n1.{user.get("global_name", user.get("username"))}")
        print(f"2.{user.get("username")}")
        print(f"3.{user.get("email")}")
        print(f"\n{Fore.WHITE}Server Information:{Fore.RESET}")
        print(f"\n1.{guild.get("name")}")
        print(f"2.{guild.get("id")}")
        choice = input("\n[yes/no] :").lower()
        while True:
            if not choice:
                print(f"{Fore.RED}[!] Please Enter Something!{Fore.RESET}")
                choice = input("[yes/no] :").lower()
            elif choice not in ["yes", "no"]:
                print(f"{Fore.RED}[!] Choice is not valid!{Fore.RESET}")
                choice = input("[yes/no] :").lower()
            else:
                return choice == "yes"

    @staticmethod
    def clear_globals():
        global G_name, G_json
        G_name, G_json = None, None

    @staticmethod
    def choose_what_to_download():
        cls()
        print(f"{Fore.BLUE}[+] Choose From The Menu Below!{Fore.RESET}")
        print(f"{Fore.WHITE}\n[1] Download Emoji"
              "\n[2] Download Stickers"
              "\n[3] Download Channels Info (json)"
              "\n[4] Download Roles Info (json)"
              "\n[5] Download Server Info"
              "\n[6] Download Everything"
              f"{Fore.RESET}\n")
        choice = input(f"{Fore.YELLOW}[?] Choice : {Fore.RESET}")
        while True:
            if not choice:
                print(f"{Fore.RED}[!] Please Make A Choice.{Fore.RESET}")
                choice = input(f"{Fore.BLUE}[+] Please Choose Again : {Fore.RESET}")
            elif not choice.isdigit():
                print(f"{Fore.RED}[!] Choice Must be a number.{Fore.RESET}")
                choice = input(f"{Fore.BLUE}[+] Please Choose Again : {Fore.RESET}")
            elif int(choice) not in [1, 2, 3, 4, 5, 6]:
                print(f"{Fore.RED}[!] Invalid Choice.{Fore.RESET}")
                choice = str(input(f"{Fore.BLUE}[+] Please Choose Again : {Fore.RESET}"))
            else:
                choice = int(choice)
                Download(choice=choice)
                system("title Downloaded!")
                Utils.retry()
                return

    @staticmethod
    def sanitize_filename(filename):
        # Replace reserved characters with underscore
        reserved_chars = [r'<', r'>', r':', r'"', r'/', r'\\', r'|', r'?', r'*']
        for char in reserved_chars:
            filename = filename.replace(char, '_')

        # Trim leading and trailing spaces
        filename = filename.strip()

        # Ensure the filename is not empty after sanitization
        if not filename:
            filename = 'File Name is Empty lol'

        return filename


class Download:
    def __init__(self, choice: int):
        system("title Downloading...")
        self.guild = G_json
        self.directory_name = Utils.sanitize_filename(self.guild.get("name"))
        makedirs(name=rf"{self.directory_name}", exist_ok=True)
        self.directory = rf"./{self.directory_name}/"
        print(
            f"{Fore.LIGHTMAGENTA_EX}[#] Current Working Directory: "
            f"{Fore.LIGHTCYAN_EX}{path.abspath(self.directory)}{Fore.RESET}"
        )
        if choice == 1:
            self.choice_1()
        elif choice == 2:
            self.choice_2()
        elif choice == 3:
            self.choice_3()
        elif choice == 4:
            self.choice_4()
        elif choice == 5:
            self.choice_5()
        elif choice == 6:
            self.choice_6()
        else:
            print(f"{Fore.RED}[!] Not A Valid Choice!{Fore.RESET}")

    async def download(self, download_type: str, files: list[Tuple], sub_folder_name: str):
        """
        Downloads A File!
        :param download_type: The Download Type. For ex: Sticker, Emoji, Movie, etc...
        :param files: A list of Tuple containing (name, url, animated).
        :param sub_folder_name: The Folder Where They Will Be saved!
        :return: Nothing
        """
        if len(files) == 0:
            print(f"{Fore.RED}[!] No {download_type} to download!{Fore.RESET}")
            return

        with alive_bar(len(files), title=f'Downloading {download_type}...', spinner='dots') as bar:
            makedirs(path.join(self.directory, sub_folder_name), exist_ok=True)
            async with ClientSession() as session:
                for name, url, animated in files:
                    file_name = name + ".gif" if animated else name + ".png"
                    full_path = path.join(path.join(self.directory, sub_folder_name), file_name)

                    if path.exists(full_path):
                        print(f"{Fore.GREEN}[+] {file_name} is already downloaded!{Fore.RESET}")
                        bar()
                        continue

                    try:
                        async with session.get(url) as response:
                            with open(full_path, 'wb') as file:
                                file.write(await response.read())
                                print(f"{Fore.BLUE}[+] {file_name} is downloaded!{Fore.RESET}")
                    except Exception as download_exception:
                        print(f"{Fore.RED}[!] Can't Download {file_name} because of {download_exception}{Fore.RESET}")
                    finally:
                        bar()
        print(
            f"{Fore.BLUE}[+] All {len(files)} {download_type} Downloaded To "
            f"{Fore.GREEN}{path.join(path.join(getcwd(), self.directory_name), sub_folder_name)}{Fore.RESET}"
        )

    def choice_1(self):
        emoji_list = Guild.emoji(self.guild.get("id"))
        if emoji_list:
            files = [
                (emoji.get("name"), emoji.get("url"), emoji.get("animated"))
                for emojis in emoji_list for _, emoji in emojis.items()
            ]
            run(self.download(files=files, download_type="Emojis", sub_folder_name="emoji"))
        else:
            print(f"{Fore.RED}[!] {self.guild.get("name")} don't have emoji!")

    def choice_2(self):
        sticker_list = Guild.sticker(self.guild.get("id"))
        if sticker_list:
            files = [
                (s.get("name"), s.get("url"), s.get("animated"))
                for sticker in sticker_list for _, s in sticker.items()
            ]
            run(self.download(download_type="Stickers", files=files, sub_folder_name="sticker"))
        else:
            print(f"{Fore.RED}[!] {self.guild.get("name")} don't have stickers!")

    def choice_3(self):
        try:
            with open(f'{self.directory}/{self.directory_name}_channel_info.json', 'w') as choice_3:
                choice_3.flush()
        except Exception as choice_3_exception:
            print(f"{Fore.RED}[!] Can't Flush The File! {choice_3_exception}{Fore.RESET}")
        channel_list = Guild.channel(self.guild.get("id"))
        if channel_list:
            try:
                with open(
                    f"{self.directory}/{self.directory_name}_channel_info.json",
                    'w',
                    encoding="utf-8",
                    errors="ignore"
                ) as choice_3_write:
                    choice_3_write.write(
                        dumps(
                            channel_list,
                            indent=2,
                            ensure_ascii=False
                        )
                    )
                print(f"{Fore.GREEN}[+] Channel Json Downloaded!{Fore.RESET}")
            except Exception as choice_3_exception:
                print(
                    f"{Fore.RED}[!] Can't open : {self.directory_name}_channel_info.json, "
                    f"because of {choice_3_exception}{Fore.RESET}"
                )
                return
        else:
            print(f"{Fore.RED}[!] Seems like {self.guild.get("name")} doesn't have channels!{Fore.RESET}")

    def choice_4(self):
        try:
            with open(f'{self.directory}/{self.directory_name}_role_info.json', 'w') as file:
                file.flush()
        except Exception as choice_4_exception:
            print(f"{Fore.RED}[!] Can't Flush The File! {choice_4_exception}{Fore.RESET}")

        role_list = Guild.role(self.guild.get("id"))
        if role_list:
            try:
                with open(
                        f'{self.directory}/{self.directory_name}_role_info.json',
                        'w',
                        encoding="utf-8",
                        errors="ignore"
                ) as file:
                    file.write(
                        dumps(
                            role_list,
                            indent=2,
                            ensure_ascii=False
                        )
                    )
                print(f"{Fore.GREEN}[+] Roles Json Downloaded!{Fore.RESET}")
            except Exception as choice_4_exception:
                print(
                    f"{Fore.RED}[!] Can't Open : {self.guild.get('name')}_role_info.json, "
                    f"Because of : {choice_4_exception}{Fore.RESET}"
                )
                return
        else:
            print(f"{Fore.RED}[!] Seems like {self.guild.get('name')} doesn't have roles!{Fore.RESET}")

    def choice_5(self):
        info = {
            "Name": Guild.name(self.guild),
            'ID': self.guild.get("id"),
            "Description": Guild.description(self.guild),
            "ICON URL": Guild.icon(self.guild),
            "Banner": Guild.banner(self.guild),
            "Splash": Guild.splash(self.guild),
            "Discovery Splash": Guild.discovery_splash(self.guild)
        }
        try:
            with open(
                    f'{self.directory}/{self.directory_name}_info.json',
                    'w',
                    encoding="utf-8",
                    errors="ignore"
            ) as file:
                file.flush()
                file.write(dumps(info, ensure_ascii=False, indent=2))
            print(f"{Fore.GREEN}[+] Guild Info Json Downloaded!{Fore.RESET}")
        except Exception as choice_5_exception:
            print(
                f"{Fore.RED}[!] Can't Open File: {self.guild.get('name')}_info.json, "
                f"because of {choice_5_exception}{Fore.RESET}"
            )

    def choice_6(self):
        try:
            self.choice_1()
            sleep(uniform(0.6, 1.2))
        except Exception as choice_1_exception:
            print(f"{Fore.RED}[!] Can't Download Emojis Because of {choice_1_exception}{Fore.RESET}")

        try:
            self.choice_2()
            sleep(uniform(0.6, 1.2))
        except Exception as choice_2_exception:
            print(f"{Fore.RED}[!] Can't Download Stickers Because of {choice_2_exception}{Fore.RESET}")

        try:
            self.choice_3()
            sleep(uniform(0.6, 1.2))
        except Exception as choice_3_exception:
            print(f"{Fore.RED}[!] Can't Download Channels info Because of {choice_3_exception}{Fore.RESET}")

        try:
            self.choice_4()
            sleep(uniform(0.6, 1.2))
        except Exception as choice_4_exception:
            print(f"{Fore.RED}[!] Can't Download Roles info Because of {choice_4_exception}{Fore.RESET}")

        try:
            self.choice_5()
            sleep(uniform(0.6, 1.2))
        except Exception as choice_5_exception:
            print(f"{Fore.RED}[!] Can't Download Server info Because of {choice_5_exception}{Fore.RESET}")

        try:
            startfile(path.abspath(self.directory_name))
        except Exception as open_dir_exception:
            print(f"{Fore.RED}[!] Can't Open {self.directory_name}, "
                  f"Because of {open_dir_exception}{Fore.RESET}")

        print(f"{Fore.GREEN}[+] Everything Downloaded!{Fore.RESET}")


def main():

    # Starting Pont
    cls()
    system("title Guild Downloader")

    # Get Basic Info
    guild_id = Utils.get_guild_id()
    token = Utils.get_user_token()

    # Generate headers
    headers = Utils.generate_headers(token)

    # Get User & Guild (async)
    user, guild = run(Utils.get_user_and_guild(headers, guild_id))

    # Checks For User & Guild
    if not user:
        print(f"{Fore.RED}[!] Unable To Get User!")
        main()

    if not guild:
        print(f"{Fore.RED}[!] Unable To Get User!")
        main()

    # Sets Global Variables
    Utils.set_globals(guild)
    cls()

    # Confirmation
    confirm = Utils.confirmation(user, G_json)
    if not confirm:
        Utils.clear_globals()
        main()

    # Shows Menu
    Utils.choose_what_to_download()

    # Retry
    Utils.retry()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f"{Fore.LIGHTCYAN_EX}\n[#] Okay!{Fore.RESET}")
        exit(0)
    except Exception as e:
        print(f"{Fore.RED}[!] Got An Exception :{e}")
        Utils.retry()
