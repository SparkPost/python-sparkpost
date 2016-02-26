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
