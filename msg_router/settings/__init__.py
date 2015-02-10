from __future__ import unicode_literals
import os

env = os.environ

default_settings = {
    'api.version_header_value': 'msg_router:__version__',
    'api.revision_header_value': 'msg_router:__git_revision__',
    'routing.table': eval(
        env.get(
            'ROUTING_TABLE',
            repr([
                (1, '10.0.1.0/24'),
                (5, '10.0.2.0/24'),
                (10, '10.0.3.0/24'),
                (25, '10.0.4.0/24'),
            ])
        )
    ),
}
