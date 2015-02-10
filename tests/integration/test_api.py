from __future__ import unicode_literals

import pytest
from webtest import TestApp

from msg_router import main


_routing_case1 = (
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

_routing_case2 = (
    # input
    {
        'message': 'Whatsup',
        'recipients': [
            '+15555555551',
            '+15555555552',
            '+15555555553',
            '+15555555554',
            '+15555555555',
            '+15555555556',
            '+15555555557',
            '+15555555558',
        ],
    },
    # output
    {
        'message': 'Whatsup',
        'routes': [
            {
                'ip': '10.0.1.1',
                'recipients': [
                    '+15555555551',
                ]
            },
            {
                'ip': '10.0.1.2',
                'recipients': [
                    '+15555555552',
                ]
            },
            {
                'ip': '10.0.1.3',
                'recipients': [
                    '+15555555553',
                ]
            },
            {
                'ip': '10.0.2.1',
                'recipients': [
                    '+15555555554',
                    '+15555555555',
                    '+15555555556',
                    '+15555555557',
                    '+15555555558',
                ]
            },
        ],
    }
)

_round_robin_case = (
    # input
    {
        'message': 'YOLO!',
        'recipients': [
            '+15555555551',
            '+15555555552',
            '+15555555553',
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
                    '+15555555551',
                ]
            },
            {
                'ip': '10.0.1.2',
                'recipients': [
                    '+15555555552',
                ]
            },
            {
                'ip': '10.0.1.3',
                'recipients': [
                    '+15555555553',
                ]
            },
            {
                'ip': '10.0.1.1',
                'recipients': [
                    '+15555555554',
                ]
            },
        ],
    }
)

_bad_case = (
    # input
    {
        'message': 'YOLO!',
        'recipients': [
            '+15555555551',
            '+155555555',
            'abcd',
            '123456789',
            '',
        ],
    },
    # output
    {
        'error': {
            'code': 'invalid-phone-number',
            'message': (
                'Invalid phone numbers "+155555555", "abcd", "123456789", ""'
            ),
            'info': {
                'bad_numbers': [
                    '+155555555',
                    'abcd',
                    '123456789',
                    '',
                ],
            },
        },
    }
)


routing_cases = [
    _routing_case1,
    _routing_case2,
]


round_robin_cases = [
    _round_robin_case,
]

bad_number_cases = [
    _bad_case,
]


@pytest.fixture
def app(app_settings=None):
    settings = app_settings or {}
    app = main({}, **settings)
    testapp = TestApp(app)
    return testapp


@pytest.fixture
def small_subnet_app():
    return app({
        'routing.table': [
            # these subnets only have 3 addresses (.0 is excluded)
            (1,  '10.0.1.0/30'),
            (5,  '10.0.2.0/30'),
            (10, '10.0.3.0/30'),
            (25, '10.0.4.0/30'),
        ],
    })


@pytest.fixture
def bad_subnet_app():
    return app({
        'routing.table': [
            (1,  '10.0.1.0/32'),
        ],
    })


@pytest.mark.parametrize('payload,expected', routing_cases)
def test_api(app, payload, expected):
    resp = app.post_json('/route-msg', payload)
    assert resp.json == expected


@pytest.mark.parametrize('payload,expected', round_robin_cases)
def test_ip_round_robin_dispatch(small_subnet_app, payload, expected):
    return test_api(small_subnet_app, payload, expected)


def test_bad_cidr(bad_subnet_app):
    with pytest.raises(ValueError):
        bad_subnet_app.post_json('/route-msg', {
            'message': 'SendHub Rocks',
            'recipients': ['+15555555556'],
        })


@pytest.mark.parametrize('payload,expected', bad_number_cases)
def test_bad_phone_numbers(app, payload, expected):
    resp = app.post_json('/route-msg', payload, status=400)
    assert resp.json == expected
