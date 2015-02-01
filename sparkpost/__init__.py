import os

from .exceptions import SparkPostException
from .transmission import Transmission


__version__ = '1.0.0.dev1'


def get_api_key():
    "Get API key from environment variable"
    return os.environ.get('SPARKPOST_API_KEY', None)


class SparkPost(object):
    def __init__(self, api_key=None, base_url='https://api.sparkpost.com',
                 version='1'):
        "Set up the SparkPost API client"
        if not api_key:
            api_key = get_api_key()
            if not api_key:
                raise SparkPostException("No API key. Improve message.")

        self.base = base_url + '/api/v' + version
        self.api_key = api_key

        self.transmission = Transmission()
