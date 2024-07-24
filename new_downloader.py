# Standard Packages
from os import system, path, makedirs, startfile, getcwd, walk
from platform import system as psys
from json import dump, load
from typing import Optional, Tuple
from asyncio import run
from time import sleep
from random import uniform

# external packages
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
    from colorama import Fore, init
except ModuleNotFoundError:
    print("[!] colorama Module Not Found!, Downloading...")
    system("pip install colorama")
    from colorama import Fore, init
try:
    from fake_useragent import UserAgent
except ModuleNotFoundError:
    system("pip install fake-useragent")
    from fake_useragent import UserAgent


init(autoreset=True)


def success(text: str):
    print(f"{Fore.LIGHTGREEN_EX}[+] {text.title()}")


def error(text: str):
    print(f"{Fore.LIGHTRED_EX}[!] {text.title()}")


def info(text: str):
    print(f"{Fore.LIGHTMAGENTA_EX}[?] {text.title()}")


class Utility:
    def __init__(self):
        self.os = psys().lower()
        self.token_file_name = "token.json"
        self.guild_id = None
        self.__token__ = None
        self.headers = {}
        self.user = {}
        self.guild = {}
        self.main_art = f"""
        ██████╗   ██████╗  ██╗    ██╗ ███╗   ██╗ ██╗       ██████╗   █████╗  ██████╗  ███████╗ ██████╗ 
        ██╔══██╗ ██╔═══██╗ ██║    ██║ ████╗  ██║ ██║      ██╔═══██╗ ██╔══██╗ ██╔══██╗ ██╔════╝ ██╔══██╗
        ██║  ██║ ██║   ██║ ██║ █╗ ██║ ██╔██╗ ██║ ██║      ██║   ██║ ███████║ ██║  ██║ █████╗   ██████╔╝
        ██║  ██║ ██║   ██║ ██║███╗██║ ██║╚██╗██║ ██║      ██║   ██║ ██╔══██║ ██║  ██║ ██╔══╝   ██╔══██╗
        ██████╔╝ ╚██████╔╝ ╚███╔███╔╝ ██║ ╚████║ ███████╗ ╚██████╔╝ ██║  ██║ ██████╔╝ ███████╗ ██║  ██║
        ╚═════╝   ╚═════╝   ╚══╝╚══╝  ╚═╝  ╚═══╝ ╚══════╝  ╚═════╝  ╚═╝  ╚═╝ ╚═════╝  ╚══════╝ ╚═╝  ╚═╝
        """
        self.menu_art = f"""
        ███╗   ███╗ ███████╗ ███╗   ██╗ ██╗   ██╗
        ████╗ ████║ ██╔════╝ ████╗  ██║ ██║   ██║
        ██╔████╔██║ █████╗   ██╔██╗ ██║ ██║   ██║
        ██║╚██╔╝██║ ██╔══╝   ██║╚██╗██║ ██║   ██║
        ██║ ╚═╝ ██║ ███████╗ ██║ ╚████║ ╚██████╔╝
        ╚═╝     ╚═╝ ╚══════╝ ╚═╝  ╚═══╝  ╚═════╝ 
        """
        self.downloading_art = f"""
        ███████╗  █████╗  ██╗   ██╗ ██╗ ███╗   ██╗  ██████╗ 
        ██╔════╝ ██╔══██╗ ██║   ██║ ██║ ████╗  ██║ ██╔════╝ 
        ███████╗ ███████║ ██║   ██║ ██║ ██╔██╗ ██║ ██║  ███╗
        ╚════██║ ██╔══██║ ╚██╗ ██╔╝ ██║ ██║╚██╗██║ ██║   ██║
        ███████║ ██║  ██║  ╚████╔╝  ██║ ██║ ╚████║ ╚██████╔╝
        ╚══════╝ ╚═╝  ╚═╝   ╚═══╝   ╚═╝ ╚═╝  ╚═══╝  ╚═════╝ 
        """

    def retry(self):
        retry_prompt = input(f"{Fore.LIGHTYELLOW_EX}[?] Retry? (yes/no): {Fore.RESET}").lower()
        while retry_prompt not in ["yes", "no", "y", "n"]:
            retry_prompt = input(f"{Fore.LIGHTYELLOW_EX}[?] Retry? (yes/no): {Fore.RESET}").lower()
        if retry_prompt in ["no", "n"]:
            print(f"{Fore.GREEN}[#] Everything went smoothly and all emojis were downloaded!")
            exit(0)
        else:
            self.main_entrypoint()

    def main_cls(self):
        if self.os in ["windows", "nt"]:
            system("cls")
            print(f"{Fore.LIGHTCYAN_EX}{self.main_art}")
        else:
            system("clear")
            print(f"{Fore.LIGHTCYAN_EX}{self.main_art}")

    def menu_cls(self):
        if self.os in ["windows", "nt"]:
            system("cls")
            print(f"{Fore.LIGHTCYAN_EX}{self.menu_art}")
        else:
            system("clear")
            print(f"{Fore.LIGHTCYAN_EX}{self.menu_art}")

    def downloading_cls(self, download_path: str):
        if self.os in ["windows", "nt"]:
            system("cls")
            print(f"{Fore.LIGHTCYAN_EX}{self.downloading_art}")
            print(f"Download path: \"{Fore.LIGHTMAGENTA_EX}{download_path}{Fore.RESET}\"")
        else:
            system("clear")
            print(f"{Fore.LIGHTCYAN_EX}{self.downloading_art}")
            print(f"Download path: \"{Fore.LIGHTMAGENTA_EX}{download_path}{Fore.RESET}\"")

    def get_guild_id(self) -> int:
        prompt = f"{Fore.LIGHTBLUE_EX}[+] Enter The Guild ID (ls to list all server): {Fore.RESET}\n"
        while True:
            guild_id = input(prompt)
            if not guild_id:
                self.main_cls()
                error("Please enter a Guild ID!")
            elif guild_id == "exit":
                success("Okay!")
                exit(0)
            elif guild_id == "ls":
                self.guild_id = int(self.list_guilds()[0])
                return self.guild_id
            elif not guild_id.isdigit():
                self.main_cls()
                error("entered id is not digit!")
            elif not len(guild_id) > 5:
                self.main_cls()
                error("guild id can't be so small!")
            else:
                self.guild_id = int(guild_id)
                return self.guild_id

    def get_user_token(self) -> str:
        token = self.validate()
        prompt = f"{Fore.LIGHTBLUE_EX}[+] Enter Your Account Token (h for help): \n"

        if token:
            choice = input(f"{Fore.LIGHTYELLOW_EX}[?] Load token from file? (yes/no): {Fore.RESET}\n").lower()
            while choice not in ["yes", "no", "y", "n"]:
                self.main_cls()
                choice = input(f"{Fore.LIGHTYELLOW_EX}[?] Load token from file? (yes/no): {Fore.RESET}\n").lower()
            if choice in ["yes", "y"]:
                self.__token__ = token
                return self.__token__

        while True:
            token = input(prompt)
            if not token:
                self.main_cls()
                error("please enter a token")
                continue
            if token in ["h", "help"]:
                self.main_cls()
                system("start https://github.com/max-4-3/discord-guild-downloader/blob/main/how%20to%20get%20token.md")
                continue
            try:
                split_text = len(token.split("."))
                if split_text != 3:
                    self.main_cls()
                    error("The account token is not valid!")
                    continue
            except IndexError:
                self.main_cls()
                error("The account token is not valid!")
                continue
            with open(f'{self.token_file_name}', 'w') as file:
                dump({"token": token}, file)
            self.__token__ = token
            return self.__token__

    def validate(self) -> Optional[str]:
        try:
            if not path.exists(self.token_file_name):
                return
            with open(self.token_file_name, 'r') as file:
                token = load(file).get("token")
            if not token or len(token.split(".")) != 3:
                return
            return token
        except Exception as token_exception:
            error(f"Got An Exception While Opening \"{self.token_file_name}\" File, {token_exception}")
            return

    def generate_headers(self, auth: str) -> dict[str, str]:
        self.headers.update({
            "Authorization": auth,
            "User-Agent": UserAgent().random
        })
        return self.headers

    async def get_user_and_guild(self):
        async with ClientSession() as session:
            info("getting user info...")
            self.user = await self.get_user(session)
            info("getting server info...")
            self.guild = await self.get_guild(session)
            return self.user, self.guild

    async def get_user(self, session: ClientSession):
        url = BASE + f"/users/@me"
        async with session.get(url, headers=self.headers) as response:
            if response.status != 200:
                error(f"Error getting user : {response.status}")
                return None
            return await response.json()

    async def get_guild(self, session: ClientSession):
        url = BASE + f"/guilds/{self.guild_id}"
        async with session.get(url, headers=self.headers, params={"with_counts": "true"}) as response:
            if response.status != 200:
                error(f"Error getting guild : {response.status}")
                return None
            return await response.json()

    async def get_guilds(self):
        async with ClientSession() as session:
            url = f"{BASE}/users/@me/guilds"
            self.headers = self.generate_headers(self.__token__)
            async with session.get(url, headers=self.headers) as response:
                guilds_json = await response.json()
                return {idx: (g.get("id"), g.get("name")) for idx, g in enumerate(guilds_json, start=1)}

    def list_guilds(self):
        guild_list = run(self.get_guilds())

        def print_guilds():
            for idx, guild_info in guild_list.items():
                print(f"{idx}. {guild_info[1]}")

        print_guilds()
        while True:
            choice = input(f"{Fore.LIGHTMAGENTA_EX}Choose The Guild: {Fore.RESET}\n")
            if not choice:
                error("choose a guild!")
                self.main_cls()
                print_guilds()
            elif not choice.isdigit():
                error("enter only number!")
                self.main_cls()
                print_guilds()
            elif int(choice) > len(guild_list):
                error("not in guild list")
                self.main_cls()
                print_guilds()
            else:
                for key, value in guild_list.items():
                    if key == int(choice):
                        return value

    def confirmation(self):
        user, guild = self.user, self.guild
        self.main_cls()
        i = f'''
{Fore.LIGHTBLUE_EX}Your Information:{Fore.LIGHTWHITE_EX}
    Name: {user.get("global_name", user.get("username"))}
    Username: {user.get("username", user.get("id"))}
    Contact Info: {user.get("email", "no email.")}

{Fore.LIGHTBLUE_EX}Server Information:{Fore.LIGHTWHITE_EX}
    Name: {guild.get("name", "no name")}
    ID: {guild.get("id")}
        '''
        info("is this info correct?")
        print(i)
        choice = input("\n[yes/no] :").lower()
        while True:
            if not choice:
                self.main_cls()
                print(i)
                error("please enter something!")
                choice = input("[yes/no] :").lower()
            elif choice not in ["yes", "no", "y", "n"]:
                self.main_cls()
                print(i)
                error("invalid choice, choose between (y, n, yes, no)!")
                choice = input("[yes/no] :").lower()
            else:
                return choice in ["yes", "y"]

    def choose_what_to_download(self):
        self.menu_cls()
        menu = rf'''
[1] Download Emoji
[2] Download Stickers
[3] Download Channels Info (json)
[4] Download Roles Info (json)
[5] Download Server Info
[6] Download Everything
        '''
        print(f"{Fore.LIGHTMAGENTA_EX}[+] Choose From The Menu Below!")
        print(menu)

        choice = input(f"{Fore.LIGHTYELLOW_EX}[?] Choice : {Fore.RESET}")
        while True:
            if not choice:
                self.menu_cls()
                print(menu)
                error("make a choice!")
                choice = input(f"{Fore.LIGHTBLUE_EX}[+] Please Choose Again : {Fore.RESET}")
            elif not choice.isdigit():
                self.menu_cls()
                print(menu)
                error(f"choice is not a number! [{choice}]")
                choice = input(f"{Fore.LIGHTBLUE_EX}[+] Please Choose Again : {Fore.RESET}")
            elif int(choice) not in [1, 2, 3, 4, 5, 6]:
                self.menu_cls()
                print(menu)
                error(f"invalid choice! [{choice}]")
                choice = input(f"{Fore.LIGHTBLUE_EX}[+] Please Choose Again : {Fore.RESET}")
            else:
                choice = int(choice)
                Download(choice=choice, guild_json=self.guild, headers=self.headers)
                system("title Downloading!")
                self.retry()
                return

    def main_entrypoint(self, **errors):
        system("title Guild Downloader")
        self.main_cls()

        if errors.get("with_error"):
            error("\n".join(errors.get("errors")))

        # Get Basic Info
        token = self.get_user_token()
        self.main_cls()
        self.get_guild_id()
        self.main_cls()

        # Generate headers
        self.generate_headers(token)

        # Get User & Guild (async)
        user, guild = run(self.get_user_and_guild())

        errors_ = []

        # Checks For User & Guild
        if not user:
            errors_.append("unable to get user!")

        if not guild:
            errors_.append("unable to get guild!")

        if not user or not guild:
            self.main_entrypoint(with_error=True, errors=errors_)

        self.main_cls()

        # Confirmation
        confirm = self.confirmation()
        if not confirm:
            self.main_entrypoint()

        # Shows Menu
        self.choose_what_to_download()

        # Retry
        self.retry()

    @staticmethod
    def sanitize_filename(filename):
        reserved_chars = [r'<', r'>', r':', r'"', r'/', r'\\', r'|', r'?', r'*']
        for char in reserved_chars:
            filename = filename.replace(char, '_')

        filename = filename.strip()

        if not filename:
            filename = 'File Name is Empty lol'

        return filename


