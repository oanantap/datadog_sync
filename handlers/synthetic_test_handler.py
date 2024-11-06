import os
import json
from config.config import (
    SOURCE_SYNTHETIC_VALIDATE_API, SOURCE_URL, DUMP_DIR,
    IMPORT_DUMP_PATH, SOURCE_V1_API_URL, SOURCE_SYNTHETIC_TESTS_DETAIL_API
)
from synthetic_tests.synthetic_test_factory import SyntheticTestFactory
from clients.api_client import APIClient
from utils.file_utils import create_dump_folder


class SyntheticTestHandler:
    def __init__(self, api_key, app_key):
        self.api_key = api_key
        self.app_key = app_key
        self.client = APIClient(api_key, app_key)

    @staticmethod
    def dump(results):
        create_dump_folder()
        with open(IMPORT_DUMP_PATH, 'w') as f:
            json.dump(results, f, indent=4)

    @staticmethod
    def steps_exists(synthetic_test):
        return 'config' in synthetic_test and 'steps' in synthetic_test['config']

    def get_steps_for_synthetic_test(self, synthetic_test):
        if 'public_id' in synthetic_test:
            url = SOURCE_SYNTHETIC_TESTS_DETAIL_API.format(
                SOURCE_V1_API_URL=SOURCE_V1_API_URL,
                public_id=synthetic_test['public_id']
            )
            print(f"Fetching steps for synthetic_test {synthetic_test['public_id']}: {synthetic_test['name']}")
            response = self.client.get(url)
            result = response.json()
            return result.get('steps', [])
        return []

    def extract_steps(self, synthetic_tests):
        for synthetic_test in synthetic_tests:
            if not SyntheticTestHandler.steps_exists(synthetic_test):
                steps = self.get_steps_for_synthetic_test(synthetic_test)
                synthetic_test['config']['steps'] = steps
        return synthetic_tests

    def import_synthetic_tests(self):
        self.client.validate_api(SOURCE_SYNTHETIC_VALIDATE_API)

        synthetic_test = SyntheticTestFactory.create_synthetic_test(self.api_key, self.app_key, type='import')
        try:
            print(f"Importing DD data from source {SOURCE_URL}")
            synthetic_tests = synthetic_test.download().get('tests', [])
            synthetic_tests = self.extract_steps(synthetic_tests)
            SyntheticTestHandler.dump(synthetic_tests)
            print("Import successful")
        except Exception as e:
            print(f"DD failed to import from the source {SOURCE_URL}. Error: {str(e)}")

    @staticmethod
    def already_imported():
        return os.path.exists(IMPORT_DUMP_PATH)
