import json

from .base import Resource


class SuppressionList(Resource):
    """
    SuppressionList class used to search, get and modify suppression status.
    For detailed request and response formats, see the `Suppresion List API
    documentation<https://www.sparkpost.com/api#/reference/suppression-list>`_.
    """

    key = 'suppression-list'

    def search(self, **kwargs):
        """
        Search for an entry based on the supplied parameters

        :param datetime to: DateTime to end searching
        :param datetime from: DateTime to start searching
        :param list types: Types of entries to include in the search
        :param int limit: Maximum number of results to return

        :returns: a ``list`` of entries
        :raises: :exc:`SparkPostAPIException` if API call fails
        """
        params = dict([(i, kwargs[i]) for i in ["to", "from", "types", "limit"]
                      if i in kwargs])
        results = self.request('GET', self.uri, params=params)
        return results

    def check_status(self, email):
        """
        Retrieve the suppression status for a specific recipient by email

        :param str email: Email of the recipient whose status you want to
            check_status

        :returns: a list entry
        :raises: :exc:`SparkPostAPIException` if API call fails
        """
        uri = "%s/%s" % (self.uri, email)
        results = self.request('GET', uri)
        return results

    def remove_status(self, email):
        """
        Delete the suppression status for a specific recipient by email

        :param str email: Email of the recipient whose status you want to
            remove

        :returns: TODO
        :raises: :exc:`SparkPostAPIException` if API call fails
        """
        uri = "%s/%s" % (self.uri, email)
        results = self.request('DELETE', uri)
        return results

    def upsert(self, status):
        """
        Insert or Update a status entry.

        :param dict|list status: If dict it is a single entry to upsert
            ``{
                'email': 'test@test.com',
                'transactional': True,
                'non_transactional': True,
                'description': 'Test description'
            }``, if list it is multiple entries to upsert

        :returns: a ``dict`` with a message
        :raises: :exc:`SparkPostAPIException` if API call fails
        """
        uri = self.uri
        if isinstance(status, dict):
            # single upsert, update uri and remove email property
            uri = "%s/%s" % (self.uri, status.pop("email", None))
        else:
            status = {"recipients": status}
        results = self.request('PUT', uri, data=json.dumps(status))
        return results
