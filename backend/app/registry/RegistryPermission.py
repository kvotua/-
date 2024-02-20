class RegistryPermission:
    """
    Represents permissions for creating, reading, updating, and deleting \
        registry entries.

    Attributes:
        canCreate (bool): Indicates whether the permission to create registry
            entries is granted.
        canRead (bool): Indicates whether the permission to read registry
            entries is granted.
        canUpdate (bool): Indicates whether the permission to update registry
            entries is granted.
        canDelete (bool): Indicates whether the permission to delete registry
            entries is granted.
    """

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
        """
        Initializes a new instance of the RegistryPermission class.

        Args:
            canCreate (bool, optional): Indicates whether the permission to
                create registry entries is granted. Defaults to False.
            canRead (bool, optional): Indicates whether the permission to read
                registry entries is granted. Defaults to False.
            canUpdate (bool, optional): Indicates whether the permission to
                update registry entries is granted. Defaults to False.
            canDelete (bool, optional): Indicates whether the permission to
                delete registry entries is granted. Defaults to False.
        """
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
