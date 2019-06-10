# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals, division, absolute_import

from six.moves import range

from monkeylearn.base import ModelEndpointSet
from monkeylearn.response import MonkeyLearnResponse
from monkeylearn.settings import DEFAULT_BATCH_SIZE
from monkeylearn.validation import validate_batch_size, validate_order_by_param


class Classification(ModelEndpointSet):
    model_type = 'classifiers'

    @property
    def tags(self):
        if not hasattr(self, '_tags'):
            self._tags = Tags(self.token, self.base_url)
        return self._tags

    def list(self, page=None, per_page=None, order_by=None, retry_if_throttled=True):
        if order_by is not None:
            order_by = validate_order_by_param(order_by)
        query_string = self.remove_none_value(dict(
            page=page,
            per_page=per_page,
            order_by=order_by,
        ))
        url = self.get_list_url(query_string=query_string)
        response = self.make_request('GET', url, retry_if_throttled=retry_if_throttled)
        return MonkeyLearnResponse(response)

    def detail(self, model_id, retry_if_throttled=True):
        url = self.get_detail_url(model_id)
        response = self.make_request('GET', url, retry_if_throttled=retry_if_throttled)
        return MonkeyLearnResponse(response)

    def edit(self, model_id, name=None, description=None, algorithm=None, language=None,
             max_features=None, ngram_range=None, use_stemming=None, preprocess_numbers=None,
             preprocess_social_media=None, normalize_weights=None, stopwords=None,
             whitelist=None, retry_if_throttled=True):
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

        url = self.get_detail_url(model_id)
        response = self.make_request('PATCH', url, data, retry_if_throttled=retry_if_throttled)
        return MonkeyLearnResponse(response)

    def deploy(self, model_id, retry_if_throttled=True):
        url = self.get_detail_url(model_id, action='deploy')
        response = self.make_request('POST', url, retry_if_throttled=retry_if_throttled)
        return MonkeyLearnResponse(response)

    def train(self, model_id, retry_if_throttled=True):
        url = self.get_detail_url(model_id, action='train')
        response = self.make_request('POST', url, retry_if_throttled=retry_if_throttled)
        return MonkeyLearnResponse(response)

    def delete(self, model_id, retry_if_throttled=True):
        url = self.get_detail_url(model_id)
        response = self.make_request('DELETE', url, retry_if_throttled=retry_if_throttled)
        return MonkeyLearnResponse(response)

    def create(self, name, description='', algorithm='svc', language='en', max_features=10000,
               ngram_range=(1, 2), use_stemming=True, preprocess_numbers=True,
               preprocess_social_media=False, normalize_weights=True, stopwords=True,
               whitelist=None, retry_if_throttled=True):
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
        response = self.make_request('POST', url, data, retry_if_throttled=retry_if_throttled)
        return MonkeyLearnResponse(response)

    def classify(self, model_id, data, production_model=False, batch_size=DEFAULT_BATCH_SIZE,
                 auto_batch=True, retry_if_throttled=True):
        validate_batch_size(batch_size)

        url = self.get_detail_url(model_id, action='classify')

        response = MonkeyLearnResponse()
        for i in range(0, len(data), batch_size):
            data_dict = self.remove_none_value({
                'data': data[i:i + batch_size],
                'production_model': production_model,
            })
            raw_response = self.make_request('POST', url, data_dict,
                                             retry_if_throttled=retry_if_throttled)
            response.add_raw_response(raw_response)

        return response

    def upload_data(self, model_id, data, input_duplicates_strategy=None,
                    existing_duplicates_strategy=None, retry_if_throttled=True):
        url = self.get_detail_url(model_id, action='data')
        data_dict = {'data': data}
        data_dict = self.remove_none_value({
            'data': data,
            'input_duplicates_strategy': input_duplicates_strategy,
            'existing_duplicates_strategy': existing_duplicates_strategy
        })
        response = self.make_request('POST', url, data_dict, retry_if_throttled=retry_if_throttled)
        return MonkeyLearnResponse(response)


class Tags(ModelEndpointSet):
    model_type = ('classifiers', 'tags')

    def detail(self, model_id, tag_id, retry_if_throttled=True):
        url = self.get_nested_detail_url(model_id, tag_id)
        response = self.make_request('GET', url, retry_if_throttled=retry_if_throttled)
        return MonkeyLearnResponse(response)

    def create(self, model_id, name, parent_id=None, retry_if_throttled=True):
        data = self.remove_none_value({
            'name': name,
            'parent_id': parent_id
        })
        url = self.get_nested_list_url(model_id)
        response = self.make_request('POST', url, data, retry_if_throttled=retry_if_throttled)
        return MonkeyLearnResponse(response)

    def edit(self, model_id, tag_id, name=None, parent_id=None, retry_if_throttled=True):
        data = self.remove_none_value({
            'name': name,
            'parent_id': parent_id
        })
        url = self.get_nested_detail_url(model_id, tag_id)
        response = self.make_request('PATCH', url, data, retry_if_throttled=retry_if_throttled)
        return MonkeyLearnResponse(response)

    def delete(self, model_id, tag_id, move_data_to=None, retry_if_throttled=True):
        data = self.remove_none_value({
            'move_data_to': move_data_to,
        })
        url = self.get_nested_detail_url(model_id, tag_id)
        response = self.make_request('DELETE', url, data, retry_if_throttled=retry_if_throttled)
        return MonkeyLearnResponse(response)
