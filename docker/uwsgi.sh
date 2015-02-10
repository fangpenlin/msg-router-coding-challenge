#!/bin/sh

export APP_NAME=msg_router

if [ -z "$NEW_RELIC_CONFIG_FILE" ]; then
    export NEW_RELIC_CONFIG_FILE=/etc/newrelic.ini
fi
if [ -z "$NEW_RELIC_ENVIRONMENT" ]; then
    export NEW_RELIC_ENVIRONMENT=test
fi

# `/sbin/setuser uwsgi` runs the given command as the user `uwsgi`.
# If you omit that part, the command will be run as root.
if [ -z "$UWSGI_ARGS" ]; then
    # use the default uwsgi setting
    export UWSGI_ARGS="--wsgi-file /srv/$APP_NAME/application.py --http=:80 --enable-threads"
fi
if [ "$NO_NEW_RELIC" = true ] ; then
    exec /usr/local/bin/uwsgi $UWSGI_ARGS >> /var/log/uwsgi.log 2>&1
    exit $?;
fi
exec /usr/local/bin/newrelic-admin run-program \
    /usr/local/bin/uwsgi $UWSGI_ARGS >> /var/log/uwsgi.log 2>&1
