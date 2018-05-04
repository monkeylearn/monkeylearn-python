# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals, division, absolute_import


class MonkeyLearnException(Exception):
    pass


class MonkeyLearnResponseException(MonkeyLearnException):
    def __init__(self, status_code=500, detail='Internal server error',
                 error_code=None, response=None):
        self.detail = detail
        self.error_code = error_code
        self.status_code = status_code
        self.response = response

        message = 'Error'
        if error_code:
            message += ' {}'.format(error_code)
        message += ': {}'.format(detail)

        super(Exception, self).__init__(message)


# Request Validation Errors (422)


class RequestParamsError(MonkeyLearnResponseException):
    pass


# Authentication (401)


class AuthenticationError(MonkeyLearnResponseException):
    pass


# Forbidden (403)


class ForbiddenError(MonkeyLearnResponseException):
    pass


class ModelLimitError(ForbiddenError):
    pass


# Not found Exceptions (404)


class ResourceNotFound(MonkeyLearnResponseException):
    pass


class ModelNotFound(ResourceNotFound):
    pass


class CategoryNotFound(ResourceNotFound):
    pass

# Rate limit (429)


class RateLimitError(MonkeyLearnResponseException):
    pass


class PlanRateLimitError(RateLimitError):
    pass


class ConcurrencyRateLimitError(RateLimitError):
    pass


# State errors (423)


class ModuleStateError(MonkeyLearnResponseException):
    pass


RESPONSE_CODES_EXCEPTION_MAP = {
    422: RequestParamsError,
    401: AuthenticationError,
    403: {
        'MODEL_LIMIT': ModelLimitError,
        '*': ForbiddenError,
    },
    404: {
        'MODEL_NOT_FOUND': ModelNotFound,
        'CATEGORY_NOT_FOUND': CategoryNotFound,
        '*': ResourceNotFound,
    },
    429: {
        'REQUEST_LIMIT': PlanRateLimitError,
        'REQUEST_CONCURRENCY_LIMIT': ConcurrencyRateLimitError,
        '*': RateLimitError,
    },
    423: ModuleStateError,
}


def get_exception_class(status_code, error_code=None):
    exception_or_dict = RESPONSE_CODES_EXCEPTION_MAP.get(status_code, MonkeyLearnResponseException)
    if isinstance(exception_or_dict, dict):
        exception_class = exception_or_dict.get(error_code, exception_or_dict['*'])
    else:
        exception_class = exception_or_dict
    return exception_class
