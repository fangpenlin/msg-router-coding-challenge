from __future__ import unicode_literals
import re


class Normalizer(object):
    """Normalizer normalizes a given phone number into +1XXXXXXXXXX format and
    return

    """

    removable_pattern = re.compile('[\s()-]')

    def __call__(self, phone_number):
        phone_number = self.removable_pattern.sub('', phone_number)
        if len(phone_number) == 10:
            phone_number = ('+1' + phone_number)
        elif len(phone_number) == 11:
            phone_number = ('+' + phone_number)
        return phone_number
