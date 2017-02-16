import os

from sparkpost.base import Resource


class Webhooks(Resource):
    key = "webhooks"

    def list(self, **kwargs):
        results = self.request('GET', self.uri, **kwargs)
        return results


api_key = os.environ.get('SPARKPOST_API_KEY', None)
webhooks = Webhooks('https://api.sparkpost.com/api/v1', api_key)

# returns a list of webhooks for your account
print(webhooks.list())
