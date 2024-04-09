from moto import mock_aws

from app.main import app

from .api import ClientApi

mock_aws().start()
client = ClientApi(app)
