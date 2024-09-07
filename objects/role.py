class Role:
    __slots__ = (
        'id',
        'name',
        'permissions',
        'colour',
        'position',
        'managed',
        'mentionable',
        'hoist',
        'guild'
    )

    def __init__(self, data: dict):
        self.id = data['id']

        self._from_data(data)

    def _from_data(self, data: dict):
        self.name: str = data['name']
        self.permissions: int = int(data.get('permissions', 0))
        self.position: int = data.get('position', 0)
        self.colour: int = data.get('color', 0)
        self.hoist: bool = data.get('hoist', False)
        self.managed: bool = data.get('managed', False)
        self.mentionable: bool = data.get('mentionable', False)

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f'<Role id={self.id} name={self.name!r}>'

    def __iter__(self):
        for attr in self.__slots__:
            if attr[0] == '-':
                continue
            value = getattr(self, attr, None)
            if value is None:
                continue
            yield attr, value


class Roles:
    def __init__(self, data: list[dict]):
        self.__data = data

    def __iter__(self):
        for data in self.__data:
            yield Role(data)

    def __len__(self):
        return len(self.__data)

    def __getitem__(self, index):
        return Role(self.__data[index])

    def __repr__(self):
        return f'Total {self.__len__()} {self.__class__.__name__}!'

