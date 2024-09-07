import asyncio

from objects.guild import Guild, PartialGuilds

BASE = "https://discord.com/api/v9"
DISCORD_BASE = "https://discord.com"
ASSET_BASE = "https://cdn.discordapp.com"
ASSET_BASE_TWO = "https://media.discordapp.net"


def get_guild(headers: dict, **kwargs) -> Guild | PartialGuilds:
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    partial = kwargs.get('partial', False)
    guild_id = kwargs.get('guild_id', None)

    if not partial:
        if not guild_id:
            raise ValueError('Guild id must be given if partial is set to False!')
        return Guild(guild_id, loop, headers)
    else:
        return PartialGuilds(loop, headers)
