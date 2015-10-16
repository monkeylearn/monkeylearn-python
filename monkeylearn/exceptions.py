# -*- coding: utf-8 -*-
from __future__ import (
    print_function, unicode_literals, division, absolute_import)


class MonkeyLearnException(Exception):
    def __init__(self, detail):
        super(Exception, self).__init__(
            'Error: ' + detail
        )
