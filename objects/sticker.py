from objects.constants import ASSET_BASE, ASSET_BASE_TWO


class Sticker:
    __slots__ = ("id", "name", "file_type", "animated", "url")

    def __init__(self, data: dict):
        self._from_data(data)

    def _from_data(self, data: dict) -> None:
        self.id: int = int(data["id"])
        self.name: str = data["name"]

        format_type: int = int(data["format_type"] or "1")
        format_map = {
            1: "png",
            2: "png",  # apng
            3: "json",  # lottie
            4: "gif",
        }
        base: str = ASSET_BASE if format_type != 4 else ASSET_BASE_TWO

        self.animated: bool = format_type in [2, 4]
        self.file_type: str = format_map.get(format_type) or "png"
        self.url: str = f"{base}/stickers/{self.id}.{self.file_type}?size=2048"

    def __repr__(self) -> str:
        return f"<Sticker id={self.id} name={self.name!r} animated={self.animated}>"

    def __str__(self) -> str:
        return self.name

    def __eq__(self, other):
        return isinstance(other, Sticker) and self.id == other.id

    def __iter__(self):
        for attr in self.__slots__:
            if attr[0] == "-":
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
        return f"Total {self.__len__()} {self.__class__.__name__}!"
