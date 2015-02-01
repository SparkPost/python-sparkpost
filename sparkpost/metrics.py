from .base import Resource


class Metrics(object):
    "Wrapper for sub-resources"

    def __init__(self, base_uri, api_key):
        self.base_uri = "%s/%s" % (base_uri, 'metrics')
        self.domains = Domains(self.base_uri, api_key)


class Domains(Resource):
    key = 'domains'
