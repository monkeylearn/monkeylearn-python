# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals, division, absolute_import

from six.moves import range

from monkeylearn.base import ModelEndpointSet
from monkeylearn.settings import DEFAULT_BATCH_SIZE
from monkeylearn.response import MonkeyLearnResponse
from monkeylearn.validation import validate_batch_size


class Extraction(ModelEndpointSet):
    model_type = 'extractors'

    def list(self, page=1, per_page=20, retry_if_throttled=True):
        url = self.get_list_url(query_string={'page': page, 'per_page': per_page})
        response = self.make_request('GET', url, retry_if_throttled=retry_if_throttled)
        return MonkeyLearnResponse(response)

    def detail(self, model_id, retry_if_throttled=True):
        url = self.get_detail_url(model_id)
        response = self.make_request('GET', url, retry_if_throttled=retry_if_throttled)
        return MonkeyLearnResponse(response)

    def extract(self, model_id, data, production_model=False, batch_size=DEFAULT_BATCH_SIZE,
                retry_if_throttled=True, extra_args=None):
        if extra_args is None:
            extra_args = {}

        validate_batch_size(batch_size)

        url = self.get_detail_url(model_id, action='extract')

        response = MonkeyLearnResponse()
        for i in range(0, len(data), batch_size):
            data_dict = self.remove_none_value({
                'data': data[i:i + batch_size],
                'production_model': production_model,
            })
            data_dict.update(extra_args)
            raw_response = self.make_request('POST', url, data_dict,
                                             retry_if_throttled=retry_if_throttled)
            response.add_raw_response(raw_response)

        return response
