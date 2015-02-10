from __future__ import unicode_literals
import functools

from pyramid.threadlocal import get_current_request
from jsonschema import Draft4Validator

from ..utils import PhoneNumberValidator
from ..exceptions import ExceptionBase


class InvalidJSONSchema(ExceptionBase):
    """Error raised when we encoutnered a JSON schema validation error

    """
    code = 'invalid-json-schema'


class InvalidPhoneNumber(ExceptionBase):
    code = 'invalid-phone-number'


class InvalidJSONBody(ExceptionBase):
    code = 'invalid-json-body'


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


class JSONBodyValidator(object):
    """Validates whether request contains valid JSON body

    """

    def __call__(self, request):
        if request.content_type != 'application/json':
            raise InvalidJSONBody(
                message=(
                    'Invalid Content-Type {!r}, should be application/json'
                    .format(request.content_type)
                ),
            )
        try:
            request.json
        except ValueError:
            raise InvalidJSONBody(
                message='Invalid JSON body {!r}'.format(request.text),
                info=dict(
                    body=request.text,
                ),
            )


class JSONSchemaValidator(object):
    """Validate a given JSON schema and raise an InvalidJSONSchema exception
    if the given json data is not valid

    """

    def __init__(self, schema, retrieve=None):
        self.schema = schema
        self.retrieve = None

    def __call__(self, request):
        if callable(self.retrieve):
            json_data = self.retrieve(request)
        else:
            json_data = request.json

        validator = Draft4Validator(self.schema)
        errors = list(validator.iter_errors(json_data))
        if not errors:
            return
        error_msg = ', '.join(error.message for error in errors)
        error_info = make_error_info(errors)
        raise InvalidJSONSchema(
            message='Invalid JSON schema: {}'.format(error_msg),
            info=error_info,
        )


class PhoneNumbersValidator(object):

    def __init__(self, retrieve):
        self.retrieve = retrieve

    def __call__(self, request):
        """Validate given phone numbers and raise an InvalidPhoneNumber exception
        if there is any invalid phone number found

        """
        phone_numbers = self.retrieve(request)
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


def validate_with(validators):
    """Decorate a given function to be validated with validators

    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Notice: pyramid doesn't like threadlocal stuff, maybe we should
            # find a better way to handle this later?
            request = get_current_request()
            for validator in validators:
                validator(request)
            return func(*args, **kwargs)
        return wrapper
    return decorator
