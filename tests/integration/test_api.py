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

invalid_json_schema_cases = [
    (
        {},
        'is a required property',
    ),
    (
        {'message': ''},
        'is a required property',
    ),
    (
        {'message': '', 'recipients': []},
        'is too short',
    ),
    (
        {'message': '', 'recipients': ['a', 'a']},
        'has non-unique elements',
    ),
    (
        {'message': '', 'recipients': ['a', 'a', 123]},
        (
            'has non-unique elements',
            "123 is not of type u'string'",
        ),
    ),
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


@pytest.mark.parametrize('payload', [
    '',
    'foobar',
    "{'bad_json': True}",
])
def test_invalid_json_body(app, payload):
    resp = app.post(
        '/route-msg',
        payload,
        headers={b'Content-Type': b'application/json'},
        status=400,
    )
    assert 'Invalid JSON body' in resp.text


def test_invalid_content_type(app):
    resp = app.post(
        '/route-msg',
        '',
        status=400,
    )
    assert 'Invalid Content-Type' in resp.text


@pytest.mark.parametrize('payload,expected_msg', invalid_json_schema_cases)
def test_invalid_json_schema(app, payload, expected_msg):
    resp = app.post_json('/route-msg', payload, status=400)
    body = resp.text
    assert 'Invalid JSON schema' in body
    if isinstance(expected_msg, tuple):
        for msg in expected_msg:
            assert msg in body
    else:
        assert expected_msg in body
    for error in resp.json['error']['info']:
        assert error['message'] in body
