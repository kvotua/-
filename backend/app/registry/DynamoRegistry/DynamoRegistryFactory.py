import os
from typing import Any

import boto3

from ..IRegistry import IRegistry, IRegistryFactory
from .DynamoRegistry import DynamoRegistry


class DynamoRegistryFactory(IRegistryFactory):
    __dynamodb: Any

    def __init__(self) -> None:
        super().__init__()
        endpoint = os.getenv("YDB_DOCUMENT_API_ENDPOINT")
        if endpoint is None:
            raise ValueError("env var 'YDB_DOCUMENT_API_ENDPOINT' is not set")
        self.__dynamodb = boto3.resource(
            "dynamodb", endpoint_url=endpoint, region_name="dummy"
        )

    def get(self, name: str) -> IRegistry:
        return DynamoRegistry(self.__dynamodb.Table(name))
