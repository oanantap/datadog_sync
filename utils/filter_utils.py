from config.config import EXCLUDE_TAGS


def filter_sse_tests(tests):
    sse_tag = 'sse'
    return [test for test in tests if 'tags' in test and (sse_tag in test['tags'] or sse_tag.upper() in test['tags'])]


def exclude_tags(tests):
    return [test for test in tests if 'tags' in test and not any(tag in test['tags'] for tag in EXCLUDE_TAGS)]


def remove_excluded_tests(tests):
    tests = exclude_tags(tests)
    return tests


def filter_tests(tests):
    tests = filter_sse_tests(tests)
    tests = remove_excluded_tests(tests)
    return tests
