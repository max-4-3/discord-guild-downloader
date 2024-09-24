from objects.guild import get_guild
from utility.cls import cls
from utility.store import read_config, store_config


def is_valid_string(string: str):
    return len(string.strip().split(".")) == 3


def get_token():
    config = read_config()
    if config and config.get('token'):
        while True:
            token_choice = input(f"[?] Load token from file? (yes/no): \n").lower()
            if token_choice not in ["yes", "no", "y", "n"]:
                cls()
                continue
            elif token_choice in ["yes", "y"]:
                return config.get('token')
            elif token_choice in ["no", "n"]:
                break

    prompt = f"[+] Enter Your Account Token (h for help): \n"
    while True:
        token = input(prompt)
        if not token:
            cls()
            print("please enter a token")
            continue

        elif token in ["h", "help"]:
            print('https://github.com/max-4-3/discord-guild-downloader/blob/main/how%20to%20get%20token.md')
            continue

        elif not is_valid_string(token):
            cls()
            print("invalid token given!")
            continue

        store_config(token=token)
        return token


def list_guilds(headers):
    guild_list = get_guild(headers, partial=True)

    if guild_list is None:
        return

    def print_guilds():
        for idx, guild in enumerate(guild_list, start=1):
            print(f'{idx}. {guild.name}')

    while True:
        print_guilds()
        list_guild_choice = input(f"Choose The Guild: \n")
        if not list_guild_choice:
            print("choose a guild!")
        elif not list_guild_choice.isdigit():
            print("enter only number!")
        elif int(list_guild_choice) > len(guild_list):
            print("not in guild list")
        else:
            return guild_list[int(list_guild_choice) - 1].id


def get_guild_id(headers):
    while True:
        prompt = f"[+] Enter The Guild ID (ls to list all server): \n"
        guild_id = input(prompt).lower()
        if not guild_id:
            print("Please enter a Guild ID!")
        elif guild_id == "exit":
            print("Okay!")
            exit(0)
        elif guild_id == "ls":
            guild_id = list_guilds(headers)
            return guild_id
        elif not guild_id.isdigit():
            print("entered id is not digit!")
        elif not len(guild_id) > 5:
            print("guild id can't be so small!")
        else:
            guild_id = int(guild_id)
            return guild_id
