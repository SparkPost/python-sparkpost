import json

from .base import Resource


class SendingDomainStatus(object):
    VALID = 'valid'
    INVALID = 'invalid'
    UNVERIFIED = 'unverified'
    PENDING = 'pending'


class SendingDomains(Resource):
    """
    Domains class for managing sending domains.
    For detailed request and response formats, see the `Sending Domains List API
    documentation
    <https://developers.sparkpost.com/api/sending-domains/>`.
    """

    key = 'sending-domains'

    def list(self, **kwargs):
        """
        List sending domain entries based on the supplied parameters

        :param bool ownership_verified: ownership verified filter
        :param SendingDomainStatus dkim_status: filter
        :param SendingDomainStatus cname_status: filter
        :param SendingDomainStatus mx_status: filter
        :param SendingDomainStatus abuse_at_status: filter
        :param SendingDomainStatus postmaster_at_status: filter
        :param SendingDomainStatus compliance_status: filter
        :param bool is_default_bounce_domain: default bounce domain filter

        :returns: a ``list`` of entries
        :raises: :exc:`SparkPostAPIException` if API call fails
        """

        return self.request('GET', self.uri, params=kwargs)

    def get(self, domain):
        """
        Get a sending domain

        :param str domain: the sending domain to retrieve

        :returns: the requested sending domain if found
        :raises: :exc:`SparkPostAPIException` if sending domain is not found
        """
        uri = "%s/%s" % (self.uri, domain)
        return self.request('GET', uri)

    def delete(self, domain):
        """
        Delete a sending domain.

        NOTE: Before deleting a sending domain please ensure you are no longer using it.
        After deleting a sending domain, any new transmissions that use it will result
        in a rejection. This includes any transmissions that are in progress, scheduled
        for the future, or use a stored template referencing the sending domain.

        :param str domain: the domain to delete

        :returns: 204 if successful
        :raises: :exc:`SparkPostAPIException` otherwise
        """
        uri = "%s/%s" % (self.uri, domain)
        return self.request('DELETE', uri)

    def update(self, domain, **kwargs):
        """
        Update sending domain entries based on the supplied parameters. All params
        are optional (but nothing will happen if you send none of them!). However, if
        any of the dkim params are passed, then dkim_private, dkim_public, and
        dkim_selector are all required.

        :param bool tracking_domain: associate a tracking domain with a sending domain.
          To remove a tracking domain association, set to empty string.
        :param str dkim_private: DKIM signature private key
        :param str dkim_public: DKIM signature public key
        :param str dkim_selector: value used as the DomainKey selector which indicates
          the DKIM public key location.
        :param bool shared_with_subaccounts: whether this domain can be used by
          subaccounts. Only available to domains belonging to a master account.
        :param bool is_default_bounce_domain: Whether this domain should be used as the
          bounce domain when no other valid bounce domain has been specified in the
          transmission or SMTP injection. Only available to domains with cname_status
          or mx_status equal to valid. The master account and each subaccount may set
          its own unique default bounce domain.

        :returns: a ``dict`` with a message
        :raises: :exc:`SparkPostAPIException` otherwise
        """
        uri = "%s/%s" % (self.uri, domain)

        payload = {}
        if 'tracking_domain' in kwargs:
            payload['tracking_domain'] = kwargs.get('tracking_domain')

        dkim_dict = self._get_dkim_dict(**kwargs)
        if dkim_dict is not None:
            payload['dkim'] = dkim_dict

        if 'shared_with_subaccounts' in kwargs:
            payload['shared_with_subaccounts'] = kwargs.get('shared_with_subaccounts')

        if 'is_default_bounce_domain' in kwargs:
            payload['is_default_bounce_domain'] = kwargs.get('is_default_bounce_domain')

        return self.request('PUT', uri, data=json.dumps(payload))

    def create(self, domain, **kwargs):
        """
        Creates a new sending domain. Each domain and its subdomains can only be added
        to a single account.

        :param bool domain: the domain to create. Required.
        :param bool tracking_domain: associated tracking domain. The tracking domain
          and sending domain must belong to the same subaccount.
        :param str dkim_private: DKIM signature private key
        :param str dkim_public: DKIM signature public key
        :param str dkim_selector: value used as the DomainKey selector which indicates
          the DKIM public key location
        :param bool generate_dkim: whether to generate a DKIM keypair on creation.
          If true, dkim_private, dkim_public, and dkim_selector are ignored. Default
          true.
        :param int dkim_key_length: size, in bits, of the DKIM private key to be
          generated. Ignored if generate_dkim is false. Default 1024.
        :param bool shared_with_subaccounts: whether this domain can be used by
          subaccounts. Only available to domains belonging to a master account.
          Default false.

        :returns: the new domain
        :raises: :exc:`SparkPostAPIException` otherwise
        """
        payload = {'domain': domain}

        if 'tracking_domain' in kwargs:
            payload['tracking_domain'] = kwargs.get('tracking_domain')

        if 'generate_dkim' in kwargs and kwargs.get('generate_dkim') is False:
            dkim = self._get_dkim_dict(**kwargs)
            payload['dkim'] = dkim
        else:
            payload['generate_dkim'] = True
            if 'dkim_key_length' in kwargs:
                payload['dkim_key_length'] = kwargs.get('dkim_key_length')

        if 'shared_with_subaccounts' in kwargs:
            payload['shared_with_subaccounts'] = kwargs.get('shared_with_subaccounts')

        return self.request('POST', self.uri, data=json.dumps(payload))


    @staticmethod
    def _get_dkim_dict(**kwargs):
        dkim_present = 'dkim_private' in kwargs or \
                       'dkim_public' in kwargs or \
                       'dkim_selector' in kwargs

        if dkim_present:
            if not ('dkim_private' in kwargs and
                    'dkim_public' in kwargs and
                    'dkim_selector' in kwargs):
                raise ValueError('If any DKIM parameters are provided, all of'
                                 'dkim_private, dkim_public, and dkim_selector'
                                 'are required')

            return {'dkim_private': kwargs.get('dkim_private'),
                    'dkim_public': kwargs.get('dkim_public'),
                    'dkim_selector': kwargs.get('dkim_selector')}
        else:
            return None


