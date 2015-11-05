from django.conf import settings
from django.core.mail.backends.base import BaseEmailBackend

from sparkpost import SparkPost

from .exceptions import UnsupportedContent
from .exceptions import UnsupportedParam


class SparkPostEmailBackend(BaseEmailBackend):
    """
    SparkPost wrapper for Django email backend
    """

    def __init__(self, fail_silently=False, **kwargs):
        super(SparkPostEmailBackend, self)\
            .__init__(fail_silently=fail_silently, **kwargs)

        sp_api_key = getattr(settings, 'SPARKPOST_API_KEY', None)

        self.client = SparkPost(sp_api_key)

    def send_messages(self, email_messages):
        """
        Send emails, returns integer representing number of successful emails
        """
        success = 0
        for message in email_messages:
            try:
                response = self._send(message)
                success += response['total_accepted_recipients']
            except Exception:
                if not self.fail_silently:
                    raise
        return success

    def _send(self, message):
        self.check_unsupported(message)
        self.check_attachments(message)

        params = dict(
            recipients=message.to,
            text=message.body,
            from_email=message.from_email,
            subject=message.subject
        )

        if hasattr(message, 'alternatives') and len(message.alternatives) > 0:
            for alternative in message.alternatives:

                if alternative[1] == 'text/html':
                    params['html'] = alternative[0]
                else:
                    raise UnsupportedContent(
                        'Content type %s is not supported' % alternative[1]
                    )

        return self.client.transmissions.send(**params)

    @staticmethod
    def check_attachments(message):
        if len(message.attachments):
            raise UnsupportedContent(
                'The SparkPost Django email backend does not '
                'currently support attachment.'
            )

    @staticmethod
    def check_unsupported(message):
        unsupported_params = ['cc', 'bcc', 'reply_to']
        for param in unsupported_params:
            if len(getattr(message, param, [])):
                raise UnsupportedParam(
                    'The SparkPost Django email backend does not currently '
                    'support %s.' % param
                )
