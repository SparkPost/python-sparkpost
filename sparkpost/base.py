import requests

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
            'User-Agent': 'python-sparkpost',
            'Content-Type': 'application/json',
            'Authorization': self.api_key
        }
        response = requests.request(method, uri, headers=headers, **kwargs)
        if not response.ok:
            raise SparkPostAPIException(response)
        return response.json()['results']

    def get(self, uri, **kwargs):
        return self.request('get', uri, **kwargs)

    def post(self, uri, **kwargs):
        return self.request('post', uri, **kwargs)

    def put(self, uri, **kwargs):
        return self.request('put', uri, **kwargs)

    def delete(self, uri, **kwargs):
        return self.request('delete', uri, **kwargs)