class Guild(Utility):

    def __init__(self, guild_json: dict, headers: dict):
        super().__init__()
        self.__raw__ = guild_json
        self.headers = headers
        self.guild_id = self.__raw__.get("id")

        # basic
        self.name = self.__raw__.get("name", "No Name LOL")
        self.description = self.__raw__.get("description", "No Description! Noob server")
        self.icon = self.get_icon()
        self.splash = self.get_splash()
        self.banner = self.get_banner()
        self.discovery_splash = self.get_discovery_splash()

        # external
        self.emojis = self.get_emoji()
        self.stickers = self.get_sticker()
        self.channels = self.get_channel()
        self.roles = self.get_role()

    def get_emoji(self) -> list[dict[int, dict[str, str | bool]]] | None:
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
            data = self.__raw__.get("emojis", None)
            if not data:
                data = get(f"{BASE}/guilds/{self.guild_id}/emojis", headers=self.headers).json()
            return extract_emoji_info(data)
        except Exception as emoji_exception:
            error(f"got an error while getting emojis, {emoji_exception}")
            return

    def get_role(self) -> list[dict[str, str]] | None:

        def extract_role_info(roles_raw) -> list[dict[str, str]]:
            roles = roles_raw
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
            data = self.__raw__.get("roles", None)
            if not data:
                data = get(f"{BASE}/guilds/{self.guild_id}/roles", headers=self.headers).json()
            return extract_role_info(data)
        except Exception as roles_exception:
            error(f"error getting roles, {roles_exception}")
            return None

    def get_channel(self) -> list[dict[str, str | int | dict[str, str | int]]] | None:

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
            data = get(f"{BASE}/guilds/{self.guild_id}/channels", headers=self.headers).json()
            return extract_channel_info(data)
        except Exception as channels_exception:
            error(f"error getting channels info {channels_exception}")
            return

    def get_sticker(self) -> list[dict[int, dict[str, str | bool]]] | None:

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
                    error(f"{s.get('name')} can't be downloaded!")
            return stick_url_list

        try:
            data = self.__raw__.get("stickers", None)
            if not data:
                data = get(f"{BASE}/guilds/{self.guild_id}/stickers", headers=self.headers).json()
            return extract_sticker_info(data)
        except Exception as sticker_exception:
            error(f"error getting stickers, {sticker_exception}")
            return None

    def get_icon(self) -> None | str:
        icon_hash = self.__raw__.get("icon", None)
        if not icon_hash:
            error(f"{self.name} don't have any icon!")
            return
        fmt = ".gif" if icon_hash.startswith("a_") else ".png"
        return f"{ASSET_BASE}/icons/{self.guild_id}/{icon_hash}{fmt}?size=4096"

    def get_banner(self) -> None | str:
        banner_hash = self.__raw__.get("banner", None)
        if not banner_hash:
            error(f"{self.name} don't have any banner!")
            return
        fmt = ".gif" if banner_hash.startswith("a_") else ".png"
        return f"{ASSET_BASE}/banner/{self.guild_id}/{banner_hash}{fmt}?size=4096"

    def get_splash(self) -> None | str:
        splash_hash = self.__raw__.get("splash", None)
        if not splash_hash:
            error(f"{self.name} don't have any splash!")
            return
        fmt = ".gif" if splash_hash.startswith("a_") else ".png"
        return f"{ASSET_BASE}/splashes/{self.guild_id}/{splash_hash}{fmt}?size=4096"

    def get_discovery_splash(self) -> None | str:
        discovery_splash_hash = self.__raw__.get("discovery_splash", None)
        if not discovery_splash_hash:
            error(f"{self.name} don't have any discovery splash!")
            return
        fmt = ".gif" if discovery_splash_hash.startswith("a_") else ".png"
        return f"{ASSET_BASE}/discovery-splashes/{self.guild_id}/{discovery_splash_hash}.{fmt}?size=4096"

    def __repr__(self):
        r = f'''
{Fore.LIGHTCYAN_EX}Basic Info:{Fore.LIGHTWHITE_EX}
Name: {self.name}
id: {self.guild_id}
description: {self.description}
icon: {self.icon}
splash: {self.splash}
discovery splash: {self.discovery_splash}
banner: {self.banner}

{Fore.LIGHTCYAN_EX}Media Info:{Fore.LIGHTWHITE_EX}
{self.name} has {len(self.emojis)} emojis.
{self.name} has {len(self.stickers)} stickers.

{Fore.LIGHTCYAN_EX}Advance Info:{Fore.LIGHTWHITE_EX}
{self.name} has {len(self.roles)} roles.
{self.name} has {len(self.channels)} channels.
{self.name} has following features:
{"\t".join(self.__raw__.get("features", []))}

{Fore.LIGHTCYAN_EX}Presence Info:{Fore.LIGHTWHITE_EX}
{self.name} has {self.__raw__.get("approximate_member_count", "\"not able to get\"")} members (approx).
{self.name} has {self.__raw__.get("approximate_presence_count", "\"not able to get\"")} members online (approx).
        '''
        return r


