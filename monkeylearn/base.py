# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals, division, absolute_import

import re
import json
import time

import six
from six.moves.urllib.parse import urlencode
import requests

from monkeylearn.settings import DEFAULT_BASE_URL


class ModelEndpointSet(object):
    def __init__(self, token, base_url=DEFAULT_BASE_URL):
        self.token = token
        self.base_url = base_url

    def _add_action_or_query_string(self, url, action, query_string):
        if action is not None:
            url += '{}/'.format(action)
        if query_string is not None:
            url += '?' + urlencode(query_string)
        return url

    def get_list_url(self, action=None, query_string=None):
        url = '{}v3/{}/'.format(self.base_url, self.model_type)
        return self._add_action_or_query_string(url, action, query_string)

    def get_detail_url(self, model_id, action=None, query_string=None):
        url = '{}{}/'.format(self.get_list_url(), model_id)
        return self._add_action_or_query_string(url, action, query_string)

    def get_nested_list_url(self, parent_id, action=None, query_string=None):
        url = '{}v3/{}/{}/{}/'.format(
            self.base_url, self.model_type[0], parent_id, self.model_type[1]
        )
        return self._add_action_or_query_string(url, action, query_string)

    def get_nested_detail_url(self, parent_id, children_id, action=None, query_string=None):
        url = '{}{}/'.format(self.get_nested_list_url(parent_id, action=None), children_id)
        return self._add_action_or_query_string(url, action, query_string)

    def make_request(self, method, url, data=None, retry_if_throttled=True):
        if data is not None:
            data = json.dumps(data)

        retries_left = 2
        while retries_left:
            response = requests.request(method, url, data=data, headers={
                'Authorization': 'Token ' + self.token,
                'Content-Type': 'application/json'
            })

            if response.content:
                body = response.json()

            if retry_if_throttled and response.status_code == 429:
                error_code = body.get('error_code')

                wait = None
                if error_code == 'PLAN_RATE_LIMIT':
                    wait = int(re.findall(r'available in (\d+) seconds', body['detail'])[0])
                elif error_code == 'CONCURRENCY_RATE_LIMIT':
                    wait = 2

                if wait:
                    time.sleep(wait)
                    retries_left -= 1
                    continue

            return response

    def remove_none_value(self, d):
        return {k: v for k, v in six.iteritems(d) if v is not None}
