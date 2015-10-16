# -*- coding: utf-8 -*-
from __future__ import (
    print_function, unicode_literals, division, absolute_import)

from monkeylearn.utils import SleepRequestsMixin, MonkeyLearnResponse, HandleErrorsMixin
from monkeylearn.settings import EXTRACTION_ENDPOINT, DEFAULT_BATCH_SIZE

class Extraction(SleepRequestsMixin, HandleErrorsMixin):

    def __init__(self, token):
        self.token = token
        self.endpoint = EXTRACTION_ENDPOINT

    def extract(self, module_id, text_list, batch_size=DEFAULT_BATCH_SIZE,
                sleep_if_throttled=True):
        text_list = list(text_list)
        self.check_batch_limits(text_list, batch_size)
        url = self.endpoint + module_id + '/extract/'
        res = []
        responses = []
        for i in xrange(0, len(text_list), batch_size):
            data = {
                'text_list': text_list[i:i+batch_size]
            }
            response = self.make_request(url, 'POST', data, sleep_if_throttled)
            self.handle_errors(response)
            responses.append(response)
            res.extend(response.json()['result'])

        return MonkeyLearnResponse(res, responses)
