# Standard Packages
from os import system, path, makedirs, startfile, getcwd, walk
from platform import system as psys
from json import dump, load
from typing import Optional, Tuple
from asyncio import run
from time import sleep, perf_counter
from random import uniform
from tkinter import filedialog
from random import choice

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

init(autoreset=True)


def success(text: str):
    print(f"{Fore.LIGHTGREEN_EX}[+] {text.capitalize()}")


def error(text: str):
    print(f"{Fore.LIGHTRED_EX}[!] {text.capitalize()}")


def info(text: str):
    print(f"{Fore.LIGHTMAGENTA_EX}[?] {text.capitalize()}")


class UserAgent:
    def __init__(self) -> None:
        self.__ua_list = None

        self.set_agent()

    def set_agent(self):
        agents = r'''
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.1
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.3
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.
Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.3
Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 OPR/106.0.0.
Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.3
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.6
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.3
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.2
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.3
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.4
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.3
Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.
Mozilla/5.0 (X11; CrOS x86_64 14541.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.3
Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.3
Mozilla/5.0 (iPhone; CPU iPhone OS 17_2_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.
Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Mobile Safari/537.3
Mozilla/5.0 (iPhone; CPU iPhone OS 16_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.2 Mobile/15E148 Safari/604.
Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.3
Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.3
Mozilla/5.0 (Linux; Android 10; MAR-LX1A) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 Mobile Safari/537.3
Mozilla/5.0 (Linux; Android 14; SAMSUNG SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/23.0 Chrome/115.0.0.0 Mobile Safari/537.3
Mozilla/5.0 (Linux; Android 14; SAMSUNG SM-S908B) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/23.0 Chrome/115.0.0.0 Mobile Safari/537.3
Mozilla/5.0 (iPhone; CPU iPhone OS 17_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3 Mobile/15E148 Safari/604.
Mozilla/5.0 (Linux; Android 13; SAMSUNG SM-A546B) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/23.0 Chrome/115.0.0.0 Mobile Safari/537.3
Mozilla/5.0 (iPhone; CPU iPhone OS 15_8 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/120.0.6099.119 Mobile/15E148 Safari/604.
Mozilla/5.0 (iPhone; CPU iPhone OS 16_1_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Mobile/15E148 Safari/604.
Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/121.0.6167.66 Mobile/15E148 Safari/604.
Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) GSA/300.0.598994205 Mobile/15E148 Safari/604.
Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.3
Mozilla/5.0 (Linux; Android 10; YAL-L21; HMSCore 6.13.0.302; GMSCore 24.02.13) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.88 HuaweiBrowser/14.0.2.311 Mobile Safari/537.3
Mozilla/5.0 (Linux; Android 11; moto e20 Build/RONS31.267-94-14) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.230 Mobile Safari/537.3
Mozilla/5.0 (Linux; Android 13; SAMSUNG SM-G781B) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/23.0 Chrome/115.0.0.0 Mobile Safari/537.3
Mozilla/5.0 (Linux; Android 13; SAMSUNG SM-G990B2) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/23.0 Chrome/115.0.0.0 Mobile Safari/537.3
Mozilla/5.0 (Linux; Android 14; SAMSUNG SM-A528B) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/23.0 Chrome/115.0.0.0 Mobile Safari/537.3
Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/120.0.6099.119 Mobile/15E148 Safari/604.
Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Mobile Safari/537.3
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/120.0.2210.144
Mozilla/5.0 (Windows NT 10.0; Win64; x64; Xbox; Xbox One) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edge/44.18363.8131
Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/122.0
Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:115.0) Gecko/20100101 Firefox/115.0
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 OPR/106.0.0.0
Mozilla/5.0 (Windows NT 10.0; WOW64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 OPR/106.0.0.0
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/120.0.2210.144
Mozilla/5.0 (Macintosh; Intel Mac OS X 14.3; rv:109.0) Gecko/20100101 Firefox/122.0
Mozilla/5.0 (Macintosh; Intel Mac OS X 14.3; rv:115.0) Gecko/20100101 Firefox/115.0
Mozilla/5.0 (Macintosh; Intel Mac OS X 14_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15
Mozilla/5.0 (Macintosh; Intel Mac OS X 14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 OPR/106.0.0.0
Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36
Mozilla/5.0 (X11; Linux i686; rv:109.0) Gecko/20100101 Firefox/122.0
Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/122.0
Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:109.0) Gecko/20100101 Firefox/122.0
Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/122.0
Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/122.0
Mozilla/5.0 (X11; Linux i686; rv:115.0) Gecko/20100101 Firefox/115.0
Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:115.0) Gecko/20100101 Firefox/115.0
Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:115.0) Gecko/20100101 Firefox/115.0
Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:115.0) Gecko/20100101 Firefox/115.0
Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 OPR/106.0.0.0
Mozilla/5.0 (iPhone; CPU iPhone OS 17_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/121.0.6167.66 Mobile/15E148 Safari/604.1
Mozilla/5.0 (iPhone; CPU iPhone OS 17_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 EdgiOS/120.2210.150 Mobile/15E148 Safari/605.1.15
Mozilla/5.0 (iPhone; CPU iPhone OS 14_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) FxiOS/122.0 Mobile/15E148 Safari/605.1.15
Mozilla/5.0 (iPhone; CPU iPhone OS 17_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1
Mozilla/5.0 (iPod; CPU iPhone OS 17_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/121.0.6167.66 Mobile/15E148 Safari/604.1
Mozilla/5.0 (iPod touch; CPU iPhone OS 14_3 like Mac OS X) AppleWebKit/604.5.6 (KHTML, like Gecko) FxiOS/122.0 Mobile/15E148 Safari/605.1.15
Mozilla/5.0 (iPod touch; CPU iPhone 17_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1
Mozilla/5.0 (iPad; CPU OS 14_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) FxiOS/122.0 Mobile/15E148 Safari/605.1.15
Mozilla/5.0 (iPad; CPU OS 17_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1
Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6167.101 Mobile Safari/537.36
Mozilla/5.0 (Linux; Android 10; HD1913) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6167.101 Mobile Safari/537.36 EdgA/120.0.2210.141
Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6167.101 Mobile Safari/537.36 EdgA/120.0.2210.141
Mozilla/5.0 (Linux; Android 10; Pixel 3 XL) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6167.101 Mobile Safari/537.36 EdgA/120.0.2210.141
Mozilla/5.0 (Linux; Android 10; ONEPLUS A6003) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6167.101 Mobile Safari/537.36 EdgA/120.0.2210.141
Mozilla/5.0 (Windows Mobile 10; Android 10.0; Microsoft; Lumia 950XL) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36 Edge/40.15254.603
Mozilla/5.0 (Android 14; Mobile; rv:109.0) Gecko/122.0 Firefox/122.0
Mozilla/5.0 (Android 14; Mobile; LG-M255; rv:122.0) Gecko/122.0 Firefox/122.0
Mozilla/5.0 (Linux; Android 10; VOG-L29) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6167.101 Mobile Safari/537.36 OPR/76.2.4027.73374
Mozilla/5.0 (Linux; Android 10; SM-G970F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6167.101 Mobile Safari/537.36 OPR/76.2.4027.73374
Mozilla/5.0 (Linux; Android 10; SM-N975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6167.101 Mobile Safari/537.36 OPR/76.2.4027.73374
Mozilla/5.0 (Linux; Android 13; SM-S901B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36
Mozilla/5.0 (Linux; Android 13; SM-S901U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36
Mozilla/5.0 (Linux; Android 13; SM-S908B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36
Mozilla/5.0 (Linux; Android 13; SM-S908U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Mobile Safari/537.36
Mozilla/5.0 (Linux; Android 13; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36
Mozilla/5.0 (Linux; Android 13; SM-G991U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36
Mozilla/5.0 (Linux; Android 13; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36
Mozilla/5.0 (Linux; Android 13; SM-G998U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36
Mozilla/5.0 (Linux; Android 13; SM-A536B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36
Mozilla/5.0 (Linux; Android 13; SM-A536U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36
Mozilla/5.0 (Linux; Android 13; SM-A515F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36
Mozilla/5.0 (Linux; Android 13; SM-A515U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36
Mozilla/5.0 (Linux; Android 12; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36
Mozilla/5.0 (Linux; Android 12; SM-G973U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36
'''.strip().splitlines(keepends=False)
        self.__ua_list = agents
        return agents

    def random(self):
        return choice(self.__ua_list)


