import httpx

from .base import ApiBase


class ApiTemplates(ApiBase):

    def create_template(
        self,
        node_id: str,
        user_init_data: str,
    ) -> httpx.Response:

        url = self.TEMPLATES
        headers = {"user-init-data": user_init_data}
        json = {"node_id": node_id}

        return self.post(url=url, json=json, headers=headers)

    def get_templates(
        self,
        user_init_data: str,
    ) -> httpx.Response:

        url = self.TEMPLATES
        headers = {"user-init-data": user_init_data}

        return self.get(url=url, headers=headers)

    def get_template(
        self,
        template_id: str,
        user_init_data: str,
    ) -> httpx.Response:

        url = self.TEMPLATE.format(template_id=template_id)
        headers = {"user-init-data": user_init_data}

        return self.get(url=url, headers=headers)
