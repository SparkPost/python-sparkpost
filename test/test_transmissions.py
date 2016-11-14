import base64
import json
import os
import tempfile

import pytest
import responses
import six

from sparkpost import SparkPost
from sparkpost import Transmissions
from sparkpost.exceptions import SparkPostAPIException


def test_translate_keys_with_list():
    t = Transmissions('uri', 'key')
    results = t._translate_keys(recipient_list='test')
    assert results['return_path'] == 'default@sparkpostmail.com'
    assert results['content']['use_draft_template'] is False
    assert results['recipients'] == {'list_id': 'test'}


def test_translate_keys_with_recips():
    t = Transmissions('uri', 'key')
    results = t._translate_keys(recipients=['test',
                                            {'key': 'value'}, 'foobar'])
    assert results['recipients'] == [{'address': {'email': 'test'}},
                                     {'key': 'value'},
                                     {'address': {'email': 'foobar'}}]


def test_translate_keys_with_unicode_recips():
    t = Transmissions('uri', 'key')
    results = t._translate_keys(recipients=[u'unicode_email@example.com',
                                            'str_email@example.com'])
    assert results['recipients'] == [
        {'address': {'email': 'unicode_email@example.com'}},
        {'address': {'email': 'str_email@example.com'}}
    ]


def test_translate_keys_for_email_parsing():
    t = Transmissions('uri', 'key')
    results = t._translate_keys(recipients=['hansel@example.com',
                                            'Gretel <gretel@example.com>'])
    assert results['recipients'] == [
        {'address': {'email': 'hansel@example.com'}},
        {'address': {'name': 'Gretel', 'email': 'gretel@example.com'}}
    ]


def test_translate_keys_for_from_email():
    t = Transmissions('uri', 'key')
    results = t._translate_keys(from_email='Testing <testing@example.com>')
    assert results['content']['from'] == {
        'name': 'Testing',
        'email': 'testing@example.com'
    }


def test_format_header_to():
    t = Transmissions('uri', 'key')
    formatted = t._format_header_to(recipient={
        'address': {'email': 'primary@example.com'}
    })
    assert formatted == 'primary@example.com'

    formatted = t._format_header_to(recipient={
        'address': {'name': 'Testing', 'email': 'primary@example.com'}
    })
    assert formatted == '"Testing" <primary@example.com>'


def test_cc_with_sub_data():
    t = Transmissions('uri', 'key')
    results = t._translate_keys(
        recipients=[{
            'address': {'email': 'primary@example.com'},
            'substitution_data': {'fake': 'data'}
        }],
        cc=['ccone@example.com']
    )
    assert results['recipients'] == [
        {
            'address': {'email': 'primary@example.com'},
            'substitution_data': {'fake': 'data'}
        },
        {
            'address': {
                'email': 'ccone@example.com',
                'header_to': 'primary@example.com'
            },
            'substitution_data': {'fake': 'data'}
        }
    ]


def test_translate_keys_with_cc():
    t = Transmissions('uri', 'key')
    results = t._translate_keys(recipients=['primary@example.com'],
                                cc=['ccone@example.com'])
    assert results['recipients'] == [
        {'address': {'email': 'primary@example.com'}},
        {'address': {'email': 'ccone@example.com',
                     'header_to': 'primary@example.com'}},
    ]
    assert results['content']['headers'] == {
        'CC': 'ccone@example.com'
    }


def test_translate_keys_with_multiple_cc():
    t = Transmissions('uri', 'key')
    results = t._translate_keys(recipients=['primary@example.com'],
                                cc=['ccone@example.com', 'cctwo@example.com'])
    assert results['recipients'] == [
        {'address': {'email': 'primary@example.com'}},
        {'address': {'email': 'ccone@example.com',
                     'header_to': 'primary@example.com'}},
        {'address': {'email': 'cctwo@example.com',
                     'header_to': 'primary@example.com'}},
    ]
    assert results['content']['headers'] == {
        'CC': 'ccone@example.com,cctwo@example.com'
    }


def test_translate_keys_with_bcc():
    t = Transmissions('uri', 'key')
    results = t._translate_keys(recipients=['primary@example.com'],
                                bcc=['bccone@example.com'])
    assert results['recipients'] == [
        {'address': {'email': 'primary@example.com'}},
        {'address': {'email': 'bccone@example.com',
                     'header_to': 'primary@example.com'}},
    ]


def test_translate_keys_with_inline_css():
    t = Transmissions('uri', 'key')
    results = t._translate_keys(inline_css=True)
    assert results['options'].get('inline_css') is True


@responses.activate
def test_success_send():
    responses.add(
        responses.POST,
        'https://api.sparkpost.com/api/v1/transmissions',
        status=200,
        content_type='application/json',
        body='{"results": "yay"}'
    )
    sp = SparkPost('fake-key')
    results = sp.transmission.send()
    assert results == 'yay'


