from abc import ABC, abstractmethod

from .schemas import UserCreateSchema, UserId, UserSchema


class IUserService(ABC):
    @abstractmethod
    def try_get_by_id(self, initiator_id: UserId, user_id: UserId) -> UserSchema:
        pass

    @abstractmethod
    def create(self, new_user: UserCreateSchema) -> None:
        pass

    @abstractmethod
    def user_exist_validation(self, user_id: UserId) -> None:
        pass

    @abstractmethod
    def exist(self, user_id: UserId) -> bool:
        pass
