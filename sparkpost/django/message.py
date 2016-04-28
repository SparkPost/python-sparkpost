import mimetypes
from base64 import b64encode

from django.core.mail import EmailMultiAlternatives
from django.core.mail.message import DEFAULT_ATTACHMENT_MIME_TYPE
from django.conf import settings

from .exceptions import UnsupportedContent


class SparkPostMessage(dict):
    """
    Takes a Django EmailMessage and formats it for use with the SparkPost API.

    The dictionary returned would be formatted like this:

    {
        'recipients': ['recipient@example.com'],
        'from_email': 'from@example.com',
        'text': 'Hello world',
        'html': '<p>Hello world</p>',
        'subject': 'Hello from the SparkPost Django email backend'
    }
    """

    def __init__(self, message):
        formatted = dict()

        if message.to:
            formatted['recipients'] = message.to

        if message.from_email:
            formatted['from_email'] = message.from_email

        if message.subject:
            formatted['subject'] = message.subject

        if hasattr(message, 'template'):
            formatted['template'] = message.template
        elif message.content_subtype == 'html':
            formatted['html'] = message.body
        else:
            formatted['text'] = message.body

        if message.cc:
            formatted['cc'] = message.cc

        if message.bcc:
            formatted['bcc'] = message.bcc

        if hasattr(message, 'reply_to') and message.reply_to:
            formatted['reply_to'] = ','.join(message.reply_to)

        if isinstance(message, EmailMultiAlternatives):
            for alternative in message.alternatives:
                if alternative[1] == 'text/html':
                    formatted['html'] = alternative[0]
                else:
                    raise UnsupportedContent(
                        'Content type %s is not supported' % alternative[1]
                    )

        if message.attachments:
            formatted['attachments'] = []
            str_encoding = settings.DEFAULT_CHARSET
            for attachment in message.attachments:
                filename, content, mimetype = attachment

                if mimetype is None:
                    mimetype, _ = mimetypes.guess_type(filename)
                    if mimetype is None:
                        mimetype = DEFAULT_ATTACHMENT_MIME_TYPE

                try:
                    if isinstance(content, unicode):
                        content = content.encode(str_encoding)
                except NameError:
                    if isinstance(content, str):
                        content = content.encode(str_encoding)
                base64_encoded_content = b64encode(content)
                formatted['attachments'].append({
                    'name': filename,
                    'data': base64_encoded_content.decode('ascii'),
                    'type': mimetype
                })

        if hasattr(message, 'substitution_data'):
            formatted['substitution_data'] = message.substitution_data

        super(SparkPostMessage, self).__init__(formatted)
