from pymongo import MongoClient
from app.config import (
    host,
    port,
    db_name,
    uuid,
    users_collection_name,
    projects_collection_name,
)

mongoClient = MongoClient(host=host, port=port, uuidRepresentation=uuid)

database = mongoClient.get_database(db_name)

users_collection = database.get_collection(users_collection_name)
projects_collection = database.get_collection(projects_collection_name)

__all__ = [users_collection, projects_collection]
