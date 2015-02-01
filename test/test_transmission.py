import pytest
import responses

from sparkpost import SparkPost
from sparkpost.exceptions import SparkPostAPIException


@responses.activate
def test_success_create():
    responses.add(
        responses.POST,
        'https://api.sparkpost.com/api/v1/transmissions',
        status=200,
        content_type='application/json',
        body='{"results": "yay"}'
    )
    sp = SparkPost('fake-key')
    results = sp.transmission.create()
    assert results == 'yay'


@responses.activate
def test_fail_create():
    responses.add(
        responses.POST,
        'https://api.sparkpost.com/api/v1/transmissions',
        status=500,
        content_type='application/json',
        body='{"errors": [{"message": "You failed"}]}'
    )
    with pytest.raises(SparkPostAPIException):
        sp = SparkPost('fake-key')
        sp.transmission.create()


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
        body='{"errors": [{"message": "cant find"}]}'
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
