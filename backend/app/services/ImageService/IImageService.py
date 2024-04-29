from abc import ABC, abstractmethod

from fastapi import UploadFile

from ..NodeService.schemas.NodeId import NodeId


class IImageService(ABC):

    @abstractmethod
    async def add_image(self, node_id: NodeId, file: UploadFile) -> None:
        pass

    @abstractmethod
    async def remove_image(self, node_id: NodeId) -> None:
        pass

    @abstractmethod
    async def validate_image_response(self, node_id: NodeId) -> str:
        pass
