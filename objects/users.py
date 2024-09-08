import asyncio
from typing import Optional

import aiohttp

from objects.constants import BASE, ASSET_BASE


class BaseUser:
    __slots__ = (
        'name',
        'id',
        'discriminator',
        'global_name',
        '_avatar',
        '_banner',
        'bot',
        'system',
        'public_flags',
        'bio',
        'pronoun',
        'accent_colour'
    )

    def __init__(self, data: dict, client: bool = False) -> None:
        self._update(data, client)

    def _update(self, data: dict, client) -> None:
        if not client:
            user = data.get('user')
            self.pronoun = data.get("user_profile", {}).get("pronouns")
        else:
            self.pronoun = None
            user = data
        self.name = user['username']
        self.id = int(user['id'])
        self.discriminator = user.get("discriminator", 0)
        self.global_name = user.get('global_name')
        self._avatar = user['avatar']
        self._banner = user.get('banner', "")
        self.accent_colour = user.get('accent_color', None)
        self.public_flags = user.get('public_flags', 0)
        self.bot = user.get('bot', False)
        self.system = user.get('system', False)
        self.bio = user.get("bio")

    @property
    def avatar(self) -> Optional[str]:
        if self._avatar is not None:
            fmt = ".gif" if self._avatar.startswith('a_') else ".png"
            return f"{ASSET_BASE}/avatars/{self.id}/{self._avatar}{fmt}?size=2048"
        return None

    @property
    def banner(self) -> Optional[str]:
        if self._banner is not None:
            fmt = ".gif" if self._banner.startswith('a_') else ".png"
            return f"{ASSET_BASE}/banners/{self.id}/{self._banner}{fmt}?size=2048"
        return None

    @property
    def display_name(self) -> str:
        if self.global_name:
            return self.global_name
        return self.name

    def __iter__(self):
        for attr in self.__slots__:
            if attr[0] == '_':
                continue
            value = getattr(self, attr, None)
            if value is None:
                continue
            yield attr, value

    def __repr__(self) -> str:
        return (
            f"<BaseUser id={self.id} name={self.name!r} global_name={self.global_name!r}"
            f" bot={self.bot} system={self.system}>"
        )

    def __str__(self) -> str:
        if self.discriminator == '0':
            return self.name
        return f'{self.name}#{self.discriminator}'

    def __eq__(self, other: object) -> bool:
        return isinstance(other, self.__class__) and other.id == self.id

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def __hash__(self) -> int:
        return self.id >> 22
    

class Owner(BaseUser):
    __slots__ = (*BaseUser.__slots__, '__loop')

    def __init__(self, loop: asyncio.AbstractEventLoop, owner_id: int, headers: dict):
        self.__loop = loop
        super().__init__(self._owner_data(owner_id, headers), client=False)

    @staticmethod
    async def __get_owner(owner_id, headers):
        async with aiohttp.ClientSession() as session:
            url = BASE + '/users/' + str(owner_id) + '/profile'
            async with session.get(url, headers=headers) as response:
                return await response.json()

    def _owner_data(self, owner_id, headers):
        task = self.__loop.create_task(self.__get_owner(owner_id, headers))
        result = self.__loop.run_until_complete(task)
        return result


class Clint(BaseUser):
    __slots__ = (*BaseUser.__slots__, 'contact', 'verified')

    def __init__(self, loop: asyncio.AbstractEventLoop, headers: dict):
        data = self._client_data(loop, headers)
        self.contact = data.get("phone", data.get('email'))
        self.verified = data.get('verified')
        super().__init__(data, client=True)

    @staticmethod
    async def __get_user(headers):
        async with aiohttp.ClientSession() as session:
            url = BASE + '/users/@me'
            async with session.get(url, headers=headers) as response:
                return await response.json()

    def _client_data(self, loop: asyncio.AbstractEventLoop, headers):
        task = loop.create_task(self.__get_user(headers))
        result = loop.run_until_complete(task)
        return result
