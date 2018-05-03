# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals, division, absolute_import


class MonkeyLearnException(Exception):
    def __init__(self, detail, error_code=None, status_code=None):
        self.detail = detail
        self.error_code = error_code
        self.status_code = status_code
        message = 'Error'
        if error_code:
            message += ' {}'.format(error_code)
        message += ': {}'.format(detail)
        super(Exception, self).__init__(message)
