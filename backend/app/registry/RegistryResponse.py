class RegistryResponse:
    """
    Represents a response from a registry operation.
    """

    __count: int

    def __init__(self, *, count: int) -> None:
        """
        Initializes a new instance of the RegistryResponse class.

        Args:
            count (int): The number of affected entities in the response.
        """
        self.__count = count

    @property
    def count(self) -> int:
        return self.__count
