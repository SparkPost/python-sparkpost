try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

import pytest
from django.core.mail import EmailMultiAlternatives
from django.core.mail.message import EmailMessage

from sparkpost.django.exceptions import UnsupportedContent
from sparkpost.django.message import SparkPostMessage
from .utils import at_least_version


base_options = dict(
    subject='Test',
    body='Testing',
    from_email='test@from.com',
    to=['recipient@example.com']
)


def message(**options):
    options.update(base_options)
    email_message = EmailMessage(**options)
    return SparkPostMessage(email_message)


def multipart_message(**options):
    options.update(base_options)
    email_message = EmailMultiAlternatives(**options)
    email_message.attach_alternative('<p>Testing</p>', 'text/html')
    return SparkPostMessage(email_message)


base_expected = dict(
    recipients=['recipient@example.com'],
    from_email='test@from.com',
    subject='Test',
    text='Testing'
)


def test_minimal():
    assert message() == base_expected


def test_multipart():
    expected = dict(
        html='<p>Testing</p>'
    )
    expected.update(base_expected)
    assert multipart_message() == expected


def test_cc_bcc():
    expected = dict(
        cc=['ccone@example.com'],
        bcc=['bccone@example.com']
    )
    expected.update(base_expected)

    options = dict(cc=['ccone@example.com'],
                   bcc=['bccone@example.com'])
    assert message(**options) == expected


def test_attachment():
    attachment = StringIO()
    attachment.write('hello file')
    email_message = EmailMessage(**base_options)
    email_message.attach('file.txt', attachment, 'text/plain')

    with pytest.raises(UnsupportedContent):
        SparkPostMessage(email_message)

if at_least_version('1.8'):
    def test_reply_to():
        expected = dict(
            reply_to=['replyto@example.com']
        )
        expected.update(base_expected)

        assert message(reply_to=['replyto@example.com']) == expected
