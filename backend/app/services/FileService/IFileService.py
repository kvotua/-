from abc import ABC, abstractmethod
from re import Pattern

from fastapi import UploadFile


class IFileService(ABC):

    @abstractmethod
    async def add_file(
        self,
        file: UploadFile,
        allowed_formats: Pattern,
        file_name: str,
    ) -> None:
        pass

    @abstractmethod
    async def remove_file(self, file_name: str) -> None:
        pass

    @abstractmethod
    async def create_folder(self, folder_path: str, folder_name: str) -> None:
        pass

    @abstractmethod
    async def remove_folder(self, folder_path: str) -> None:
        pass

    @abstractmethod
    async def save_page(self, path: str, html: str) -> None:
        pass

    @abstractmethod
    async def exists(self, file_path: str) -> bool:
        pass
