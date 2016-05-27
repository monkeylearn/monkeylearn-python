# -*- coding: utf-8 -*-
from __future__ import (
    print_function, unicode_literals, division, absolute_import)

import six
from six.moves import range
try:
    from urllib import urlencode
except:  # For Python 3
    from urllib.parse import urlencode

from monkeylearn.utils import SleepRequestsMixin, MonkeyLearnResponse, HandleErrorsMixin
from monkeylearn.settings import DEFAULT_BASE_ENDPOINT, DEFAULT_BATCH_SIZE
from monkeylearn.exceptions import MonkeyLearnException


class Clustering(SleepRequestsMixin, HandleErrorsMixin):

    def __init__(self, token, base_endpoint=DEFAULT_BASE_ENDPOINT):
        self.token = token
        self.endpoint = base_endpoint + 'clusters/'

    def predict(self, module_id, sample_list=None, sandbox=False,
                batch_size=DEFAULT_BATCH_SIZE, sleep_if_throttled=True):
        try:
            sample_list = list(sample_list)
        except TypeError:
            raise MonkeyLearnException('The sample_list can\'t be None.')
        self.check_batch_limits(sample_list, batch_size)

        url = self.endpoint + module_id + '/predict/'
        url_params = {}
        if sandbox:
            url_params['sandbox'] = 1
        if url_params:
            url += '?{}'.format(urlencode(url_params))

        res = []
        responses = []
        for i in range(0, len(sample_list), batch_size):
            data = {
                'text_list': sample_list[i:i + batch_size]
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

    def upload_samples(self, module_id, samples_to_upload, sleep_if_throttled=True):
        url = self.endpoint + module_id + '/samples/'
        samples = []
        for i, s in enumerate(samples_to_upload):
            if isinstance(s[0], six.string_types):
                sample_dict = {"text": s[0]}
            else:
                raise MonkeyLearnException('The sample must be a text in sample ' + str(i))

            if (len(s) > 1 and s[1] and (isinstance(s[1], six.string_types) or
                    (isinstance(s[1], list) and all(isinstance(c, six.string_types) for c in s[1])))):
                sample_dict['tag'] = s[1]

            samples.append(sample_dict)
        data = {
            'samples': samples
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
               is_twitter_data=None, industry=None, text_type=None, permissions=None,
               n_clusters=None, auto_clusters=None, clustering_algorithm=None, sleep_if_throttled=True):
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
            "is_twitter_data": is_twitter_data,
            "industry": industry,
            "text_type": text_type,
            "permissions": permissions,
            "n_clusters": n_clusters,
            "auto_clusters": auto_clusters,
            "clustering_algorithm": clustering_algorithm,
        }
        data = {key: value for key, value in six.iteritems(data) if value is not None}

        url = self.endpoint
        response = self.make_request(url, 'POST', data, sleep_if_throttled)
        self.handle_errors(response)
        return MonkeyLearnResponse(response.json()['result'], [response])
