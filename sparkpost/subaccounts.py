import json

from .base import Resource

class Subaccounts(Resource):
    """
    Domains class for managing subaccounts.
    For detailed request and response formats, see the 
    `Subaccounts API documentation
    <https://developers.sparkpost.com/api/subaccounts/>`.
    """

    def create(self, **kwargs):
        """
        Creates subaccount based on the supplied parameters
        :param str name: subaccount name
        :param str ip_pool: ID of an IP Pool in which to restrict this subaccount's mail deliveries
        :param bool setup_api_key: Whether or not to create an API key for the subaccount.
        :param str key_label: User friendly identifier for the initial subaccount api key. 
        :param list key_grants: List of grants to give to the initial subaccount api key.
        :param list key_valid_ips: List of IP's that the initial subaccount API key can be used from.
        :returns: Subaccount's ID, along with the API key and API key label, if one was created.
        :raises: :exc:`SparkPostAPIException` if API call fails
        """

        return self.request('POST', self.uri, params=kwargs)

    def get(self, id):
        """
        Get a subaccount

        :param str id: the id of the subaccount to retrieve

        :returns: the requested subaccount if found
        :raises: :exc:`SparkPostAPIException` if subaccount is not found
        """

        uri = "%s/%s" % (self.uri, id)
        return self.request('GET', uri)

    def list(self):
        """
        Get all subaccounts

        :returns: all subaccounts
        :raises: :exc:`SparkPostAPIException` if no subaccount is not found
        """

        return self.request('GET', self.uri)

    def update(self, id, **kwargs):
        """
        Updates a subaccount based on the supplied parameters
        :param str name: subaccount name
        :param str status: Status of the subaccount
        :param str ip_pool: ID of an IP Pool in which to restrict this subaccount's mail deliveries
        
        :returns: Message detailing the success of the operation.
        :raises: :exc:`SparkPostAPIException` if API call fails
        """

        uri = "%s/%s" % (self.uri, id)
        return self.request('PUT', uri, params=kwargs)
