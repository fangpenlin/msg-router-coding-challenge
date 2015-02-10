from __future__ import unicode_literals

import pytest
from webtest import TestApp

from msg_router import main


_routing_case_1 = (
    # input
    {
        'message': 'SendHub Rocks',
        'recipients': [
            '+15555555556',
            '+15555555555',
            '+15555555554',
            '+15555555553',
            '+15555555552',
            '+15555555551',
        ],
    },
    # output
    {
        'message': 'SendHub Rocks',
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
        ],
    }
)

_routing_case_2 = (
    # input
    {
        'message': 'YOLO!',
        'recipients': [
            '+15555555556',
            '+15555555555',
            '+15555555554',
        ],
    },
    # output
    {
        'message': 'YOLO!',
        'routes': [
            {
                'ip': '10.0.1.1',
                'recipients': [
                    '+15555555556',
                ]
            },
            {
                'ip': '10.0.1.2',
                'recipients': [
                    '+15555555555',
                ]
            },
            {
                'ip': '10.0.1.3',
                'recipients': [
                    '+15555555554',
                ]
            },
        ],
    }
)

routing_cases = [
    _routing_case_1,
    _routing_case_2,
]


@pytest.fixture
def testapp(app_settings=None):
    settings = app_settings or {}
    app = main({}, **settings)
    testapp = TestApp(app)
    return testapp


@pytest.mark.parametrize('payload,expected', routing_cases)
def test_api(testapp, payload, expected):
    resp = testapp.post_json('/route-msg', payload)
    assert resp.json == expected
