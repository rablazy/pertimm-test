import logging
from typing import Dict

import requests
from requests.exceptions import RequestException

logger = logging.getLogger(__name__)

#requests.packages.urllib3.add_stderr_logger()

__all__ = ['HttpException', 'ApiException', 'get', 'post']



class HttpException(Exception):
    def __init__(self, message, code=None):
        self.code = code
        self.message = message
        super().__init__(self.message)

class ApiException(Exception):...


def get(url: str, payload:Dict={}):
    try:
        response = requests.get(url, params=payload)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            raise HttpException(response.reason, response.status_code)
    except Exception as e:
       raise ApiException(e.message)


def post(url: str, payload=None):
    try:
        response = requests.post(
            url,
            data=payload,
            allow_redirects=True
        )
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            raise HttpException(response.reason, response.status_code)
    except Exception as e:
       raise ApiException(e.message)
