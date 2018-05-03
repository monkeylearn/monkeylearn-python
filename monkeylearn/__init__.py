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
        return Classification(token=self.token, base_url=self.base_url)

    @property
    def extractors(self):
        return Extraction(token=self.token, base_url=self.base_url)
