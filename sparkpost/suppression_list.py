import json

from .base import Resource


class SuppressionList(Resource):
    """
    SuppressionList class used to search, get and modify suppression status.
    For detailed request and response formats, see the `Suppresion List API
    documentation
    <https://www.sparkpost.com/api#/reference/suppression-list>`_.
    """

    key = 'suppression-list'

    def list(self, **kwargs):
        """
        List supression list entries based on the supplied parameters

        :param datetime from_date: DateTime to start listing
        :param datetime to_date: DateTime to end listing
        :param list types: Types of entries to return
        :param int limit: Maximum number of entries to return

        :returns: a ``list`` of entries
        :raises: :exc:`SparkPostAPIException` if API call fails
        """
        key_map = {
            'from_date': 'from',
            'to_date': 'to',
            'types': 'types',
            'sources': 'sources',
            'limit': 'limit'
        }
        params = dict([(key_map[i], kwargs[i]) for i in list(key_map.keys())
                       if i in kwargs])
        results = self.request('GET', self.uri, params=params)
        return results

    def get(self, email):
        """
        Retrieve a suppression list entry for a specific recipient by email

        :param str email: Email of the recipient whose status you want to
            check_status

        :returns: a suppression list entry
        :raises: :exc:`SparkPostAPIException` if API call fails
        """
        uri = "%s/%s" % (self.uri, email)
        results = self.request('GET', uri)
        return results

    def _upsert(self, status):
        uri = self.uri
        if isinstance(status, dict):
            # single upsert, update uri and remove email property
            uri = "%s/%s" % (self.uri, status.pop("email", None))
        else:
            status = {"recipients": status}
        results = self.request('PUT', uri, data=json.dumps(status))
        return results

    def create(self, entry):
        """
        Create a suppression list entry.

        :param dict|list status: If dict it is a single entry to create
            ``{
            'email': 'test@test.com',
            'transactional': True,
            'non_transactional': True,
            'description': 'Test description'
            }``, if list it is multiple entries to create

        :returns: a ``dict`` with a message
        :raises: :exc:`SparkPostAPIException` if API call fails
        """
        return self._upsert(entry)

    def update(self, entry):
        """
        Update a suppression list entry.

        :param dict|list status: If dict it is a single entry to update
            ``{
            'email': 'test@test.com',
            'transactional': True,
            'non_transactional': True,
            'description': 'Test description'
            }``, if list it is multiple entries to update

        :returns: a ``dict`` with a message
        :raises: :exc:`SparkPostAPIException` if API call fails
        """
        return self._upsert(entry)

    def delete(self, email):
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
