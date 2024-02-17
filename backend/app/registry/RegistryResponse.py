class RegistryResponse:
    __count: int

    def __init__(self, *, count: int) -> None:
        self.__count = count

    @property
    def count(self) -> int:
        return self.__count
