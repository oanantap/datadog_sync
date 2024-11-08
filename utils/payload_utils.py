import json

from config.config import (
    HOST_TO_REPLACE, SSE_GOV_DEV_URL, REPLACE_TAG, TAG_TO_REPLACE,
    REPLACE_ORGS, ORG_TO_REPLACE, WEBEX_WEBHOOK_TO_REPLACE,
    REPLACE_WEBEX_ALERT_SPACE, PAGERDUTY_WEBHOOK_TO_REPLACE,
    REPLACE_PAGERDUTY_WEBHOOK, RUM_APPLICATION_ID, RUM_CLIENT_TOKEN_ID,
    SOURCE_GLOBAL_VARIABLES_DUMP_PATH
)


def update_steps(synthetic_test):
    steps = synthetic_test['config']['steps']
    synthetic_test['steps'] = []
    for step in steps:
        step.pop('public_id', None)
        synthetic_test['steps'].append(step)
    return synthetic_test


def update_variables(synthetic_test):
    with open(SOURCE_GLOBAL_VARIABLES_DUMP_PATH) as file:
        global_variables = json.load(file)
        global_variables = global_variables['variables']

    if 'config' in synthetic_test and 'variables' in synthetic_test['config']:
        for variable in synthetic_test['config']['variables']:
            if 'id' in variable and any(var['name'] == variable['name'] for var in global_variables):
                print("Variable ID {} exists in global_variables.json".format(variable['id']))
                index = synthetic_test['config']['variables'].index(variable)
                global_variable_index = next((i for i, var in enumerate(global_variables) if var['name'] == variable['name']), None)
                if global_variable_index is not None:
                    synthetic_test['config']['variables'][index]['id'] = global_variables[global_variable_index]['id']
                # variable['id'] = variable['id'].replace(variable['id'], global_variables[variable['id']])
    return synthetic_test


def update_tags(synthetic_test):
    if 'tags' in synthetic_test and REPLACE_TAG in synthetic_test['tags']:
        index = synthetic_test['tags'].index(REPLACE_TAG)
        synthetic_test['tags'][index] = TAG_TO_REPLACE
    return synthetic_test


def request_url_exists(synthetic_test):
    return 'config' in synthetic_test and 'request' in synthetic_test['config'] and 'url' in synthetic_test['config']['request']


def update_org_id(synthetic_test):
    for org in REPLACE_ORGS:
        if org in synthetic_test['config']['request']['url']:
            synthetic_test['config']['request']['url'] = synthetic_test['config']['request']['url'].replace(org, ORG_TO_REPLACE)
    return synthetic_test


def update_url(synthetic_test):
    if request_url_exists(synthetic_test):
        synthetic_test['config']['request']['url'] = synthetic_test['config']['request']['url'].replace(HOST_TO_REPLACE, SSE_GOV_DEV_URL)
        synthetic_test = update_org_id(synthetic_test)
    return synthetic_test


def update_locations(synthetic_test):
    if 'locations' in synthetic_test:
        synthetic_test['locations'] = ['aws:us-gov-west-1']
    return synthetic_test


def update_webex_webhook(synthetic_test):
    if 'message' in synthetic_test:
        synthetic_test['message'] = synthetic_test['message'].replace(
            f'{WEBEX_WEBHOOK_TO_REPLACE}', f'{REPLACE_WEBEX_ALERT_SPACE}'
        ).strip()
    return synthetic_test


def update_pagerduty_webhook(synthetic_test):
    if 'message' in synthetic_test:
        synthetic_test['message'] = synthetic_test['message'].replace(
            PAGERDUTY_WEBHOOK_TO_REPLACE, REPLACE_PAGERDUTY_WEBHOOK
        ).strip()
    return synthetic_test


def update_rum_settings(synthetic_test):
    if 'options' in synthetic_test and 'rumSettings' in synthetic_test['options'] \
            and 'applicationId' in synthetic_test['options']['rumSettings']:
        synthetic_test['options']['rumSettings']['applicationId'] \
            = RUM_APPLICATION_ID
        synthetic_test['options']['rumSettings']['clientTokenId'] \
            = RUM_CLIENT_TOKEN_ID
    return synthetic_test


def update_min_location_failed(synthetic_test):
    if 'options' in synthetic_test and 'min_location_failed' in synthetic_test['options']:
        synthetic_test['options']['min_location_failed'] = 1
    return synthetic_test


def update_payload_contexts(test_payload):
    test_payload = update_tags(test_payload)
    test_payload = update_url(test_payload)
    test_payload = update_locations(test_payload)
    test_payload = update_webex_webhook(test_payload)
    test_payload = update_min_location_failed(test_payload)
    test_payload = update_pagerduty_webhook(test_payload)
    test_payload = update_variables(test_payload)
    test_payload = update_rum_settings(test_payload)
    test_payload = update_steps(test_payload)
    return test_payload
