import httpx

from .base import ApiBase


class ApiNodes(ApiBase):

    def create_node(
        self,
        parent_id: str,
        user_init_data: str,
    ) -> httpx.Response:
        url = self.NODES
        json = {"parent": parent_id}
        headers = {"user-init-data": user_init_data}

        return self.post(url=url, json=json, headers=headers)

    def get_node(
        self,
        node_id: str,
        user_init_data: str,
    ) -> httpx.Response:
        url = self.NODE.format(node_id=node_id)
        headers = {"user-init-data": user_init_data}

        return self.get(url=url, headers=headers)

    def update_node(
        self,
        parent_id: str,
        node_id: str,
        user_init_data: str,
    ) -> httpx.Response:
        url = self.NODE.format(node_id=node_id)
        json = {"parent": parent_id}
        headers = {"user-init-data": user_init_data}

        return self.patch(url=url, json=json, headers=headers)

    def delete_node(
        self,
        node_id: str,
        user_init_data: str,
    ) -> httpx.Response:
        url = self.NODE.format(node_id=node_id)
        headers = {"user-init-data": user_init_data}

        return self.delete(url=url, headers=headers)

    def get_node_tree(
        self,
        node_id: str,
        user_init_data: str,
    ) -> httpx.Response:
        url = self.NODE_TREE.format(node_id=node_id)
        headers = {"user-init-data": user_init_data}

        return self.get(url=url, headers=headers)
