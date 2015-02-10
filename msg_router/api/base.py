from __future__ import unicode_literals


class ResourceBase(object):
    def __init__(self, request, parent=None, name=None, entity=None):
        self.__name__ = name
        self.__parent__ = parent
        self.request = request
        self.entity = entity


class ControllerBase(object):
    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.settings = request.registry.settings
