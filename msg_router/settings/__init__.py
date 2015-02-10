from __future__ import unicode_literals
import os

env = os.environ

default_settings = {
    'routing.table': eval(
        env.get(
            'ROUTING_TABLE',
            repr([
                (1,  '10.0.1.0/24'),  # noqa
                (5,  '10.0.2.0/24'),  # noqa
                (10, '10.0.3.0/24'),  # noqa
                (25, '10.0.4.0/24'),  # noqa
            ])
        )
    ),
}
