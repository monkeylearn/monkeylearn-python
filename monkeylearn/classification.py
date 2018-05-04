# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals, division, absolute_import

from six.moves import range

from monkeylearn.base import ModuleEndpointSet
from monkeylearn.response import MonkeyLearnResponse
from monkeylearn.settings import DEFAULT_BATCH_SIZE
from monkeylearn.validation import validate_batch_size


class Classification(ModuleEndpointSet):
    module_type = 'classifiers'

    @property
    def categories(self):
        return Categories(self.token, self.base_url)

    def list(self, sleep_if_throttled=True):
        url = self.get_list_url()
        response = self.make_request('GET', url, sleep_if_throttled=sleep_if_throttled)
        return MonkeyLearnResponse(response)

    def detail(self, module_id, sleep_if_throttled=True):
        url = self.get_detail_url(module_id)
        response = self.make_request('GET', url, sleep_if_throttled=sleep_if_throttled)
        return MonkeyLearnResponse(response)

    def edit(self, module_id, name=None, description=None, algorithm=None, language=None,
             max_features=None, ngram_range=None, use_stemming=None, preprocess_numbers=None,
             preprocess_social_media=None, normalize_weights=None, stopwords=None,
             whitelist=None, sleep_if_throttled=True):
        data = self.remove_none_value({
            'name': name,
            'description': description,
            'algorithm': algorithm,
            'language': language,
            'max_features': max_features,
            'ngram_range': ngram_range,
            'use_stemming': use_stemming,
            'preprocess_numbers': preprocess_numbers,
            'preprocess_social_media': preprocess_social_media,
            'normalize_weights': normalize_weights,
            'stopwords': stopwords,
            'whitelist': whitelist,
        })
        url = self.get_detail_url(module_id)
        response = self.make_request('PATCH', url, data, sleep_if_throttled=sleep_if_throttled)
        return MonkeyLearnResponse(response)

    def deploy(self, module_id, sleep_if_throttled=True):
        url = self.get_detail_url(module_id, action='deploy')
        response = self.make_request('POST', url, sleep_if_throttled=sleep_if_throttled)
        return MonkeyLearnResponse(response)

    def delete(self, module_id, sleep_if_throttled=True):
        url = self.get_detail_url(module_id)
        response = self.make_request('DELETE', url, sleep_if_throttled=sleep_if_throttled)
        return MonkeyLearnResponse(response)

    def create(self, name, description=None, algorithm=None, language=None, max_features=None,
               ngram_range=None, use_stemming=None, preprocess_numbers=None,
               preprocess_social_media=None, normalize_weights=None, stopwords=None,
               whitelist=None, sleep_if_throttled=True):
        data = self.remove_none_value({
            'name': name,
            'description': description,
            'algorithm': algorithm,
            'language': language,
            'max_features': max_features,
            'ngram_range': ngram_range,
            'use_stemming': use_stemming,
            'preprocess_numbers': preprocess_numbers,
            'preprocess_social_media': preprocess_social_media,
            'normalize_weights': normalize_weights,
            'stopwords': stopwords,
            'whitelist': whitelist,
        })
        url = self.get_list_url()
        response = self.make_request('POST', url, data, sleep_if_throttled=sleep_if_throttled)
        return MonkeyLearnResponse(response)

    def classify(self, module_id, data, production_model=None, batch_size=DEFAULT_BATCH_SIZE,
                 sleep_if_throttled=True):
        validate_batch_size(batch_size)

        url = self.get_detail_url(module_id, action='classify')

        response = MonkeyLearnResponse()
        for i in range(0, len(data['data']), batch_size):
            data_dict = self.remove_none_value({
                'data': data['data'][i:i + batch_size],
                'production_model': production_model,
            })
            raw_response = self.make_request('POST', url, data_dict,
                                             sleep_if_throttled=sleep_if_throttled)
            response.add_raw_response(raw_response)

        return response

    def upload_data(self, module_id, data, sleep_if_throttled=True):
        url = self.get_detail_url(module_id, action='data')
        data_dict = {'data': data}
        response = self.make_request('POST', url, data_dict, sleep_if_throttled=sleep_if_throttled)
        return MonkeyLearnResponse(response)


class Categories(ModuleEndpointSet):
    module_type = ('classifiers', 'categories')

    def detail(self, module_id, category_id, sleep_if_throttled=True):
        url = self.get_nested_detail_url(module_id, category_id)
        response = self.make_request('GET', url, sleep_if_throttled=sleep_if_throttled)
        return MonkeyLearnResponse(response)

    def create(self, module_id, name, parent_id=None, sleep_if_throttled=True):
        data = self.remove_none_value({
            'name': name,
            'parent_id': parent_id
        })
        url = self.get_nested_list_url(module_id)
        response = self.make_request('POST', url, data, sleep_if_throttled=sleep_if_throttled)
        return MonkeyLearnResponse(response)

    def edit(self, module_id, category_id, name=None, parent_id=None, sleep_if_throttled=True):
        data = self.remove_none_value({
            'name': name,
            'parent_id': parent_id
        })
        url = self.get_nested_detail_url(module_id, category_id)
        response = self.make_request('PATCH', url, data, sleep_if_throttled=sleep_if_throttled)
        return MonkeyLearnResponse(response)

    def delete(self, module_id, category_id, move_data_to=None, sleep_if_throttled=True):
        data = self.remove_none_value({
            'move_data_to': move_data_to,
        })
        url = self.get_nested_detail_url(module_id, category_id)
        response = self.make_request('DELETE', url, data, sleep_if_throttled=sleep_if_throttled)
        return MonkeyLearnResponse(response)
