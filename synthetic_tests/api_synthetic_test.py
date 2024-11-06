from config.config import SOURCE_SYNTHETIC_TESTS_API
from .synthetic_test import SyntheticTest


class APISyntheticTest(SyntheticTest):

    def download(self):
        url = SOURCE_SYNTHETIC_TESTS_API
        response = self.client.get(url)
        return response.json()
