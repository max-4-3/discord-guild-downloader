from objects import ASSET_BASE


class Emoji:
    __slots__ = ("name", "id", "animated", "url")

    def __init__(self, data: dict):
        self._from_data(data)

    def _from_data(self, data: dict):
        self.id: int = int(data.get("id"))
        self.name: str = data.get("name", "no name lol")
        self.animated: bool = data.get("animated", False)
        fmt = 'gif' if self.animated else 'png'
        self.url = f'{ASSET_BASE}/emojis/{self.id}.{fmt}?size=2048'

    def __iter__(self):
        for attr in self.__slots__:
            if attr[0] == '-':
                continue
            value = getattr(self, attr, None)
            if value is None:
                continue
            yield attr, value

    def __str__(self) -> str:
        if self.animated:
            return f'<a:{self.name}:{self.id}>'
        return f'<:{self.name}:{self.id}>'

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Emoji) and self.id == other.id

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def __hash__(self) -> int:
        return self.id >> 22

    def __repr__(self) -> str:
        return f'<Emoji id={self.id} name={self.name!r} animated={self.animated}>'


class Emojis:
    def __init__(self, data: list[dict]):
        self.__data = data

    def __iter__(self):
        for data in self.__data:
            yield Emoji(data)

    def __len__(self):
        return len(self.__data)

    def __getitem__(self, index):
        return Emoji(self.__data[index])

    def __repr__(self):
        return f'Total {self.__len__()} {self.__class__.__name__}!'

