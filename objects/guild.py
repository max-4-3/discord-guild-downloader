import asyncio

import aiohttp

from objects.channel import Channels
from objects.constants import BASE, ASSET_BASE
from objects.emoji import Emojis
from objects.role import Roles
from objects.sticker import Stickers
from objects.users import Owner


class Guild:
    __slots__ = (
        'id',
        'name',
        'description',
        'approximate_member_count',
        'approximate_presence_count',
        '_mfa',
        '_boost_perks',
        '_nsfw',
        '_verification_level',
        '_icon',
        '_splash',
        '_banner',
        '_discovery_splash',
        'owner',
        '_channels',
        '_roles',
        '_emojis',
        '_stickers',
        '_features',
        '__headers__',
        '__loop__',
    )

    def __init__(self, guild_id: int, loop: asyncio.AbstractEventLoop, headers: dict):
        self.id = guild_id
        self.__loop__ = loop
        self.__headers__ = headers

        self._init_(self.__do_async_work())

    async def __make_req(self, **kwargs):
        async with aiohttp.ClientSession() as session:
            path = kwargs.get('path')
            if path:
                url = BASE + '/guilds/' + str(self.id) + '/' + str(path)
            else:
                url = BASE + '/guilds/' + str(self.id)
            async with session.get(url, headers=self.__headers__, params={'with_counts': 'true'}) as response:
                return await response.json()

    def __do_async_work(self, **kwargs):
        task = self.__loop__.create_task(self.__make_req(**kwargs))
        results = self.__loop__.run_until_complete(task)
        return results

    def _init_(self, data: dict):
        self.name: str = data.get("name", f"No Name [{self.id}]")
        self.description: str = data.get("description", f"No description [{self.id}]")
        self.approximate_member_count: int = data.get('approximate_member_count', 0)
        self.approximate_presence_count: int = data.get('approximate_presence_count', 0)
        self._icon: str | None = data.get('icon', None)
        self._banner: str | None = data.get('banner', None)
        self._discovery_splash: str | None = data.get('discovery_splash', None)
        self._splash: str | None = data.get('splash', None)
        self._verification_level: int = data.get('verification_level', 0)
        self._boost_perks: int = data.get('premium_tier', 0)
        self._mfa: int = data.get('mfa_level', 0)
        self._nsfw: int = data.get('nsfw_level', 0)
        self._features: list[str | None] = data.get('features', [])
        self._stickers: list[dict | None] = data.get('stickers', [])
        self._emojis: list[dict | None] = data.get('emojis', [])
        self._roles: list[dict | None] = data.get('roles', [])
        self._channels: list[dict | None] = self.__do_async_work(path="channels")
        self.owner = Owner(self.__loop__, data.get('owner_id'), self.__headers__)

    @property
    def icon(self) -> None | str:
        icon_hash = self._icon
        if not icon_hash:
            return
        fmt = ".gif" if icon_hash.startswith("a_") else ".png"
        return f"{ASSET_BASE}/icons/{self.id}/{icon_hash}{fmt}?size=2048"

    @property
    def banner(self) -> None | str:
        banner_hash = self._banner
        if not banner_hash:
            return
        fmt = ".gif" if banner_hash.startswith("a_") else ".png"
        return f"{ASSET_BASE}/banners/{self.id}/{banner_hash}{fmt}?size=2048"

    @property
    def splash(self) -> None | str:
        splash_hash = self._splash
        if not splash_hash:
            return
        fmt = ".gif" if splash_hash.startswith("a_") else ".png"
        return f"{ASSET_BASE}/splashes/{self.id}/{splash_hash}{fmt}?size=2048"

    @property
    def discovery_splash(self) -> None | str:
        discovery_splash_hash = self._discovery_splash
        if not discovery_splash_hash:
            return
        fmt = ".gif" if discovery_splash_hash.startswith("a_") else ".png"
        return f"{ASSET_BASE}/discovery-splashes/{self.id}/{discovery_splash_hash}{fmt}?size=2048"

    @property
    def mfa_level(self) -> None | str:
        reference_json = {
            0: f"🥰|{self.name} does not require to have 2FA/MFA enabled for MODERATION ACTIONS!",
            1: f"🤓|{self.name} requires to have 2FA/MFA enabled for MODERATION ACTIONS"
        }
        return reference_json.get(self._mfa)

    @property
    def verification_level(self) -> None | str:
        reference_json = {
            0: f"🥰|{self.name} doesn't have any kind of verification!",
            1: f"🙂|{self.name} requires user to have a verified email.",
            2: f"😭|{self.name} requires user to have a verified email + must be registered on discord for more than 5 "
               f"min.",
            3: f"🥺|{self.name} requires user to have a verified email + must be member of {self.name} for more than 10 "
               f"min.",
            4: f"💀|{self.name} requires user to have a verified email + a verified phone number 💀."
        }
        return reference_json.get(self._verification_level)

    @property
    def premium_level(self) -> None | str:
        reference_json = {
            0: f"😂|{self.name} doesn't have any server boost perks!",
            1: f"😃|{self.name} have level 1 server boost perks.",
            2: f"🧐|{self.name} have level 2 server boost perks.",
            3: f"💀|{self.name} have level 3 server boost perks."
        }
        return reference_json.get(self._boost_perks)

    @property
    def nsfw_level(self) -> None | str:
        reference_json = {
            0: "😃|Normal",
            1: "🙂|Explicit",
            2: "🤓|Safe",
            3: "💀|Age Restricted"
        }
        return reference_json.get(self._nsfw)

    @property
    def channels(self) -> Channels | None:
        if not self._channels:
            self._channels = self.__do_async_work(path='channels')
        return Channels(self._channels)

    @property
    def emojis(self) -> Emojis | None:
        if not self._emojis:
            self._emojis = self.__do_async_work(path='emojis')
        return Emojis(self._emojis)

    @property
    def roles(self) -> Roles | None:
        if not self._roles:
            self.__do_async_work(path='roles')
        return Roles(self._roles)

    @property
    def stickers(self) -> Stickers | None:
        if not self._stickers:
            self.__do_async_work(path='stickers')
        return Stickers(self._stickers)

    @property
    def features(self):
        if not self._features:
            return
        return '\n'.join([f.replace("_", " ").title() for f in self._features if f])

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.id == other.id

    def __ne__(self, other):
        return not self.__eq__(other)

    def __iter__(self):
        raise NotImplementedError

    def __int__(self):
        return self.id

    def __str__(self):
        from datetime import datetime
        features = '\n'.join(
            [f"\t{feature.strip().replace('_', ' ').title()}".expandtabs(6) for feature in self._features if feature]
        )
        r = f"""
Basic Info:
\tName: {self.name}
\tid: {self.id}
\tdescription: {self.description}
\ticon: {self.icon}
\tsplash: {self.splash}
\tdiscovery splash: {self.discovery_splash}
\tbanner: {self.banner}

Owner Info:
\tName: {self.owner.display_name}
\tid: {self.owner.id}
\tpronoun: {self.owner.pronoun}
\tavatar: {self.owner.avatar}
\tbanner: {self.owner.banner}
\tbio: {self.owner.bio}

Presence Info:
\t{self.name} has {self.approximate_member_count} members (approx).
\t{self.name} has {self.approximate_presence_count} members online (approx).

Media Info:
\t{self.name} has {len(self.emojis)} emojis.
\t{self.name} has {len(self.stickers)} stickers.

Advance Info:
\t{self.name} has {len(self.roles)} roles.
\t{self.name} has {len(self.channels)} channels.
\t{self.nsfw_level} is the NSFW level of {self.name}.
\t{self.mfa_level}
\t{self.premium_level}
\t{self.verification_level}
\t{self.name} has following features:
{features}

*This info is gathered at:
{datetime.now().strftime('%Y-%m-%d %H:%M:%S%p')}
"""
        return r.strip().expandtabs(3)

    def __repr__(self):
        return self.__str__()


