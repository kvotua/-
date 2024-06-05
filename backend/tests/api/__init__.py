from .nodes import ApiNodes
from .projects import ApiProjects
from .templates import ApiTemplates
from .users import ApiUsers


class ClientApi(
    ApiUsers,
    ApiProjects,
    ApiNodes,
    ApiTemplates,
):
    pass
