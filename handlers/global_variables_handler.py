import json
import os
from clients.api_client import APIClient
from config.config import (
    DESTINATION_GLOBAL_VARIABLES_DUMP_PATH, SOURCE_GLOBAL_VARIABLES_DUMP_PATH,
    IMPORT_SYNTHETIC_TESTS_DUMP_PATH
)


class GlobalVariablesHandler:
    def __init__(self, api_key, app_key, source_url, destination_url):
        self.source_url = source_url
        self.destination_url = destination_url
        self.source_client = APIClient(api_key, app_key, type='import')
        self.destination_client = APIClient(api_key, app_key, type='destination')

    def save_global_variables(self, global_variables, type):
        dump_url = DESTINATION_GLOBAL_VARIABLES_DUMP_PATH if type == 'destination' else SOURCE_GLOBAL_VARIABLES_DUMP_PATH
        with open(dump_url, 'w') as f:
            json.dump(global_variables, f, indent=4)

    def downloaded(self, type):
        dump_url = DESTINATION_GLOBAL_VARIABLES_DUMP_PATH if type == 'destination' else SOURCE_GLOBAL_VARIABLES_DUMP_PATH
        return os.path.exists(dump_url)

    def get_downloaded_file_path(self, type):
        return DESTINATION_GLOBAL_VARIABLES_DUMP_PATH if type == 'destination' else SOURCE_GLOBAL_VARIABLES_DUMP_PATH

    def download_global_variables(self, url, type):
        print("Downloading global variables from source...")
        self._download(self.source_url, type='source')

        print("Downloading global variables from destination...")
        self._download(self.destination_url, type='destination')

    def _download(self, url, type):
        client = self.source_client if type == 'source' else self.destination_client
        response = client.get(url)
        if response.status_code == 200:
            global_variables = response.json()
            self.save_global_variables(global_variables, type)
            return global_variables
        else:
            raise Exception(f"Failed to download global variables from {url}")

    def get_global_variables(self, type):
        if self.downloaded(type):
            with open(self.get_downloaded_file_path(type), 'r') as f:
                data = json.load(f)
                return [variable['name'] for variable in data['variables']] if 'variables' in data else data
        else:
            raise Exception(f"Global variables are not initialized. Please run the import command first")

    def load_source_synthetic_tests(self):
        if os.path.exists(IMPORT_SYNTHETIC_TESTS_DUMP_PATH):
            with open(IMPORT_SYNTHETIC_TESTS_DUMP_PATH, 'r') as f:
                return json.load(f)
        raise Exception("Source Synthetic tests does not exists")

    def compare_global_variables(self):

        missing_variables = []
        source_variables = []
        source_synthetic_tests = self.load_source_synthetic_tests()
        for synthetic_test in source_synthetic_tests:
            if 'config' in synthetic_test and 'variables' in synthetic_test['config']:
                source_variables = synthetic_test['config']['variables']
                for source_variable in source_variables:
                    print(source_variable['name'])
                    if source_variable['name'] not in destination_global_variables:
                        missing_variables.append(source_variable)
        return missing_variables

    def create_missing_global_variables(self):
        missing_variables = self.compare_global_variables()
        response = self.destination_client.post(self.destination_url, body=missing_variables)
        if response.status_code != 201:
            raise Exception("Failed to create missing global variables in destination URL")
