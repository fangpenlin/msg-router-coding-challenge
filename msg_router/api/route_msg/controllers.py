from __future__ import unicode_literals

from netaddr import IPNetwork
from pyramid.view import view_config
from pyramid.view import view_defaults

from ... import models
from ..base import ControllerBase
from .resources import RouteMessageResource


@view_defaults(context=RouteMessageResource, renderer='json')
class RouteMessageController(ControllerBase):

    @view_config(request_method='POST')
    def post(self):
        routing_table = self.settings['routing.table']
        denominations = map(lambda item: item[0], routing_table)
        denomination_to_cidr = dict(routing_table)

        message = self.request.json['message']
        recipients = self.request.json['recipients']
        # TODO: validate recipients

        # use cachier algorithm to solve the problem
        cashier = models.Cashier(denominations)
        solution = cashier(len(recipients))

        routes = []
        result_denominations = sorted(solution.keys())
        for denomination in result_denominations:
            # count of requests for the denomination (routing)
            req_count = solution[denomination]
            for _ in xrange(req_count):
                cidr = denomination_to_cidr[denomination]
                network = IPNetwork(cidr)
                # TODO: use a round-robin manner to get an IP address from the
                # subnet?
                ip = str(network[1])

                routes.append(dict(
                    ip=ip,
                    recipients=recipients[:denomination],
                ))
                recipients = recipients[denomination:]

        return dict(
            message=message,
            routes=routes,
        )
