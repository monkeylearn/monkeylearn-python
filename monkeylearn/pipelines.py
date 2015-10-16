# -*- coding: utf-8 -*-
from __future__ import (
    print_function, unicode_literals, division, absolute_import)

from monkeylearn.utils import SleepRequestsMixin, MonkeyLearnResponse, HandleErrorsMixin
from monkeylearn.settings import PIPELINES_ENDPOINT

class Pipelines(SleepRequestsMixin, HandleErrorsMixin):

    def __init__(self, token):
        self.token = token
        self.endpoint = PIPELINES_ENDPOINT

    def run(self, module_id, data, sandbox=False, sleep_if_throttled=True):
        url = self.endpoint + module_id + '/run/'
        if sandbox:
            url += '?sandbox=1'
        response = self.make_request(url, 'POST', data, sleep_if_throttled)
        self.handle_errors(response)

        return MonkeyLearnResponse(response.json()['result'], [response])
