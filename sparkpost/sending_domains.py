import json

from .base import Resource


class Sending_Domains(Resource):
    """
    Sending_Domains class used to create, update, verify, list,
     and find sending domains. For detailed request and response
     formats, see the `Sending Domains API documentation
    <https://www.sparkpost.com/api#/reference/sending-domains>`_.
    """

    key = 'sending-domains'

    def _translate_keys(self, **kwargs):
        model = {
            "dkim": {}
        }

        model['domain'] = kwargs.get('domain')
        model['dkim']['private'] = kwargs.get('private_key')
        model['dkim']['public'] = kwargs.get('public_key')
        model['dkim']['selector'] = kwargs.get('selector')
        model['dkim']['headers'] = kwargs.get('headers')

        return model

    def all(self):
        """
        Get a list of your sending domains

        :returns: list of sending domains
        :raises: :exc:`SparkPostAPIException` if API call fails
        """
        results = self.get(self.uri)
        return results

    def find(self, domain):
        """
        Get a sending domain by domain name

        :param str domain: name of the sending domain you want to retrieve

        :returns: the requested sending domain if found
        :raises: :exc:`SparkPostAPIException` if transmission is not found
        """
        uri = "%s/%s" % (self.uri, domain)
        results = self.get(uri)
        return results

    def create(self, **kwargs):
        """
        Create a sending domain based on supplied parameters

        :param str domain: name of the sending domain
        :param str private_key: private key used to create the DKIM Signature
        :param str public_key: public key retrieved from DNS of the sending
            domain
        :param str selector: indicates the DKIM public key location
        :param str headers: header fields to be included in the DKIM signature

        :returns: a ``dict`` with the domain and a message
        :raises: :exc:`SparkPostAPIException` if sending domain cannot be
            created
        """
        payload = self._translate_keys(**kwargs)
        results = self.post(self.uri, data=json.dumps(payload))
        return results

    def update(self, **kwargs):
        """
        Update a sending domain based on supplied parameters

        :param str domain: name of the sending domain to update
        :param str private_key: private key used to create the DKIM Signature
        :param str public_key: public key retrieved from DNS of the sending
            domain
        :param str selector: indicates the DKIM public key location
        :param str headers: header fields to be included in the DKIM signature

        :returns: a ``dict`` with the domain and a message
        :raises: :exc:`SparkPostAPIException` if sending domain cannot be
            updated
        """
        uri = "%s/%s" % (self.uri, kwargs.get('domain'))
        payload = self._translate_keys(**kwargs)
        payload.pop('domain', None)
        results = self.put(uri, data=json.dumps(payload))
        return results

    def verify(self, domain, **kwargs):
        """
        Verify a sending domain

        :param str domain: name of the sending domain you want to verify
        :param bool dkim_verify: initiates a check against the sending domain's
             DKIM record
        :param bool spf_verify: initiates a check against the sending domain's
             SPF record

        :returns: a ``dict`` with the verification status results
        :raises: :exc:`SparkPostAPIException` if API call fails
        """
        uri = "%s/%s/verify" % (self.uri, domain)
        payload = {
            "dkim_verify": kwargs.get('dkim_verify', True),
            "spf_verify": kwargs.get('spf_verify', True)
        }
        results = self.post(uri, data=json.dumps(payload))
        return results
