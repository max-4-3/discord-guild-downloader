import os
from asyncio import create_task, gather
from asyncio import run
from json import dump
from random import uniform
from time import sleep
from typing import List, Union
import subprocess as sp

import aiohttp
from alive_progress import alive_bar

from objects.emoji import Emoji, Emojis
from objects.guild import Guild
from objects.sticker import Sticker, Stickers
from utility import is_android


class DirectoryHelper:
    """
    A class to handle the creation and sanitization of directory paths.
    """

    def __init__(self, name: str, path: str):
        if not path:
            path = os.getcwd()

        self.dir_name = os.path.join(path, self.sanitize_dir_name(name))
        self.name = os.path.basename(self.dir_name)
        os.makedirs(self.dir_name, exist_ok=True)

    @staticmethod
    def sanitize_dir_name(filename) -> str:
        """
        Replace any reserved characters in the directory name for Windows systems.
        """
        reserved_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
        for char in reserved_chars:
            filename = filename.replace(char, '_')

        filename = filename.strip()

        if not filename:
            filename = 'File Name is Empty lol'

        return filename

    def create_directory(self, sub_dir: str) -> str:
        """
        Create the directory if it doesn't exist.
        """
        path = os.path.join(self.dir_name, sub_dir)
        os.makedirs(path, exist_ok=True)
        return path
    
    def update_media(self):
        """
        Updates the Download directory so that android apps can recognize the file changes.
        """
        if not is_android:
            return
        
        command = f"am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE -d file://{os.path.split(self.dir_name)[0]}"
        sp.run(command, stdin=sp.DEVNULL, stdout=sp.DEVNULL, stderr=sp.DEVNULL, text=False, capture_output=False, shell=True)


