from __future__ import unicode_literals

from pyramid.view import view_config
from pyramid.renderers import render_to_response

from ..exceptions import ExceptionBase
from .validators import InvalidJSONBody
from .validators import InvalidPhoneNumber
from .validators import InvalidJSONSchema


# default exception HTTP status to use
DEFAULT_EXC_STATUS = 500

# maps exception to HTTP status
EXC_STATUS_MAPPING = {
    InvalidPhoneNumber: 400,
    InvalidJSONBody: 400,
    InvalidJSONSchema: 400,
}


@view_config(context=ExceptionBase)
def error_view(exc, request):
    resp = render_to_response('json', exc)
    status = EXC_STATUS_MAPPING.get(type(exc))
    if status is None:
        status = DEFAULT_EXC_STATUS
    resp.status_code = status
    resp.content_type = 'application/json'
    return resp
