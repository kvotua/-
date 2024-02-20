class RegistryPermissionException(Exception):
    def __init__(self) -> None:
        super().__init__("Operation not allowed")
