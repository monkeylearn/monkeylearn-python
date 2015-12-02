# -*- coding: utf-8 -*-
from __future__ import (
    print_function, unicode_literals, division, absolute_import)

from monkeylearn.settings import DEFAULT_BASE_ENDPOINT
from monkeylearn.classification import Classification
from monkeylearn.extraction import Extraction
from monkeylearn.pipelines import Pipelines

class MonkeyLearn(object):

    def __init__(self, token, base_endpoint=DEFAULT_BASE_ENDPOINT):
        self.token = token
        self.base_endpoint = base_endpoint

    @property
    def classifiers(self):
        return Classification(token=self.token,
                              base_endpoint=self.base_endpoint)

    @property
    def extractors(self):
        return Extraction(token=self.token,
                          base_endpoint=self.base_endpoint)

    @property
    def pipelines(self):
        return Pipelines(token=self.token,
                         base_endpoint=self.base_endpoint)
