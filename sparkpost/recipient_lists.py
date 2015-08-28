import json

from .base import Resource


class RecipientLists(Resource):
    """
    RecipientLists class used to create, update, delete, list and get recipient
    lists. For detailed request and response formats, see the `Recipient Lists
    API documentation
    <https://www.sparkpost.com/api#/reference/recipient-lists>`_.
    """

    key = 'recipient-lists'

    def _translate_keys(self, **kwargs):
        model = {}

        if 'id' in kwargs:
            model['id'] = kwargs.get('id')
        model['name'] = kwargs.get('name')
        model['description'] = kwargs.get('description')
        model['attributes'] = kwargs.get('attributes')
        model['recipients'] = kwargs.get('recipients')

        return model

    def create(self, **kwargs):
        """
        Create a recipient list based on the supplied parameters

        :param str id: ID used to reference the recipient list
        :param str name: Editable display name
        :param str description: Detailed description of the recipient list
        :param dict attributes: Arbitrary metadata related to the list
        :param list recipients: Array of recipient dicts

        :returns: a ``dict`` with the ID, name, and number of accepted
            and rejected recipients
        :raises: :exc:`SparkPostAPIException` if API call fails
        """
        payload = self._translate_keys(**kwargs)
        results = self.request('POST', self.uri, data=json.dumps(payload))
        return results

    def update(self, list_id, **kwargs):
        """
        Update a recipient list by ID based on the supplied parameters

        :param str list_id: ID of the recipient list you want to update
        :param str name: Editable display name
        :param str description: Detailed description of the recipient list
        :param dict attributes: Arbitrary metadata related to the list
        :param list recipients: Array of recipient dicts

        :returns: a ``dict`` with the ID, name, and number of accepted
            and rejected recipients
        :raises: :exc:`SparkPostAPIException` if API call fails
        """
        uri = "%s/%s" % (self.uri, list_id)
        payload = self._translate_keys(**kwargs)
        results = self.request('PUT', uri, data=json.dumps(payload))
        return results

    def delete(self, list_id):
        """
        Delete a recipient list by ID

        :param str list_id: ID of the recipient list you want to delete

        :returns: empty ``dict``
        :raises: :exc:`SparkPostAPIException` if recipient list is not found
            or if recipient list is in use
        """
        uri = "%s/%s" % (self.uri, list_id)
        results = self.request('DELETE', uri)
        return results

    def get(self, list_id, show_recipients=None):
        """
        Get a recipient list by ID

        :param str list_id: ID of the recipient list you want to retrieve
        :param bool show_recipients: If True, returns attributes for
            all recipients

        :returns: the requested recipient list if found
        :raises: :exc:`SparkPostAPIException` if recipient list is not found
        """
        uri = "%s/%s" % (self.uri, list_id)
        params = {}
        if show_recipients is not None:
            params['show_recipients'] = str(show_recipients).lower()
        results = self.request('GET', uri, params=params)
        return results

    def list(self):
        """
        Get a list of your recipient lists

        :returns: list of recipient lists
        :raises: :exc:`SparkPostAPIException` if API call fails
        """
        results = self.request('GET', self.uri)
        return results
