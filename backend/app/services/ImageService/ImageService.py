from os import path

from fastapi import UploadFile

from app.config import settings

from ..AttributeService import IAttributeService
from ..exceptions import FileDoesNotExistError, IncompatibleNodeError
from ..FileService import IFileService
from ..NodeService.schemas.NodeId import NodeId
from .IImageService import IImageService


class ImageService(IImageService):
    __attribute_service: IAttributeService
    __file_service: IFileService
    __allowed_file_types = (
        "image/png",
        "image/jpeg",
        "image/jpg",
        "image/heic",
        "image/heif",
        "image/heics",
        "png",
        "jpeg",
        "jpg",
        "heic",
        "heif",
        "heics",
    )

    async def inject_dependencies(
        self,
        attribute_service: IAttributeService,
        file_service: IFileService,
    ) -> None:
        self.__attribute_service = attribute_service
        self.__file_service = file_service

    async def add_image(self, node_id: NodeId, file: UploadFile) -> None:
        attrs = await self.__attribute_service.get_attribute(node_id)
        if not await self.__attribute_service.is_file_type(attrs.type_id):
            raise IncompatibleNodeError()
        await self.__file_service.add_file(file, self.__allowed_file_types, node_id)

    async def remove_image(self, node_id: NodeId) -> None:
        await self.__file_service.remove_file(str(node_id))

    async def validate_image_response(self, node_id: NodeId) -> str:
        if not await self.__file_service.exists(str(node_id)):
            raise FileDoesNotExistError()
        return path.join("/", settings.storage, str(node_id))
