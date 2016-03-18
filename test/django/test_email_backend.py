import pytest
import mock

from django.conf import settings
from django.core.mail import send_mail
from django.core.mail import send_mass_mail
from django.core.mail import EmailMultiAlternatives
from django.utils.functional import empty

from sparkpost.django.email_backend import SparkPostEmailBackend
from sparkpost.django.exceptions import UnsupportedContent
from sparkpost.transmissions import Transmissions

API_KEY = 'API_Key'


def reconfigure_settings(**new_settings):
    old_settings = settings._wrapped

    settings._wrapped = empty
    settings.configure(default_settings=old_settings, **new_settings)


reconfigure_settings(
    DEBUG=True,
    EMAIL_BACKEND='sparkpost.django.email_backend.SparkPostEmailBackend',
    SPARKPOST_API_KEY=API_KEY
)


def get_params(overrides=None):
    if overrides is None:
        overrides = {}

    defaults = {
        'subject': 'test subject',
        'message': 'test body',
        'from_email': 'from@example.com',
        'recipient_list': ['to@example.com'],
    }

    params = defaults.copy()
    params.update(overrides)
    return params


def mailer(params):
    return send_mail(**params)


def test_password_retrieval():
    backend = SparkPostEmailBackend()
    assert backend.client.api_key == API_KEY


def test_fail_silently():
    # should not raise
    with mock.patch.object(Transmissions, 'send') as mock_send:
        mock_send.side_effect = Exception('i should not be raised')
        mailer(get_params({'fail_silently': True}))

    # should raise
    with mock.patch.object(Transmissions, 'send') as mock_send:
        mock_send.side_effect = Exception('i should be raised')
        with pytest.raises(Exception):
            mailer(get_params())


def test_successful_sending():
    with mock.patch.object(Transmissions, 'send') as mock_send:
        mock_send.return_value = {'total_accepted_recipients': 1,
                                  'total_rejected_recipients': 2}

        result = mailer(get_params({
            'recipient_list': ['to1@example.com', 'to2@example.com'],
            'fail_silently': True
        }))
        assert result == 1

    with mock.patch.object(Transmissions, 'send') as mock_send:
        mock_send.return_value = {'total_accepted_recipients': 10,
                                  'total_rejected_recipients': 2}

        result = mailer(
            get_params(
                {'recipient_list': ['to1@example.com', 'to2@example.com'],
                 'fail_silently': True
                 }
            ))

        assert result == 10


def test_send_number_of_emails_correctly():
    with mock.patch.object(Transmissions, 'send') as mock_send:
        mailer(get_params({
            'recipient_list': ['to1@example.com', 'to2@example.com'],
            'fail_silently': True
        }))
        assert mock_send.call_count == 1

    with mock.patch.object(Transmissions, 'send') as mock_send:
        message1 = ('message 1 subject', 'message 1 body', 'from@example.com',
                    ['to1@example.com'])
        message2 = ('message 2 subject', 'message 2 body', 'from@example.com',
                    ['to2@example.com'])
        message3 = ('message 3 subject', 'message 3 body', 'from@example.com',
                    ['to3@example.com'])

        send_mass_mail((message1, message2, message3), fail_silently=False)
        assert mock_send.call_count == 3


def test_params():
    recipients = ['to1@example.com', 'to2@example.com']
    with mock.patch.object(Transmissions, 'send'):
        mailer(get_params(
            {'recipient_list': recipients,
             'fail_silently': True
             }
        ))

        Transmissions.send.assert_called_with(recipients=recipients,
                                              text='test body',
                                              from_email='from@example.com',
                                              subject='test subject'
                                              )


def test_content_types():
    def new_send(**kwargs):
        assert kwargs['text'] == 'hello there'
        assert kwargs['html'] == '<p>Hello There</p>'

        return {
            'total_accepted_recipients': 0,
            'total_rejected_recipients': 0
        }

    with mock.patch.object(Transmissions, 'send') as mock_send:
        mock_send.side_effect = new_send
        send_mail(
            'test subject',
            'hello there',
            'from@example.com',
            ['to@example.com'],
            html_message='<p>Hello There</p>'
        )


def test_send_plain_mail_after_html_mail():
    SPARKPOST_OPTIONS = {
        'track_opens': False,
        'track_clicks': False,
        'transactional': True,
    }

    reconfigure_settings(SPARKPOST_OPTIONS=SPARKPOST_OPTIONS)

    def new_send(**kwargs):
        assert kwargs['text'] == 'hello there'
        assert kwargs['html'] == '<p>Hello There</p>'

        return {
            'total_accepted_recipients': 0,
            'total_rejected_recipients': 0
        }

    def new_send_text_only(**kwargs):
        assert kwargs['text'] == 'hello there again in text only'
        assert "html" not in kwargs

        return {
            'total_accepted_recipients': 0,
            'total_rejected_recipients': 0
        }

    with mock.patch.object(Transmissions, 'send') as mock_send:
        mock_send.side_effect = new_send
        send_mail(
            'test subject',
            'hello there',
            'from@example.com',
            ['to@example.com'],
            html_message='<p>Hello There</p>'
        )
        mock_send.side_effect = new_send_text_only
        send_mail(
            'test subject 2',
            'hello there again in text only',
            'from@example.com',
            ['to@example.com'],
        )


def test_unsupported_content_types():
    params = get_params()

    with pytest.raises(UnsupportedContent):
        mail = EmailMultiAlternatives(
            params['subject'],
            'plain text',
            params['from_email'],
            params['recipient_list'])
        mail.attach_alternative('<ppp>non-plain content</ppp>', 'text/alien')
        mail.send()


def test_settings_options():
    SPARKPOST_OPTIONS = {
        'track_opens': False,
        'track_clicks': False,
        'transactional': True,
    }

    reconfigure_settings(SPARKPOST_OPTIONS=SPARKPOST_OPTIONS)

    with mock.patch.object(Transmissions, 'send'):
        mailer(get_params())
        expected_kargs = get_params().copy()
        expected_kargs["text"] = expected_kargs["message"]
        expected_kargs["recipients"] = expected_kargs["recipient_list"]
        del expected_kargs["message"]
        del expected_kargs["recipient_list"]
        expected_kargs.update(SPARKPOST_OPTIONS)
        Transmissions.send.assert_called_with(**expected_kargs)
