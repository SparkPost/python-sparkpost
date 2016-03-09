try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

import pytest
from django.core.mail import EmailMultiAlternatives
from django.core.mail.message import EmailMessage

from sparkpost.django.exceptions import UnsupportedContent
from sparkpost.django.message import SparkPostMessage


def message(**extras):
    options = dict(
        subject='Test',
        body='Testing',
        from_email='test@from.com',
        to=['recipient@example.com']
    )
    options.update(extras)
    email_message = EmailMessage(**options)
    return SparkPostMessage(email_message)


def multipart_message(**extras):
    options = dict(
        subject='Test',
        body='Testing',
        from_email='test@from.com',
        to=['recipient@example.com']
    )
    options.update(extras)
    email_message = EmailMultiAlternatives(**options)
    email_message.attach_alternative('<p>Testing</p>', 'text/html')
    return SparkPostMessage(email_message)


def test_minimal():
    expected = dict(
        recipients=['recipient@example.com'],
        from_email='test@from.com',
        subject='Test',
        text='Testing'
    )
    assert message() == expected


def test_multipart():
    expected = dict(
        recipients=['recipient@example.com'],
        from_email='test@from.com',
        subject='Test',
        text='Testing',
        html='<p>Testing</p>'
    )
    assert multipart_message() == expected


def test_cc_bcc_reply_to():
    expected = dict(
        recipients=['recipient@example.com'],
        from_email='test@from.com',
        subject='Test',
        text='Testing',
        cc=['ccone@example.com'],
        bcc=['bccone@example.com'],
        reply_to=['replyto@example.com']
    )

    extras = dict(cc=['ccone@example.com'],
                  bcc=['bccone@example.com'],
                  reply_to=['replyto@example.com'])
    assert message(**extras) == expected


def test_attachment():
    options = dict(
        subject='Test',
        body='Testing',
        from_email='test@from.com',
        to=['recipient@example.com']
    )

    attachment = StringIO()
    attachment.write('hello file')
    email_message = EmailMessage(**options)
    email_message.attach('file.txt', attachment, 'text/plain')

    with pytest.raises(UnsupportedContent):
        SparkPostMessage(email_message)
