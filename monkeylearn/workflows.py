# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals, division, absolute_import

from monkeylearn.base import ModelEndpointSet
from monkeylearn.response import MonkeyLearnResponse


class Workflows(ModelEndpointSet):
    model_type = 'workflows'

    @property
    def steps(self):
        if not hasattr(self, '_steps'):
            self._steps = WorkflowSteps(self.token, self.base_url)
        return self._steps

    @property
    def data(self):
        if not hasattr(self, '_data'):
            self._data = WorkflowData(self.token, self.base_url)
        return self._data

    @property
    def custom_fields(self):
        if not hasattr(self, '_custom_fields'):
            self._custom_fields = WorkflowCustomFields(self.token, self.base_url)
        return self._custom_fields

    def create(self, name, db_name, steps, description='', webhook_url=None, custom_fields=None,
               sources=None, retry_if_throttled=True):
        data = self.remove_none_value({
            'name': name,
            'description': description,
            'db_name': db_name,
            'webhook_url': webhook_url,
            'steps': steps,
            'custom_fields': custom_fields,
            'sources': sources
        })
        url = self.get_list_url()
        response = self.make_request('POST', url, data, retry_if_throttled=retry_if_throttled)
        return MonkeyLearnResponse(response)

    def detail(self, model_id, retry_if_throttled=True):
        url = self.get_detail_url(model_id)
        response = self.make_request('GET', url, retry_if_throttled=retry_if_throttled)
        return MonkeyLearnResponse(response)

    def delete(self, model_id, retry_if_throttled=True):
        url = self.get_detail_url(model_id)
        response = self.make_request('DELETE', url, retry_if_throttled=retry_if_throttled)
        return MonkeyLearnResponse(response)


class WorkflowSteps(ModelEndpointSet):
    model_type = ('workflows', 'steps')

    def detail(self, model_id, step_id, retry_if_throttled=True):
        url = self.get_nested_list_url(model_id, step_id)
        response = self.make_request('GET', url, retry_if_throttled=retry_if_throttled)
        return MonkeyLearnResponse(response)

    def create(self, model_id, name, step_model_id, input=None, conditions=None,
               retry_if_throttled=True):
        data = self.remove_none_value({
            'name': name,
            'model_id': step_model_id,
            'input': input,
            'conditions': conditions,
        })
        url = self.get_nested_list_url(model_id)
        response = self.make_request('POST', url, data, retry_if_throttled=retry_if_throttled)
        return MonkeyLearnResponse(response)

    def delete(self, model_id, step_id, retry_if_throttled=True):
        url = self.get_nested_list_url(model_id, step_id)
        response = self.make_request('DELETE', url, retry_if_throttled=retry_if_throttled)
        return MonkeyLearnResponse(response)


class WorkflowData(ModelEndpointSet):
    model_type = ('workflows', 'data')

    def create(self, model_id, data, retry_if_throttled=True):
        data = {'data': data}
        url = self.get_nested_list_url(model_id)
        response = self.make_request('POST', url, data, retry_if_throttled=retry_if_throttled)
        return MonkeyLearnResponse(response)

    def list(self, model_id, batch_id=None, is_processed=None, sent_to_process_date_from=None,
             sent_to_process_date_to=None, page=None, per_page=None, retry_if_throttled=True):
        params = self.remove_none_value({
            'batch_id': batch_id,
            'is_processed': is_processed,
            'sent_to_process_date_from': sent_to_process_date_from,
            'sent_to_process_date_to': sent_to_process_date_to,
            'page': page,
            'per_page': per_page,
        })
        url = self.get_nested_list_url(model_id)
        response = self.make_request('GET', url, params=params,
                                     retry_if_throttled=retry_if_throttled)
        return MonkeyLearnResponse(response)


class WorkflowCustomFields(ModelEndpointSet):
    model_type = ('workflows', 'custom-fields')

    def create(self, model_id, name, data_type, retry_if_throttled=True):
        data = {'name': name, 'type': data_type}
        url = self.get_nested_list_url(model_id)
        response = self.make_request('POST', url, data, retry_if_throttled=retry_if_throttled)
        return MonkeyLearnResponse(response)
