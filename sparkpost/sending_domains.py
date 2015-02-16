from .base import Resource


class SendingDomains(Resource):
    """
    SendingDomains class used to manage custom sending domains. For detailed
    request and response formats, see the `Sending Domains API documentation
    <https://www.sparkpost.com/docs/sending-domains-api>`_.
    """

    key = 'sending-domains'

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
