import base64
import json
import os
import tempfile

import pytest
import six

from sparkpost.tornado import SparkPost, SparkPostAPIException
from tornado import ioloop
from .utils import AsyncClientMock

responses = AsyncClientMock()


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
    results = ioloop.IOLoop().run_sync(sp.transmission.send)
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

        def send():
            return sp.transmission.send(attachments=[attachment])
        results = ioloop.IOLoop().run_sync(send)

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

        def send():
            return sp.transmission.send(attachments=[attachment])
        results = ioloop.IOLoop().run_sync(send)

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
        ioloop.IOLoop().run_sync(sp.transmission.send)


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

    def send():
        return sp.transmission.get('foobar')
    results = ioloop.IOLoop().run_sync(send, timeout=3)
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

        def send():
            return sp.transmission.get('foobar')
        ioloop.IOLoop().run_sync(send, timeout=3)


@responses.activate
def test_nocontent_get():
    responses.add(
        responses.GET,
        'https://api.sparkpost.com/api/v1/transmissions',
        status=204,
        content_type='application/json',
        body=''
    )
    sp = SparkPost('fake-key')
    response = ioloop.IOLoop().run_sync(sp.transmission.list)
    assert response is True


@responses.activate
def test_brokenjson_get():
    responses.add(
        responses.GET,
        'https://api.sparkpost.com/api/v1/transmissions',
        status=200,
        content_type='application/json',
        body='{"results":'
    )
    with pytest.raises(SparkPostAPIException):
        sp = SparkPost('fake-key')
        ioloop.IOLoop().run_sync(sp.transmission.list)


@responses.activate
def test_noresults_get():
    responses.add(
        responses.GET,
        'https://api.sparkpost.com/api/v1/transmissions',
        status=200,
        content_type='application/json',
        body='{"ok": false}'
    )
    sp = SparkPost('fake-key')
    response = ioloop.IOLoop().run_sync(sp.transmission.list)
    assert response == {"ok": False}


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
    response = ioloop.IOLoop().run_sync(sp.transmission.list)
    assert response == []
