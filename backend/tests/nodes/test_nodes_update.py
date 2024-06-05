from typing import Callable

from fastapi import status

from ..conftest import Node
from ..setup import client

"""
### PATCH /nodes/{node_id}

user-init-data:
1. пользователь существует
2. пользователь не существует
3. неправильный формат

node_id:
1. существует и принадлежит инициатору
    a. находится в том же проекте
    b. находится в другом проекте
2. существует и не принадлежит инициатору
    a. находится в том же проекте
    b. находится в другом проекте
3. не существует

parent_id:
1. существует и принадлежит инициатору
    a. находится в том же проекте
    b. находится в другом проекте
2. существует и не принадлежит инициатору
    a. находится в том же проекте
    b. находится в другом проекте
3. не существует

- (1, 1a, 1a) - 200 - родитель узла поменялся
- (1, 1a, 1b) - 400
- (1, 2a, 2a) - 403
- (1, 2a, 2b) - 403
- (1, 2b, 2b) - 403
- (1, 3, 3) - 404
- (2, 1a, 1a) - 401
- (2, 1a, 1b) - 401
- (2, 1b, 1b) - 401
- (2, 2a, 2a) - 401
- (2, 2a, 2b) - 401
- (2, 2b, 2b) - 401
- (2, 3, 3) - 401
- (3, 1a, 1a) - 401
- (3, 1a, 1b) - 401
- (3, 1b, 1b) - 401
- (3, 2a, 2a) - 401
- (3, 2a, 2b) - 401
- (3, 2b, 2b) - 401
- (3, 3, 3) - 401
"""


# (1, 1a, 1a)
def test_move_node(
    create_user: Callable, create_project: Callable, create_node: Callable
) -> None:
    """(1, 1a, 1a) - 200 - родитель узла поменялся"""
    _, user_init_data = create_user()
    project = create_project(user_init_data=user_init_data)
    node_1 = create_node(user_init_data=user_init_data, parent_id=project.core_node_id)
    node_2 = create_node(user_init_data=user_init_data, parent_id=project.core_node_id)

    subnode = create_node(parent_id=node_1, user_init_data=user_init_data)

    response = client.get_node(
        node_id=subnode,
        user_init_data=user_init_data,
    )

    assert response.status_code == status.HTTP_200_OK
    assert Node.from_dict(response.json()).parent == node_1

    response = client.update_node(
        parent_id=node_2,
        node_id=subnode,
        user_init_data=user_init_data,
    )

    response = client.get_node(
        node_id=subnode,
        user_init_data=user_init_data,
    )

    assert response.status_code == status.HTTP_200_OK
    assert Node.from_dict(response.json()).parent == node_2


# (1, 1a, 1b)
def test_move_node_in_other_project(
    create_user: Callable, create_project: Callable, create_node: Callable
) -> None:
    """(1, 1a, 1b) - 400"""
    _, user_init_data = create_user()
    project = create_project(user_init_data=user_init_data)
    node_1 = create_node(user_init_data=user_init_data, parent_id=project.core_node_id)
    subnode = create_node(parent_id=node_1, user_init_data=user_init_data)

    project = create_project(user_init_data=user_init_data)
    node_2 = create_node(user_init_data=user_init_data, parent_id=project.core_node_id)

    response = client.get_node(
        node_id=subnode,
        user_init_data=user_init_data,
    )

    assert response.status_code == status.HTTP_200_OK
    assert Node.from_dict(response.json()).parent == node_1

    response = client.update_node(
        parent_id=node_2,
        node_id=subnode,
        user_init_data=user_init_data,
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
