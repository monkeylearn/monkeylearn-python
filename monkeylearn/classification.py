# -*- coding: utf-8 -*-
from __future__ import (
    print_function, unicode_literals, division, absolute_import)

import six
import warnings
from six.moves import range
try:
    from urllib import urlencode
except:  # For Python 3
    from urllib.parse import urlencode

from monkeylearn.utils import SleepRequestsMixin, MonkeyLearnResponse, HandleErrorsMixin
from monkeylearn.settings import DEFAULT_BASE_ENDPOINT, DEFAULT_BATCH_SIZE
from monkeylearn.exceptions import MonkeyLearnException


class Classification(SleepRequestsMixin, HandleErrorsMixin):

    def __init__(self, token, base_endpoint=DEFAULT_BASE_ENDPOINT):
        self.token = token
        self.endpoint = base_endpoint + 'classifiers/'

    @property
    def categories(self):
        return Categories(self.token, self.endpoint)

    def classify(self, module_id, sample_list=None, sandbox=False,
                 batch_size=DEFAULT_BATCH_SIZE, sleep_if_throttled=True,
                 debug=False, text_list=None, **kwargs):

        if text_list:
            warnings.warn("The text_list parameter will be deprecated in future versions. Please use sample_list.")
            sample_list = text_list

        try:
            sample_list = list(sample_list)
        except TypeError:
            raise MonkeyLearnException('The sample_list can\'t be None.')
        self.check_batch_limits(sample_list, batch_size)

        url = self.endpoint + module_id + '/classify/'
        url_params = {}
        if sandbox:
            url_params['sandbox'] = 1
        if debug:
            url_params['debug'] = 1
        if kwargs is not None:
            for key, value in six.iteritems(kwargs):
                url_params[key] = value
        if url_params:
            url += '?{}'.format(urlencode(url_params))

        res = []
        responses = []
        for i in range(0, len(sample_list), batch_size):
            # if is multi feature
            if isinstance(sample_list[0], dict):
                data = {
                    'sample_list': sample_list[i:i + batch_size]
                }
            else:
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

    def upload_samples(self, module_id, samples_with_categories, sleep_if_throttled=True,
                       features_schema=None):
        url = self.endpoint + module_id + '/samples/'
        samples = []
        for i, s in enumerate(samples_with_categories):
            # if is multi-feature
            if isinstance(s[0], dict):
                sample_dict = {"features": s[0]}
            elif isinstance(s[0], six.string_types):
                sample_dict = {"text": s[0]}
            else:
                raise MonkeyLearnException('The sample must be a text in sample ' + str(i))

            if (isinstance(s[1], int) or
                    (isinstance(s[1], list) and all(isinstance(c, int) for c in s[1]))):
                sample_dict["category_id"] = s[1]
            elif (isinstance(s[1], six.string_types) or
                    (isinstance(s[1], list) and all(isinstance(c, six.string_types) for c in s[1]))):
                sample_dict["category_path"] = s[1]
            elif s[1] is not None:
                raise MonkeyLearnException('Invalid category value in sample ' + str(i))

            if (len(s) > 2 and s[2] and (isinstance(s[2], six.string_types) or
                    (isinstance(s[2], list) and all(isinstance(c, six.string_types) for c in s[2])))):
                sample_dict['tag'] = s[2]

            samples.append(sample_dict)
        data = {
            'samples': samples
        }
        if features_schema:
            data['features_schema'] = features_schema
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

    def detail(self, module_id, category_id, sleep_if_throttled=True):
        url = self.endpoint + module_id + '/categories/' + str(category_id) + '/'
        response = self.make_request(url, 'GET', sleep_if_throttled=sleep_if_throttled)
        self.handle_errors(response)
        return MonkeyLearnResponse(response.json()['result'], [response])

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
