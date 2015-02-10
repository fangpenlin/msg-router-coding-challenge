from __future__ import unicode_literals

import pytest
from webtest import TestApp

from msg_router import main


@pytest.fixture
def testapp(app_settings=None):
    settings = app_settings or {}
    app = main({}, **settings)
    testapp = TestApp(app)
    return testapp


def test_api(testapp):
    payload = {
        'message': 'SendHub Rocks',
        'recipients': [
            '+15555555556',
            '+15555555555',
            '+15555555554',
            '+15555555553',
            '+15555555552',
            '+15555555551',
        ]
    }
    resp = testapp.post('/route-msg', payload)
    expected_json = {
        'message': 'SendHubRocks',
        'routes': [
            {
                'ip': '10.0.1.1',
                'recipients': [
                    '+15555555556',
                ]
            },
            {
                'ip': '10.0.2.1',
                'recipients': [
                    '+15555555555',
                    '+15555555554',
                    '+15555555553',
                    '+15555555552',
                    '+15555555551',
                ]
            },
        ]
    }
    assert resp.json == expected_json
