import base64
import copy
import datetime
import json
import warnings
from email.utils import parseaddr

from .base import Resource
from .base import RequestsTransport
from .exceptions import SparkPostException


class Events(Resource):
    """
    Events class used to search events. For detailed
    request and response formats, see the `Events API documentation
    <https://developers.sparkpost.com/api/events/>.
    """

    key = 'events/message'

    def __init__(self, base_uri, api_key, transport_class=RequestsTransport):
        super(Events, self).__init__(base_uri, api_key, transport_class=transport_class)
        self.local_time_offset = 0

    def _update_list_and_date_parameters(self, param_dict):
        for key, value in param_dict.items():
            if isinstance(value, type([])):
                param_dict[key] = ",".join(value)
            if isinstance(value, datetime.datetime):
                param_dict[key] = self.create_date_string(value)
        return param_dict

    def _fetch_get(self, **kwargs):
        uri = "%s" % (self.uri)
        params = self._update_list_and_date_parameters(dict(kwargs))
        results = self.request('GET', uri, params=params)
        return results

    def set_local_time_offset_in_hours(self, local_time_offset):
        """

        :param local_time_offset: integer for the number of hours for the local time office
            This is only used when passing in a datetime object for either the 'from'
            or 'to' values with get()
        """
        self.local_time_offset = local_time_offset

    def get(self, **kwargs):
        """
        :param optional kwargs
        :param kwargs["from_addresses"] comma-separated string or List[str]
        :param kwargs["recipients"] comma-separated string or List[str]
        :param kwargs["transmissions"] comma-separated string or List[str]
        :param kwargs["from"] string with API-required date formatting OR a datetime object. See
            set_local_time_offset_in_hours()
        :param kwargs["to"] string with API-required date formatting OR a datetime object. See
            set_local_time_offset_in_hours()
        :param kwargs["events"] comma-separated string or List[str] with valid event types.
            Common event types: bounce, delivery, injection
            Documentation for all event types: https://developers.sparkpost.com/api/events/#header-event-types

            If kwargs does not have a from/to combination, the API service will usually return all events for the
            current day only.

        :return: List of dicts, one for each event message being returned
        """

        results = self._fetch_get(**kwargs)
        return results

    def create_date_string(self, local_datetime):
        ut_datetime = local_datetime
        ut_datetime += datetime.timedelta(hours=self.local_time_offset)
        return ut_datetime.strftime("%Y-%m-%dT%H:%M")
