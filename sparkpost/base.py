import sparkpost

from .exceptions import SparkPostAPIException


class RequestsTransport(object):
    def request(self, method, uri, headers, return_all_keys=False, **kwargs):
        import requests
        response = requests.request(method, uri, headers=headers, **kwargs)
        if response.status_code == 204:
            return True
        if not response.ok:
            raise SparkPostAPIException(response)
        # in case you don't want to return just the results
        if return_all_keys:
            return response.json()
        if 'results' in response.json():
            return response.json()['results']
        return response.json()


class Resource(object):
    key = ""

    def __init__(self, base_uri, api_key, transport_class=RequestsTransport):
        self.base_uri = base_uri
        self.api_key = api_key
        self.transport = transport_class()

    @property
    def uri(self):
        return "%s/%s" % (self.base_uri, self.key)

    def request(self, method, uri, **kwargs):
        headers = {
            'User-Agent': 'python-sparkpost/' + sparkpost.__version__,
            'Content-Type': 'application/json',
            'Authorization': self.api_key
        }
        response = self.transport.request(method, uri, headers=headers,
                                          **kwargs)
        return response

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
