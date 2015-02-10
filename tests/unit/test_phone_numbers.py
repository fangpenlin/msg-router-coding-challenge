from __future__ import unicode_literals

import pytest

from msg_router.models.phone_numbers import Validator


phone_number_validation_cases = [
    ('+15555555556', True),
    ('+1 (555) 5555556', True),
    ('+1 (555) 555-5556', True),
    ('+1(555)5555556', True),
    ('1 5555555556', True),
    ('+1 5555555556', True),
    ('+1 555-555-5556', True),
    ('1 555 555 5556', True),
    ('1-555-555-5556', True),
    ('1234', False),
    ('123456789', False),
    ('aaaaaaaaaa', False),
    ('aaaaaaaaaa1', False),
    ('+0 (555) 5555556', False),
    ('+886 (555) 5555556', False),
    ('+886 912 769 443', False),
]


@pytest.fixture
def validator():
    return Validator()


@pytest.mark.parametrize('value,expected', phone_number_validation_cases)
def test_phone_number_validation(validator, value, expected):
    assert validator(value) == expected
