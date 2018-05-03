# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals, division, absolute_import

from monkeylearn.settings import MAX_BATCH_SIZE
from monkeylearn.exceptions import MonkeyLearnException


def validate_batch_size(batch_size):
    if batch_size > MAX_BATCH_SIZE:
        raise MonkeyLearnException('batch_size must be less than {0}'.format(MAX_BATCH_SIZE))
