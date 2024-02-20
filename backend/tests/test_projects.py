from .setup import test_client, PROJECTS, PROJECT, PROJECT_BY_USER, USERS
from fastapi import status

user_1 = {"id": "10"}
user_2 = {"id": "11"}
user_3 = {"id": "12"}
user_4 = {"id": "13"}
user_5 = {"id": "14"}
user_6 = {"id": "15"}

name_1 = "project_1"
name_2 = "project_2"
name_3 = "project_3"
name_4 = "project_4"
name_5 = "project_5"
names = [name_1, name_2, name_3, name_4, name_5]

user_init_data_1 = f'user={{"id": {user_1["id"]}}}'
user_init_data_2 = f'user={{"id": {user_2["id"]}}}'
user_init_data_3 = f'user={{"id": {user_3["id"]}}}'
user_init_data_4 = f'user={{"id": {user_4["id"]}}}'
user_init_data_5 = f'user={{"id": {user_5["id"]}}}'
user_init_data_6 = f'user={{"id": {user_6["id"]}}}'


class TestProjects:
    # POST /projects/
    def test_create_project(self):
        """Test for create new project"""

        response_1 = test_client.post(f"{USERS}", json=user_1)
        response_2 = test_client.post(f"{USERS}", json=user_2)
        response_3 = test_client.post(f"{USERS}", json=user_3)
        response_4 = test_client.post(f"{USERS}", json=user_4)
        response_5 = test_client.post(f"{USERS}", json=user_5)

        assert response_1.status_code == 201
        assert response_2.status_code == 201
        assert response_3.status_code == 201
        assert response_4.status_code == 201
        assert response_5.status_code == 201

        response_1 = test_client.post(
            f"{PROJECTS}",
            json={"name": name_1},
            headers={"user-init-data": user_init_data_1},
        )
        response_2 = test_client.post(
            f"{PROJECTS}",
            json={"name": name_2},
            headers={"user-init-data": user_init_data_2},
        )

        assert response_1.status_code == 201
        assert response_2.status_code == 201

    def test_create_project_with_bad_token(self):
        """Test for create project with bad token"""

        user_init_data = "bad-format"

        response = test_client.post(
            f"{PROJECTS}",
            json={"name": name_1},
            headers={"user-init-data": user_init_data},
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_project_for_existent_user(self):
        """Test for create project for existent user"""
        response = test_client.post(
            f"{PROJECTS}",
            json={"name": name_1},
            headers={"user-init-data": user_init_data_6},
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    # GET /projects/by/id/{user_id}
    def test_create_get_project(self):
        """Test for create and get project"""
        response = test_client.post(
            f"{PROJECTS}",
            json={"name": name_3},
            headers={"user-init-data": user_init_data_3},
        )

        assert response.status_code == 201

        response = test_client.get(
            PROJECT_BY_USER.format(user_id=user_3["id"]),
            headers={"user-init-data": user_init_data_3},
        )

        assert response.status_code == 200
        assert len(response.json()) == 1
        assert response.json()[0]["name"] == name_3
        assert response.json()[0]["owner_id"] == user_3["id"]

    def test_create_get_projects(self):
        """Test for create and get projects"""
        responses = []
        responses.append(
            test_client.post(
                f"{PROJECTS}",
                json={"name": name_1},
                headers={"user-init-data": user_init_data_4},
            )
        )
        responses.append(
            test_client.post(
                f"{PROJECTS}",
                json={"name": name_2},
                headers={"user-init-data": user_init_data_4},
            )
        )
        responses.append(
            test_client.post(
                f"{PROJECTS}",
                json={"name": name_3},
                headers={"user-init-data": user_init_data_4},
            )
        )
        responses.append(
            test_client.post(
                f"{PROJECTS}",
                json={"name": name_4},
                headers={"user-init-data": user_init_data_4},
            )
        )
        responses.append(
            test_client.post(
                f"{PROJECTS}",
                json={"name": name_5},
                headers={"user-init-data": user_init_data_4},
            )
        )

        for response in responses:
            assert response.status_code == 201

        response = test_client.get(
            PROJECT_BY_USER.format(user_id=user_4["id"]),
            headers={"user-init-data": user_init_data_4},
        )

        response_list = response.json()
        assert response.status_code == 200
        assert len(response_list) == 5
        for i in range(len(response_list)):
            assert response_list[i]["name"] == names[i]
            assert response_list[i]["owner_id"] == user_4["id"]

    def test_get_projects_empty(self):
        """Test for get projects from user who has no projects"""
        response = test_client.get(
            PROJECT_BY_USER.format(user_id=user_5["id"]),
            headers={"user-init-data": user_init_data_5},
        )

        assert response.status_code == 200
        assert len(response.json()) == 0

    def test_try_get_projects_with_bad_token(self):
        """Test for get projects with bad token"""
        user_init_data = "bad-format"

        response = test_client.get(
            PROJECT_BY_USER.format(user_id=user_1["id"]),
            headers={"user-init-data": user_init_data},
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_try_get_projects_for_another_user(self):
        """Test for get projects for another user"""
        response = test_client.get(
            PROJECT_BY_USER.format(user_id=user_1["id"]),
            headers={"user-init-data": user_init_data_2},
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_try_get_projects_for_existent_user(self):
        """Test for get projects for existent user"""
        response = test_client.get(
            PROJECT_BY_USER.format(user_id=user_6["id"]),
            headers={"user-init-data": user_init_data_6},
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    # DELETE /projects/by/id/{user_id}
    def test_delete_project(self):
        """Test for delete project"""
        response = test_client.get(
            PROJECT_BY_USER.format(user_id=user_3["id"]),
            headers={"user-init-data": user_init_data_3},
        )

        assert response.status_code == status.HTTP_200_OK
        _id = response.json()[0]["id"]

        response = test_client.delete(
            PROJECT.format(project_id=_id),
            headers={"user-init-data": user_init_data_3},
        )

        assert response.status_code == status.HTTP_200_OK

        response = test_client.get(
            PROJECT_BY_USER.format(user_id=user_3["id"]),
            headers={"user-init-data": user_init_data_3},
        )

        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 0

    def test_try_delete_project_with_bad_token(self):
        """Test for delete project with bad token"""
        response = test_client.get(
            PROJECT_BY_USER.format(user_id=user_2["id"]),
            headers={"user-init-data": user_init_data_2},
        )

        assert response.status_code == status.HTTP_200_OK
        _id = response.json()[0]["id"]

        user_init_data = "bad-format"

        response = test_client.get(
            PROJECT.format(project_id=_id),
            headers={"user-init-data": user_init_data},
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_try_delete_nonexistent_project(self):
        """Test for delete nonexistent project"""
        _id = "0"

        response = test_client.delete(
            PROJECT.format(project_id=_id),
            headers={"user-init-data": user_init_data_3},
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_try_delete_another_project(self):
        """Test for delete another project"""
        response = test_client.get(
            PROJECT_BY_USER.format(user_id=user_1["id"]),
            headers={"user-init-data": user_init_data_1},
        )

        assert response.status_code == status.HTTP_200_OK
        _id = response.json()[0]["id"]

        response = test_client.delete(
            PROJECT.format(project_id=_id),
            headers={"user-init-data": user_init_data_2},
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_try_delete_another_project_from_nonexistent_user(self):
        """Test for delete another project from nonexistent user"""
        response = test_client.get(
            PROJECT_BY_USER.format(user_id=user_1["id"]),
            headers={"user-init-data": user_init_data_1},
        )

        assert response.status_code == status.HTTP_200_OK
        _id = response.json()[0]["id"]

        response = test_client.delete(
            PROJECT.format(project_id=_id),
            headers={"user-init-data": user_init_data_6},
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    # PATCH /projects/{project_id}
    def test_update_project(self):
        """Test for update project"""
        response = test_client.get(
            PROJECT_BY_USER.format(user_id=user_1["id"]),
            headers={"user-init-data": user_init_data_1},
        )

        assert response.status_code == status.HTTP_200_OK
        _id = response.json()[0]["id"]

        name = "new name"

        response = test_client.patch(
            PROJECT.format(project_id=_id),
            json={"name": name},
            headers={"user-init-data": user_init_data_1},
        )

        assert response.status_code == status.HTTP_200_OK

        response = test_client.get(
            PROJECT_BY_USER.format(user_id=user_1["id"]),
            headers={"user-init-data": user_init_data_1},
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.json()[0]["name"] == name

    def test_update_project_with_bad_token(self):
        """Test for update project with bad token"""
        response = test_client.get(
            PROJECT_BY_USER.format(user_id=user_1["id"]),
            headers={"user-init-data": user_init_data_1},
        )

        assert response.status_code == status.HTTP_200_OK
        _id = response.json()[0]["id"]

        name = "new name"

        user_init_data = "bad-format"

        response = test_client.patch(
            PROJECT.format(project_id=_id),
            json={"name": name},
            headers={"user-init-data": user_init_data},
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_try_update_another_project(self):
        response = test_client.get(
            PROJECT_BY_USER.format(user_id=user_1["id"]),
            headers={"user-init-data": user_init_data_1},
        )

        assert response.status_code == status.HTTP_200_OK
        _id = response.json()[0]["id"]

        name = "new name"

        response = test_client.patch(
            PROJECT.format(project_id=_id),
            json={"name": name},
            headers={"user-init-data": user_init_data_2},
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_try_update_another_nonexistent_project(self):
        _id = "0"

        name = "new name"

        response = test_client.patch(
            PROJECT.format(project_id=_id),
            json={"name": name},
            headers={"user-init-data": user_init_data_2},
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_try_update_project_from_nonexistent_user(self):
        _id = "0"

        name = "new name"

        response = test_client.patch(
            PROJECT.format(project_id=_id),
            json={"name": name},
            headers={"user-init-data": user_init_data_6},
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    # POST /projects/{project_id}
    def test_create_get_project_by_id(self):
        """Test for create and get project"""
        response = test_client.get(
            PROJECT_BY_USER.format(user_id=user_2["id"]),
            headers={"user-init-data": user_init_data_2},
        )

        assert response.status_code == status.HTTP_200_OK
        _id = response.json()[0]["id"]

        response = test_client.get(
            PROJECT.format(project_id=_id),
            headers={"user-init-data": user_init_data_2},
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {
            "name": name_2,
            "id": _id,
            "owner_id": user_2["id"],
        }

    def test_try_create_get_project_by_id_with_bad_token(self):
        """Test for create and get project with bad token"""
        response = test_client.get(
            PROJECT_BY_USER.format(user_id=user_1["id"]),
            headers={"user-init-data": user_init_data_1},
        )

        assert response.status_code == status.HTTP_200_OK
        _id = response.json()[0]["id"]

        user_init_data = "bad-format"

        response = test_client.get(
            PROJECT.format(project_id=_id),
            headers={"user-init-data": user_init_data},
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_try_get_another_project_by_id(self):
        """Test for get project from another user"""
        response = test_client.get(
            PROJECT_BY_USER.format(user_id=user_2["id"]),
            headers={"user-init-data": user_init_data_2},
        )

        assert response.status_code == status.HTTP_200_OK
        _id = response.json()[0]["id"]

        response = test_client.get(
            PROJECT.format(project_id=_id),
            headers={"user-init-data": user_init_data_1},
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_try_get_nonexistent_project_by_id(self):
        """Test for get nonexistent project from another user"""
        _id = "0"

        response = test_client.get(
            PROJECT.format(project_id=_id),
            headers={"user-init-data": user_init_data_1},
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN
