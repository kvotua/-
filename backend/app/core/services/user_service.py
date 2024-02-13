from app.api_v1.users.schemas import (
    UserSchema,
    UserCreateSchema,
    UserUpdateSchema,
)
from app.core.services.base_service import ServiceBase


class UserService(ServiceBase):
    def get_by_id(self, user_id: int) -> UserSchema | None:
        """Function to retrieve single user by id"""
        user = self.registry.get_by_id(user_id)
        if user:
            return UserSchema(**user)

    def create(self, new_user: UserCreateSchema) -> str:
        """Function to create a project and return the user's id."""
        user = UserSchema(**new_user.model_dump())
        return self.registry.create(user.model_dump(by_alias=True))

    def update(self, user_id: int, user_update: UserUpdateSchema):
        """Function to update a single user and return
        the number of users matched for this update."""
        if self.registry.exist(user_id):
            return self.registry.update(
                user_id,
                user_update.model_dump(exclude_none=True),
            )

    def delete_by_id(self, user_id: int) -> int | None:
        """Function to delete a single user and
        return the number of users deleted."""
        if self.registry.exist(user_id):
            return self.registry.delete(user_id)

    def exist(self, user_id: int) -> bool:
        """Verification of existence"""
        return self.registry.exist(user_id)
