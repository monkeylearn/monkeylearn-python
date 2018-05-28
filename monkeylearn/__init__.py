# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals, division, absolute_import

from monkeylearn.settings import DEFAULT_BASE_URL
from monkeylearn.classification import Classification
from monkeylearn.extraction import Extraction


class MonkeyLearn(object):
    def __init__(self, token, base_url=DEFAULT_BASE_URL):
        self.token = token
        self.base_url = base_url

    @property
    def classifiers(self):
        if not hasattr(self, '_classifiers'):
            self._classifiers = Classification(token=self.token, base_url=self.base_url)
        return self._classifiers

    @property
    def extractors(self):
        if not hasattr(self, '_extractors'):
            self._extractors = Extraction(token=self.token, base_url=self.base_url)
        return self._extractors
