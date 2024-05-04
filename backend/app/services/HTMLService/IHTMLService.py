from abc import ABC, abstractmethod

from fastapi import Request

from ..ProjectService.schemas.ProjectId import ProjectId


class IHTMLService(ABC):
    @abstractmethod
    async def return_index_page(self, request: Request, project_id: ProjectId) -> str:
        pass
