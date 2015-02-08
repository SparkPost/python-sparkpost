import json

from .base import Resource


class Transmission(Resource):
    """
    Transmission class used to send, list and get transmissions. For detailed
    request and response formats, see the `Transmissions API documentation
    <https://www.sparkpost.com/docs/transmissions-api>`_.
    """

    key = 'transmissions'

    def _translate_keys(self, **kwargs):
        model = {
            'content': {},
            'options': {},
            'recipients': {}
        }

        model['description'] = kwargs.get('description')
        model['return_path'] = kwargs.get('return_path',
                                          'default@sparkpostmail.com')
        model['campaign_id'] = kwargs.get('campaign')
        model['metadata'] = kwargs.get('metadata')
        model['substitution_data'] = kwargs.get('substitution_data')

        model['options']['open_tracking'] = kwargs.get('track_opens', True)
        model['options']['click_tracking'] = kwargs.get('track_clicks', True)
        model['options']['sandbox'] = kwargs.get('use_sandbox')

        model['content']['use_draft_template'] = \
            kwargs.get('use_draft_template', False)
        model['content']['reply_to'] = kwargs.get('reply_to')
        model['content']['subject'] = kwargs.get('subject')
        model['content']['from'] = kwargs.get('from_email')
        model['content']['html'] = kwargs.get('html')
        model['content']['text'] = kwargs.get('text')
        model['content']['template_id'] = kwargs.get('template')
        model['content']['headers'] = kwargs.get('custom_headers')

        recipient_list = kwargs.get('recipient_list')
        if recipient_list:
            model['recipients']['list_id'] = recipient_list
        else:
            recipients = kwargs.get('recipients', [])
            model['recipients'] = self._extractRecipients(recipients)

        return model

    def _extractRecipients(self, recipients):
        formatted_recipients = []
        for recip in recipients:
            if isinstance(recip, str):
                formatted_recipients.append({'address': {'email': recip}})
        else:
            formatted_recipients.append(recip)
        return formatted_recipients

    def send(self, **kwargs):
        """
        Send a transmission based on the supplied parameters

        :param list|dict recipients: If list it is an array of email addresses,
            if dict ``{'address': {'name': 'Name', 'email': 'me' }}``
        :param str recipient_list: ID of recipient list, if set recipients
            above will be ignored
        :param str template: ID of template. If set HTML or text will not be
            used
        :param bool use_draft_template: Default to False. Set to true if you
            want to send a template that is a draft
        :param str html: HTML part of transmission
        :param str text: Text part of transmission
        :param str subject: Subject of transmission
        :param str from_email: Friendly from of transmission, domain must be a
            verified sending domain to your account or transmission will fail
        :param str reply_to: Reply to of transmission
        :param str description: Description of transmission
        :param str campaign: Campaign of transmission
        :param dict metatdata: Any data you want to send along with
            transmission, used in WebHooks
        :param dict substitution_data: Corresponds to substitutions in
            html/text content. See `substitutions reference
            <https://www.sparkpost.com/docs/substitutions-reference>`_.
        :param bool track_opens: Defaults to True. Used to track opens of
            transmission
        :param bool track_clicks: Defaults to True. Used to track clicks of
            transmission
        :param bool use_sandbox: Flag must be set to use sandbox domain instead
            of verified sending domain. Limited to a lifetime of 50
            transmissions with this domain
        :param dict custom_headers: Used to set any headers associated with
            transmission

        :returns: a ``dict`` with the ID and number of accepted and rejected
            recipients
        :raises: :exc:`SparkPostAPIException` if transmission cannot be sent
        """

        payload = self._translate_keys(**kwargs)
        results = self.request('POST', self.uri, data=json.dumps(payload))
        return results

    def get(self, transmission_id):
        """
        Get a transmission by ID

        :param str transmission_id: ID of the transmission you want to retrieve

        :returns: the requested transmission if found
        :raises: :exc:`SparkPostAPIException` if transmission is not found
        """
        uri = "%s/%s" % (self.uri, transmission_id)
        results = self.request('GET', uri)
        return results['transmission']

    def list(self):
        """
        Get a list of your transmissions

        :returns: list of transmissions
        :raises: :exc:`SparkPostAPIException` if API call fails
        """
        results = self.request('GET', self.uri)
        return results
