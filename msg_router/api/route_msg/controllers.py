from __future__ import unicode_literals
import itertools

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

        message = self.request.json['message']
        recipients = self.request.json['recipients']
        # TODO: validate recipients

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
