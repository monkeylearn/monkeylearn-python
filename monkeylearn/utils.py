# -*- coding: utf-8 -*-
from __future__ import (
    print_function, unicode_literals, division, absolute_import)

import requests
import json
import time
import re
import six

from monkeylearn.settings import (MAX_BATCH_SIZE, MIN_BATCH_SIZE)
from monkeylearn.exceptions import MonkeyLearnException

class MonkeyLearnResponse(object):
    def __init__(self, result, responses):
        self.result = result
        self.query_limit_remaining = responses[-1].headers['X-Query-Limit-Remaining']
        self.raw_responses = responses


class SleepRequestsMixin(object):
    def make_request(self, url, method, data=None, sleep_if_throttled=True):
        while True:
            if data:
                response = requests.request(
                    method,
                    url,
                    data=json.dumps(data),
                    headers={
                        'Authorization': 'Token ' + self.token,
                        'Content-Type': 'application/json'
                    }
                )
            else:
                response = requests.request(
                    method,
                    url,
                    headers={
                        'Authorization': 'Token ' + self.token,
                        'Content-Type': 'application/json'
                    }
                )

            response_json = response.json()
            if sleep_if_throttled and response.status_code == 429 and 'seconds' in response_json['detail']:
                seconds = re.findall(r'available in (\d+) seconds', response_json['detail'])[0]
                time.sleep(int(seconds))
                continue
            elif (sleep_if_throttled and response.status_code == 429 and
                    'Too many concurrent requests' in response_json['detail']):
                time.sleep(2)
                continue
            return response


class HandleErrorsMixin(object):
    def check_batch_limits(self, text_list, batch_size):
        if batch_size > MAX_BATCH_SIZE or batch_size < MIN_BATCH_SIZE:
            raise MonkeyLearnException('batch_size has to be between {0} and {1}'.format(
                                       MIN_BATCH_SIZE, MAX_BATCH_SIZE))
        if not text_list:
            raise MonkeyLearnException('The text_list can\'t be empty.')

        # if is multi feature
        if isinstance(text_list[0], dict):
            if {} in text_list:
                raise MonkeyLearnException('You have an empty sample in position {0} in sample_list'.format(
                                           text_list.index({})))
            for i, sample in enumerate(text_list):
                if not isinstance(sample, dict):
                    raise MonkeyLearnException(
                        'Element in position {0} in sample_list must be a dict.'.format(i)
                    )

        # if is single feature
        else:
            if '' in text_list:
                raise MonkeyLearnException('You have an empty text in position {0} in text_list'.format(
                                           text_list.index('')))
            for i, text in enumerate(text_list):
                if not isinstance(text, six.string_types):
                    raise MonkeyLearnException(
                        'Element in position {0} in text_list must be a string.'.format(i)
                    )

    def handle_errors(self, response):
        if not response.ok:
            try:
                res = response.json()
            except ValueError:
                response.raise_for_status()
            raise MonkeyLearnException(json.dumps(res['detail']))
