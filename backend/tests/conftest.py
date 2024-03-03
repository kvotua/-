from typing import Callable

import pytest
from fastapi import status

from .setup import client


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
def create_project() -> Callable[[str], tuple[str, str]]:
    def _create_project(user_init_data: str) -> tuple[str, str]:
        name = client.get_random_project_name()

        response = client.create_project(
            project_name=name,
            user_init_data=user_init_data,
        )
        _id = str(response.json())

        assert response.status_code == status.HTTP_201_CREATED

        return name, _id

    return _create_project
