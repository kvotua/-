from typing import Optional

import httpx
from fastapi import FastAPI
from fastapi.testclient import TestClient


class ApiBase:
    """
    API wrapper for testing endpoints
    """

    API_V1 = "/api/v1"

    USERS = API_V1 + "/users"
    PROJECTS = API_V1 + "/projects"
    NODES = API_V1 + "/nodes"

    USER = USERS + "/{user_id}"
    PROJECT = PROJECTS + "/{project_id}"
    PROJECT_BY_USER = PROJECTS + "/by/user/{user_id}"
    NODE = NODES + "/{node_id}"
    NODE_TREE = NODES + "/tree/{node_id}"

    def __init__(self, app: FastAPI):
        self.client = TestClient(app)

    def post(
        self,
        url: str,
        json: Optional[dict] = None,
        headers: Optional[dict] = None,
    ) -> httpx.Response:
        """
        Sends a POST HTTP request to the specified URL.

        Args:
            url (str): The target URL for the request.
            json (dict, optional): JSON data to include in the request body. \
                Defaults to dict().
            headers (dict, optional): Additional headers to include in the request. \
                Defaults to dict().

        Returns:
            httpx.Response: The response object from the server.
        """

        return self.client.post(
            url=url,
            json=json,
            headers=headers,
        )

    def get(
        self,
        url: str,
        params: Optional[dict] = None,
        headers: Optional[dict] = None,
    ) -> httpx.Response:
        """
        Sends a GET HTTP request to the specified URL.

        Args:
            url (str): The target URL for the request.
            params (dict, optional): Query parameters to include in the request. \
                Defaults to dict().
            headers (dict, optional): Additional headers to include in the request. \
                Defaults to dict().

        Returns:
            httpx.Response: The response object from the server.
        """

        return self.client.get(
            url=url,
            params=params,
            headers=headers,
        )

    def delete(
        self,
        url: str,
        headers: Optional[dict] = None,
    ) -> httpx.Response:
        """
        Sends a DELETE HTTP request to the specified URL.

        Args:
            url (str): The target URL for the request.
            headers (dict, optional): Additional headers to include in the request. \
                Defaults to dict().

        Returns:
            httpx.Response: The response object from the server.
        """
        headers = headers or dict()

        return self.client.delete(
            url=url,
            headers=headers,
        )

    def patch(
        self,
        url: str,
        json: Optional[dict] = None,
        headers: Optional[dict] = None,
    ) -> httpx.Response:
        """
        Sends a PATCH HTTP request to the specified URL.

        Args:
            url (str): The target URL for the request.
            json (dict, optional): JSON data to include in the request body. \
                Defaults to dict().
            headers (dict, optional): Additional headers to include in the request. \
                Defaults to dict().

        Returns:
            httpx.Response: The response object from the server.
        """

        return self.client.patch(
            url=url,
            json=json,
            headers=headers,
        )
