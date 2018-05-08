# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals, division, absolute_import

from six.moves import range

from monkeylearn.base import ModuleEndpointSet
from monkeylearn.settings import DEFAULT_BATCH_SIZE
from monkeylearn.response import MonkeyLearnResponse
from monkeylearn.validation import validate_batch_size


class Extraction(ModuleEndpointSet):
    module_type = 'extractors'

    def list(self, page=1, per_page=20, sleep_if_throttled=True):
        url = self.get_list_url(query_string={'page': page, 'per_page': per_page})
        response = self.make_request('GET', url, sleep_if_throttled=sleep_if_throttled)
        return MonkeyLearnResponse(response)

    def detail(self, module_id, sleep_if_throttled=True):
        url = self.get_detail_url(module_id)
        response = self.make_request('GET', url, sleep_if_throttled=sleep_if_throttled)
        return MonkeyLearnResponse(response)

    def extract(self, module_id, data, production_model=None, batch_size=DEFAULT_BATCH_SIZE,
                sleep_if_throttled=True, extra_args=None):
        if extra_args is None:
            extra_args = {}

        validate_batch_size(batch_size)

        url = self.get_detail_url(module_id, action='extract')

        response = MonkeyLearnResponse()
        for i in range(0, len(data['data']), batch_size):
            data_dict = self.remove_none_value({
                'data': data['data'][i:i + batch_size],
                'production_model': production_model,
            })
            data_dict.update(extra_args)
            raw_response = self.make_request('POST', url, data_dict,
                                             sleep_if_throttled=sleep_if_throttled)
            response.add_raw_response(raw_response)

        return response
