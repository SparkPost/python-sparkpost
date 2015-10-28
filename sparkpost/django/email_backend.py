from django.core.mail.backends.base import BaseEmailBackend
from sparkpost import SparkPost
from django.conf import settings
from . import UnSupportedFormat


class SparkPostEmailBackend(BaseEmailBackend):
    """
    SparkPost wrapper for Django email backend
    """

    def __init__(self, fail_silently=False, **kwargs):
        super(SparkPostEmailBackend, self)\
            .__init__(fail_silently=fail_silently, **kwargs)

        sp_password = getattr(settings, 'SP_PASSWORD', None)

        self.client = SparkPost(sp_password)

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
                    raise UnSupportedFormat('Content type %s is not supported' % alternative[1])

        return self.client.transmissions.send(**params)
