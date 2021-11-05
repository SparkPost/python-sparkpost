import base64
import copy
import json
import warnings
from email.utils import parseaddr

from .base import Resource
from .exceptions import SparkPostException


try:
    string_types = basestring
except NameError:
    string_types = str  # Python 3 doesn't have basestring


model_remap = {
    'campaign': 'campaign_id',
    'start_time': 'options/start_time',
    'track_opens': 'options/open_tracking',
    'track_initial_opens': 'options/initial_open',
    'track_clicks': 'options/click_tracking',
    'transactional': 'options/transactional',
    'use_sandbox': 'options/sandbox',
    'skip_suppression': 'options/skip_suppression',
    'ip_pool': 'options/ip_pool',
    'inline_css': 'options/inline_css',
    'perform_substitutions': 'options/perform_substitutions',
    'email_rfc822': 'content/email_rfc822',
    'custom_headers': 'content/headers',
    'use_draft_template': 'content/use_draft_template',
    'reply_to': 'content/reply_to',
    'subject': 'content/subject',
    'from_email': 'content/from',
    'html': 'content/html',
    'amp_html': 'content/amp_html',
    'text': 'content/text',
    'template': 'content/template_id',
    'attachments': 'content/attachments',
    'inline_images': 'content/inline_images',
    'recipient_list': 'recipients/list_id',
}
model_remap_keys = frozenset(model_remap.keys())


class Transmissions(Resource):
    """
    Transmission class used to send, list and get transmissions. For detailed
    request and response formats, see the `Transmissions API documentation
    <https://www.sparkpost.com/docs/transmissions-api>`_.
    """

    key = 'transmissions'

    def _translate_keys(self, **kwargs):
        model = copy.deepcopy(kwargs)

        # Intersection of keys that need to be remapped
        data_remap_keys = model_remap_keys.intersection(model.keys())

        for from_key in data_remap_keys:
            # Remap model keys to match API
            if from_key in model:
                to_model = model
                to_key = model_remap[from_key]
                if '/' in to_key:
                    # Nested within a dict
                    into_list = to_key.split('/')
                    to_key = into_list[-1]
                    to_model = model.setdefault(into_list[0], {})

                # Move from current key and place into new key
                to_model[to_key] = model.pop(from_key)

        content = model.setdefault('content', {})
        recipients = model.setdefault('recipients', [])

        if content.get('email_rfc822'):
            # Remove unnecessary keys from model['content'], if rfc822
            rfc822_keys = frozenset([
                'headers',
                'use_draft_template',
                'reply_to',
                'subject',
                'from',
                'html',
                'text',
                'template_id',
                'attachments',
                'inline_images',
            ])
            del_content_keys = rfc822_keys.intersection(content.keys())
            for key in del_content_keys:
                del content[key]

        if 'from' in content:
            from_email = content.get('from')
            if isinstance(from_email, string_types):
                content['from'] = self._parse_address(from_email)

        if 'attachments' in content:
            attachments = content.get('attachments')
            content['attachments'] = self._extract_attachments(attachments)

        if 'inline_images' in content:
            inline_images = content.get('inline_images')
            content['inline_images'] = self._extract_attachments(inline_images)

        if recipients and not isinstance(recipients, dict):
            model['recipients'] = self._extract_recipients(recipients)
            recipients = model['recipients']

            cc = model.pop('cc', None)
            if cc:
                headers = content.setdefault('headers', {})
                headers['CC'] = ','.join(cc)
                cc_copies = self._format_copies(recipients, cc)
                recipients.extend(cc_copies)

            bcc = model.pop('bcc', None)
            if bcc:
                bcc_copies = self._format_copies(recipients, bcc)
                recipients.extend(bcc_copies)

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

        if not (isinstance(recipients, (list, dict))):
            raise SparkPostException('recipients must be a list or dict')

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

        :param list|dict recipients: List of email addresses, or a dict:
            ``{'address': {'name': 'Kyla', 'email': 'hello@example.com' }}``
        :param str recipient_list: ID of recipient list. If this is set,
            the `recipients` param will be ignored
        :param cc: List of email addresses to send carbon copy to
        :param bcc: List of email addresses to send blind carbon copy to
        :param str template: ID of template to be used. Setting a template
            overrides the HTML and text params
        :param bool use_draft_template: Defaults to False. Set to true if you
            want to send a template that is a draft
        :param str html: HTML part of transmission
        :param str amp_html: AMP HTML part of the transmission
        :param str text: Text part of transmission
        :param str subject: Subject of transmission
        :param str from_email: Email that the transmission comes from. The
            domain must be a verified sending domain belonging to your account
            or the transmission will fail. You can pass a from email or both
            from name and from email - `testing@example.com` or
            `Test Email <testing@example.com>` will both work.
        :param str reply_to: Reply to of transmission
        :param str return_path: Email address to use for envelope FROM. The
            domain part of the return_path address must be a
            CNAME-verified sending domain.
        :param str description: Description of transmission
        :param str campaign: Campaign of transmission
        :param dict metadata: Any data you want to send along with
            transmission, used in WebHooks
        :param dict substitution_data: Corresponds to substitutions in
            html/text content. See `substitutions reference
            <https://developers.sparkpost.com/api/substitutions-reference>`_.
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
        :param bool track_initial_opens:  Used to track opens of
            transmission with top pixel
        :param bool track_clicks: Defaults to True. Used to track clicks of
            transmission
        :param bool use_sandbox: Flag must be set to use sandbox domain instead
            of verified sending domain. Limited to a lifetime of 50
            transmissions with this domain
        :param bool transactional: Whether message is transactional or
            non-transactional for unsubscribe and suppression purposes
        :param bool skip_suppression: Whether or not to ignore customer
            suppression rules, for this transmission only. Only applicable if
            your configuration supports this parameter. (Enterprise only)
        :param str ip_pool: The ID of an IP pool associated with
            your account
        :param bool inline_css: Whether or not to perform CSS inlining
        :param bool perform_substitutions: Whether or not to enable
            substitutions (default is True)
        :param dict custom_headers: Used to set any headers associated with
            transmission. See `header notes
            <https://developers.sparkpost.com/api/transmissions.html#header-header-notes>`_

        :returns: a ``dict`` with the transmission ID and number of accepted
            and rejected recipients
        :raises: :exc:`SparkPostAPIException` if transmission cannot be sent
        """

        payload = self._translate_keys(**kwargs)
        data = json.dumps(payload)
        results = self.request('POST', self.uri, data=data)
        return results

    def _fetch_get(self, transmission_id):
        uri = "%s/%s" % (self.uri, transmission_id)
        results = self.request('GET', uri)
        return results

    def get(self, transmission_id):
        """
        Get a transmission by ID

        :param str transmission_id: ID of the transmission you want to retrieve

        :returns: the requested transmission, if found
        :raises: :exc:`SparkPostAPIException` if transmission is not found
        """
        results = self._fetch_get(transmission_id)
        return results['transmission']

    def list(self, **kwargs):
        """
        Get a list of your transmissions. This method is deprecated.

        :param campaign_id: ID of the campaign used by the transmissions
        :param template_id: ID of the template used by the transmissions

        :returns: list of transmissions
        :raises: :exc:`SparkPostAPIException` if API call fails
        """
        warn_msg = 'This method is deprecated.'

        warnings.warn(warn_msg, DeprecationWarning)
        return self.request('GET', self.uri, params=kwargs)

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
