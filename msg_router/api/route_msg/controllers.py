from __future__ import unicode_literals
import itertools

from jsonschema import validate
from jsonschema import ValidationError
from netaddr import IPNetwork
from pyramid.view import view_config
from pyramid.view import view_defaults

from ... import models
from ...utils import PhoneNumberValidator
from ...exceptions import ExceptionBase
from ..base import ControllerBase
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


class InvalidJSONBody(ExceptionBase):
    code = 'invalid-json-body'


class InvalidJSONSchema(ExceptionBase):
    code = 'invalid-json-schema'


class InvalidPhoneNumber(ExceptionBase):
    code = 'invalid-phone-number'


@view_defaults(context=RouteMessageResource, renderer='json')
class RouteMessageController(ControllerBase):

    phone_number_validator = PhoneNumberValidator()

    @view_config(request_method='POST')
    def post(self):
        routing_table = self.settings['routing.table']
        # map throughput to cidr, like 5 to 10.0.2.0/24
        throughput_to_cidr = dict(routing_table)
        # all throughputs in routing table
        throughputs = throughput_to_cidr.keys()

        # map denomination (throughput) to ip address generators
        throughput_to_ip_geneator = {}
        for throughput, cidr in throughput_to_cidr.iteritems():
            # the pool of ip addresses in the cidr
            # except broadcasting address, the .0 one
            ip_pool = list(IPNetwork(cidr))[1:]
            if not len(ip_pool):
                raise ValueError(
                    'Invalid CIDR {} has zero host in it'.format(cidr)
                )
            throughput_to_ip_geneator[throughput] = itertools.cycle(ip_pool)

        try:
            validate(self.request.json, JSON_SCHEMA)
            message = self.request.json['message']
            recipients = self.request.json['recipients']
        except ValueError:
            raise InvalidJSONBody(
                message='Invalid JSON body {!r}'.format(self.request.text),
                info=dict(
                    body=self.request.text,
                ),
            )
        except ValidationError as exc:
            raise InvalidJSONSchema(
                message='Invalid JSON schema: {}'.format(exc.message),
            )

        bad_recipients = []
        for phone_number in recipients:
            if not self.phone_number_validator(phone_number):
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

        # use cachier algorithm to solve the problem
        cashier = models.Cashier(throughputs)
        solution = cashier(len(recipients))

        routes = []
        result_throughputs = sorted(solution.keys())
        for throughput in result_throughputs:
            # total count of requests for the throughput (routing)
            req_count = solution[throughput]
            for _ in xrange(req_count):
                gen_ip = throughput_to_ip_geneator[throughput]
                ip = str(gen_ip.next())

                routes.append(dict(
                    ip=ip,
                    recipients=recipients[:throughput],
                ))
                recipients = recipients[throughput:]

        return dict(
            message=message,
            routes=routes,
        )
