from clients.api_client import APIClient
from .api_synthetic_test import APISyntheticTest


class SyntheticTestFactory:
    @staticmethod
    def create_synthetic_test(api_key, app_key, type):
        client = APIClient(api_key, app_key, type)
        return APISyntheticTest(client)
