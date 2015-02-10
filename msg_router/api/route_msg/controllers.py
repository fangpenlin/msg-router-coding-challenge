from __future__ import unicode_literals

from pyramid.view import view_config
from pyramid.view import view_defaults

from ..base import ControllerBase
from .resources import RouteMessageResource


@view_defaults(context=RouteMessageResource, renderer='json')
class RouteMessageController(ControllerBase):

    @view_config(request_method='POST')
    def post(self):
        return dict()
