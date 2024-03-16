from typing import Callable

from fastapi import status

from ..setup import client

"""
### DELETE /nodes/{node_id}

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

- (1, 1a) - 200 - узел удален
- (1, 1b) - 400
- (1, 2a) - 403
- (1, 2b) - 403
- (2, 1a) - 401
- (2, 1b) - 401
- (2, 2a) - 401
- (2, 2b) - 401
- (3, 1a) - 401
- (3, 1b) - 401
- (3, 2a) - 401
- (3, 2b) - 401
- (3, 3) - 401
"""


def test_delete_node(
    create_user: Callable, create_project: Callable, create_node: Callable
) -> None:
    """(1, 1a) - 200 - узел удален"""
    user, user_init_data = create_user()
    project = create_project(user_init_data=user_init_data)

    first_layer = [
        create_node(parent_id=project.core_node_id, user_init_data=user_init_data)
        for i in range(3)
    ]
    second_layer = [
        create_node(parent_id=first_layer[i], user_init_data=user_init_data)
        for i in range(3)
        for j in range(3)
    ]

    response = client.get_node_tree(
        node_id=project.core_node_id,
        user_init_data=user_init_data,
    )

    print(response.json())

    assert response.status_code == status.HTTP_201_CREATED

    # response = client.delete_node(
    #     node_id=node_id,
    #     user_init_data=user_init_data,
    # )

    # assert response.status_code == status.HTTP_200_OK


# (1, 1b)
def test_try_delete_parent_node(
    create_user: Callable, create_project: Callable, create_node: Callable
):
    """(1, 1b) - 400"""
    user, user_init_data = create_user()
    project = create_project(user_init_data=user_init_data)

    response = client.delete_node(
        node_id=project.core_node_id,
        user_init_data=user_init_data,
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


# (1, 2a)
def test_try_delete_another_node(
    create_user: Callable, create_project: Callable, create_node: Callable
):
    """(1, 2a) - 403"""
    _, user_init_data = create_user()
    project = create_project(user_init_data=user_init_data)
    node_id = create_node(parent_id=project.core_node_id, user_init_data=user_init_data)

    _, user_init_data = create_user()

    response = client.delete_node(
        node_id=node_id,
        user_init_data=user_init_data,
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN
