from os import path, remove

import filetype  # type: ignore
from fastapi import UploadFile

from app.config import settings

from ..exceptions import FileDoesNotExistError, FileTooBigError, InvalidFileFormatError
from .IFileService import IFileService


class FileService(IFileService):
    __file_size = 2097152

    async def add_file(
        self,
        file: UploadFile,
        allowed_formats: tuple,
        file_name: str,
    ) -> None:

        if file.filename is None:
            raise InvalidFileFormatError()
        await self.__validate_file(file, allowed_formats)
        await file.seek(0)
        with open(path.join("/", settings.storage, file_name), "wb+") as end_file:
            end_file.write(await file.read())

    async def remove_file(self, file_name: str) -> None:
        file_path = path.join("/", settings.storage, file_name)
        if not await self.exists(file_path):
            raise FileDoesNotExistError()
        remove(file_path)

    async def exists(self, file_name: str) -> bool:
        return path.isfile(path.join("/", settings.storage, file_name))

    async def __validate_file(self, file: UploadFile, allowed_formats: tuple) -> None:
        file_info = filetype.guess(file.file)
        if file_info is None:
            raise InvalidFileFormatError()

        detected_content_type = file_info.extension.lower()

        if (
            file.content_type not in allowed_formats
            or detected_content_type not in allowed_formats
        ):
            raise InvalidFileFormatError()

        real_file_size = 0
        for chunk in file.file:
            real_file_size += len(chunk)
            if real_file_size > self.__file_size:
                raise FileTooBigError()
