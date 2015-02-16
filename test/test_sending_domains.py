import pytest
import responses

from sparkpost import SparkPost
from sparkpost.exceptions import SparkPostAPIException


base_uri = SparkPost('fake-key').sending_domains.uri


@responses.activate
def test_success_get():
    responses.add(
        responses.GET,
        '%s/fake.com' % base_uri,
        status=200,
        content_type='application/json',
        body='{"results": {}}'
    )
    sp = SparkPost('fake-key')
    results = sp.sending_domains.get('fake.com')
    assert results == {}


@responses.activate
def test_fail_get():
    responses.add(
        responses.GET,
        '%s/fake.com' % base_uri,
        status=404,
        content_type='application/json',
        body='{"errors": [{"message": "cannot find"}]}'
    )
    with pytest.raises(SparkPostAPIException):
        sp = SparkPost('fake-key')
        sp.sending_domains.get('fake.com')


@responses.activate
def test_success_list():
    responses.add(
        responses.GET,
        base_uri,
        status=200,
        content_type='application/json',
        body='{"results": []}'
    )
    sp = SparkPost('fake-key')
    results = sp.sending_domains.list()
    assert results == []


@responses.activate
def test_fail_list():
    responses.add(
        responses.GET,
        base_uri,
        status=500,
        content_type='application/json',
        body='{"errors": [{"message": "fail"}]}'
    )
    with pytest.raises(SparkPostAPIException):
        sp = SparkPost('fake-key')
        sp.sending_domains.list()