@responses.activate
def test_success_send_with_attachments():
    try:
        # Let's compare unicode for Python 2 / 3 compatibility
        test_content = six.u("Hello \nWorld\n")
        (_, temp_file_path) = tempfile.mkstemp()
        with open(temp_file_path, "w") as temp_file:
            temp_file.write(test_content)

        responses.add(
            responses.POST,
            'https://api.sparkpost.com/api/v1/transmissions',
            status=200,
            content_type='application/json',
            body='{"results": "yay"}'
        )
        sp = SparkPost('fake-key')

        attachment = {
            "name": "test.txt",
            "type": "text/plain",
            "filename": temp_file_path
        }
        results = sp.transmission.send(attachments=[attachment])

        request_params = json.loads(responses.calls[0].request.body)
        content = base64.b64decode(
            request_params["content"]["attachments"][0]["data"])
        # Let's compare unicode for Python 2 / 3 compatibility
        assert test_content == content.decode("ascii")

        assert results == 'yay'

        attachment = {
            "name": "test.txt",
            "type": "text/plain",
            "data": base64.b64encode(
                test_content.encode("ascii")).decode("ascii")
        }
        results = sp.transmission.send(attachments=[attachment])

        request_params = json.loads(responses.calls[1].request.body)
        content = base64.b64decode(
            request_params["content"]["attachments"][0]["data"])
        # Let's compare unicode for Python 2 / 3 compatibility
        assert test_content == content.decode("ascii")

        assert results == 'yay'
    finally:
        os.unlink(temp_file_path)


@responses.activate
def test_success_send_with_inline_images():
    current_dir = os.path.abspath(os.path.dirname(__file__))
    image_path = os.path.join(current_dir, 'assets', 'sparkpostdev.png')

    with open(image_path, "rb") as image:
        encoded_image = base64.b64encode(image.read()).decode("ascii")

    responses.add(
        responses.POST,
        'https://api.sparkpost.com/api/v1/transmissions',
        status=200,
        content_type='application/json',
        body='{"results": "yay"}'
    )
    sp = SparkPost('fake-key')

    image_data = {
        "name": "sparkpostdev",
        "type": "image/png",
        "filename": image_path
    }
    results = sp.transmission.send(inline_images=[image_data])
    request_params = json.loads(responses.calls[0].request.body)
    content = request_params["content"]["inline_images"][0]["data"]

    assert encoded_image == content
    assert results == 'yay'

    image_data = {
        "name": "sparkpostdev",
        "type": "image/png",
        "data": encoded_image
    }
    results = sp.transmission.send(inline_images=[image_data])
    request_params = json.loads(responses.calls[1].request.body)
    content = request_params["content"]["inline_images"][0]["data"]

    assert content == encoded_image
    assert results == 'yay'


@responses.activate
def test_fail_send():
    responses.add(
        responses.POST,
        'https://api.sparkpost.com/api/v1/transmissions',
        status=500,
        content_type='application/json',
        body="""
        {"errors": [{"message": "You failed", "description": "More Info"}]}
        """
    )
    with pytest.raises(SparkPostAPIException):
        sp = SparkPost('fake-key')
        sp.transmission.send()


@responses.activate
def test_success_get():
    responses.add(
        responses.GET,
        'https://api.sparkpost.com/api/v1/transmissions/foobar',
        status=200,
        content_type='application/json',
        body='{"results": {"transmission": {}}}'
    )
    sp = SparkPost('fake-key')
    results = sp.transmission.get('foobar')
    assert results == {}


@responses.activate
def test_fail_get():
    responses.add(
        responses.GET,
        'https://api.sparkpost.com/api/v1/transmissions/foobar',
        status=404,
        content_type='application/json',
        body="""
        {"errors": [{"message": "cant find", "description": "where you go"}]}
        """
    )
    with pytest.raises(SparkPostAPIException):
        sp = SparkPost('fake-key')
        sp.transmission.get('foobar')


@responses.activate
def test_success_list():
    responses.add(
        responses.GET,
        'https://api.sparkpost.com/api/v1/transmissions',
        status=200,
        content_type='application/json',
        body='{"results": []}'
    )
    sp = SparkPost('fake-key')
    response = sp.transmission.list()
    assert response == []


@responses.activate
def test_success_delete():
    responses.add(
        responses.DELETE,
        'https://api.sparkpost.com/api/v1/transmissions/foobar',
        status=200,
        content_type='application/json',
        body='{}'
    )
    sp = SparkPost('fake-key')
    results = sp.transmission.delete('foobar')
    assert results == {}


@responses.activate
def test_fail_delete():
    responses.add(
        responses.DELETE,
        'https://api.sparkpost.com/api/v1/transmissions/foobar',
        status=404,
        content_type='application/json',
        body="""
        {"errors": [{"message": "resource not found",
            "description": "Resource not found:transmission id foobar""}]}
        """
    )
    with pytest.raises(SparkPostAPIException):
        sp = SparkPost('fake-key')
        sp.transmission.delete('foobar')
