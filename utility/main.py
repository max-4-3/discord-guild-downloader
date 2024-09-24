import asyncio
import os
import time

import objects.guild
import objects.users
import utility.cls
import utility.gather_info
import utility.generate_headers
import utility.store
from downloader.downloader import Downloader
from utility.arts import *


class Main:

    __slots__ = ('guild', 'owner', 'client', 'downloadPath', 'guild_id', '__loop__', '__token__', '__headers__')

    def __init__(self):
        self.__loop__, self.__token__, self.guild_id = None, None, None
        self._set_important()

    def _set_important(self):

        utility.cls.cls(art=main_art)

        # Sets event loop
        if self.__loop__ is None:
            self._set_or_get_event_loop_()

        # Sets token and headers
        if not self.__token__:
            self.__token__ = utility.gather_info.get_token()
            self.__headers__ = utility.generate_headers.generate(self.__token__)
            self.client = objects.users.Clint(self.__loop__, self.__headers__)
        utility.cls.cls(art=main_art)

        # Sets guild and owner
        if not self.guild_id:
            self.guild_id = utility.gather_info.get_guild_id(self.__headers__)
            self.guild = objects.guild.Guild(self.guild_id, self.__loop__, self.__headers__)
            self.owner = self.guild.owner
        utility.cls.cls(art=main_art)

        # Sets the download path
        self._set_or_get_download_path()

    def _destroy(self, guild: bool = True, token: bool = False):
        if guild:
            self.guild_id = None
        if token:
            self.__token__ = None
        self._set_important()

    def _set_or_get_download_path(self, **kwargs):
        config = utility.store.read_config()

        # Check if a new path is provided via kwargs
        if kwargs.get('path'):
            self.downloadPath = kwargs.get('path')
            utility.store.store_config(path=self.downloadPath)

        # If no new path is provided, use the path from the config
        elif config.get('path'):
            self.downloadPath = config.get('path')

        # If no path is stored in the config, use the current working directory
        else:
            self.downloadPath = os.getcwd()
            utility.store.store_config(path=self.downloadPath)

    def _set_or_get_event_loop_(self):
        try:
            self.__loop__ = asyncio.get_running_loop()
        except RuntimeError:
            self.__loop__ = asyncio.new_event_loop()
            asyncio.set_event_loop(self.__loop__)

    def confirmation(self) -> bool:

        utility.cls.cls(art=main_art)

        info = (f'Your Info:'
                f'\n\tName: {self.client.display_name}'
                f'\n\tContact: {self.client.contact}\n'
                f'Guild Info:'
                f'\n\tName: {self.guild.name}'
                f'\n\tID: {self.guild.id}\n'
                f'Owner Info:'
                f'\n\tName: {self.owner.display_name}'
                f'\n\tID: {self.owner.id}'
                f'\n\tbio: {self.owner.bio}\n').expandtabs(2)
        print('is this info correct? [y/n]')
        print(info)
        while True:
            choice = input(':')
            if not choice:
                print('Choose b/w yes and no')
            elif choice.lower() not in ['yes', 'no', 'n', 'y']:
                print('Invalid Choice')
            elif choice.lower() in ['no', 'n']:
                self._destroy()
            elif choice.lower() in ['exit']:
                exit(0)
            else:
                return True

    def showOptions(self):
        utility.cls.cls(art=menu_art)
        menu = {
            1: "Download emojis",
            2: "Download stickers",
            3: "Save channel info",
            4: "Save roles info",
            5: "Save guild info",
            6: "All of the above!",
            7: f"Change Download Dir\n[{self.downloadPath}]"
        }
        for idx, name in menu.items():
            print(f"{idx}.", name)
        print('Choose:\n')
        while True:
            choice = input('-> ')
            if not choice:
                self.showOptions()
            elif choice in ['exit', 'stop']:
                return
            elif not choice.isdigit():
                self.showOptions()
            elif int(choice) > len(menu):
                self.showOptions()
            elif int(choice) == 7:
                try:
                    from tkinter import filedialog
                    newPath = filedialog.askdirectory(title='Download Directory', mustexist=True)
                    self._set_or_get_download_path(path=newPath)
                    self.showOptions()
                except (ModuleNotFoundError, ImportError, ImportWarning):
                    newPath = input('Enter a Path:\n')
                    self._set_or_get_download_path(path=newPath)
                    self.showOptions()
            else:
                start_time = time.perf_counter()
                task = Downloader(self.guild, self.downloadPath, int(choice))
                end_time = time.perf_counter()

                print(f"Took {end_time - start_time:.2f}s to complete!"
                      f"\nReport: {task.report()}")
                return 


    def retry(self):
    	self._destroy(guild=True)
        
