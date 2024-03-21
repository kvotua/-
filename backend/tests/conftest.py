from dataclasses import dataclass
from typing import Callable

import pytest
from dataclass_wizard import JSONWizard
from fastapi import status

from .setup import client


@dataclass
class Project(JSONWizard):
    """
    name: str
    id: str
    core_node_id: str
    owner_id: str
    """

    name: str
    id: str
    core_node_id: str
    owner_id: str


@dataclass
class Node(JSONWizard):
    id: str
    parent_node: str | None
    children: list["Node"]


@pytest.fixture
def create_user() -> Callable[[], tuple[dict[str, str], str]]:
    def _create_user() -> tuple[dict[str, str], str]:
        user, user_init_data = client.get_random_user()

        response = client.create_user(
            user_id=user["id"],
        )
        assert response.status_code == status.HTTP_201_CREATED

        return user, user_init_data

    return _create_user


@pytest.fixture
def create_project() -> Callable[[str], Project]:
    def _create_project(user_init_data: str) -> Project:
        name = client.get_random_project_name()

        response = client.create_project(
            project_name=name,
            user_init_data=user_init_data,
        )

        project = Project.from_dict(response.json())

        assert response.status_code == status.HTTP_201_CREATED

        return project

    return _create_project


@pytest.fixture
def create_node() -> Callable[[str, str], str]:
    def _create_node(parent_id: str, user_init_data: str) -> str:
        response = client.create_node(
            parent_id=parent_id,
            user_init_data=user_init_data,
        )

        assert response.status_code == status.HTTP_201_CREATED

        return str(response.json())

    return _create_node
