from __future__ import unicode_literals

from jsonschema import Draft4Validator

from ..utils import PhoneNumberValidator
from ..exceptions import ExceptionBase


class InvalidJSONSchema(ExceptionBase):
    """Error raised when we encoutnered a JSON schema validation error

    """
    code = 'invalid-json-schema'


class InvalidPhoneNumber(ExceptionBase):
    code = 'invalid-phone-number'


def make_error_info(json_errors):
    """Make error info for given json errors

    """
    error_info = []
    for error in json_errors:
        error_info.append(dict(
            message=error.message,
            path=list(error.path),
            schema_path=list(error.schema_path),
        ))
    return error_info


def validate_json_schema(schema, json_data):
    """Validate a given JSON schema and raise an InvalidJSONSchema exception
    if the given json data is not valid

    """
    validator = Draft4Validator(schema)
    errors = list(validator.iter_errors(json_data))
    if not errors:
        return
    error_msg = ', '.join(error.message for error in errors)
    error_info = make_error_info(errors)
    raise InvalidJSONSchema(
        message='Invalid JSON schema: {}'.format(error_msg),
        info=error_info,
    )


def validate_phone_numbers(phone_numbers):
    """Validate given phone numbers and raise an InvalidPhoneNumber exception
    if there is any invalid phone number found

    """
    phone_number_validator = PhoneNumberValidator()

    bad_recipients = []
    for phone_number in phone_numbers:
        if not phone_number_validator(phone_number):
            bad_recipients.append(phone_number)
    if bad_recipients:
        bad_numbers_str = ', '.join(map(
            lambda num: '"{}"'.format(num),
            bad_recipients
        ))
        msg = 'Invalid phone numbers {}'.format(bad_numbers_str)
        raise InvalidPhoneNumber(
            message=msg,
            info=dict(
                bad_numbers=bad_recipients,
            ),
        )
