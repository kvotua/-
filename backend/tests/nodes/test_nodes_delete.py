import random
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


# (1, 1a)
def test_delete_node(
    create_user: Callable, create_project: Callable, create_node: Callable
) -> None:
    """(1, 1a) - 200 - узел удален со всеми дочерними узлами"""
    _, user_init_data = create_user()
    project = create_project(user_init_data=user_init_data)

    amount = 3
    parents = [
        create_node(parent_id=project.core_node_id, user_init_data=user_init_data)
        for i in range(amount)
    ]
    print(f"parents: {parents}")
    childrens = [
        [
            create_node(parent_id=parents[j], user_init_data=user_init_data)
            for i in range(amount)
        ]
        for j in range(amount)
    ]

    tree: dict[str, list[str]] = dict()
    for i in range(amount):
        tree[parents[i]] = []
        for children in childrens[i]:
            tree[parents[i]].append(children)

    random_num = random.randint(0, amount - 1)
    random_node = parents[random_num]
    response = client.delete_node(
        node_id=random_node,
        user_init_data=user_init_data,
    )

    assert response.status_code == status.HTTP_200_OK

    for i in range(amount):
        for children in tree[parents[i]]:
            response = client.get_node(
                node_id=children,
                user_init_data=user_init_data,
            )
            if i == random_num:
                assert response.status_code == status.HTTP_404_NOT_FOUND
            else:
                assert response.status_code == status.HTTP_200_OK


# (1, 1b)
def test_try_delete_root_node(create_user: Callable, create_project: Callable):
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


# (1, 2b)
def test_try_delete_another_root_node(create_user: Callable, create_project: Callable):
    """(1, 2b) - 403"""
    _, user_init_data = create_user()
    project = create_project(user_init_data=user_init_data)

    _, user_init_data = create_user()

    response = client.delete_node(
        node_id=project.core_node_id,
        user_init_data=user_init_data,
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


# (1, 3)
def test_try_delete_nonexistent_node(create_user: Callable):
    """(1, 3) - 404"""
    _, user_init_data = create_user()
    node_id = "0"

    response = client.delete_node(
        node_id=node_id,
        user_init_data=user_init_data,
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


# (2, 1a), (2, 2a)
def test_try_delete_node_from_nonexistent_user(
    create_user: Callable, create_project: Callable, create_node: Callable
):
    """(2, 1a), (2, 2a) - 401"""
    _, user_init_data = create_user()
    project = create_project(user_init_data=user_init_data)
    node_id = create_node(parent_id=project.core_node_id, user_init_data=user_init_data)

    _, user_init_data = client.get_random_user()

    response = client.delete_node(
        node_id=node_id,
        user_init_data=user_init_data,
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


# (2, 1b), (2, 2b)
def test_try_delete_root_node_from_nonexistent_user(
    create_user: Callable, create_project: Callable
):
    """(2, 1b), (2, 2b) - 401"""
    _, user_init_data = create_user()
    project = create_project(user_init_data=user_init_data)

    _, user_init_data = client.get_random_user()

    response = client.delete_node(
        node_id=project.core_node_id,
        user_init_data=user_init_data,
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


# (2, 3)
def test_try_delete_nonexistent_node_from_nonexistent_user():
    """(2, 3) - 401"""
    _, user_init_data = client.get_random_user()
    node_id = "0"

    response = client.delete_node(
        node_id=node_id,
        user_init_data=user_init_data,
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


# (3, 1a), (3, 2a)
def test_try_delete_node_with_bad_token(
    create_user: Callable, create_project: Callable, create_node: Callable
):
    """(3, 1a), (3, 2a) - 401"""
    _, user_init_data = create_user()
    project = create_project(user_init_data=user_init_data)
    node_id = create_node(parent_id=project.core_node_id, user_init_data=user_init_data)

    user_init_data = "bad-token"

    response = client.delete_node(
        node_id=node_id,
        user_init_data=user_init_data,
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


# (3, 1b), (3, 2b)
def test_try_delete_root_node_with_bad_token(
    create_user: Callable, create_project: Callable
):
    """(3, 1b), (3, 2b) - 401"""
    _, user_init_data = create_user()
    project = create_project(user_init_data=user_init_data)

    user_init_data = "bad-token"

    response = client.delete_node(
        node_id=project.core_node_id,
        user_init_data=user_init_data,
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


# (3, 3)
def test_try_delete_nonexistent_node_with_bad_token():
    """(3, 3) - 401"""
    user_init_data = "bad-token"
    node_id = "0"

    response = client.delete_node(
        node_id=node_id,
        user_init_data=user_init_data,
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
