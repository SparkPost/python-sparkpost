import base64
import copy
import json
from email.utils import parseaddr

from .base import Resource


try:
    string_types = basestring
except NameError:
    string_types = str  # Python 3 doesn't have basestring


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
        model['options']['ip_pool'] = kwargs.get('ip_pool')
        model['options']['inline_css'] = kwargs.get('inline_css')

        model['content']['use_draft_template'] = \
            kwargs.get('use_draft_template', False)
        model['content']['reply_to'] = kwargs.get('reply_to')
        model['content']['subject'] = kwargs.get('subject')
        from_email = kwargs.get('from_email')
        if isinstance(from_email, string_types):
            from_email = self._parse_address(from_email)
        model['content']['from'] = from_email
        model['content']['html'] = kwargs.get('html')
        model['content']['text'] = kwargs.get('text')
        model['content']['template_id'] = kwargs.get('template')
        model['content']['headers'] = kwargs.get('custom_headers', {})

        recipient_list = kwargs.get('recipient_list')
        if recipient_list:
            model['recipients']['list_id'] = recipient_list
        else:
            recipients = kwargs.get('recipients', [])
            recipients = self._extract_recipients(recipients)
            cc = kwargs.get('cc')
            bcc = kwargs.get('bcc')

            if cc:
                model['content']['headers']['CC'] = ','.join(cc)
                cc_copies = self._format_copies(recipients, cc)
                recipients = recipients + cc_copies
            if bcc:
                bcc_copies = self._format_copies(recipients, bcc)
                recipients = recipients + bcc_copies

            model['recipients'] = recipients

        attachments = kwargs.get('attachments', [])
        model['content']['attachments'] = self._extract_attachments(
            attachments)

        if 'inline_images' in kwargs:
            inline_images = kwargs['inline_images']
            model['content']['inline_images'] = self._extract_attachments(
                inline_images)

        return model

    def _format_copies(self, recipients, copies):
        formatted_copies = []
        if len(recipients) > 0:
            formatted_copies = self._extract_recipients(copies)
            main_recipient = copy.deepcopy(recipients[0])
            main_recipient.pop('address')
            for recipient in formatted_copies:
                recipient['address'].update({
                    'header_to': self._format_header_to(recipients[0])
                })
                recipient.update(**main_recipient)
        return formatted_copies

    def _format_header_to(self, recipient):
        if 'name' in recipient['address']:
            return '"{name}" <{email}>'.format(
                name=recipient['address']['name'],
                email=recipient['address']['email']
            )
        return recipient['address']['email']

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

    def _parse_address(self, address):
        name, email = parseaddr(address)
        parsed_address = {
            'email': email
        }
        if name:
            parsed_address['name'] = name
        return parsed_address

    def _extract_recipients(self, recipients):
        formatted_recipients = []
        for recip in recipients:
            if isinstance(recip, string_types):
                formatted_recipients.append({
                    'address': self._parse_address(recip)
                })
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
        :param str from_email: Email that the transmission comes from. The
            domain must be a verified sending domain to your account or
            the transmission will fail. You can pass a from email or both
            from name and from email - `testing@example.com` or
            `Test Email <testing@example.com>` will both work.
        :param str reply_to: Reply to of transmission
        :param str description: Description of transmission
        :param str campaign: Campaign of transmission
        :param dict metadata: Any data you want to send along with
            transmission, used in WebHooks
        :param dict substitution_data: Corresponds to substitutions in
            html/text content. See `substitutions reference
            <https://www.sparkpost.com/docs/substitutions-reference>`_.
        :param attachments: List of dicts. For example:

            .. code-block:: python

                dict(
                    type='application/pdf',
                    name='document.pdf',
                    data='base64 encoded string'
                )

            Replace `data` with `filename` if you want the library to perform
            the base64 conversion. For example:

            .. code-block:: python

                dict(
                    type='application/pdf',
                    name='document.pdf',
                    filename='/full/path/to/document.pdf'
                )
        :param inline_images: List of dicts. For example:

            .. code-block:: python

                dict(
                    type='image/png',
                    name='imageCID',
                    data='base64 encoded string'
                )

            Replace `data` with `filename` if you want the library to perform
            the base64 conversion. For example:

            .. code-block:: python

                dict(
                    type='image/png',
                    name='imageCID',
                    filename='/full/path/to/image.png'
                )

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
        :param str ip_pool: The name of a dedicated IP pool associated with
            your account
        :param bool inline_css: Whether or not to perform CSS inlining
        :param dict custom_headers: Used to set any headers associated with
            transmission

        :returns: a ``dict`` with the ID and number of accepted and rejected
            recipients
        :raises: :exc:`SparkPostAPIException` if transmission cannot be sent
        """

        payload = self._translate_keys(**kwargs)
        results = self.request('POST', self.uri, data=json.dumps(payload))
        return results

    def _fetch_get(self, transmission_id):
        uri = "%s/%s" % (self.uri, transmission_id)
        results = self.request('GET', uri)
        return results

    def get(self, transmission_id):
        """
        Get a transmission by ID

        :param str transmission_id: ID of the transmission you want to retrieve

        :returns: the requested transmission if found
        :raises: :exc:`SparkPostAPIException` if transmission is not found
        """
        results = self._fetch_get(transmission_id)
        return results['transmission']

    def list(self):
        """
        Get a list of your transmissions

        :returns: list of transmissions
        :raises: :exc:`SparkPostAPIException` if API call fails
        """
        results = self.request('GET', self.uri)
        return results

    def delete(self, transmission_id):
        """
        Delete a transmission by ID

        :param str transmission_id: ID of the transmission you want to delete

        :returns: {}  if transmission is deleted
        :raises: :exc:`SparkPostAPIException` if transmission is not found
            or Canceled
        """
        uri = "%s/%s" % (self.uri, transmission_id)
        results = self.request('DELETE', uri)
        return results
