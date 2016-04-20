from datetime import datetime

from .base import Resource

try:
    string_types = basestring
except NameError:
    string_types = str  # Python 3 doesn't have basestring


class MessageEvents(Resource):
    """
    Message class used to get the various states of a of a message.
    for detailed request and response formats, see the `Message Events API
    Documentation <https://developers.sparkpost.com/api/#/reference/message-events/>`
    """
    key = "message-events"

    def _format_listable_param(self, mesg_filter):
        """
        if the message event can take in a list or not
        """
        mesg_filter_str = ""
        if type(mesg_filter) is list:
            mesg_filter_str = reduce(
                lambda acc, x: "{acc},{x}".format(acc=acc, x=x),
                mesg_filter
            )
        else:
            mesg_filter_str = str(mesg_filter)
        return mesg_filter_str

    def _format_datetime_param(self, mesg_filter):
        """
        the way to format datetimes
        """
        mesg_filter_str = ""
        if type(mesg_filter) is datetime:
            mesg_filter_str = mesg_filter.strftime("%Y-%m-%d:T%H:%M")
        else:
            mesg_filter_str = str(mesg_filter)

        return mesg_filter_str

    def _format_request_params(self, **kwargs):
        """
        takes in message event kwargs and returns the request string

        param: str/num/list bounce_classes - Comma-delimited
            list of bounce classification codes to search

        params dict is a dict of avaliable params. Each param is keyed to a tuple of the
            (param type, special validator function (if wanted / needed))

            - Listable are params that can be in a list format(commma seperated)
            - datetime can be a datetime string, or a datetime object
            - single_val are params that are only single values (ie not lists or dates)
        """

        # can only be in a certain range
        def per_page_validator(per_page):
            per_page = int(per_page)
            if per_page > 10000 or per_page < 1:
                raise ValueError("You entered %d, Per "
                    "page must be inbetween 1 and 10,000" % per_page)
            else:
                return per_page

        params_dict = {
            # Listable options
            'bounce_classes': ('listable', None),
            'campaign_ids': ('listable', None),
            'events': ('listable', None),
            'friendly_froms': ('listable', None),
            'message_ids': ('listable', None),
            'recipients': ('listable', None),
            'subaccounts': ('listable', None),
            'template_ids': ('listable', None),
            'transmission_ids': ('listable', None),
            # datetimes
            'from': ('datetime', None),
            'to': ('datetime', None),
            # single vals
            'page': ('single_val', None),
            'per_page': ('single_val', per_page_validator),
            'reason': ('single_val', None),
            'timezone': ('single_val', None)
        }

        request_list = []
        for param, filter_val in kwargs.iteritems():
            param_type, special_validator = params_dict[param]

            if special_validator is not None:
                filter_val = special_validator(filter_val)

            if param_type is "listable":
                filter_val = self._format_listable_param(filter_val)
            elif param_type is "datetime":
                filter_val = self._format_datetime_param(filter_val)
            else:
                filter_val = str(filter_val)

            request_list.append("{param}={filter_val}".format(
                param=param,
                filter_val=filter_val
            ))

        request_str = "&".join(request_list)
        return request_str

    def _fetch_get(self, request_str):
        uri = "%s?%s" % (self.uri, request_str)
        results = self.request('GET', uri)
        return results

    def get(self, **kwargs):
        """
        Get a transmission by ID

        :param message event params

        :returns: the requested messages if found
        :raises: :exc:`SparkPostAPIException` if transmission is not found
        """
        request_str = self._format_request_params(**kwargs)
        results = self._fetch_get(request_str)
        return results





