from __future__ import unicode_literals

import pytest

from msg_router.models.phone_numbers import Normalizer


phone_number_normalizing_cases = [
    ('+15555555556', '+15555555556'),
    ('+1 (555) 5555556', '+15555555556'),
    ('+1 (555) 555-5556', '+15555555556'),
    ('+1(555)5555556', '+15555555556'),
    ('1 5555555556', '+15555555556'),
    ('+1 5555555556', '+15555555556'),
    ('+1 555-555-5556', '+15555555556'),
    ('1 555 555 5556', '+15555555556'),
    ('1-555-555-5556', '+15555555556'),
]


@pytest.fixture
def normalizer():
    return Normalizer()


@pytest.mark.parametrize('value,expected', phone_number_normalizing_cases)
def test_phone_number_normalizing(normalizer, value, expected):
    assert normalizer(value) == expected
