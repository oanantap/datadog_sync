import os

# source configurations
SOURCE_API_URL = 'https://api.datadoghq.com'
SOURCE_URL = 'https://app.datadoghq.com'
SOURCE_V1_API_URL = f'{SOURCE_API_URL}/api/v1'
SOURCE_API_KEY = os.environ.get('SOURCE_API_KEY', '')
SOURCE_APPLICATION_KEY = os.environ.get('SOURCE_APPLICATION_KEY', '')
SOURCE_SYNTHETIC_VALIDATE_API = f'{SOURCE_V1_API_URL}/validate'
SOURCE_SYNTHETIC_TESTS_API = f'{SOURCE_V1_API_URL}/synthetics/tests'
SOURCE_SYNTHETIC_TESTS_DETAIL_API = '{SOURCE_V1_API_URL}/synthetics/tests/browser/{public_id}'


# destination configurations
DESTINATION_URL = 'https://ciscoumbrella-dev-knex.ddog-gov.com'
DESTINATION_V1_API_URL = f'{DESTINATION_URL}/api/v1'
DESTINATION_API_KEY = os.environ.get('DESTINATION_API_KEY', '')
DESTINATION_APPLICATION_KEY = os.environ.get('DESTINATION_APPLICATION_KEY', '')
DESTINATION_SYNTHETIC_VALIDATE_API = f'{DESTINATION_V1_API_URL}/validate'
DESTINATION_SYNTHETIC_TESTS_API = f'{DESTINATION_V1_API_URL}/synthetics/tests'
DESTINATION_SYNTHETIC_TESTS_DETAIL_API = '{DESTINATION_V1_API_URL}/synthetics/tests/browser/{public_id}'


RUM_APPLICATION_ID = os.environ.get('RUM_APPLICATION_ID', '')
RUM_CLIENT_TOKEN_ID = os.environ.get('RUM_CLIENT_TOKEN_ID', '')

DUMP_DIR = 'imported_tests'
IMPORT_SYNTHETIC_TESTS_DUMP_PATH = f'{DUMP_DIR}/source_synthetic_tests.json'
IMPORT_DESTINATION_TESTS_DUMP_PATH = f'{DUMP_DIR}/destination_synthetic_tests.json'
IMPORT_GLOBAL_VARIABLES_DUMP_PATH = f'{DUMP_DIR}/global_variables.json'

EXCLUDE_TESTS = ['App Connectors']
EXCLUDE_TAGS = ['env:service:mgmt-api-v2', 'env:service:up-api']

SSE_GOV_DEV_URL = 'https://dashboard.dev.secureaccessfed.cisco'
REPLACE_ORGS = ['8068522', '8157452']
REPLACE_TAG = 'env:PROD'
REPLACE_PAGERDUTY_WEBHOOK = ''
REPLACE_WEBEX_ALERT_SPACE = 'WEBEX_ALERT_SPACE'

TAG_TO_REPLACE = 'env:GOVDEV'
HOST_TO_REPLACE = 'https://dashboard.sse.cisco.com'
ORG_TO_REPLACE = '8068522'
WEBEX_WEBHOOK_TO_REPLACE = '@webhook-KNEX_Alerts_Room'
PAGERDUTY_WEBHOOK_TO_REPLACE = '@pagerduty-CDFW_services_-_frontend'
GLOBAL_VARIABLES_REPLACES_DICT = {
    'KNEX_UMBRELLA_CHROME_US_WEST_MFA': os.environ.get('KNEX_UMBRELLA_CHROME_US_WEST_MFA', ''),
    'KNEX_UMBRELLA_CHROME_US_WEST_USERNAME': os.environ.get('KNEX_UMBRELLA_CHROME_US_WEST_USERNAME', ''),
    'KNEX_SSE_CHROME_US_WEST_PASSWORD': os.environ.get('KNEX_SSE_CHROME_US_WEST_PASSWORD', ''),
    'KNEX_SSE_CHROME_US_WEST_MFA': '',
    'KNEX_SSE_CHROME_US_WEST_USERNAME': ''
}

SYNTHETIC_TEST_URL_MAP = {
    'browser': '{SOURCE_V1_API_URL}/synthetics/browser/tests/{public_id}'
}
