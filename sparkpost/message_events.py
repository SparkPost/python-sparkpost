from datetime import datetime

from .base import Resource



class MessageEvents(Resource):
    """
    Message class used to get the various states of a of a message.
    for detailed request and response formats, see the `Message Events API
    Documentation
    <https://developers.sparkpost.com/api/#/reference/message-events/>`
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
            print "asdf"
        else:
            mesg_filter_str = mesg_filter
        return str(mesg_filter_str)

    def _format_datetime_param(self, mesg_filter):
        """
        the way to format datetimes
        """
        mesg_filter_str = ""
        if type(mesg_filter) is datetime:
            mesg_filter_str = mesg_filter.strftime("%Y-%m-%dT%H:%M")
        else:
            mesg_filter_str = str(mesg_filter)

        return mesg_filter_str

    def _format_request_params(self, **kwargs):
        """
        takes in message event kwargs and returns the request string

        param: str/num/list bounce_classes - Comma-delimited
            list of bounce classification codes to search

        params dict is a dict of avaliable params.
            Each param is keyed to a tuple of the
            (param type, special validator function (if wanted / needed))

            - Listable
                are params that can be in a list format(commma seperated)
            - datetime
                can be a datetime string, or a datetime object
            - single_val
                are params that are only single values (ie not lists or dates)
        """

        # can only be in a certain range
        def per_page_validator(per_page):
            per_page = int(per_page)
            if per_page > 10000 or per_page < 1:
                raise ValueError("""You entered, Per \
                    "page must be inbetween 1 and 10,000""")
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
            'from_date': ('datetime', None),
            'to_date': ('datetime', None),
            # single vals
            'page': ('single_val', None),
            'per_page': ('single_val', per_page_validator),
            'reason': ('single_val', None),
            'timezone': ('single_val', None)
        }

        request_list = []
        for param, filter_val in kwargs.iteritems():
            param_type, special_validator = params_dict[param]

            # see if there as special validators
            if special_validator is not None:
                filter_val = special_validator(filter_val)

            # then format the param
            if param_type == "listable":
                filter_val = self._format_listable_param(filter_val)
            elif param_type == "datetime":
                filter_val = self._format_datetime_param(filter_val)
                # if the param is to or from date, strip out the `_date` to
                # get the correct api param
                param = param.replace("_date", "")
            else:
                filter_val = str(filter_val)

            request_list.append("{param}={filter_val}".format(
                param=param,
                filter_val=filter_val
            ))

        request_str = "&".join(request_list)
        return request_str

    def _fetch_get(self, request_str, return_full_response):
        uri = "%s?%s" % (self.uri, request_str)
        results = self.request('GET', uri, return_full_response=return_full_response)
        return results

    def get(self, return_all_pages=False, return_full_response=False, **kwargs):
        """
        Get a transmission by ID

        :params
            - additional get params
                + return_full_response returns all of the data
                        results: results list,
                        total_count: count,
                        links: list of links
                + return_all_pages joins all of the result pages together
            - message event params

        :returns: the requested messages in dict of the full result, or a list
            of event objects
        :raises: :exc:`SparkPostAPIException` if transmission is not found
        """
        page_num = 1  # start at one
        default_per_page = 5000  # a good chunk size
        total_pages = 1  # the total number of pages / api call to go through
        dont_sum = set(["total_count"]) # response variable to not sum / join
        results = {}

        # while there are still pages to iterate over
        while page_num <= total_pages:
            # if we are returning all, start at the first page
            if return_all_pages:
                kwargs["page"] = page_num
                kwargs["per_page"] = default_per_page
            # get the request string
            request_str = self._format_request_params(**kwargs)
            # We always pass true for the request as we need
            # the full results for returning all pages and
            # it keeps the code simpler
            response = self._fetch_get(request_str, return_full_response=True)
            # if we want all the results, concat them
            if return_all_pages:
                total_pages = (response["total_count"] // default_per_page) + 1

            # join the dictionary
            for key, val in response.iteritems():
                if key in results and key not in dont_sum:
                    results[key] += val
                else:
                    results[key] = val

            # increase the page number
            page_num += 1


        if return_full_response is False:
            return results["results"]
        return results
