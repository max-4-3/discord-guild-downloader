from objects.constants import ASSET_BASE


class Sticker:
    __slots__ = ('id', 'name', 'animated', 'url')

    def __init__(self, data: dict):
        self._from_data(data)

    def _from_data(self, data: dict) -> None:
        self.id: int = int(data['id'])
        self.name: str = data['name']
        format_type = data["format_type"]
        if format_type == 4:
            self.animated = True
        else:
            self.animated = False
        self.url: str = f'{ASSET_BASE}/stickers/{self.id}.{"gif" if self.animated else "png"}?size=2048'

    def __repr__(self) -> str:
        return f'<Sticker id={self.id} name={self.name!r} animated={self.animated}>'

    def __str__(self) -> str:
        return self.name

    def __eq__(self, other):
        return isinstance(other, Sticker) and self.id == other.id

    def __iter__(self):
        for attr in self.__slots__:
            if attr[0] == '-':
                continue
            value = getattr(self, attr, None)
            if value is None:
                continue
            yield attr, value


class Stickers:
    def __init__(self, data: list[dict]):
        self.__data = data

    def __iter__(self):
        for data in self.__data:
            yield Sticker(data)

    def __len__(self):
        return len(self.__data)

    def __getitem__(self, index):
        return Sticker(self.__data[index])

    def __repr__(self):
        return f'Total {self.__len__()} {self.__class__.__name__}!'

