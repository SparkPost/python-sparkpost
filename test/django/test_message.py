from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.core.mail.message import EmailMessage
from django.utils.functional import empty

from sparkpost.django.message import SparkPostMessage
from .utils import at_least_version


def reconfigure_settings(**new_settings):
    old_settings = settings._wrapped

    settings._wrapped = empty
    settings.configure(default_settings=old_settings, **new_settings)


reconfigure_settings(
    DEFAULT_CHARSET='utf-8'
)


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
    email_message = EmailMessage(**base_options)
    email_message.attach('file.txt', 'test content', 'text/plain')

    actual = SparkPostMessage(email_message)
    expected = dict(
        attachments=[
            {
                'name': 'file.txt',
                'data': 'dGVzdCBjb250ZW50',
                'type': 'text/plain'
            }
        ]
    )
    expected.update(base_expected)
    assert actual == expected


def test_attachment_unicode():
    email_message = EmailMessage(**base_options)
    email_message.attach('file.txt', u'test content', 'text/plain')

    actual = SparkPostMessage(email_message)
    expected = dict(
        attachments=[
            {
                'name': 'file.txt',
                'data': 'dGVzdCBjb250ZW50',
                'type': 'text/plain'
            }
        ]
    )
    expected.update(base_expected)
    assert actual == expected


def test_attachment_guess_mimetype():
    email_message = EmailMessage(**base_options)
    email_message.attach('file.txt', 'test content')

    actual = SparkPostMessage(email_message)
    expected = dict(
        attachments=[
            {
                'name': 'file.txt',
                'data': 'dGVzdCBjb250ZW50',
                'type': 'text/plain'
            }
        ]
    )
    expected.update(base_expected)
    assert actual == expected


def test_attachment_guess_mimetype_fallback():
    email_message = EmailMessage(**base_options)
    email_message.attach('file', 'test content')

    actual = SparkPostMessage(email_message)
    expected = dict(
        attachments=[
            {
                'name': 'file',
                'data': 'dGVzdCBjb250ZW50',
                'type': 'application/octet-stream'
            }
        ]
    )
    expected.update(base_expected)
    assert actual == expected


def test_content_subtype():
    email_message = EmailMessage(
        to=['to@example.com'],
        from_email='test@from.com',
        body='<p>Testing</p>'
    )
    email_message.content_subtype = 'html'
    actual = SparkPostMessage(email_message)
    expected = dict(
        recipients=['to@example.com'],
        from_email='test@from.com',
        html='<p>Testing</p>'
    )
    assert actual == expected


def test_template():
    email_message = EmailMessage(
        to=['to@example.com'],
        from_email='test@from.com'
    )
    email_message.template = 'template-id'
    actual = SparkPostMessage(email_message)
    expected = dict(
        recipients=['to@example.com'],
        from_email='test@from.com',
        template='template-id'
    )
    assert actual == expected


def test_substitution_data():
    email_message = EmailMessage(
        to=[
            {
                "address": "to@example.com",
                "substitution_data": {
                    "key": "value"
                }
            }
        ],
        from_email='test@from.com'
    )
    email_message.template = 'template-id'
    email_message.substitution_data = {"key2": "value2"}
    actual = SparkPostMessage(email_message)

    expected = dict(
        recipients=[
            {
                "address": "to@example.com",
                "substitution_data": {
                    "key": "value"
                }
            }
        ],
        from_email='test@from.com',
        template='template-id',
        substitution_data={"key2": "value2"}
    )

    assert actual == expected


if at_least_version('1.8'):
    def test_reply_to():
        expected = dict(
            reply_to='replyone@example.com,replytwo@example.com'
        )
        expected.update(base_expected)

        assert message(reply_to=['replyone@example.com',
                                 'replytwo@example.com']) == expected
