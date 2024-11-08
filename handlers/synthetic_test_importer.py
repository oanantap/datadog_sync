import os
import json
from config.config import (
    SOURCE_SYNTHETIC_VALIDATE_API, SOURCE_URL, DUMP_DIR,
    IMPORT_SYNTHETIC_TESTS_DUMP_PATH, SOURCE_V1_API_URL,
    SOURCE_SYNTHETIC_TESTS_DETAIL_API
)
from clients.api_client import APIClient
from utils.file_utils import create_dump_folder
from synthetic_tests.synthetic_test_factory import SyntheticTestFactory


class SyntheticTestImporter:
    def __init__(self, api_key, app_key):
        self.api_key = api_key
        self.app_key = app_key
        self.client = APIClient(api_key, app_key, type='import')
        self.imported_tests_dir = DUMP_DIR
        self.create_imported_tests_folder()

    def create_imported_tests_folder(self):
        if not os.path.exists(self.imported_tests_dir):
            os.makedirs(self.imported_tests_dir)

    def dump(self, results, filename):
        self.create_imported_tests_folder()
        file_path = os.path.join(self.imported_tests_dir, f"{filename}.json")
        with open(file_path, 'w') as f:
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
        print("Total Synthetic tests found: ", len(synthetic_tests))
        for synthetic_test in synthetic_tests:
            if not self.steps_exists(synthetic_test):
                steps = self.get_steps_for_synthetic_test(synthetic_test)
                synthetic_test['config']['steps'] = steps
        return synthetic_tests

    def already_imported(self):
        return os.path.exists(IMPORT_SYNTHETIC_TESTS_DUMP_PATH)

    def import_synthetic_tests(self):
        if self.already_imported():
            with open(IMPORT_SYNTHETIC_TESTS_DUMP_PATH, 'r') as f:
                synthetic_tests = json.load(f)
                return synthetic_tests
        else:
            self.client.validate_api(SOURCE_SYNTHETIC_VALIDATE_API)

            synthetic_test = SyntheticTestFactory.create_synthetic_test(
                self.api_key, self.app_key, type='import'
            )
            try:
                print(f"Importing Synthetic tests from the source url {SOURCE_URL}....")
                synthetic_tests = synthetic_test.download().get('tests', [])
                print("Extracting steps for each synthetic test....")
                synthetic_tests = self.extract_steps(synthetic_tests)
                self.dump(synthetic_tests, filename='source_synthetic_tests')
                print("Import successful ans saved file to source_synthetic_tests.json")
            except Exception as e:
                print(f"Datadog failed to import from the source {SOURCE_URL}. Error: {str(e)}")
