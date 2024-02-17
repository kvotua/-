from app.registry import registry_factory, RegistryPermission
from .project_service import ProjectService
from .user_service import UserService

project_service = ProjectService(
    registry_factory.get(
        "projects",
        RegistryPermission(
            canCreate=True, canRead=True, canUpdate=True, canDelete=True
        ),
    )
)
user_service = UserService(
    registry_factory.get(
        "users",
        RegistryPermission(
            canCreate=True, canRead=True, canUpdate=True, canDelete=True
        ),
    )
)
