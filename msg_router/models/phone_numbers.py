from __future__ import unicode_literals
import re


class Validator(object):
    """Validator tries to normalize the given phone number, validates it, then
    return the normalized format

    """

    annotation_chars_pattern = re.compile('[\s()-./]')
    phone_number_pattern = re.compile('^(\+)?(1)?[0-9]{10}$')

    def __call__(self, phone_number):
        stripped = self.annotation_chars_pattern.sub('', phone_number)
        return self.phone_number_pattern.match(stripped) is not None
