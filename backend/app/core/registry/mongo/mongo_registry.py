from abc import ABC
from typing import Any
from uuid import UUID

from pymongo.collection import Collection

from app.core.registry.base_registry import RegistryBase


class MongoRegistry(RegistryBase, ABC):
    def __init__(self, collection: Collection) -> None:
        self.collection = collection

    def get(
        self,
        field_name: str,
        value: Any,
        skip: int = 0,
        limit: int = 5,
    ):
        """Search for a document by the specified field and the value of this field"""
        return self.collection.find({field_name: value}).skip(skip).limit(limit)

    def get_by_id(self, object_id: UUID | int):
        """Function to retrieve single documents from a provided
        Collection using a dictionary containing a document's elements."""
        return self.collection.find_one({"_id": object_id})

    def create(self, document: dict) -> str:
        """Function to insert a document into a collection and
        return the document's id."""
        return str(self.collection.insert_one(document).inserted_id)

    def update(self, object_id: UUID | int, new_values: dict) -> int:
        """Function to update a single document in a collection and return
        the number of documents matched for this update."""
        result = self.collection.update_one(
            {"_id": object_id},
            {"$set": new_values},
        )
        return result.matched_count

    def delete(self, object_id: UUID | int) -> int:
        """Function to delete a single document from a collection and
        return the number of documents deleted."""
        result = self.collection.delete_one({"_id": object_id})
        return result.deleted_count

    def exist(self, object_id) -> bool:
        return self.get_by_id(object_id) is not None
