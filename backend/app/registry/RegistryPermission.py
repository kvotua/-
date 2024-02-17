class RegistryPermission:
    __canCreate: bool
    __canRead: bool
    __canUpdate: bool
    __canDelete: bool

    def __init__(
        self,
        *,
        canCreate: bool = False,
        canRead: bool = False,
        canUpdate: bool = False,
        canDelete: bool = False
    ) -> None:
        self.__canCreate = canCreate
        self.__canRead = canRead
        self.__canUpdate = canUpdate
        self.__canDelete = canDelete

    @property
    def canCreate(self) -> bool:
        return self.__canCreate

    @property
    def canRead(self) -> bool:
        return self.__canRead

    @property
    def canUpdate(self) -> bool:
        return self.__canUpdate

    @property
    def canDelete(self) -> bool:
        return self.__canDelete
