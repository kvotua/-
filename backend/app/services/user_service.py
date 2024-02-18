from app.schemas.User import (
    UserSchema,
    UserCreateSchema,
    UserUpdateSchema,
)
from app.registry import IRegistry


class UserService:
    __registry: IRegistry

    def __init__(self, registry: IRegistry) -> None:
        self.__registry = registry

    def get_by_id(self, user_id: str) -> UserSchema | None:
        """Function to retrieve single user by id"""
        result = self.__registry.read({"id": user_id})
        if len(result) != 1:
            return None
        return UserSchema(**result[0])

    def create(self, new_user: UserCreateSchema) -> None:
        """Function to create a project and return the user's id."""
        user = UserSchema(**new_user.model_dump(by_alias=True))
        self.__registry.create(user.model_dump(by_alias=True))

    def update(self, user_id: str, user_update: UserUpdateSchema) -> int:
        """Function to update a single user and return
        the number of users matched for this update."""
        response = self.__registry.update(
            {"id": user_id}, user_update.model_dump(exclude_none=True)
        )
        return response.count

    def delete_by_id(self, user_id: str) -> int:
        """Function to delete a single user and
        return the number of users deleted."""
        response = self.__registry.delete({"id": user_id})
        return response.count

    def exist(self, user_id: str) -> bool:
        """Verification of existence"""
        result = self.__registry.read({"id": user_id})
        return len(result) > 0
