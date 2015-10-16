# -*- coding: utf-8 -*-
from __future__ import (
    print_function, unicode_literals, division, absolute_import)

from monkeylearn.classification import Classification
from monkeylearn.extraction import Extraction
from monkeylearn.pipelines import Pipelines

class MonkeyLearn(object):

    def __init__(self, token):
        self.token = token

    @property
    def classifiers(self):
        return Classification(self.token)

    @property
    def extractors(self):
        return Extraction(self.token)

    @property
    def pipelines(self):
        return Pipelines(self.token)
