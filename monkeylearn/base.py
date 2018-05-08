# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals, division, absolute_import

import re
import json
import time

import six
from six.moves.urllib.parse import urlencode
import requests

from monkeylearn.settings import DEFAULT_BASE_URL


class ModuleEndpointSet(object):
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
        url = '{}v3/{}/'.format(self.base_url, self.module_type)
        return self._add_action_or_query_string(url, action, query_string)

    def get_detail_url(self, module_id, action=None, query_string=None):
        url = '{}{}/'.format(self.get_list_url(), module_id)
        return self._add_action_or_query_string(url, action, query_string)

    def get_nested_list_url(self, parent_id, action=None, query_string=None):
        url = '{}v3/{}/{}/{}/'.format(
            self.base_url, self.module_type[0], parent_id, self.module_type[1]
        )
        return self._add_action_or_query_string(url, action, query_string)

    def get_nested_detail_url(self, parent_id, children_id, action=None, query_string=None):
        url = '{}{}/'.format(self.get_nested_list_url(parent_id, action=None), children_id)
        return self._add_action_or_query_string(url, action, query_string)

    def make_request(self, method, url, data=None, sleep_if_throttled=True):
        if data is not None:
            data = json.dumps(data)

        failure_counter = 0
        while True:
            response = requests.request(method, url, data=data, headers={
                'Authorization': 'Token ' + self.token,
                'Content-Type': 'application/json'
            })

            try:
                body = response.json()
            except ValueError:  # No JSON object could be decoded
                failure_counter += 1
                if failure_counter > 3:
                    raise
                else:
                    continue

            if sleep_if_throttled and response.status_code == 429:
                error_code = body['error_code']
                if error_code == 'REQUEST_LIMIT':
                    seconds = re.findall(r'available in (\d+) seconds', body['detail'])[0]
                    time.sleep(int(seconds))
                    continue
                elif error_code == 'REQUEST_CONCURRENCY_LIMIT':
                    time.sleep(2)
                    continue

            return response

    def remove_none_value(self, d):
        return {k: v for k, v in six.iteritems(d) if v is not None}