class Download(Guild):
    def __init__(self, choice: int, guild_json: dict, headers: dict):
        super().__init__(guild_json, headers)
        system("title Downloading...")

        self.directory_name = self.sanitize_filename(self.name)
        makedirs(name=rf"{self.directory_name}", exist_ok=True)
        self.directory = rf"{self.directory_name}"
        self.downloading_cls(self.directory)
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
            error("not a valid choice")

    async def download(self, download_type: str, files: list[Tuple], sub_folder_name: str):
        """
        Downloads A File!
        :param download_type: The Download Type. For ex: Sticker, Emoji, Movie, etc...
        :param files: A list of Tuple containing (name, url, animated).
        :param sub_folder_name: The Folder Where They Will Be saved!
        :return: Nothing
        """
        file_size = 0

        if len(files) == 0:
            error(f"no {download_type} to download")
            return

        with alive_bar(len(files), title=f'Downloading {download_type}...', spinner='dots') as bar:
            makedirs(path.join(self.directory, sub_folder_name), exist_ok=True)
            async with ClientSession() as session:
                prev_id = None
                for name, id_, url, animated in files:
                    name = self.sanitize_filename(name)
                    file_name = name + ".gif" if animated else name + ".png"
                    full_path = path.join(path.join(self.directory, sub_folder_name), file_name)

                    if path.exists(full_path):
                        if prev_id == id_:
                            exist_size_kb = path.getsize(full_path) / 1024
                            file_size += exist_size_kb
                            success(f"{file_name} already exists ({exist_size_kb:.2f}kb)!")
                            bar()
                            continue
                        else:
                            name += f"_dup_{id_}"
                            file_name = name + ".gif" if animated else name + ".png"
                            full_path = path.join(path.join(self.directory, sub_folder_name), file_name)

                    try:
                        async with session.get(url) as response:
                            with open(full_path, 'wb') as file:
                                byte = await response.read()
                                file.write(byte)
                                size_in_kb = len(byte) / 1024
                                success(f"\"{file_name}\" downloaded ({size_in_kb:.2f}kb)!")
                                file_size += size_in_kb
                    except Exception as download_exception:
                        error(f"Can't Download {file_name} because of {download_exception}")
                    finally:
                        bar()
                    prev_id = id_
                    sleep(0.1)
        abs_path = path.join(path.join(getcwd(), self.directory_name), sub_folder_name)
        success(
            f"All {len(files)} files downloaded in \"{abs_path}\", size: {file_size / 1024:.2f}MB ({file_size:.2f}KB)"
        )

    def choice_1(self):
        emoji_list = self.emojis
        if emoji_list:
            files = [
                (emoji.get("name"), emoji.get("id"), emoji.get("url"), emoji.get("animated"))
                for emojis in emoji_list for _, emoji in emojis.items()
            ]
            run(self.download(files=files, download_type="Emojis", sub_folder_name="emoji"))
        else:
            error(f"{self.guild.get("name")} don't have emoji!")

    def choice_2(self):
        sticker_list = self.stickers
        if sticker_list:
            files = [
                (s.get("name"), s.get("id"), s.get("url"), s.get("animated"))
                for sticker in sticker_list for _, s in sticker.items()
            ]
            run(self.download(download_type="Stickers", files=files, sub_folder_name="sticker"))
        else:
            error(f"seems like {self.name} don't have stickers!")

    def choice_3(self):
        try:
            with open(f'{self.directory}/{self.directory_name}_channel_info.json', 'w') as choice_3:
                choice_3.flush()
        except Exception as choice_3_exception:
            error(f"Can't Flush The File! {choice_3_exception}")
        channel_list = self.channels
        if channel_list:
            try:
                with open(
                        f"{self.directory}/{self.directory_name}_channel_info.json",
                        'w',
                        encoding="utf-8",
                        errors="ignore"
                ) as choice_3_write:
                    dump(channel_list, choice_3_write, ensure_ascii=False, indent=2)
                success(f"channels info downloaded!")
            except Exception as choice_3_exception:
                error(f"can't open {self.directory_name}_channel_info.json, because: {choice_3_exception}")
                return
        else:
            error(f"seems like {self.name} don't have channels! strange?")

    def choice_4(self):
        try:
            with open(f'{self.directory}/{self.directory_name}_role_info.json', 'w') as file:
                file.flush()
        except Exception as choice_4_exception:
            error(f"Can't Flush The File \"{self.directory}/{self.directory_name}_role_info.json\"!"
                  f"\nbecause of: {choice_4_exception}")

        role_list = self.roles
        if role_list:
            try:
                with open(
                        f'{self.directory}/{self.directory_name}_role_info.json',
                        'w',
                        encoding="utf-8",
                        errors="ignore"
                ) as file:
                    dump(role_list, file, ensure_ascii=False, indent=2)
                    success(f"roles info downloaded!")
            except Exception as choice_4_exception:
                error(f"can't open {self.directory_name}_role_info.json, because: {choice_4_exception}")
                return
        else:
            error(f"seems like {self.name} don't have roles!")

    def choice_5(self):
        inf = f'''
- Basic Info:
Name: {self.name}
id: {self.guild_id}
description: {self.description}
icon: {self.icon}
splash: {self.splash}
discovery splash: {self.discovery_splash}
banner: {self.banner}

- Media Info:
{self.name} has {len(self.emojis)} emojis.
{self.name} has {len(self.stickers)} stickers.

- Advance Info:
{self.name} has {len(self.roles)} roles.
{self.name} has {len(self.channels)} channels.
{self.name} has following features:
    {"\n    ".join(self.__raw__.get("features", []))}

- Presence Info:
{self.name} has {self.__raw__.get("approximate_member_count", "\"not able to get\"")} members (approx).
{self.name} has {self.__raw__.get("approximate_presence_count", "\"not able to get\"")} members online (approx).
        '''
        try:
            with open(
                    f'{self.directory}/{self.directory_name}_info.txt',
                    'w',
                    encoding="utf-8",
                    errors="ignore"
            ) as file:
                file.flush()
                file.write(inf.lstrip())
            success(f"{self.name} info downloaded!")
        except Exception as choice_5_exception:
            error(f"can't open {self.directory_name}_info.json, because: {choice_5_exception}")
            return

    def choice_6(self):
        try:
            self.choice_1()
            sleep(uniform(0.6, 1.2))
        except Exception as choice_1_exception:
            error(f"can't download emojis because of {choice_1_exception}")

        try:
            self.choice_2()
            sleep(uniform(0.6, 1.2))
        except Exception as choice_2_exception:
            error(f"can't download stickers because of {choice_2_exception}")

        try:
            self.choice_3()
            sleep(uniform(0.6, 1.2))
        except Exception as choice_3_exception:
            error(f"can't download roles info because of {choice_3_exception}")

        try:
            self.choice_4()
            sleep(uniform(0.6, 1.2))
        except Exception as choice_4_exception:
            error(f"can't download channels info because of {choice_4_exception}")

        try:
            self.choice_5()
            sleep(uniform(0.6, 1.2))
        except Exception as choice_5_exception:
            error(f"can't download server info because of {choice_5_exception}")

        try:
            startfile(path.abspath(self.directory_name))
        except Exception as open_dir_exception:
            error(f"Can't open \"{self.directory_name}\"!"
                  f"\nbecause of: {open_dir_exception}")

        size_in_byte = 0
        total_files = 0
        total_gifs = 0
        for root, dirs, files in walk(self.directory):
            for file in files:
                name, ext = path.splitext(file)
                if ext == ".gif":
                    total_gifs += 1
                file_path = path.join(root, file)
                if not path.isfile(file_path):
                    continue
                total_files += 1
                file_size = path.getsize(file_path)
                size_in_byte += file_size

        system("title Downloaded!")
        success("everything downloaded!")
        print(f"{Fore.LIGHTCYAN_EX}[+] Total Size: {size_in_byte / 1024:.2f}kb ({size_in_byte / (1024*1024):.2f}mb)"
              f"\n[+] Total Files: {total_files} files ({total_files - total_gifs} images and {total_gifs} gifs)")


if __name__ == '__main__':
    Utility().main_entrypoint()
