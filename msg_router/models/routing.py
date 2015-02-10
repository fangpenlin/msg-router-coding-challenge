from __future__ import unicode_literals
import itertools

from netaddr import IPNetwork

from .cashier import Cashier


def round_robin_dispatcher(ip_pool):
    """Dispatch IP address from given IP pool in round robin manner

    """
    return itertools.cycle(ip_pool)


class MessageRouter(object):
    """Message router routes given messages to different disposals with
    minimum requests

    """
    def __init__(self, routing_table, dispatcher=round_robin_dispatcher):
        self.routing_table = routing_table
        # map throughput to cidr, like 5 to 10.0.2.0/24
        self.throughput_to_cidr = dict(self.routing_table)
        # all throughputs in routing table
        self.throughputs = self.throughput_to_cidr.keys()

        # map denomination (throughput) to ip address generators
        self.throughput_to_ip_geneator = {}
        for throughput, cidr in self.throughput_to_cidr.iteritems():
            # the pool of ip addresses in the cidr
            # except broadcasting address, the .0 one
            ip_pool = list(IPNetwork(cidr))[1:]
            if not len(ip_pool):
                raise ValueError(
                    'Invalid CIDR {} has zero host in it'.format(cidr)
                )
            self.throughput_to_ip_geneator[throughput] = dispatcher(ip_pool)

    def __call__(self, message, recipients):
        # use cachier algorithm to solve the problem
        cashier = Cashier(self.throughputs)
        solution = cashier(len(recipients))

        routes = []
        result_throughputs = sorted(solution.keys())
        for throughput in result_throughputs:
            # total count of requests for the throughput (routing)
            req_count = solution[throughput]
            for _ in xrange(req_count):
                gen_ip = self.throughput_to_ip_geneator[throughput]
                ip = str(gen_ip.next())

                routes.append(dict(
                    ip=ip,
                    recipients=recipients[:throughput],
                ))
                recipients = recipients[throughput:]
        return routes
