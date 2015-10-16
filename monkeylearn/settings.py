# -*- coding: utf-8 -*-
from __future__ import (
    print_function, unicode_literals, division, absolute_import)

DEFAULT_BATCH_SIZE = 200
MAX_BATCH_SIZE = 500
MIN_BATCH_SIZE = 100
BASE_ENDPOINT = 'https://api.monkeylearn.com/v2/'
CLASSIFICATION_ENDPOINT = BASE_ENDPOINT + 'classifiers/'
EXTRACTION_ENDPOINT = BASE_ENDPOINT + 'extractors/'
PIPELINES_ENDPOINT = BASE_ENDPOINT + 'pipelines/'
