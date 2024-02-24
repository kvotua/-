from app.registry import IRegistry
from .schemas import UserCreateSchema, UserSchema

from ..exceptions import UserExistError, UserNotFoundError, NotAllowedError
from .IUserService import IUserService


class UserService(IUserService):
    """
    A service class for managing user-related operations.
    """

    __registry: IRegistry

    def __init__(self, registry: IRegistry) -> None:
        """
        Initialize the UserService with a registry.

        Parameters:
            registry (IRegistry): The registry to use for user operations.
        """
        self.__registry = registry

    def user_exist_validation(self, user_id: str) -> str:
        if not self._exist(user_id):
            raise UserNotFoundError()
        return user_id

    def try_get_by_id(self, initiator_id: str, user_id: str) -> UserSchema:
        """
        Attempt to retrieve user information by user ID.

        Parameters:
            initiator_id (str): The ID of the initiator performing the operation.
            user_id (str): The ID of the user to retrieve.

        Returns:
            UserSchema: The user information.

        Raises:
            NotAllowedError: If the initiator is not allowed to perform the operation.
            UserNotFoundError: If the user with the specified ID is not found.
        """
        self.user_exist_validation(initiator_id)
        if initiator_id != user_id:
            raise NotAllowedError()
        return self._get_by_id(user_id)

    def create(self, new_user: UserCreateSchema) -> None:
        """
        Create a new user.

        Parameters:
            new_user (UserCreateSchema): The schema representing the new user to create.

        Raises:
            UserExistError: If a user with the same ID already exists.
        """
        if self._exist(new_user.id):
            raise UserExistError()
        user = UserSchema(**new_user.model_dump())
        self.__registry.create(user.model_dump())

    def _exist(self, user_id: str) -> bool:
        """
        Check if a user exists based on the provided ID.

        Parameters:
            user_id (str): The ID of the user to check.

        Returns:
            bool: True if the user exists, False otherwise.
        """
        result = self.__registry.read({"id": user_id})
        return len(result) > 0

    def _get_by_id(self, user_id: str) -> UserSchema:
        """
        Get user information by ID.

        Parameters:
            user_id (str): The ID of the user to retrieve.

        Returns:
            UserSchema: The user information.

        Raises:
            UserNotFoundError: If the user with the specified ID is not found.
        """
        self.user_exist_validation(user_id)
        result = self.__registry.read({"id": user_id})
        if len(result) < 1:
            raise UserNotFoundError()
        return UserSchema(**result[0])
