from os import path
from re import compile

from fastapi import UploadFile

from app.config import settings

from ..AttributeService import IAttributeService
from ..exceptions import FileDoesNotExistError, IncompatibleNodeError
from ..FileService import IFileService
from ..NodeService.schemas.NodeId import NodeId
from .IImageService import IImageService


class ImageService(IImageService):
    """
    service class for managing image related operations
    """

    __attribute_service: IAttributeService
    __file_service: IFileService
    # TODO make a prettier (and optionaly shorter) regex
    __allowed_file_types = compile(
        "^(image\\/(png|jpeg|jpg|heics|heif|heic))$|^(png|jpeg|jpg|heics|heif|heic)$"
    )

    async def inject_dependencies(
        self,
        attribute_service: IAttributeService,
        file_service: IFileService,
    ) -> None:
        """injects service dependancies"""
        self.__attribute_service = attribute_service
        self.__file_service = file_service

    async def add_image(self, node_id: NodeId, file: UploadFile) -> None:
        """
        adds image to a node

        Args:
            node_id (NodeId): id of node
            file (UploadFile): file to be added

        Raises:
            IncompatibleNodeError: raised when attempting to add image \
                to incompatible node
        """
        if not await self.__attribute_service.is_file_type(node_id):
            raise IncompatibleNodeError()
        await self.__file_service.add_file(file, self.__allowed_file_types, node_id)

    async def remove_image(self, node_id: NodeId) -> None:
        """
        removes image from system

        Args:
            node_id (NodeId): id of a node whose image \
                  needs to be removed
        """
        await self.__file_service.remove_file(str(node_id))

    async def get_image_response(self, node_id: NodeId) -> str:
        """
        checks if given node has an image and \
            returns filepath to it

        Args:
            node_id (NodeId): node id

        Raises:
            FileDoesNotExistError: raised when given node \
                  doesn't have an image

        Returns:
            str: path to an image
        """
        if not await self.__file_service.exists(str(node_id)):
            raise FileDoesNotExistError()
        return path.join("/", settings.storage, str(node_id))
