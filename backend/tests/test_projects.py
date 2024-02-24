from fastapi import status

from .setup import client


class TestProjects:
    """
    ## Тестирование эндпоинта projects

    ### POST /projects
    - Правильное создание проекта \
        `test_create_project`. \
        Должно возвращаться HTTP 201 CREATED
    - Создание проекта с некорректным токеном \
        `test_create_project_with_bad_token`. \
        Должно возвращаться HTTP 401 UNAUTHORIZED
    - Создание проекта для несуществующим пользователем \
        `test_create_for_unexistent_user`. \
        Должно возвращаться HTTP 404 NOT FOUND

    ### GET /projects/by/id/{user_id}
    - Создание проекта и получение его \
        `test_create_get_project_by_user`. \
        Должно возвращаться HTTP 200 OK, длина списка 1, \
        у проекта совпадают owner_id с user_id и name
    - Создание нескольких проектов и получение их \
        `test_create_get_projects_by_user`. \
        Должно возвращаться HTTP 200 OK, длина списка 4, \
        у проектов совпадают owner_id с user_id и name
    - Получение проектов у пользователя без проектов \
        `test_get_projects_by_user_for_user_without_projects`. \
        Должно возвращаться HTTP 200 OK, длина списка 0
    - Получение проектов с некорректным токеном \
        `test_try_get_project_by_user_with_bad_token`. \
        Должно возвращаться HTTP 401 UNAUTHORIZED
    - Получение проектов другого пользователя \
        `test_try_get_projects_by_user_for_another_user`. \
        Должно возвращаться HTTP 403 FORBIDDEN
    - Получение проектов для несуществующего пользователя \
        `test_try_get_projects_by_user_for_nonexistent_user`. \
        Должно возвращаться HTTP 404 NOT FOUND

    ### DELETE /projects/{project_id}
    - Удаление проекта от имени владельца \
        `test_delete_project_by_user`. \
        Должно возвращаться HTTP 200 OK, длина списка 0
    - Удаление проекта с некорректным токеном \
        `test_try_delete_project_with_bad_token`. \
        Должно возвращаться HTTP 401 UNAUTHORIZED
    - Удаление несуществующего проекта \
        `test_try_delete_nonexistent_project`. \
        Должно возвращаться HTTP 404 NOT FOUND
    - Удаление проекта другого пользователя \
        `test_try_delete_another_project`. \
        Должно возвращаться HTTP 403 FORBIDDEN
    - Удаление проекта от имени несуществующего пользователя \
        `test_try_delete_another_project_from_nonexistent_user`. \
        Должно возвращаться HTTP 404 NOT FOUND

    ### PATCH /projects/{project_id}
    - Обновление проекта (имя) \
        `test_update_project`. \
        Должно возвращаться HTTP 200 OK, имя совпадает с новым
    - Обновление проекта с некорректным токеном \
        `test_try_update_project_with_bad_token`. \
        Должно возвращаться HTTP 401 UNAUTHORIZED
    - Обновление проекта другого пользователя \
        `test_try_update_another_project`. \
        Должно возвращаться HTTP 403 FORBIDDEN
    - Обновление несуществующего проекта \
        `test_try_update_nonexistent_project`. \
        Должно возвращаться HTTP 403 FORBIDDEN
    - Обновление проекта от имени несуществующего пользователя \
        `test_try_update_project_from_nonexistent_user`. \
        Должно возвращаться HTTP 404 NOT FOUND

    ### POST /projects/{project_id}
    - Получение проекта по его id \
        `test_create_get_project_by_id`. \
        Должно возвращаться HTTP 200 OK, длина списка 1, \
        у проекта совпадают owner_id с user_id и name
    - Получение проекта с некорректным токеном \
        `test_try_get_project_by_id_with_bad_token`. \
        Должно возвращаться HTTP 401 UNAUTHORIZED
    - Получение проекта другого пользователя \
        `test_try_get_another_project_by_id`. \
        Должно возвращаться HTTP 403 FORBIDDEN
    - Получение несуществующего проекта \
        `test_try_get_nonexistent_project_by_id` \
        Должно возвращаться HTTP 403 FORBIDDEN
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

    def create_project(self, user_init_data: str) -> str:
        """
        Метод для быстрого создания проекта

        Возвращает название проекта
        """
        name = client.get_random_project_name()
        response = client.create_project(
            project_name=name,
            user_init_data=user_init_data,
        )

        assert response.status_code == status.HTTP_201_CREATED
        return name

    # POST /projects
    def test_create_project(self):
        _, user_init_data = self.create_user()
        name = client.get_random_project_name()

        response = client.create_project(
            project_name=name,
            user_init_data=user_init_data,
        )

        assert response.status_code == status.HTTP_201_CREATED

    def test_create_project_with_bad_token(self):
        user_init_data = "bad-format"
        name = client.get_random_project_name()

        response = client.create_project(
            project_name=name,
            user_init_data=user_init_data,
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_project_for_unexistent_user(self):
        _, user_init_data = client.get_random_user()
        name = client.get_random_project_name()

        response = client.create_project(
            project_name=name,
            user_init_data=user_init_data,
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    # GET /projects/by/id/{user_id}
    def test_create_get_project_by_user(self):
        user, user_init_data = self.create_user()
        name = self.create_project(user_init_data=user_init_data)

        response = client.get_projects_by_user(
            user_id=user["id"],
            user_init_data=user_init_data,
        )

        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 1
        assert response.json()[0]["name"] == name
        assert response.json()[0]["owner_id"] == user["id"]

    def test_create_get_projects_by_user(self):
        projects_amount = 4
        user, user_init_data = self.create_user()
        projects_names = []

        for _ in range(projects_amount):
            name = self.create_project(user_init_data=user_init_data)
            projects_names.append(name)

        response = client.get_projects_by_user(
            user_id=user["id"],
            user_init_data=user_init_data,
        )

        assert response.status_code == status.HTTP_200_OK
        projects = response.json()
        assert len(projects) == projects_amount
        for i in range(projects_amount):
            # TODO: подумать над порядком возвращаемых проектов
            assert projects[i]["name"] in projects_names[i]
            assert projects[i]["owner_id"] == user["id"]

    def test_get_projects_by_user_for_user_without_projects(self):
        user, user_init_data = self.create_user()

        response = client.get_projects_by_user(
            user_id=user["id"],
            user_init_data=user_init_data,
        )

        assert response.status_code == 200
        assert len(response.json()) == 0

    def test_try_get_projects_by_user_with_bad_token(self):
        user, user_init_data = self.create_user()
        user_init_data = "bad-format"

        response = client.get_projects_by_user(
            user_id=user["id"],
            user_init_data=user_init_data,
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_try_get_projects_by_user_for_another_user(self):
        user, _ = self.create_user()
        _, user_init_data = self.create_user()

        response = client.get_projects_by_user(
            user_id=user["id"],
            user_init_data=user_init_data,
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_try_get_projects_by_user_for_nonexistent_user(self):
        user, user_init_data = client.get_random_user()

        response = client.get_projects_by_user(
            user_id=user["id"],
            user_init_data=user_init_data,
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    # DELETE /projects/by/id/{user_id}
    def test_delete_project(self):
        user, user_init_data = self.create_user()
        _ = self.create_project(user_init_data=user_init_data)

        response = client.get_projects_by_user(
            user_id=user["id"],
            user_init_data=user_init_data,
        )

        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 1

        _id = response.json()[0]["id"]

        response = client.delete_project(
            project_id=_id,
            user_init_data=user_init_data,
        )

        assert response.status_code == status.HTTP_200_OK

        response = client.get_projects_by_user(
            user_id=user["id"],
            user_init_data=user_init_data,
        )

        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 0

    def test_try_delete_project_with_bad_token(self):
        user, user_init_data = self.create_user()
        _ = self.create_project(user_init_data=user_init_data)

        response = client.get_projects_by_user(
            user_id=user["id"],
            user_init_data=user_init_data,
        )

        assert response.status_code == status.HTTP_200_OK
        _id = response.json()[0]["id"]

        user_init_data = "bad-format"

        response = client.delete_project(
            project_id=_id,
            user_init_data=user_init_data,
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_try_delete_nonexistent_project(self):
        _, user_init_data = self.create_user()
        _id = "0"

        response = client.delete_project(
            project_id=_id,
            user_init_data=user_init_data,
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_try_delete_another_project(self):
        user, user_init_data = self.create_user()
        _ = self.create_project(user_init_data=user_init_data)

        response = client.get_projects_by_user(
            user_id=user["id"],
            user_init_data=user_init_data,
        )

        assert response.status_code == status.HTTP_200_OK
        _id = response.json()[0]["id"]
        _, user_init_data = self.create_user()

        response = client.delete_project(
            project_id=_id,
            user_init_data=user_init_data,
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_try_delete_another_project_from_nonexistent_user(self):
        user, user_init_data = self.create_user()
        _ = self.create_project(user_init_data=user_init_data)

        response = client.get_projects_by_user(
            user_id=user["id"],
            user_init_data=user_init_data,
        )

        assert response.status_code == status.HTTP_200_OK
        _id = response.json()[0]["id"]

        _, user_init_data = client.get_random_user()

        response = client.delete_project(
            project_id=_id,
            user_init_data=user_init_data,
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    # PATCH /projects/{project_id}
    def test_update_project(self):
        user, user_init_data = self.create_user()
        _ = self.create_project(user_init_data=user_init_data)

        response = client.get_projects_by_user(
            user_id=user["id"],
            user_init_data=user_init_data,
        )

        assert response.status_code == status.HTTP_200_OK
        _id = response.json()[0]["id"]

        name = "new name"

        response = client.update_project(
            project_id=_id,
            name=name,
            user_init_data=user_init_data,
        )

        assert response.status_code == status.HTTP_200_OK

        response = client.get_projects_by_user(
            user_id=user["id"],
            user_init_data=user_init_data,
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.json()[0]["name"] == name

    def test_try_update_project_with_bad_token(self):
        user, user_init_data = self.create_user()
        _ = self.create_project(user_init_data=user_init_data)

        response = client.get_projects_by_user(
            user_id=user["id"],
            user_init_data=user_init_data,
        )

        assert response.status_code == status.HTTP_200_OK
        _id = response.json()[0]["id"]

        name = "new name"
        user_init_data = "bad-format"

        response = client.update_project(
            project_id=_id,
            name=name,
            user_init_data=user_init_data,
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_try_update_another_project(self):
        user, user_init_data = self.create_user()
        _ = self.create_project(user_init_data=user_init_data)

        response = client.get_projects_by_user(
            user_id=user["id"],
            user_init_data=user_init_data,
        )

        assert response.status_code == status.HTTP_200_OK
        _id = response.json()[0]["id"]

        name = "new name"
        user, user_init_data = self.create_user()

        response = client.update_project(
            project_id=_id,
            name=name,
            user_init_data=user_init_data,
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_try_update_nonexistent_project(self):
        user, user_init_data = self.create_user()
        _id = "0"
        name = "new name"

        response = client.update_project(
            project_id=_id,
            name=name,
            user_init_data=user_init_data,
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_try_update_project_from_nonexistent_user(self):
        _, user_init_data = client.get_random_user()
        _id = "0"

        name = "new name"

        response = client.update_project(
            project_id=_id,
            name=name,
            user_init_data=user_init_data,
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    # POST /projects/{project_id}
    def test_get_project_by_id(self):
        user, user_init_data = self.create_user()
        name = self.create_project(user_init_data=user_init_data)

        response = client.get_projects_by_user(
            user_id=user["id"],
            user_init_data=user_init_data,
        )

        assert response.status_code == status.HTTP_200_OK
        _id = response.json()[0]["id"]

        response = client.get_project_by_id(
            project_id=_id,
            user_init_data=user_init_data,
        )

        assert response.status_code == status.HTTP_200_OK
        json = response.json()
        assert json["name"] == name
        assert json["id"] == _id
        assert json["owner_id"] == user["id"]

    def test_try_get_project_by_id_with_bad_token(self):
        user, user_init_data = self.create_user()
        _ = self.create_project(user_init_data=user_init_data)

        response = client.get_projects_by_user(
            user_id=user["id"],
            user_init_data=user_init_data,
        )

        assert response.status_code == status.HTTP_200_OK
        _id = response.json()[0]["id"]

        user_init_data = "bad-format"

        response = client.get_project_by_id(
            project_id=_id,
            user_init_data=user_init_data,
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_try_get_another_project_by_id(self):
        user, user_init_data = self.create_user()
        _ = self.create_project(user_init_data=user_init_data)

        response = client.get_projects_by_user(
            user_id=user["id"],
            user_init_data=user_init_data,
        )

        assert response.status_code == status.HTTP_200_OK
        _id = response.json()[0]["id"]
        user, user_init_data = self.create_user()

        response = client.get_project_by_id(
            project_id=_id,
            user_init_data=user_init_data,
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_try_get_nonexistent_project_by_id(self):
        user, user_init_data = self.create_user()
        _id = "0"

        response = client.get_project_by_id(
            project_id=_id,
            user_init_data=user_init_data,
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN
