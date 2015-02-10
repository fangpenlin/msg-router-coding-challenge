from __future__ import unicode_literals


class ExceptionBase(Exception):
    """Base exception class for this project

    """

    code = None

    def __init__(self, message, info=None):
        super(ExceptionBase, self).__init__(message)
        self.info = info
