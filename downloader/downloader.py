import os
from asyncio import create_task, gather
from asyncio import run
from json import dump
from platform import system as platform_name
from random import uniform
from time import sleep
from typing import List, Union
import subprocess as sp

import aiohttp
from alive_progress import alive_bar

from objects.emoji import Emojis
from objects.guild import Guild
from objects.sticker import Stickers
from utility import is_android


class DirectoryHelper:
    """
    A class to handle the creation and sanitization of directory paths.
    """

    def __init__(self, name: str, path: str):
        self.dir_name = name
        if platform_name().lower() in ['windows', 'nt']:
            self.dir_name = self.sanitize_dir_name(self.dir_name)
        self.dir_name = os.path.join(path if path else os.getcwd(), self.dir_name)
        self.name = os.path.basename(self.dir_name)

    @staticmethod
    def sanitize_dir_name(filename):
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
        return 


class Downloader(DirectoryHelper):
    """
    The main class that handles downloading files such as Emojis, Stickers, and more.
    """

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
            content = await response.read()
            with open(file_path, 'wb') as f:
                f.write(content)
            return len(content) / 1024

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

    async def _download(self, session, file, bar):
        
        # Handle case for dict file type
        if isinstance(file, dict):
            is_animated = file.get('animated', False)
            file_name = DirectoryHelper.sanitize_dir_name(file.get('name', 'No Name')) + (
                '.gif' if is_animated else '.png')
            sub_dir = os.path.join(
                (file.__class__.__name__ if not isinstance(file, list) else 'Resources'),
                ('gifs' if is_animated else 'images')
            )
            download_path = self.create_directory(sub_dir)
        
        # Emojis or Stickers
        else:
            file_name = DirectoryHelper.sanitize_dir_name(file.name) + ('.gif' if file.animated else '.png')
            sub_dir = os.path.join(
                (file.__class__.__name__ if not isinstance(file, list) else 'Resources'),
                ('gifs' if file.animated else 'images')
            )
            download_path = self.create_directory(sub_dir)

        file_path = os.path.join(download_path, file_name)

        if os.path.exists(file_path):
            print("Already Downloaded!")
            return

        try:
            file_size = await self._download_file(
                session,
                file.get('url') if isinstance(file, dict) else file.url,
                file_path
            )
            print(f'"{file_name}" downloaded ({file_size:.2f} KB)!')
        except Exception as e:
            print(f"Failed to download {file_name}: {e}")
        finally:
            bar()

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