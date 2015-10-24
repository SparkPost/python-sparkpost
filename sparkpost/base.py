import httplib2
import sparkpost
import json

from .exceptions import SparkPostAPIException


class Resource(object):
    def __init__(self, base_uri, api_key):
        self.base_uri = base_uri
        self.api_key = api_key

    @property
    def uri(self):
        return "%s/%s" % (self.base_uri, self.key)

    def request(self, method, uri, data):
        headers = {
            'User-Agent': 'python-sparkpost/' + sparkpost.__version__,
            'Content-Type': 'application/json',
            'Authorization': self.api_key
        }
        h = httplib2.Http('.cache')
        (r, content) = h.request(uri, method, headers=headers, body=data)
        if int(r['status']) == 200:
            return True
        if int(r['status']) >= 400:
            response = {}
            response['errors'] = json.loads(content)['errors']
            response['uri'] = uri
            response['status'] = r['status']
            raise SparkPostAPIException(response)
        if 'results' in json.loads(content):
            return json.loads(content)['results']
        return json.loads(content)
                
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
