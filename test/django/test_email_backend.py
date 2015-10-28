from sparkpost.django.email_backend import SparkPostEmailBackend
from sparkpost.transmissions import Transmissions
from django.conf import settings
from django.core.mail import send_mail, send_mass_mail
import pytest

import mock

API_KEY = 'API_Key'

settings.configure(
    DEBUG=True,
    EMAIL_BACKEND='sparkpost.django.email_backend.SparkPostEmailBackend',
    SP_PASSWORD=API_KEY
)


def mailer(to=None, fail_silently=False):
    if not to:
        to = ['to@example.com']

    return send_mail(subject='test subject',
                     message='test body',
                     from_email='from@example.com',
                     recipient_list=to,
                     fail_silently=fail_silently)


def test_password_retrieval():
    backend = SparkPostEmailBackend()
    assert backend.client.api_key == API_KEY


def test_fail_silently():
    # should not raise
    with mock.patch.object(Transmissions, 'send') as mock_send:
        mock_send.side_effect = Exception('i should not be raised')
        mailer(fail_silently=True)

    # should raise
    with mock.patch.object(Transmissions, 'send') as mock_send:
        mock_send.side_effect = Exception('i should be raised')
        with pytest.raises(Exception):
            mailer()


def test_successful_sending():
    with mock.patch.object(Transmissions, 'send') as mock_send:
        mock_send.return_value = {'total_accepted_recipients': 1,
                                  'total_rejected_recipients': 2}

        result = mailer(to=['to1@example.com', 'to2@example.com'],
                        fail_silently=True)

        assert result == 1

    with mock.patch.object(Transmissions, 'send') as mock_send:
        mock_send.return_value = {'total_accepted_recipients': 10,
                                  'total_rejected_recipients': 2}

        result = mailer(to=['to1@example.com', 'to2@example.com'],
                        fail_silently=True)

        assert result == 10


def test_send_number_of_emails_correctly():
    with mock.patch.object(Transmissions, 'send') as mock_send:
        mailer(to=['to1@example.com', 'to2@example.com'], fail_silently=True)
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
        mailer(to=recipients, fail_silently=True)

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
        send_mail('test subject',
                  'hello there',
                  'from@example.com',
                  ['to@example.com'],
                  html_message='<p>Hello There</p>'
              )

