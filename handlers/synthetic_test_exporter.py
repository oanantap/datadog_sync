import os
import sys
import json
from config.config import (
    IMPORT_SYNTHETIC_TESTS_DUMP_PATH, IMPORT_DESTINATION_TESTS_DUMP_PATH,
    DESTINATION_SYNTHETIC_TESTS_API, DESTINATION_URL, DUMP_DIR,
    DESTINATION_SYNTHETIC_TESTS_DETAIL_API, DESTINATION_V1_API_URL
)
from clients.api_client import APIClient
from utils.filter_utils import filter_tests
from utils.payload_utils import update_payload_contexts


create_test_template = {
  "config": {},
  "locations": [],
  "message": "Test message",
  "name": "Example-Synthetic",
  "options": {},
  "tags": [
    "testing:browser"
  ],
  "type": "browser",
  "steps": []
}


class SyntheticTestExporter:
    def __init__(self, api_key, app_key):
        self.api_key = api_key
        self.app_key = app_key
        self.client = APIClient(api_key, app_key, type='export')

        self.source_steps_by_id = {}
        self.existing_steps_by_name = {}
        self.created_tests = {}
        self.created_subtests = {}

        self.dump_dir = DUMP_DIR
        self.import_destination_dump_path = IMPORT_DESTINATION_TESTS_DUMP_PATH

        self.create_dump_folder()
        self.import_created_tests_from_destination()
        self.synthetic_tests_from_source = \
            self.load_synthetic_tests_from_source()
        self.sse_tests = filter_tests(self.synthetic_tests_from_source)

    def create_dump_folder(self):
        if not os.path.exists(self.dump_dir):
            os.makedirs(self.dump_dir)

    def dump(self, results, filename):
        self.create_dump_folder()
        file_path = os.path.join(self.dump_dir, f"{filename}.json")
        with open(file_path, 'w') as f:
            json.dump(results, f, indent=4)

    def steps_exists(self, synthetic_test):
        return 'config' in synthetic_test and 'steps' in synthetic_test['config']

    def _is_substep(self, synthetic_test):
        return 'params' in synthetic_test and 'subtestPublicId' in synthetic_test['params']

    def build_all_steps_by_id(self, synthetic_tests):
        for synthetic_test in synthetic_tests:
            if self.steps_exists(synthetic_test):
                self.source_steps_by_id[synthetic_test['public_id'].strip()] = synthetic_test
                steps = synthetic_test['config']['steps'] or []
                for step in steps:
                    if self._is_substep(step) and step['params']['subtestPublicId'].strip() not in self.source_steps_by_id:
                        self.source_steps_by_id[step['params']['subtestPublicId'].strip()] = step

    def load_synthetic_tests_from_source(self):
        path = IMPORT_SYNTHETIC_TESTS_DUMP_PATH
        try:
            with open(path, 'r') as f:
                data = json.load(f)
                self.build_all_steps_by_id(data)
        except Exception as e:
            print("Failed to load data from file. Error: {}".format(str(e)))
            return None
        return data

    def _get_steps(self, synthetic_test):
        if 'public_id' in synthetic_test:
            url = DESTINATION_SYNTHETIC_TESTS_API.format(
                DESTINATION_URL=DESTINATION_URL,
                public_id=synthetic_test['public_id']
            )
            response = self.client.get(url)
            result = response.json()
            return result.get('steps', [])
        return []

    def _fetch_steps(self, synthetic_test):
        if 'public_id' in synthetic_test:
            url = DESTINATION_SYNTHETIC_TESTS_DETAIL_API.format(
                DESTINATION_V1_API_URL=DESTINATION_V1_API_URL,
                public_id=synthetic_test['public_id']
            )
            response = self.client.get(url).json().get('steps', [])
            return response
            # result = response.json()
            # return result['steps'] if 'steps' in result else []
        return []

    def fetch_all_steps(self, tests):
        for index, synthetic_test in enumerate(tests):
            if synthetic_test['type'] == 'browser':
                print(f"Fetching steps for synthetic_test {synthetic_test['public_id']}: {synthetic_test['name']} ")
                steps = self._fetch_steps(synthetic_test)
                if steps and 'steps' not in synthetic_test:
                    synthetic_test['config']['steps'] = steps
        return tests

    def import_tests_from_destination(self):

        try:
            print(f"importing dd data from destination {DESTINATION_URL}")
            url = DESTINATION_SYNTHETIC_TESTS_API
            response = self.client.get(url)
            tests = response.json()['tests']
            tests = self.fetch_all_steps(tests)
            self.dump(tests, filename='destination_synthetic_tests')
            print("import destination url successful")
        except Exception as e:
            error_message = f"DD failed to import from the destination {DESTINATION_URL}. Error: {str(e)}"
            print(error_message)
            sys.exit(1)

    def _build_existing_substeps_by_name(self, synthetic_test):
        if 'config' in synthetic_test and 'steps' in synthetic_test['config']:
            steps = synthetic_test['config']['steps'] or []
            for step in steps:
                if 'params' in step and 'subtestPublicId' in step['params']:
                    self.existing_steps_by_name[step['name'].strip()] = step

    def _build_existing_steps_by_name(self):
        with open(self.import_destination_dump_path) as f:
            synthetic_tests = json.load(f)
            for synthetic_test in synthetic_tests:
                self.existing_steps_by_name[synthetic_test['name'].strip()] = synthetic_test
                self._build_existing_substeps_by_name(synthetic_test)

    def import_created_tests_from_destination(self):
        if not os.path.exists(IMPORT_DESTINATION_TESTS_DUMP_PATH):
            self.import_tests_from_destination()
        self._build_existing_steps_by_name()
        # for test_name, test in self.existing_steps_by_name.items():
        #     print("Test name: ", test_name)

    def step_not_migrated(self, step):
        return 'params' in step and 'subtestPublicId' in step['params'] \
            and step['name'] not in self.existing_steps_by_name

    def build_post_body(synthetic_test):
        keys = create_test_template.keys()
        body_json = {}
        test_dict_keys = synthetic_test.keys()
        for key in keys:
            if key in test_dict_keys:
                # print("key: ", key, test[key])
                body_json[key] = synthetic_test[key]
        body_json = update_payload_contexts(body_json)
        return body_json

    def update_tests(self, synthetic_test, test_type):
        if test_type == 'subtest':
            self.created_subtests[synthetic_test['name']] = synthetic_test
        else:
            self.created_tests[synthetic_test['name']] = synthetic_test

    def _create(self, synthetic_test, test_type):
        url = DESTINATION_SYNTHETIC_TESTS_API
        try:
            payload = self.build_post_body(synthetic_test)
            response = self.client.post(url, payload)
            new_test = response.json()
            self.update_tests(new_test, test_type)
            if response.status_code != 200:
                raise Exception("Invalid response code: {}. Error: {}".format(response.status_code, response.text))
            print("successfully created the test..", response.text)
        except Exception as e:
            print(f"DD failed to create synthetic tests {DESTINATION_URL}. Error: {str(e)}")

    def export_substeps(self, synthetic_test):
        if 'config' in synthetic_test and 'steps' in synthetic_test['config']:
            steps = synthetic_test['config']['steps'] or []
            for step in steps:
                if self.step_not_migrated(step):
                    step = self.source_steps_by_id[step['params']['subtestPublicId']]
                    print(f"creating sub step name: {step['name']} parent step: {synthetic_test['name']}", )
                    self._create(step, type='subtest')

    def _substeps_exists(self, synthetic_test):
        return 'config' in synthetic_test and 'steps' in synthetic_test['config']

    def _get_substeps(self, synthetic_test):
        if self._substeps_exists(synthetic_test):
            substeps = synthetic_test['config']['steps'] or []
            return substeps
        return []

    def _fetch_substep(self, substep):
        substep_name = substep['name']
        sub_test = None
        if substep_name in self.created_subtests:
            sub_test = self.created_subtests[substep_name]
        elif substep_name in self.existing_steps_by_name:
            sub_test = self.existing_steps_by_name[substep_name]
        return sub_test

    def _update_substep_payload(self, sub_test, synthetic_test):
        substep_payload = {
            "allowFailure": False,
            "isCritical": True,
            "name": synthetic_test['name'],
            "params": {
                "subtestPublicId": sub_test['public_id'],
                "playingTabId": -1
            },
            "type": "refresh"
        }
        synthetic_test['steps'].append(substep_payload)
        return synthetic_test

    def is_sub_test(self, synthetic_test):
        return 'params' in synthetic_test and \
            'subtestPublicId' in synthetic_test['params']

    def create_step(self, synthetic_test):
        # loop through the substeps
        # fetch the substep id from either created_substep or existing_steps_by_name
        # update the body of substep id in the step
        # create the step

        substeps = self._get_substeps(synthetic_test)

        # loop through the substeps
        for substep in substeps:

            # fetch the substep id from either created_substep or existing_steps_by_name
            if self.is_sub_test(substep):
                sub_test = self._fetch_substep(substep)
                if sub_test is not None:
                    synthetic_test = self._update_substep_payload(sub_test, synthetic_test)
            else:
                synthetic_test['steps'].append(substep)

        # create the step
        print("Creating the test..", synthetic_test['name'])
        self._create(synthetic_test, type='test')

    def _init_steps(self, step):
        if 'steps' not in step:
            step['steps'] = []
        return step

    def _export(self, tests):
        for synthetic_test in tests:
            if synthetic_test['type'] == 'browser':
                synthetic_test = self._init_steps(synthetic_test)
                self.export_substeps(synthetic_test)
                self.create_step(synthetic_test)

    def export_synthetic_tests(self):
        self._export(self.sse_tests)
        print("Export successful")
