from pathlib import Path

from fastapi import Request
from fastapi.templating import Jinja2Templates
from jinja2 import Environment, FileSystemLoader

from ..NodeService import INodeService
from ..NodeService.schemas.NodeTreeSchema import NodeTreeSchema
from ..ProjectService import IProjectService
from ..ProjectService.schemas.ProjectId import ProjectId
from .IHTMLService import IHTMLService


class HTMLService(IHTMLService):
    """A service class responsible for managing html responses"""

    __project_service: IProjectService
    __node_service: INodeService
    __templates = Jinja2Templates(
        env=Environment(
            loader=FileSystemLoader(Path(Path(__file__).parent, "templates")),
            autoescape=True,
            enable_async=True,
        )
    )

    async def inject_dependencies(
        self,
        project_service: IProjectService,
        node_service: INodeService,
    ) -> None:
        """
        inject dependencies necessary for service to work

        Args:
            project_service (IProjectService): service for interactions with projects
            node_service (INodeService): service for interactions with nodes
        """
        self.__project_service = project_service
        self.__node_service = node_service

    async def render_index_page(self, request: Request, project_id: ProjectId) -> str:
        """
        returns index page of a project

        Args:

        #TODO:add a discription to the request

            request (Request): wish I knew what that is
            project_id (ProjectId): id of a project

        Returns:
            str: html template
        """
        project = await self.__project_service.get(project_id)
        root = await self.__node_service.get_tree(project.core_node_id)

        core_node = await self.__templates.get_template(
            name=f"{str(root.type_id)}.html"
        ).render_async(
            node=root,
            node_list=await self.__return_template_list(request, root.children),
        )
        return await self.__templates.get_template(
            name="base.html",
        ).render_async(request=request, project_name=project.name, core=core_node)

    async def __return_template_list(
        self, request: Request, child_nodes: list[NodeTreeSchema]
    ) -> list[str]:
        """
        return list of templates as strings \
        this function is used in order to get templates of all child nodes \
        of a node

        Args:
        #TODO:add a discription to the request
            request (Request): wish I knew what that is
            child_nodes (list[NodeTreeSchema]): list of NodeTreeSchema objects

        Returns:
            list[str]: list of templates as strings
        """
        template_list = list()
        for child in child_nodes:
            template_list.append(
                await self.__templates.get_template(
                    name=f"{str(child.type_id)}.html"
                ).render_async(
                    node=child,
                    node_list=await self.__return_template_list(
                        request, child.children
                    ),
                    request=request,
                )
            )
        return template_list