class Downloader(DirectoryHelper):
    """
    The main class that handles downloading files such as Emojis, Stickers, and more.
    """
    READ_SIZE: int = 1024 * 1024 * 4

    def __init__(self, guild: Guild, download_path: str, choice: int):
        super().__init__(guild.name, path=download_path)
        self.choice = choice
        self.guild = guild
        self.total_files = 0
        self.total_gifs = 0
        self.path = self.dir_name

        self.choice_base_download()

    def choice_base_download(self):
        download_dict = {
            1: self.download_emojis,
            2: self.download_stickers,
            3: self.save_channel_info,
            4: self.save_roles_info,
            5: self.save_guild_info,
            6: self.run_all_tasks
        }

        if self.choice > len(download_dict):
            raise KeyError('Choice is not Implemented!')

        download_dict[self.choice]()
        self.update_media()

    @staticmethod
    async def _download_file(session: aiohttp.ClientSession, url: str, file_path: str) -> float:
        """
        Downloads a file and returns its size in KB.
        """
        async with session.get(url) as response:
            content: int = 0
            with open(file_path, 'wb') as f:
                while (resp := await response.content.read(Downloader.READ_SIZE)):
                    f.write(resp)
                    content += len(resp)

            return content / 1024

    def _get_downloaded_size(self) -> dict[str, float]:
        total_files = 0
        total_gifs = 0
        for root, _, files in os.walk(self.path):
            for file in files:
                ext = os.path.splitext(file)[1]
                if ext == ".gif":
                    total_gifs += 1
                file_path = os.path.join(root, file)
                if not os.path.isfile(file_path):
                    continue
                total_files += 1
        
        return {
            "gifs": total_gifs,
            "images": total_files - total_gifs,
            "total files": total_files
        }

    async def _download(self, session, file: Union[Emoji, Sticker, dict], bar):
        file_name, download_path, url = "", "", ""
        is_animated, file_type = False, "png"

        # Handle case for dict file type
        if isinstance(file, dict):
            url = str(file.get("url"))
            is_animated = file.get('animated', False)
            file_type = is_animated and 'gif' or 'png'

            file_name = DirectoryHelper.sanitize_dir_name(file.get('name', 'No Name')) + "." + file_type
            _sub_dir = os.path.join("Resource", file_type)
            download_path = self.create_directory(_sub_dir)
        # Emojis or Stickers
        else:
            url = file.url
            is_animated = file.animated
            file_type = file.file_type

            file_name = DirectoryHelper.sanitize_dir_name(file.name) + "." + file_type
            _sub_dir = os.path.join(file.__class__.__name__, file_type)
            download_path = self.create_directory(_sub_dir)

        file_path = os.path.join(download_path, file_name)

        if os.path.exists(file_path):
            print("Already Downloaded!")
            return

        try:
            file_size = await self._download_file(session, url, file_path)
            if is_animated and file_type == "png": # APNG
                if await self._convert_to_gif(file_path):
                    print(f"\"{file_name}\" converted to gif!")
            print(f'"{file_name}" downloaded ({file_size:.2f} KB)!')
        except Exception as e:
            print(f"Failed to download {file_name}: {e}")
        finally:
            bar()

    @staticmethod
    def _run_prog(*cmd: str, to_terminal: bool = False, requited_rc: int = 0) -> bool:
        return sp.run(
                cmd,
                stdout=sp.DEVNULL if not to_terminal else sp.PIPE,
                stderr=sp.DEVNULL if not to_terminal else sp.PIPE,
                stdin=sp.DEVNULL,
                text=False
            ).returncode == requited_rc

    async def _convert_to_gif(self, src: str) -> bool:
        dst = f"{os.path.splitext(src)[0]}.gif"
        if self._run_prog("ffmpeg", "-hide_banner", "-i", src, dst):
            os.rename(src, dst)
            return True

        return False

    async def download(self, files: Union[Emojis, Stickers, list[dict]]):
        """
        Downloads a list of files (Emojis or Stickers).
        """
        download_type = files.__class__.__name__.title() if not isinstance(files, list) else "Resources"

        async with aiohttp.ClientSession() as session:
            with alive_bar(len(files), title=f'Downloading {download_type}...', spinner='dots') as bar:
                # Creates async task!
                tasks = []
                for file in files:
                    tasks.append(create_task(self._download(session, file, bar)))
                if len(tasks) == 0:
                    print("Error occurred while creating tasks!")
                    return
                else:
                    # executes the task
                    await gather(*tasks)

        download_stats = self._get_downloaded_size()
        self.total_gifs = download_stats.get("gifs", 0)
        self.total_files = download_stats.get("images", 0)
        print(f"All {len(files)} {download_type} files downloaded.")

    def save_json(self, data: List[dict], file_name: str):
        """
        Saves a list of dictionaries to a JSON file.
        """
        path = os.path.join(self.path, file_name)
        with open(path, 'w', encoding='utf-8', errors='ignore') as f:
            dump(data, f, ensure_ascii=False, indent=2)
            print(f"Saved {file_name}")

    def download_emojis(self):
        """
        Downloads all emojis for the current guild.
        """
        emoji_list = self.guild.emojis
        if emoji_list:
            run(self.download(emoji_list))
        else:
            print(f"No emojis found in {self.guild.name}")

    def download_stickers(self):
        """
        Downloads all stickers for the current guild.
        """
        sticker_list = self.guild.stickers
        if sticker_list:
            run(self.download(sticker_list))
        else:
            print(f"No stickers found in {self.guild.name}")

    def save_channel_info(self):
        """
        Save all channel information to a JSON file.
        """
        channel_data = [dict(channel) for channel in self.guild.channels]
        self.save_json(channel_data, f'{self.guild.name}_channel_info.json')

    def save_roles_info(self):
        """
        Save all roles information to a JSON file.
        """
        role_data = [dict(role) for role in self.guild.roles]
        self.save_json(role_data, f'{self.guild.name}_roles_info.json')

    def save_guild_info(self):
        """
        Save basic guild information to a text file.
        """
        file_name = f'{self.guild.name}_info.txt'
        with open(os.path.join(self.path, file_name), 'w', encoding='utf-8', errors='ignore') as f:
            f.write(str(self.guild))
            print(f"Guild info saved to {file_name}")

    def run_all_tasks(self):
        """
        Runs all download and save tasks sequentially.
        """
        tasks = [
            self.download_emojis,
            self.download_stickers,
            self.save_channel_info,
            self.save_roles_info,
            self.save_guild_info
        ]

        for task in tasks:
            try:
                task()
                sleep(uniform(0.5, 1.2))  # Simulate processing time between tasks
            except Exception as e:
                print(f"[{task.__name__.replace('_', ' ').title()}] Task failed: {e}")

        # Final report of the total download
        print(f"Files saved at {self.path}")

    def report(self):
        return (f"Files saved at {self.path}"
                f"\nTotal Files downloaded: {self.total_files}"
                f"\nTotal Images Downloaded: {self.total_files - self.total_gifs}"
                f"\nTotal Gifs Downloaded: {self.total_gifs}")
