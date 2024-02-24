from fastapi import status

from .setup import client


class TestUsers:
    """
    ## Тестирование эндпоинта users

    ### POST /users
    - Правильное создание пользователя \
        `test_create_user`. \
        Должно возвращаться HTTP 201 CREATED

    - Создание существующего пользователя \
        `test_try_create_existing_user`. \
        Должно возвращаться HTTP 409 CONFLICT

    ### GET /users/{user_id}
    - Получение существующего пользователя \
        `test_get_user`. \
        Должно возвращаться HTTP 200 OK

    - Получение пользователя с некорректным токеном (неправильный формат) \
        `test_try_get_user_with_bad_token`. \
        Должно возвращаться HTTP 401 UNAUTHORIZED

    - Получение другого пользователя \
        `test_try_get_another_user`. \
        Должно возвращаться HTTP 403 FORBIDDEN

    - Получение другого несуществующего пользователя \
        `test_try_get_another_nonexistent_user`.
        Должно возвращаться HTTP 403 FORBIDDEN

    - Получение несуществующего пользователя \
        `test_try_get_nonexistent_user`. \
        Должно возвращаться HTTP 404 NOT FOUND
    """

    def create_user(self) -> tuple[dict, str]:
        """
        Метод для быстрого создания пользователя

        Возвращает кортеж: (user ({"id": str}), user_init_data (f"user={{"id": str}}"))
        """
        user, user_init_data = client.get_random_user()

        response = client.create_user(
            user_id=user["id"],
        )
        assert response.status_code == status.HTTP_201_CREATED

        return user, user_init_data

    # POST /users/
    def test_create_user(self):
        user, _ = client.get_random_user()

        response = client.create_user(
            user_id=user["id"],
        )
        assert response.status_code == status.HTTP_201_CREATED

    def test_try_create_existing_user(self):
        user, _ = self.create_user()

        response = client.create_user(
            user_id=user["id"],
        )
        assert response.status_code == status.HTTP_409_CONFLICT

    # GET /users/{user_id}
    def test_get_user(self):
        user, user_init_data = self.create_user()

        response = client.get_user(
            user_id=user["id"],
            user_init_data=user_init_data,
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == user

    def test_try_get_user_with_bad_token(self):
        user, _ = self.create_user()

        response = client.get_user(
            user_id=user["id"],
            user_init_data="bad-format",
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_try_get_another_user(self):
        user, _ = self.create_user()
        _, user_init_data = self.create_user()

        response = client.get_user(
            user_id=user["id"],
            user_init_data=user_init_data,
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_try_get_another_nonexistent_user(self):
        user, _ = client.get_random_user()
        _, user_init_data = self.create_user()

        response = client.get_user(
            user_id=user["id"],
            user_init_data=user_init_data,
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_try_get_nonexistent_user(self):
        user, user_init_data = client.get_random_user()

        response = client.get_user(
            user_id=user["id"],
            user_init_data=user_init_data,
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND
