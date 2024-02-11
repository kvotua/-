from pymongo.collection import Collection
from fastapi import HTTPException, status
from app.models import User
from app.schemas import UserNew
from app.config import user_already_exists, user_do_not_exist


class UserEntity:
    users_collection: Collection

    def __init__(self, collection: Collection) -> None:
        self.users_collection = collection

    def get_by_id(self, id: int) -> User:
        user = self.users_collection.find_one({"_id": id})

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=user_do_not_exist
            )
        return user

    def add(self, user: UserNew) -> int:

        if self.exist(user.id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=user_already_exists
            )

        user_db = User(**user.model_dump(by_alias=True))
        self.users_collection.insert_one(user_db.model_dump(by_alias=True))

        return user_db.id

    def delete(self, id: int) -> None:
        if self.exist(id):
            self.users_collection.find_one_and_delete({"_id": id})
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=user_do_not_exist
            )

    def exist(self, id: int) -> bool:
        return self.users_collection.find_one({"_id": id}) is not None
