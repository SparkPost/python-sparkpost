import json
from datetime import datetime

from Crypto.PublicKey import RSA

from .base import Resource


class SendingDomains(Resource):
    """
    SendingDomains class used to manage custom sending domains. For detailed
    request and response formats, see the `Sending Domains API documentation
    <https://www.sparkpost.com/docs/sending-domains-api>`_.
    """

    key = 'sending-domains'

    def _generate_key_pair(self):
        # TODO strip out ---public|private--- bits
        private = RSA.generate(1024)
        public = private.publickey()
        return private.exportKey(), public.exportKey()

    def _generate_selector(self):
        now = datetime.now()
        return 'scph%s' % now.strftime('%m%d')

    def create(self, domain, selector=None, headers=None):
        """
        Create a sending domain

        :param str domain: the sending domain to create
        :param str selector: DKIM selector
        :param str headers: headers to include in DKIM signing

        :returns: a ``dict`` with the successfully created domain
        :raises: :exc:`SparkPostAPIException` if sending domain cannot be
            created
        """

        private, public = self._generate_key_pair()
        payload = {
            'domain': domain,
            'dkim': {
                'private': private,
                'public': public,
                'selector': selector or self._generate_selector(),
                'headers': headers or 'from:to:subject:date'
            }
        }
        results = self.request('POST', self.uri, data=json.dumps(payload))
        return results

    def get(self, domain):
        """
        Get a sending domain

        :param str domain: sending domain you want to retrieve

        :returns: the requested sending domain if found
        :raises: :exc:`SparkPostAPIException` if sending domain is not found
        """
        uri = "%s/%s" % (self.uri, domain)
        results = self.request('GET', uri)
        return results

    def list(self):
        """
        Get a list of your sending domains

        :returns: list of sending domains
        :raises: :exc:`SparkPostAPIException` if API call fails
        """
        results = self.request('GET', self.uri)
        return results
