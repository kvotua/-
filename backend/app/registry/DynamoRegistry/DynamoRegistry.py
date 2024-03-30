from typing import Any

from ..IRegistry import IRegistry
from ..RegistryResponse import RegistryResponse
from ..RegistryTypes import RegistryData, RegistryQuery


class DynamoRegistry(IRegistry):
    __table: Any
    __pkeys: list[str]

    def __init__(self, table: Any) -> None:
        super().__init__()
        self.__table = table
        self.__pkeys = []

    @property
    def __primary_keys(self) -> list[str]:
        if len(self.__pkeys) == 0:
            self.__pkeys = [key["AttributeName"] for key in self.__table.key_schema]
        return self.__pkeys

    def create(self, data: RegistryData) -> None:
        self.__table.put_item(Item=data)

    def read(self, query: RegistryQuery) -> list[RegistryData]:
        response = self.__table.scan(
            ScanFilter={
                key: {"AttributeValueList": [value], "ComparisonOperator": "EQ"}
                for key, value in query.items()
            }
        )
        return response["Items"]

    def update(self, query: RegistryQuery, data: RegistryData) -> RegistryResponse:
        records = self.read(query)
        for record in records:
            self.__table.update_item(
                Key={key: record[key] for key in self.__primary_keys},
                AttributeUpdates={
                    key: {"Value": value, "Action": "PUT"}
                    for key, value in data.items()
                    if key not in self.__primary_keys
                },
            )
        return RegistryResponse(count=len(records))

    def delete(self, query: RegistryQuery) -> RegistryResponse:
        records = self.read(query)
        for record in records:
            self.__table.delete_item(
                Key={key: record[key] for key in self.__primary_keys},
            )
        return RegistryResponse(count=len(records))
