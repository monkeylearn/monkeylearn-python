# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals, division, absolute_import

import requests

from monkeylearn.exceptions import MonkeyLearnException


class MonkeyLearnResponse(object):
    def __init__(self, raw_responses=None):
        if raw_responses is None:
            raw_responses = []
        elif isinstance(raw_responses, requests.Response):
            raw_responses = [raw_responses]

        self.raw_responses = []
        for rr in raw_responses:
            self.add_raw_response(rr)

    def _get_last_request_header(self, header_name):
        try:
            last_response = self.raw_responses[-1]
        except IndexError:
            return None
        return getattr(last_response.headers, header_name, None)

    @property
    def request_count(self):
        return len(self.raw_responses)

    @property
    def query_limit_limit(self):
        return int(self._get_last_request_header('X-Query-Limit-Limit'))

    @property
    def query_limit_remaining(self):
        return int(self._get_last_request_header('X-Query-Limit-Remaining'))

    @property
    def query_limit_request_queries(self):
        query_count = 0
        for r in self.raw_responses:
            query_count += int(r.headers['X-Query-Limit-Request-Queries'])
        return query_count

    @property
    def body(self):
        if self.request_count == 1:
            return self.raw_responses[0].json()
        # Batched response, assume 2xx response bodies are lists (classify, extract)
        return [result for rr in self.raw_responses for result in rr.json()]

    def add_raw_response(self, raw_response):
        if raw_response.status_code != requests.codes.ok:
            self.raise_for_status(raw_response)
        self.raw_responses.append(raw_response)

    def raise_for_status(self, raw_response):
        try:
            body = raw_response.json()
        except ValueError:
            raise MonkeyLearnException('Bad JSON from server')

        raise MonkeyLearnException(
            detail=body['detail'],
            error_code=body.get('error_code'),
            status_code=raw_response.status_code
        )
