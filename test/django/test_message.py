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


def test_campaign():
    email_message = EmailMessage(**base_options)
    email_message.campaign = 'campaign-id'
    actual = SparkPostMessage(email_message)
    expected = dict(
        campaign='campaign-id'
    )
    expected.update(base_expected)
    assert actual == expected


def test_recipient_attributes():
    email_message = EmailMessage(
        to=[
            {
                'address': 'to@example.com',
                'substitution_data': {
                    'sub': 'value'
                },
                'metadata': {
                    'meta': 'value'
                },
                'tags': ['tag1']
            }
        ],
        from_email='test@from.com'
    )

    email_message.template = 'template-id'
    actual = SparkPostMessage(email_message)

    expected = dict(
        recipients=[
            {
                'address': 'to@example.com',
                'substitution_data': {
                    'sub': 'value'
                },
                'metadata': {
                    'meta': 'value'
                },
                'tags': ['tag1']
            }
        ],
        from_email='test@from.com',
        template='template-id'
    )

    assert actual == expected


def test_pass_through_attr():

    pass_through_attributes = {
      'substitution_data': {'sub': 'vale'},
      'metadata': {'meta': 'value'},
      'description': 'a description',
      'return_path': 'return@path.com',
      'ip_pool': 'pool-id',
      'inline_css': True,
      'transactional': True,
      'start_time': 'YYYY-MM-DDTHH:MM:SS+-HH:MM',
      'skip_suppression': True
    }

    email_message = EmailMessage(
        to=[{'address': 'to@example.com'}],
        from_email='test@from.com'
    )
    email_message.template = 'template-id'

    for key, value in pass_through_attributes.items():
        setattr(email_message, key, value)

    actual = SparkPostMessage(email_message)

    expected = dict(
        recipients=[{'address': 'to@example.com'}],
        from_email='test@from.com',
        template='template-id',
    )

    for key, value in pass_through_attributes.items():
        expected[key] = value

    assert actual == expected


def test_transform_attr():

    attributes_to_transform = {
        'sandbox': True,
        'open_tracking': False,
        'click_tracking': False,
    }

    email_message = EmailMessage(
        to=[{'address': 'to@example.com'}],
        from_email='test@from.com'
    )
    email_message.template = 'template-id'

    for key, value in attributes_to_transform.items():
        setattr(email_message, key, value)

    actual = SparkPostMessage(email_message)

    expected = dict(
        recipients=[{'address': 'to@example.com'}],
        from_email='test@from.com',
        template='template-id',
    )

    transformed_attributes = {
        'use_sandbox': True,
        'track_opens': False,
        'track_clicks': False
    }

    for key, value in transformed_attributes.items():
        expected[key] = value

    assert actual == expected


if at_least_version('1.8'):
    def test_reply_to():
        expected = dict(
            reply_to='replyone@example.com,replytwo@example.com'
        )
        expected.update(base_expected)

        assert message(reply_to=['replyone@example.com',
                                 'replytwo@example.com']) == expected


def test_extra_headers():
    email_message = EmailMessage(**base_options)
    email_message.extra_headers['FOO'] = 'bar'

    actual = SparkPostMessage(email_message)
    expected = dict(
        custom_headers={'FOO': 'bar'},
    )
    expected.update(base_expected)
    assert actual == expected


def test_transactional():
    email_message = EmailMessage(**base_options)
    import json
    msys_api = json.dumps({'options': {'transactional': True}})
    email_message.extra_headers['X-MSYS-API'] = msys_api

    actual = SparkPostMessage(email_message)
    expected = dict(
        custom_headers={'X-MSYS-API': msys_api},
        transactional=True,
    )
    expected.update(base_expected)
    assert actual == expected
