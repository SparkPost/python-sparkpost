import base64
import json
from email.utils import parseaddr

from .base import Resource


class Transmissions(Resource):
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

        model['options']['start_time'] = kwargs.get('start_time')
        model['options']['open_tracking'] = kwargs.get('track_opens')
        model['options']['click_tracking'] = kwargs.get('track_clicks')
        model['options']['transactional'] = kwargs.get('transactional')
        model['options']['sandbox'] = kwargs.get('use_sandbox')
        model['options']['skip_suppression'] = kwargs.get('skip_suppression')

        model['content']['use_draft_template'] = \
            kwargs.get('use_draft_template', False)
        model['content']['reply_to'] = kwargs.get('reply_to')
        model['content']['subject'] = kwargs.get('subject')
        if kwargs.get('from_name'):
            model['content']['from'] = {
                'name': kwargs.get('from_name') or '',
                'email': kwargs.get('from_email')
            }
        else:
            model['content']['from'] = kwargs.get('from_email')
        model['content']['html'] = kwargs.get('html')
        model['content']['text'] = kwargs.get('text')
        model['content']['template_id'] = kwargs.get('template')
        model['content']['headers'] = kwargs.get('custom_headers', {})

        recipient_list = kwargs.get('recipient_list')
        if recipient_list:
            model['recipients']['list_id'] = recipient_list
        else:
            recipients = kwargs.get('recipients', [])
            cc = kwargs.get('cc')
            bcc = kwargs.get('bcc')

            if cc:
                model['content']['headers']['CC'] = ','.join(cc)
                cc_copies = self._format_copies(recipients, cc)
                recipients = recipients + cc_copies
            if bcc:
                bcc_copies = self._format_copies(recipients, bcc)
                recipients = recipients + bcc_copies

            model['recipients'] = self._extract_recipients(recipients)

        attachments = kwargs.get('attachments', [])
        model['content']['attachments'] = self._extract_attachments(
            attachments)

        return model

    def _format_copies(self, recipients, copies):
        formatted_copies = []
        if len(recipients) > 0:
            formatted_copies = self._extract_recipients(copies)
            for recipient in formatted_copies:
                recipient['address'].update({'header_to': recipients[0]})
        return formatted_copies

    def _extract_attachments(self, attachments):
        formatted_attachments = []
        for attachment in attachments:
            formatted_attachment = {}
            formatted_attachment['type'] = attachment.get('type')
            formatted_attachment['name'] = attachment.get('name')
            if 'filename' in attachment:
                formatted_attachment['data'] = self._get_base64_from_file(
                    attachment['filename'])
            else:
                formatted_attachment['data'] = attachment.get('data')
            formatted_attachments.append(formatted_attachment)
        return formatted_attachments

    def _get_base64_from_file(self, filename):
        with open(filename, "rb") as a_file:
            encoded_string = base64.b64encode(a_file.read()).decode("ascii")
        return encoded_string

    def _extract_recipients(self, recipients):
        formatted_recipients = []
        for recip in recipients:
            try:
                string_types = basestring
            except NameError:
                string_types = str  # Python 3 doesn't have basestring
            if isinstance(recip, string_types):
                name, email = parseaddr(recip)
                formatted_recip = {
                    'address': {
                        'name': name,
                        'email': email
                    }
                }
                if not name:
                    del formatted_recip['address']['name']
                formatted_recipients.append(formatted_recip)
            else:
                formatted_recipients.append(recip)
        return formatted_recipients

    def send(self, **kwargs):
        """
        Send a transmission based on the supplied parameters

        :param list|dict recipients: If list it is an list of email addresses,
            if dict ``{'address': {'name': 'Name', 'email': 'me' }}``
        :param str recipient_list: ID of recipient list, if set recipients
            above will be ignored
        :param cc: List of email addresses to send carbon copy to
        :param bcc: List of email addresses to send blind carbon copy to
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
        :param dict attachments: Corresponds to attachments.
            See `Attachment Attributes reference
            <https://developers.sparkpost.com/api/#/reference/transmissions>`_.
            Replace `data` by `filename` if you want the library to perform
            the base64 conversion. Example: `"filename": "/full/path/test.txt"`
        :param str start_time: Delay generation of messages until this
            datetime. Format YYYY-MM-DDTHH:MM:SS+-HH:MM. Example:
            '2015-02-11T08:00:00-04:00'.
        :param bool track_opens: Defaults to True. Used to track opens of
            transmission
        :param bool track_clicks: Defaults to True. Used to track clicks of
            transmission
        :param bool use_sandbox: Flag must be set to use sandbox domain instead
            of verified sending domain. Limited to a lifetime of 50
            transmissions with this domain
        :param bool transactional: Whether message is transactional or
            non-transactional for unsubscribe and suppression purposes
        :param bool skip_suppression: Whether or not to ignore customer
            suppression rules, for this transmission only. Only applicable if
            your configuration supports this parameter. (SparkPost Elite only)
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
