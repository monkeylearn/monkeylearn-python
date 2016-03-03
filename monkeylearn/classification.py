# -*- coding: utf-8 -*-
from __future__ import (
    print_function, unicode_literals, division, absolute_import)

import six
from six.moves import range

from monkeylearn.utils import SleepRequestsMixin, MonkeyLearnResponse, HandleErrorsMixin
from monkeylearn.settings import DEFAULT_BASE_ENDPOINT, DEFAULT_BATCH_SIZE


class Classification(SleepRequestsMixin, HandleErrorsMixin):

    def __init__(self, token, base_endpoint=DEFAULT_BASE_ENDPOINT):
        self.token = token
        self.endpoint = base_endpoint + 'classifiers/'

    @property
    def categories(self):
        return Categories(self.token, self.endpoint)

    def classify(self, module_id, text_list, sandbox=False,
                 batch_size=DEFAULT_BATCH_SIZE, sleep_if_throttled=True):
        text_list = list(text_list)
        self.check_batch_limits(text_list, batch_size)
        url = self.endpoint + module_id + '/classify/'
        if sandbox:
            url += '?sandbox=1'
        res = []
        responses = []
        for i in range(0, len(text_list), batch_size):
            data = {
                'text_list': text_list[i:i+batch_size]
            }
            response = self.make_request(url, 'POST', data, sleep_if_throttled)
            self.handle_errors(response)
            responses.append(response)
            res.extend(response.json()['result'])

        return MonkeyLearnResponse(res, responses)

    def list(self, sleep_if_throttled=True):
        url = self.endpoint
        response = self.make_request(url, 'GET', sleep_if_throttled=sleep_if_throttled)
        self.handle_errors(response)
        return MonkeyLearnResponse(response.json()['result'], [response])

    def detail(self, module_id, sleep_if_throttled=True):
        url = self.endpoint + module_id
        response = self.make_request(url, 'GET', sleep_if_throttled=sleep_if_throttled)
        self.handle_errors(response)
        return MonkeyLearnResponse(response.json()['result'], [response])

    def upload_samples(self, module_id, samples_with_categories, sleep_if_throttled=True):
        url = self.endpoint + module_id + '/samples/'
        data = {
            'samples': [{"text": s[0], "category_id": s[1]} for s in samples_with_categories]
        }
        response = self.make_request(url, 'POST', data, sleep_if_throttled)
        self.handle_errors(response)
        return MonkeyLearnResponse(response.json()['result'], [response])

    def train(self, module_id, sleep_if_throttled=True):
        url = self.endpoint + module_id + '/train/'
        response = self.make_request(url, 'POST', sleep_if_throttled=sleep_if_throttled)
        self.handle_errors(response)
        return MonkeyLearnResponse(response.json()['result'], [response])

    def deploy(self, module_id, sleep_if_throttled=True):
        url = self.endpoint + module_id + '/deploy/'
        response = self.make_request(url, 'POST', sleep_if_throttled=sleep_if_throttled)
        self.handle_errors(response)
        return MonkeyLearnResponse(response.json()['result'], [response])

    def delete(self, module_id, sleep_if_throttled=True):
        url = self.endpoint + module_id + '/'
        response = self.make_request(url, 'DELETE', sleep_if_throttled=sleep_if_throttled)
        self.handle_errors(response)
        return MonkeyLearnResponse(response.json()['result'], [response])

    def create(self, name, description=None, train_state=None, language=None, ngram_range=None,
               use_stemmer=None, stop_words=None, max_features=None, strip_stopwords=None,
               is_multilabel=None, is_twitter_data=None, normalize_weights=None,
               classifier=None, industry=None, classifier_type=None, text_type=None, permissions=None,
               sleep_if_throttled=True):
        data = {
            "name": name,
            "description": description,
            "train_state": train_state,
            "language": language,
            "ngram_range": ngram_range,
            "use_stemmer": use_stemmer,
            "stop_words": stop_words,
            "max_features": max_features,
            "strip_stopwords": strip_stopwords,
            "is_multilabel": is_multilabel,
            "is_twitter_data": is_twitter_data,
            "normalize_weights": normalize_weights,
            "classifier": classifier,
            "industry": industry,
            "classifier_type": classifier_type,
            "text_type": text_type,
            "permissions": permissions
        }
        data = {key: value for key, value in six.iteritems(data) if value is not None}

        url = self.endpoint
        response = self.make_request(url, 'POST', data, sleep_if_throttled)
        self.handle_errors(response)
        return MonkeyLearnResponse(response.json()['result'], [response])

class Categories(SleepRequestsMixin, HandleErrorsMixin):

    def __init__(self, token, endpoint):
        self.token = token
        self.endpoint = endpoint

    def create(self, module_id, name, parent_id, sleep_if_throttled=True):
        url = self.endpoint + module_id + '/categories/'
        data = {
            'name': name,
            'parent_id': parent_id
        }
        response = self.make_request(url, 'POST', data, sleep_if_throttled)
        self.handle_errors(response)
        return MonkeyLearnResponse(response.json()['result'], [response])

    def edit(self, module_id, category_id, name=None, parent_id=None, sleep_if_throttled=True):
        url = self.endpoint + module_id + '/categories/' + str(category_id) + '/'
        data = {
            'name': name,
            'parent_id': parent_id
        }
        data = {key: value for key, value in six.iteritems(data) if value is not None}
        response = self.make_request(url, 'PATCH', data, sleep_if_throttled)
        self.handle_errors(response)
        return MonkeyLearnResponse(response.json()['result'], [response])

    def delete(self, module_id, category_id, samples_strategy=None, samples_category_id=None,
               sleep_if_throttled=True):
        url = self.endpoint + module_id + '/categories/' + str(category_id) + '/'
        data = {
            'samples-strategy': samples_strategy,
            'samples-category-id': samples_category_id
        }
        data = {key: value for key, value in six.iteritems(data) if value is not None}
        response = self.make_request(url, 'DELETE', data, sleep_if_throttled)
        self.handle_errors(response)
        return MonkeyLearnResponse(response.json()['result'], [response])
