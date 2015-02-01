from .base import Resource


class Metrics(object):
    "Wrapper for sub-resources"

    def __init__(self, base_uri, api_key):
        self.base_uri = "%s/%s" % (base_uri, 'metrics')
        self.campaigns = Campaigns(self.base_uri, api_key)
        self.domains = Domains(self.base_uri, api_key)


class Campaigns(Resource):
    key = 'campaigns'

    def list(self, **kwargs):
        results = self.request('GET', self.uri, **kwargs)
        return results['campaigns']


class Domains(Resource):
    key = 'domains'

    def list(self, **kwargs):
        results = self.request('GET', self.uri, **kwargs)
        return results['domains']
