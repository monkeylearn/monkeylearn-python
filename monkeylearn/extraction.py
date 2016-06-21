# -*- coding: utf-8 -*-
from __future__ import (
    print_function, unicode_literals, division, absolute_import)

from six.moves import range

from monkeylearn.utils import SleepRequestsMixin, MonkeyLearnResponse, HandleErrorsMixin
from monkeylearn.settings import DEFAULT_BASE_ENDPOINT, DEFAULT_BATCH_SIZE

class Extraction(SleepRequestsMixin, HandleErrorsMixin):

    def __init__(self, token, base_endpoint=DEFAULT_BASE_ENDPOINT):
        self.token = token
        self.endpoint = base_endpoint + 'extractors/'

    def extract(self, module_id, text_list, batch_size=DEFAULT_BATCH_SIZE,
                sleep_if_throttled=True):
        text_list = list(text_list)
        self.check_batch_limits(text_list, batch_size)
        url = self.endpoint + module_id + '/extract/'
        res = []
        responses = []
        for i in range(0, len(text_list), batch_size):
            data = {
                'text_list': text_list[i:i+batch_size]
            }
            if kwargs is not None:
                for key, value in kwargs.iteritems():
                    data[key] = value
            response = self.make_request(url, 'POST', data, sleep_if_throttled)
            self.handle_errors(response)
            responses.append(response)
            res.extend(response.json()['result'])

        return MonkeyLearnResponse(res, responses)
