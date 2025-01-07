import logging
from typing import Dict

import requests
from requests.exceptions import RequestException

logger = logging.getLogger(__name__)

# requests.packages.urllib3.add_stderr_logger()

__all__ = ['ApiException', 'get', 'post']


class ApiException(Exception):
    ...


def get(url: str, payload: Dict = {}):
    try:
        response = requests.get(url, params=payload)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            response.raise_for_status()
    except Exception as e:
        raise ApiException(e)


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
            response.raise_for_status()
    except Exception as e:
        raise ApiException(e)
