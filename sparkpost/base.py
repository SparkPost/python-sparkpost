import requests
import sparkpost

from .exceptions import SparkPostAPIException


class Resource(object):
    def __init__(self, base_uri, api_key):
        self.base_uri = base_uri
        self.api_key = api_key

    @property
    def uri(self):
        return "%s/%s" % (self.base_uri, self.key)

    def request(self, method, uri, **kwargs):
        headers = {
            'User-Agent': 'python-sparkpost/' + sparkpost.__version__,
            'Content-Type': 'application/json',
            'Authorization': self.api_key
        }
        response = requests.request(method, uri, headers=headers, **kwargs)
        if response.status_code == 204:
            return True
        if not response.ok:
            raise SparkPostAPIException(response)
        if 'results' in response.json():
            return response.json()['results']
        return response.json()

    def get(self):
        raise NotImplementedError

    def list(self):
        raise NotImplementedError

    def create(self):
        raise NotImplementedError

    def update(self):
        raise NotImplementedError

    def delete(self):
        raise NotImplementedError
