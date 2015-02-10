from __future__ import unicode_literals

from pyramid.view import view_config
from pyramid.renderers import render_to_response

from ..exceptions import ExceptionBase
from .route_msg.controllers import InvalidPhoneNumber


# default exception HTTP status to use
DEFAULT_EXC_STATUS = 500

# maps exception to HTTP status
EXC_STATUS_MAPPING = {
    InvalidPhoneNumber: 400,
}


@view_config(context=ExceptionBase)
def error_view(exc, request):
    resp = render_to_response('json', exc)
    status = EXC_STATUS_MAPPING.get(type(exc))
    resp.status_code = status
    resp.content_type = 'application/json'
    return resp
