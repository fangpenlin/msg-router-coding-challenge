from __future__ import unicode_literals
import os

import pytest
from webtest import TestApp

from ..integration.test_api import routing_cases


@pytest.fixture
def target_url():
    return os.environ.get(
        'TEST_URL',
        'http://127.0.0.1:5678'
    )


@pytest.fixture
def app(target_url):
    testapp = TestApp(target_url)
    return testapp


@pytest.mark.skipif(
    not int(os.environ.get('TEST_ACCEPTANCE', 0)),
    reason='export TEST_ACCEPTANCE=1 to run acceptance'
)
@pytest.mark.parametrize('payload,expected', routing_cases)
def test_api(target_url, app, payload, expected):
    resp = app.post_json('/route-msg', payload)
    assert resp.json == expected
