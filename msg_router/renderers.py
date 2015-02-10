from __future__ import unicode_literals

from pyramid.renderers import JSON
from pyramid.settings import asbool


def includeme(config):
    settings = config.registry.settings
    kwargs = {}
    cfg_key = 'api.json.pretty_print'
    pretty_print = asbool(settings.get(cfg_key, True))
    if pretty_print:
        kwargs = dict(sort_keys=True, indent=4, separators=(',', ': '))

    json_renderer = JSON(**kwargs)
    config.add_renderer('json', json_renderer)
