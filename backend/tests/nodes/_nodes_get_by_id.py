from typing import Callable

from fastapi import status

from ..conftest import Node
from ..setup import client

"""
### GET /nodes/{node_id}

user-init-data:
1. пользователь существует
2. пользователь не существует
3. неправильный формат

node_id:
1. существует и принадлежит инициатору
    a. не является корневой
    b. является корневой
2. существует и не принадлежит инициатору
    a. не является корневой
    b. является корневой
3. не существует

- (1, 1a) - 200 - узел действительно отображается
- (1, 1b) - 200 - узел действительно отображается
- (1, 2a) - 403
- (1, 2b) - 403
- (1, 3) - 404
- (2, 1) - 401
- (2, 2) - 401
- (2, 3) - 401
- (3, 1) - 401
- (3, 2) - 401
- (3, 3) - 401
"""


# (1, 1a)
def test_get_node(
    create_user: Callable, create_project: Callable, create_node: Callable
) -> None:
    """(1, 1a) - 200 - узел действительно отображается"""
    _, user_init_data = create_user()
    project = create_project(user_init_data=user_init_data)
    node = create_node(parent_id=project.core_node_id, user_init_data=user_init_data)

    response = client.get_node(
        node_id=node,
        user_init_data=user_init_data,
    )

    assert response.status_code == status.HTTP_200_OK
    assert Node.from_dict(response.json()).id == node


# (1, 1b)
def test_get_root_node(create_user: Callable, create_project: Callable) -> None:
    """(1, 1b) - 404"""
    _, user_init_data = create_user()
    project = create_project(user_init_data=user_init_data)

    response = client.get_node(
        node_id=project.core_node_id,
        user_init_data=user_init_data,
    )

    assert response.status_code == status.HTTP_200_OK
    assert Node.from_dict(response.json()).id == project.core_node_id


# (1, 2a)
def test_try_get_another_node(
    create_user: Callable, create_project: Callable, create_node: Callable
) -> None:
    """(1, 2a) - 403"""
    _, user_init_data = create_user()
    project = create_project(user_init_data=user_init_data)
    node = create_node(parent_id=project.core_node_id, user_init_data=user_init_data)

    _, user_init_data = create_user()

    response = client.get_node(
        node_id=node,
        user_init_data=user_init_data,
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


# (1, 2b)
def test_try_get_another_root_node(
    create_user: Callable, create_project: Callable
) -> None:
    """(1, 2b) - 403"""
    _, user_init_data = create_user()
    project = create_project(user_init_data=user_init_data)

    _, user_init_data = create_user()

    response = client.get_node(
        node_id=project.core_node_id,
        user_init_data=user_init_data,
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


# (1, 3)
def test_try_get_nonexistent_node(create_user: Callable) -> None:
    """(1, 3) - 404"""
    _, user_init_data = create_user()
    node_id = "0"

    response = client.get_node(
        node_id=node_id,
        user_init_data=user_init_data,
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


# (2, 1a), (2, 2a)
def test_try_get_node_from_nonexistent_user(
    create_user: Callable, create_project: Callable, create_node: Callable
) -> None:
    """(2, 1a) - 401, (2, 2a) - 401"""
    _, user_init_data = create_user()
    project = create_project(user_init_data=user_init_data)
    node = create_node(parent_id=project.core_node_id, user_init_data=user_init_data)

    _, user_init_data = client.get_random_user()

    response = client.get_node(
        node_id=node,
        user_init_data=user_init_data,
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


# (2, 2a), (2, 2b)
def test_try_get_root_node_from_nonexistent_user(
    create_user: Callable, create_project: Callable
) -> None:
    """(2, 1a) - 401, (2, 2a) - 401"""
    _, user_init_data = create_user()
    project = create_project(user_init_data=user_init_data)

    _, user_init_data = client.get_random_user()

    response = client.get_node(
        node_id=project.core_node_id,
        user_init_data=user_init_data,
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


# (2, 3)
def test_try_get_nonexistent_node_from_nonexistent_user() -> None:
    """(2, 3) - 401"""
    _, user_init_data = client.get_random_user()
    node_id = "0"

    response = client.get_node(
        node_id=node_id,
        user_init_data=user_init_data,
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


# (3, 1a), (3, 2a)
def test_try_get_node_with_bad_token(
    create_user: Callable, create_project: Callable, create_node: Callable
) -> None:
    """(3, 1a), (3, 2a) - 401"""
    _, user_init_data = create_user()
    project = create_project(user_init_data=user_init_data)
    node_id = create_node(parent_id=project.core_node_id, user_init_data=user_init_data)

    user_init_data = "bad-token"

    response = client.get_node(
        node_id=node_id,
        user_init_data=user_init_data,
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


# (3, 1b), (3, 2b)
def test_try_get_root_node_with_bad_token(
    create_user: Callable, create_project: Callable
) -> None:
    """(3, 1b), (3, 2b) - 401"""
    _, user_init_data = create_user()
    project = create_project(user_init_data=user_init_data)

    user_init_data = "bad-token"

    response = client.get_node(
        node_id=project.core_node_id,
        user_init_data=user_init_data,
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


# (3, 3)
def test_try_get_nonexistent_node_with_bad_token() -> None:
    """(3, 3) - 401"""
    user_init_data = "bad-token"
    node_id = "0"

    response = client.get_node(
        node_id=node_id,
        user_init_data=user_init_data,
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
