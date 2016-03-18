from django.conf import settings
from django.core.mail.backends.base import BaseEmailBackend

from sparkpost import SparkPost

from .message import SparkPostMessage


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
                response = self._send(SparkPostMessage(message))
                success += response['total_accepted_recipients']
            except Exception:
                if not self.fail_silently:
                    raise
        return success

    def _send(self, message):
        params = getattr(settings, 'SPARKPOST_OPTIONS', {}).copy()
        params.update(message)
        return self.client.transmissions.send(**params)
