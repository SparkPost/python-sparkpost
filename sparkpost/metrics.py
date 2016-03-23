from .base import Resource, RequestsTransport


class Metrics(object):
    "Wrapper for sub-resources"

    def __init__(self, base_uri, api_key, transport_class=RequestsTransport):
        self.base_uri = "%s/%s" % (base_uri, 'metrics')
        self.campaigns = Campaigns(self.base_uri, api_key, transport_class)
        self.domains = Domains(self.base_uri, api_key, transport_class)


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
