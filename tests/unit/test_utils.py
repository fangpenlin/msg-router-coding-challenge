from __future__ import unicode_literals

import pytest

from msg_router.utils import PhoneNumberValidator


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
def phone_number_validator():
    return PhoneNumberValidator()


@pytest.mark.parametrize('value,expected', phone_number_validation_cases)
def test_phone_number_validation(phone_number_validator, value, expected):
    assert phone_number_validator(value) == expected
