from abc import ABC, abstractmethod

from .schemas import UserCreateSchema, UserId, UserSchema


class IUserService(ABC):
    @abstractmethod
    async def try_get_by_id(self, initiator_id: UserId, user_id: UserId) -> UserSchema:
        pass

    @abstractmethod
    async def create(self, new_user: UserCreateSchema) -> None:
        pass

    @abstractmethod
    async def user_exist_validation(self, user_id: UserId) -> None:
        pass

    @abstractmethod
    async def exist(self, user_id: UserId) -> bool:
        pass