class Utility:
    def __init__(self):
        self.os = psys().lower()
        self.config_file_name = "config.json"
        self.guild_id = None
        self.__token__ = None
        self.headers = {}
        self.user = {}
        self.guild = {}
        self.guild_owner = {}
        self.download_dir = self.load_config().get("path", ".")
        self.user_agents = UserAgent()
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

    def get_user_agent(self):
        return

    def retry(self):
        
        system("title Rerun?")
        
        retry_prompt = input(f"{Fore.LIGHTYELLOW_EX}[?] Retry? (yes/no): {Fore.RESET}").lower()
        while retry_prompt not in ["yes", "no", "y", "n"]:
            retry_prompt = input(f"{Fore.LIGHTYELLOW_EX}[?] Retry? (yes/no): {Fore.RESET}").lower()
        if retry_prompt in ["no", "n"]:
            print(f"{Fore.GREEN}[#] Okay!")
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
            print(f"Download path: \"{Fore.LIGHTMAGENTA_EX}{path.relpath(download_path)}{Fore.RESET}\"")
        else:
            system("clear")
            print(f"{Fore.LIGHTCYAN_EX}{self.downloading_art}")
            print(f"Download path: \"{Fore.LIGHTMAGENTA_EX}{path.relpath(download_path)}{Fore.RESET}\"")

    def get_guild_id(self) -> int:
        
        system("title Getting Server ID")
        
        prompt = f"{Fore.LIGHTBLUE_EX}[+] Enter The Guild ID (ls to list all server): {Fore.RESET}\n"
        while True:
            guild_id = input(prompt).lower()
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

    @staticmethod
    def is_valid_string(string: str):
        return len(string.strip().split(".")) == 3

    def get_user_token(self) -> str:
        
        system("title Getting Token...")

        token = self.validate()
        if token:
            while True:
                token_choice = input(f"{Fore.LIGHTYELLOW_EX}[?] Load token from file? (yes/no): {Fore.RESET}\n").lower()
                if token_choice not in ["yes", "no", "y", "n"]:
                    self.main_cls()
                    continue
                elif token_choice in ["yes", "y"]:
                    self.__token__ = token
                    self.save_config()
                    return self.__token__
                elif token_choice in ["no", "n"]:
                    break

        prompt = f"{Fore.LIGHTBLUE_EX}[+] Enter Your Account Token (h for help): \n"
        while True:
            token = input(prompt)
            if not token:
                self.main_cls()
                error("please enter a token")
                continue

            elif token in ["h", "help"]:
                self.main_cls()
                system("start https://github.com/max-4-3/discord-guild-downloader/blob/main/how%20to%20get%20token.md")
                continue

            elif not self.is_valid_string(token):
                self.main_cls()
                error("invalid token given!")
                continue

            self.__token__ = token
            self.save_config()
            return self.__token__

    def save_config(self):
        with open(f"{self.config_file_name}", "w", encoding="utf-8", errors="ignore") as file:
            i = {"token": self.__token__, "path": self.download_dir}
            dump(i, file, ensure_ascii=True, indent=2)

    def load_config(self):
        try:
            with open(f"{self.config_file_name}", "r", encoding="utf-8", errors="ignore") as file:
                i = load(file)
                return i
        except FileNotFoundError:
            return {"token": None, "path": "."}
        except Exception as l_e:
            error(f"{type(l_e).__name__} at line <{l_e.__traceback__.tb_lineno}> of \"{__file__}\": {l_e.__doc__}")
            return {"token": None, "path": "."}

    def validate(self) -> Optional[str]:
        try:
            if not path.exists(self.config_file_name):
                return
            token = self.load_config().get("token")
            if (not token) or (not self.is_valid_string(token)):
                return
            return token
        except Exception as t:
            error(f"{type(t).__name__} at line <{t.__traceback__.tb_lineno}> of \"{__file__}\": {t.__doc__}")
            return

    def generate_headers(self, auth: str) -> dict[str, str]:
        self.headers.update({
            "Authorization": auth,
            "User-Agent": self.user_agents.random()
        })
        return self.headers

    async def get_user_and_guild(self):
        
        system("title Getting info...")
        
        async with ClientSession() as session:
            info("getting user info...")
            self.user = await self.get_user(session)
            info("getting server info...")
            self.guild = await self.get_guild(session)
            info("getting owners info...")
            self.guild_owner = await self.get_owner(session)
            return self.user, self.guild

    async def get_user(self, session) -> dict[str | int, int | str | dict | list] | None:
        url = BASE + f"/users/@me"
        async with session.get(url, headers=self.headers) as response:
            if response.status != 200:
                error(f"Error getting user : {response.status}")
                return None
            return await response.json()

    async def get_owner(self, session: ClientSession) -> dict[str | int, int | str | dict | list] | None:
        url = BASE + f"/users/{self.guild.get("owner_id")}/profile"
        async with session.get(url, headers=self.headers, params={"with_mutual_guilds": "true"}) as response:
            if response.status != 200:
                error(f"unable to get owner's info: {response.status}")
                return
            return await response.json()

    async def get_guild(self, session) -> dict[str | int, int | str | dict | list] | None:
        url = BASE + f"/guilds/{self.guild_id}"
        async with session.get(url, headers=self.headers, params={"with_counts": "true"}) as response:
            if response.status != 200:
                error(f"Error getting guild: {response.status}")
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

        while True:
            self.main_cls()
            print_guilds()
            list_guild_choice = input(f"{Fore.LIGHTMAGENTA_EX}Choose The Guild: {Fore.RESET}\n")
            if not list_guild_choice:
                error("choose a guild!")
            elif not list_guild_choice.isdigit():
                error("enter only number!")
            elif int(list_guild_choice) > len(guild_list):
                error("not in guild list")
            else:
                for key, value in guild_list.items():
                    if key != int(list_guild_choice):
                        continue
                    return value

    def confirmation(self):
        
        system("title Confirming...")
        
        user, guild, owner = self.user, self.guild, self.guild_owner
        while True:
            self.main_cls()
            i = f'''
{Fore.LIGHTBLUE_EX}Your Information:{Fore.LIGHTWHITE_EX}
    Name: {user.get("global_name", user.get("username"))}
    Username: {user.get("username", user.get("id"))}
    Contact Info: {user.get("email", "no email.")}

{Fore.LIGHTBLUE_EX}Server Information:{Fore.LIGHTWHITE_EX}
    Name: {guild.get("name", "no name")}
    ID: {guild.get("id")}
    Owner's Name: {owner.get("user", {}).get("display_name", owner.get("user", {}).get("username"))}
    Owner's ID: {owner.get("user", {}).get("id")}
    Owner's Bio: 
    {owner.get("user", {}).get("bio", "no bio").strip()}
            '''
            info("is this info correct?")
            print(i)
            confirm_choice = input("\n[yes/no] :").lower()
            if not confirm_choice:
                error("please enter something!")
            elif confirm_choice not in ["yes", "no", "y", "n"]:
                error("invalid confirm_choice, choose between (y, n, yes, no)!")
            else:
                return confirm_choice in ["yes", "y"]

    def choose_what_to_download(self):
        
        system("title Menu")
        
        while True:
            if self.download_dir is None:
                self.download_dir = "."
            self.menu_cls()
            menu = rf'''
[1] Download Emoji
[2] Download Stickers
[3] Download Channels Info (json)
[4] Download Roles Info (json)
[5] Download Server Info
[6] Download Everything

[7] Change Download Path
    [Current: {path.abspath(self.download_dir)}]
        '''

            print(f"{Fore.LIGHTMAGENTA_EX}[+] Choose From The Menu Below!")
            print(menu)
            download_choice = input(f"{Fore.LIGHTYELLOW_EX}[?] Choice : {Fore.RESET}")

            if not download_choice:
                error("make a download_choice!")
            elif not download_choice.isdigit():
                error(f"download_choice is not a number! [{download_choice}]")
            elif int(download_choice) not in [1, 2, 3, 4, 5, 6, 7]:
                error(f"invalid download_choice! [{download_choice}]")
            elif int(download_choice) == 7:
                new_path = filedialog.askdirectory(title="Where to download?", initialdir=".", mustexist=True)
                if new_path:
                    self.download_dir = new_path
                    self.save_config()
                    success(f"Download path changed to: {self.download_dir}")
                else:
                    error(f"no download path received, therefore remains: {self.download_dir}")
            else:
                download_choice = int(download_choice)
                start = perf_counter()
                Download(download_choice=download_choice,
                         guild_json=self.guild,
                         headers=self.headers,
                         owner=self.guild_owner,
                         download_dir=self.download_dir)
                end = perf_counter()

                elapsed_time = end - start

                if elapsed_time > 60.0:
                    minute = elapsed_time // 60
                    second = elapsed_time % 60
                    success(f"It took {minute}min {second:.2f}s to download!")

                else:
                    success(f"It took {elapsed_time:.2f}s to download!")

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
        self.mfa = self.get_mfa_level()
        self.boost_perks = self.get_premium_level()
        self.nsfw = self.get_nsfw_level()
        self.verification_level = self.get_verification_level()

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
            return sorted(emoji_url_list, key=lambda x: x.get("animated", True), reverse=True)

        try:
            data = self.__raw__.get("emojis", None)
            if not data:
                data = get(f"{BASE}/guilds/{self.guild_id}/emojis", headers=self.headers).json()
            return extract_emoji_info(data)
        except Exception as emoji_exception:
            error(f"got {type(emoji_exception).__name__} while getting emojis: {emoji_exception.__doc__}")
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
            return sorted(roles_info, key=lambda x: x.get("Position"))

        try:
            data = self.__raw__.get("roles", None)
            if not data:
                data = get(f"{BASE}/guilds/{self.guild_id}/roles", headers=self.headers).json()
            return extract_role_info(data)
        except Exception as roles_exception:
            error(f"got {type(roles_exception).__name__} getting roles: {roles_exception.__doc__}")
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
            return sorted(channels_info, key=lambda x: x.get("Position"))

        try:
            data = get(f"{BASE}/guilds/{self.guild_id}/channels", headers=self.headers).json()
            return extract_channel_info(data)
        except Exception as channels_exception:
            error(f"got {channels_exception.__class__.__name__} getting channels info: {channels_exception.__doc__}")
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
            return sorted(stick_url_list, key=lambda x: x.get("animated", True), reverse=True)

        try:
            data = self.__raw__.get("stickers", None)
            if not data:
                data = get(f"{BASE}/guilds/{self.guild_id}/stickers", headers=self.headers).json()
            return extract_sticker_info(data)
        except Exception as sticker_exception:
            error(f"got {sticker_exception.__class__.__name__} getting stickers: {sticker_exception.__doc__}")
            return None

    def get_icon(self) -> None | str:
        icon_hash = self.__raw__.get("icon", None)
        if not icon_hash:
            error(f"{self.name} don't have any icon!")
            return
        fmt = ".gif" if icon_hash.startswith("a_") else ".png"
        return f"{ASSET_BASE}/icons/{self.guild_id}/{icon_hash}{fmt}?size=2048"

    def get_banner(self) -> None | str:
        banner_hash = self.__raw__.get("banner", None)
        if not banner_hash:
            error(f"{self.name} don't have any banner!")
            return
        fmt = ".gif" if banner_hash.startswith("a_") else ".png"
        return f"{ASSET_BASE}/banner/{self.guild_id}/{banner_hash}{fmt}?size=2048"

    def get_splash(self) -> None | str:
        splash_hash = self.__raw__.get("splash", None)
        if not splash_hash:
            error(f"{self.name} don't have any splash!")
            return
        fmt = ".gif" if splash_hash.startswith("a_") else ".png"
        return f"{ASSET_BASE}/splashes/{self.guild_id}/{splash_hash}{fmt}?size=2048"

    def get_discovery_splash(self) -> None | str:
        discovery_splash_hash = self.__raw__.get("discovery_splash", None)
        if not discovery_splash_hash:
            error(f"{self.name} don't have any discovery splash!")
            return
        fmt = ".gif" if discovery_splash_hash.startswith("a_") else ".png"
        return f"{ASSET_BASE}/discovery-splashes/{self.guild_id}/{discovery_splash_hash}.{fmt}?size=2048"

    def get_mfa_level(self) -> None | str:
        reference_json = {
            0: f"{self.name} does not require to have 2FA/MFA enabled for MODERATION ACTIONS!",
            1: f"{self.name} requires to have 2FA/MFA enabled for MODERATION ACTIONS"
        }
        return reference_json.get(self.__raw__.get("mfa_level", 0))

    def get_verification_level(self) -> None | str:
        reference_json = {
            0: f"{self.name} doesn't have any kind of verification!",
            1: f"{self.name} requires user to have a verified email.",
            2: f"{self.name} requires user to have a verified email + must be registered on discord for more than 5 "
               f"min.",
            3: f"{self.name} requires user to have a verified email + must be member of {self.name} for more than 10 "
               f"min.",
            4: f"{self.name} requires user to have a verified email + a verified phone number 💀."
        }
        return reference_json.get(self.__raw__.get("verification_level", 0))

    def get_premium_level(self) -> None | str:
        reference_json = {
            0: f"{self.name} doesn't have any server boost perks!",
            1: f"{self.name} have level 1 server boost perks.",
            2: f"{self.name} have level 2 server boost perks.",
            3: f"{self.name} have level 3 server boost perks."
        }
        return reference_json.get(self.__raw__.get("premium_tier", 0))

    def get_nsfw_level(self) -> None | str:
        reference_json = {
            0: "Normal",
            1: "Explicit",
            2: "Safe",
            3: "Age Restricted 💀"
        }
        return reference_json.get(self.__raw__.get("nsfw_level", 0))

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
    def __init__(self, download_choice: int, guild_json: dict, headers: dict, owner: dict, download_dir: str):
        super().__init__(guild_json, headers)
        system("title Downloading...")

        self.owner = owner
        self.dir = download_dir
        self.directory_name = self.sanitize_filename(self.name)
        makedirs(name=rf"{self.directory_name}", exist_ok=True)
        self.directory = path.join(self.dir, self.directory_name)
        self.downloading_cls(self.directory)
        if download_choice == 1:
            self.choice_1()
        elif download_choice == 2:
            self.choice_2()
        elif download_choice == 3:
            self.choice_3()
        elif download_choice == 4:
            self.choice_4()
        elif download_choice == 5:
            self.choice_5()
        elif download_choice == 6:
            self.choice_6()
        else:
            error("not a valid choice")
        system("title Completed!")

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
        system(f"title Downloading {download_type.lower()}...")
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
                        error(f"Can't Download {file_name} because of {download_exception.__doc__}")
                    finally:
                        bar()
                    prev_id = id_
                    sleep(0.1)
        abs_path = path.join(path.join(getcwd(), self.directory_name), sub_folder_name)
        success(
            f"All {len(files)} files downloaded in \"{abs_path}\", size: {file_size / 1024:.2f}MB ({file_size:.2f}KB)"
        )
        system(f"title Downloaded {download_type}")

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
        channel_file_name = rf"{self.directory}/{self.directory_name}_channel_info.json"
        try:
            with open(channel_file_name, 'w') as choice_3:
                choice_3.flush()
        except Exception as choice_3_exception:
            error(f"Can't Flush The File \"{channel_file_name}\": {repr(choice_3_exception)}")
        channel_list = self.channels
        if channel_list:
            try:
                with open(
                        channel_file_name,
                        'w',
                        encoding="utf-8",
                        errors="ignore"
                ) as choice_3_write:
                    dump(channel_list, choice_3_write, ensure_ascii=False, indent=2)
                success(f"channels info downloaded!")
            except Exception as choice_3_exception:
                error(f"can't open {channel_file_name}, because: {repr(choice_3_exception)}")
                return
        else:
            error(f"seems like {self.name} don't have channels! strange?")

    def choice_4(self):
        roles_file_name = rf"{self.directory}/{self.directory_name}_role_info.json"
        try:
            with open(roles_file_name, 'w') as file:
                file.flush()
        except Exception as choice_4_exception:
            error(f"can't flush file \"{roles_file_name}\": {repr(choice_4_exception)}")

        role_list = self.roles
        if role_list:
            try:
                with open(
                        roles_file_name,
                        'w',
                        encoding="utf-8",
                        errors="ignore"
                ) as file:
                    dump(role_list, file, ensure_ascii=False, indent=2)
                    success(f"roles info downloaded!")
            except Exception as choice_4_exception:
                error(f"can't open \"{roles_file_name}\" because: {repr(choice_4_exception)}")
                return
        else:
            error(f"seems like {self.name} don't have roles!")

    def choice_5(self):
        info_file_name = fr'{self.directory}/{self.directory_name}_info.txt'
        inf = f'''
- Basic Info:
Name: {self.name}
id: {self.guild_id}
description: {self.description}
icon: {self.icon}
splash: {self.splash}
discovery splash: {self.discovery_splash}
banner: {self.banner}

- Owner Info:
Name: {self.owner.get("user", {}).get("global_name", self.owner.get("user", {}).get("username"))}
username: {self.owner.get("user", {}).get("username")}
id: {self.owner.get("user", {}).get("id")}
bio: 
{self.owner.get("user", {}).get("bio", "No Bio!")}

pronouns: {self.owner.get("user_profile", {}).get("pronouns", "no pronouns!")}
mutual friends:
    {"\n    ".join([f"{idx}. {u.get("global_name", u.get("username"))}"
                    f"\n       |-> {u.get("username")}"
                    f"\n       |-> {u.get("id")}" for idx, u in enumerate(self.owner.get("mutual_friends", [{}]), start=1) if u])}

- Media Info:
{self.name} has {len(self.emojis)} emojis.
{self.name} has {len(self.stickers)} stickers.

- Presence Info:
{self.name} has {self.__raw__.get("approximate_member_count", "\"not able to get\"")} members (approx).
{self.name} has {self.__raw__.get("approximate_presence_count", "\"not able to get\"")} members online (approx).

- Advance Info:
{self.name} has {len(self.roles)} roles.
{self.name} has {len(self.channels)} channels.
{self.name} has following features:
    {"\n    ".join(self.__raw__.get("features", []))}
{self.name} has {self.nsfw} nsfw level.
{self.boost_perks}
{self.verification_level}
{self.mfa}

'''
        try:
            with open(
                    info_file_name,
                    'w',
                    encoding="utf-8",
                    errors="ignore"
            ) as file:
                file.flush()
                file.write(inf.lstrip())
            success(f"{self.name} info downloaded!")
        except Exception as choice_5_exception:
            error(f"can't open \"{info_file_name}\", because: {repr(choice_5_exception)}")
            return

    def choice_6(self):
        try:
            self.choice_1()
            sleep(uniform(0.6, 1.2))
        except Exception as choice_1_exception:
            error(f"can't download emojis because of {repr(choice_1_exception)}")

        try:
            self.choice_2()
            sleep(uniform(0.6, 1.2))
        except Exception as choice_2_exception:
            error(f"can't download stickers because of {repr(choice_2_exception)}")

        try:
            self.choice_3()
            sleep(uniform(0.6, 1.2))
        except Exception as choice_3_exception:
            error(f"can't download roles info because of {repr(choice_3_exception)}")

        try:
            self.choice_4()
            sleep(uniform(0.6, 1.2))
        except Exception as choice_4_exception:
            error(f"can't download channels info because of {repr(choice_4_exception)}")

        try:
            self.choice_5()
            sleep(uniform(0.6, 1.2))
        except Exception as choice_5_exception:
            error(f"can't download server info because of {repr(choice_5_exception)}")

        try:
            startfile(self.directory)
        except Exception as open_dir_exception:
            error(f"Can't open \"{self.directory_name}\" because of: {repr(open_dir_exception)}")

        size_in_byte = 0
        total_files = 0
        total_gifs = 0
        for root, _, files in walk(self.directory):
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
        print(f"{Fore.LIGHTCYAN_EX}[+] Total Size: {size_in_byte / 1024:.2f}kb ({size_in_byte / (1024 * 1024):.2f}mb)"
              f"\n[+] Total Files: {total_files} files ({total_files - total_gifs} images and {total_gifs} gifs)")


if __name__ == '__main__':
    main = Utility()
    try:
        main.main_entrypoint()
    except KeyboardInterrupt:
        success("\nalright exiting...")
        sleep(0.1)
        exit(0)
    except Exception as e:
        info(f'got an exception in main:')
        print(f"{type(e).__name__} at line <{e.__traceback__.tb_lineno}> of \"{__file__}\": {e.__doc__}")
        main.retry()
