from __future__ import unicode_literals

from raven import Client
from raven.middleware import Sentry

import msg_router

application = msg_router.main({})

# configure sentry middleware if it's avaiable
if application.registry.settings.get('sentry.dsn'):
    application = Sentry(
        application,
        Client(application.registry.settings['sentry.dsn'])
    )
