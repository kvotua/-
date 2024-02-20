from .setup import test_client, USERS, USER
from fastapi import status


user_1 = {"id": "0"}
user_2 = {"id": "1"}
user_3 = {"id": "2"}

user_init_data_1 = f'user={{"id": {user_1["id"]}}}'
user_init_data_2 = f'user={{"id": {user_2["id"]}}}'
user_init_data_3 = f'user={{"id": {user_3["id"]}}}'


class TestUsers:

    # POST /users/
    def test_create_user(self):
        """Test for create new user"""

        response_1 = test_client.post(
            f"{USERS}",
            json=user_1,
        )
        response_2 = test_client.post(
            f"{USERS}",
            json=user_2,
        )

        assert response_1.status_code == 201
        assert response_2.status_code == 201

    def test_try_create_existing_user(self):
        """Test for create existing user"""

        response = test_client.post(
            f"{USERS}",
            json=user_1,
        )

        assert response.status_code == status.HTTP_409_CONFLICT

    # GET /users/{user_id}
    def test_get_user(self):
        """Test for get existing user by id"""
        response = test_client.get(
            USER.format(user_id=user_1["id"]),
            headers={"user-init-data": user_init_data_1},
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"id": "0"}

    def test_try_get_user_with_bad_token(self):
        """Test for get user with bad token"""
        user_init_data = "bad-format"

        response = test_client.get(
            USER.format(user_id=user_1["id"]),
            headers={"user-init-data": user_init_data},
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_try_get_another_user(self):
        """Test for get user from another user"""

        response = test_client.get(
            USER.format(user_id=user_1["id"]),
            headers={"user-init-data": user_init_data_2},
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_try_get_another_nonexistent_user(self):
        """Test for get non-existent user from another user"""
        response = test_client.get(
            USER.format(user_id=user_3["id"]),
            headers={"user-init-data": user_init_data_1},
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_try_get_nonexistent_user(self):
        """Test for get non-existent user"""
        response = test_client.get(
            USER.format(user_id=user_3["id"]),
            headers={"user-init-data": user_init_data_3},
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND
