from abc import ABC, abstractmethod

from .schemas import UserCreateSchema, UserSchema


class IUserService(ABC):
    @abstractmethod
    def try_get_by_id(self, initiator_id: str, user_id: str) -> UserSchema:
        pass

    @abstractmethod
    def create(self, new_user: UserCreateSchema) -> None:
        pass

    @abstractmethod
    def user_exist_validation(self, user_id: str) -> None:
        pass

    @abstractmethod
    def exist(self, user_id: str) -> bool:
        pass
