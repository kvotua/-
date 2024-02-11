from .UserEntity import UserEntity
from .ProjectEntity import ProjectEntity
from app.database import users_collection, projects_collection

users = UserEntity(users_collection)
projects = ProjectEntity(projects_collection)

__all__=[UserEntity,ProjectEntity,users,projects]