import os
from platform import system as platform_name


def cls(**kwargs):
    if platform_name().lower() in ['windows', 'nt']:
        os.system('cls')
        if kwargs.get('art'):
            print(kwargs.get('art'))
    else:
        try:
            os.system('clear')
            if kwargs.get('art'):
                print(kwargs.get('art'))
        except PermissionError:
            from subprocess import run
            run('clear')
            if kwargs.get('art'):
                print(kwargs.get('art'))
