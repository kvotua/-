from abc import ABC, abstractmethod

from ..NodeService.schemas import NodeId, NodeTreeSchema
from .schemas.TemplateId import TemplateId
from .schemas.TemplateView import TemplateView


class ITemplateService(ABC):
    @abstractmethod
    async def instantiate(self, template_id: TemplateId) -> NodeTreeSchema:
        pass

    @abstractmethod
    async def get_all(self) -> list[TemplateId]:
        pass

    @abstractmethod
    async def get(self, template_id: TemplateId) -> TemplateView:
        pass

    @abstractmethod
    async def create(self, node_id: NodeId) -> TemplateId:
        pass
