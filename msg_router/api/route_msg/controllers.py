from __future__ import unicode_literals

from pyramid.view import view_config
from pyramid.view import view_defaults

from ... import models
from ..base import ControllerBase
from ..validators import validate_with
from ..validators import JSONBodyValidator
from ..validators import JSONSchemaValidator
from ..validators import PhoneNumbersValidator
from .resources import RouteMessageResource


JSON_SCHEMA = {
    'title': 'SendHub Challenge Schema',
    'type': 'object',
    'properties': {
        'message': {
            'type': 'string',
        },
        'recipients': {
            'type': 'array',
            'minItems': 1,
            'items': {
                'type': 'string',
            },
            'uniqueItems': True,
        }
    },
    'required': [
        'message',
        'recipients',
    ]
}


@view_defaults(context=RouteMessageResource, renderer='json')
class RouteMessageController(ControllerBase):

    @view_config(request_method='POST')
    @validate_with([
        JSONBodyValidator(),
        JSONSchemaValidator(JSON_SCHEMA),
        PhoneNumbersValidator(lambda request: request.json['recipients']),
    ])
    def post(self):
        routing_table = self.settings['routing.table']
        message = self.request.json['message']
        recipients = self.request.json['recipients']

        router = models.MessageRouter(routing_table)
        routes = router(message=message, recipients=recipients)
        return dict(
            message=message,
            routes=routes,
        )
