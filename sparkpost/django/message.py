from django.core.mail import EmailMultiAlternatives

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
        formatted = {
            'recipients': message.to,
            'from_email': message.from_email,
            'subject': message.subject,
            'text': message.body
        }

        if message.cc:
            formatted['cc'] = message.cc

        if message.bcc:
            formatted['bcc'] = message.bcc

        if message.reply_to:
            formatted['reply_to'] = message.reply_to

        if isinstance(message, EmailMultiAlternatives):
            for alternative in message.alternatives:
                if alternative[1] == 'text/html':
                    formatted['html'] = alternative[0]
                else:
                    raise UnsupportedContent(
                        'Content type %s is not supported' % alternative[1]
                    )

        if message.attachments:
            raise UnsupportedContent(
                'The SparkPost Django email backend does not '
                'currently support attachment.'
            )

        return super(SparkPostMessage, self).__init__(formatted)