class PartialGuild:
    __slots__ = (
        'name',
        'id',
        'permissions',
        'isOwner',
        '_icon',
        '_banner',
        '_features'
    )

    def __init__(self, data: dict):
        self._from_data(data)

    def _from_data(self, data: dict):
        self.name = data.get('name')
        self.id = data.get('id')
        self.permissions = data.get('permissions')
        self.isOwner = data.get('owner', False)
        self._banner = data.get('banner')
        self._icon = data.get('icon')
        self._features = data.get('features')

    @property
    def icon(self):
        if not self._icon:
            return
        fmt = '.gif' if self._icon.startswith("a_") else '.png'
        return ASSET_BASE + '/icons/' + str(self.id) + '/' + self._icon + fmt + '?size=2048'

    @property
    def banner(self):
        if not self._banner:
            return
        fmt = '.gif' if self._banner.startswith("a_") else '.png'
        return ASSET_BASE + '/banners/' + str(self.id) + '/' + self._banner + fmt + '?size=2048'

    @property
    def features(self):
        if not self._features:
            return
        return '\n'.join([f.replace("_", " ").title() for f in self._features if f])

    def __iter__(self):
        for attr in self.__slots__:
            if attr[0] == '_':
                continue
            value = getattr(self, attr, None)
            if value is None:
                continue
            yield attr, value

    def __eq__(self, other):
        return isinstance(other, PartialGuild) and self.id == other.id

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return f"{self.name} [{self.id}]"

    def __str__(self):
        return self.name

    def __int__(self):
        return self.id


class PartialGuilds:

    def __init__(self, loop: asyncio.AbstractEventLoop, headers: dict):
        self.__headers__ = headers
        self.__loop__ = loop
        self.__data__ = self._get_guilds()

    async def __list_guilds(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(BASE + '/users/@me/guilds', headers=self.__headers__) as response:
                return await response.json()

    def _get_guilds(self):
        task = self.__loop__.create_task(self.__list_guilds())
        result = self.__loop__.run_until_complete(task)
        return result

    def __iter__(self):
        for data in self.__data__:
            yield PartialGuild(data)

    def __len__(self):
        return len(self.__data__)

    def __getitem__(self, index):
        return PartialGuild(self.__data__[index])

    def __repr__(self):
        return f'Total {self.__len__()} {self.__class__.__name__}!'


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
