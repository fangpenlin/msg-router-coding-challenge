#!/usr/bin/python
from __future__ import unicode_literals
import os
import json
import urlparse
import itertools

from tests.integration.test_api import routing_cases
from tests.integration.test_api import round_robin_cases
from tests.integration.test_api import bad_number_cases
from tests.integration.test_api import invalid_json_schema_cases


def main():
    target_url = os.environ.get('TEST_URL', 'http://127.0.0.1:5678')
    for payload, _ in itertools.chain(
        routing_cases,
        round_robin_cases,
        bad_number_cases,
        invalid_json_schema_cases,
    ):
        abs_url = urlparse.urljoin(target_url, '/route-msg')
        print (
            "curl -X POST -v -H 'Content-Type: application/json' "
            "-d '{}' {}"
            .format(json.dumps(payload), abs_url)
        )

if __name__ == '__main__':
    main()