class TrackingDomains(Resource):
    """
    Domains class for managing tracking domains.
    For detailed request and response formats, see the `Tracking Domains List API
    documentation
    <https://developers.sparkpost.com/api/tracking-domains/>`.
    """

    key = 'tracking-domains'

    def list(self, **kwargs):
        """
        List tracking domain entries based on the supplied parameters

        :param bool is_default: Restrict results to default domains when true and
          non-default domains when false
        :param list subaccounts: list of subaccounts to include in results

        :returns: a ``list`` of entries
        :raises: :exc:`SparkPostAPIException` if API call fails
        """
        params = {}
        if 'default' in kwargs:
            is_default = kwargs.get('default')
            # Not sure why I need to do this. Passing a python boolean on the query
            # string in SendingDomains.list() works, but if I do it here, sparkpost
            # complains that the query param is not a boolean. ¯\_(ツ)_/¯
            params['default'] = 'true' if is_default else 'false'

        if 'subaccounts' in kwargs and len(kwargs.get('subaccounts')) > 0:
            subaccount_str = ','.join(kwargs.get('subaccounts'))
            params['subaccounts'] = subaccount_str

        return self.request('GET', self.uri, params=params)

    def get(self, domain):
        """
        Get a tracking domain

        :param str domain: the tracking domain to retrieve

        :returns: the requested tracking domain if found
        :raises: :exc:`SparkPostAPIException` if tracking domain is not found
        """
        uri = "%s/%s" % (self.uri, domain)
        return self.request('GET', uri)

    def delete(self, domain):
        """
        Delete a tracking domain.

        :param str domain: the domain to delete

        :returns: 204 if successful
        :raises: :exc:`SparkPostAPIException` otherwise
        """
        uri = "%s/%s" % (self.uri, domain)
        return self.request('DELETE', uri)

    def update(self, domain, **kwargs):
        """
        Update the attributes of an existing tracking domain. The master account and
        each subaccount can only have one default tracking domain. Setting a new default
        automatically unsets the current relevant default, if it exists.

        :param str domain: the tracking domain to update (required)
        :param bool secure: whether the tracking URL should use HTTPS. HTTP will be used
          if false.
        :param bool default: whether the tracking domain should be used when not
          explicitly associated with a sending domain. The domain has to be verified to
          be set as the default.

        :returns: a ``dict`` with a message
        :raises: :exc:`SparkPostAPIException` otherwise
        """

        uri = "%s/%s" % (self.uri, domain)

        payload = {}
        if 'secure' in kwargs:
            payload['secure'] = kwargs.get('secure')
        if 'default' in kwargs:
            payload['default'] = kwargs.get('default')

        return self.request('PUT', uri, data=json.dumps(payload))

    def create(self, domain, **kwargs):
        """
        Create a tracking domain.

        :param str domain: the tracking domain to create (required)
        :param bool secure: whether the tracking URL should use HTTPS. HTTP will be used
          if false.

        :returns: the new tracking domain
        :raises: :exc:`SparkPostAPIException` otherwise
        """
        payload = {'domain': domain}
        if 'secure' in kwargs:
            payload['secure'] = kwargs.get('secure')

        return self.request('POST', self.uri, data=json.dumps(payload))

