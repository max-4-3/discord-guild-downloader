from typing import Optional, Literal

from objects import DISCORD_BASE


class Channel:
    __slots__ = (
        'name',
        'id',
        'guild_id',
        'topic',
        'nsfw',
        'position',
        'slowmode_delay',
        'overwrites',
        'type',
        'jump_url'
    )

    def __init__(self, data: dict):
        self._from_data(data)

    def _from_data(self, data: dict):
        self.name: str = data['name']
        self.id = data['id']
        self.guild_id = data['guild_id']
        self.overwrites = data['overwrites']
        self.topic: Optional[str] = data.get('topic')
        self.position: int = data['position']
        self.nsfw: bool = data.get('nsfw', False)
        self.slowmode_delay: float = data.get('rate_limit_per_user', 0)
        self.type: Literal[0, 5] = data.get('type', self.type)
        self.jump_url = f'{DISCORD_BASE}/channels/{self.guild_id}/{self.id}'

    def __eq__(self, other):
        return isinstance(other, Channel) and self.id == other.id

    def __ne__(self, other):
        return not self.__eq__(other)

    def __iter__(self):
        for attr in self.__slots__:
            if attr[0] == '-':
                continue
            value = getattr(self, attr, None)
            if value is None:
                continue
            yield attr, value

    def __int__(self):
        return self.id

    def __str__(self):
        return self.name

    def __repr__(self) -> str:
        return self.jump_url


class Channels:
    def __init__(self, data: list[dict]):
        self.__data = data

    def __iter__(self):
        for data in self.__data:
            yield Channel(data)

    def __len__(self):
        return len(self.__data)

    def __getitem__(self, index):
        return Channel(self.__data[index])

    def __repr__(self):
        return f'Total {self.__len__()} {self.__class__.__name__}!'
