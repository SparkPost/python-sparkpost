import pytest
import responses

from sparkpost import SparkPost
# from sparkpost import Sending_Domains
from sparkpost.exceptions import SparkPostAPIException


@responses.activate
def test_success_create():
    responses.add(
        responses.POST,
        'https://api.sparkpost.com/api/v1/sending-domains',
        status=200,
        content_type='application/json',
        body='{"results": "yay"}'
    )
    sp = SparkPost('fake-key')
    results = sp.sending_domains.create()
    assert results == 'yay'


@responses.activate
def test_fail_create():
    responses.add(
        responses.POST,
        'https://api.sparkpost.com/api/v1/sending-domains',
        status=500,
        content_type='application/json',
        body='{"errors": [{"message": "You failed", "description": "More Info"}]}'
    )
    with pytest.raises(SparkPostAPIException):
        sp = SparkPost('fake-key')
        sp.sending_domains.create()


@responses.activate
def test_success_update():
    responses.add(
        responses.PUT,
        'https://api.sparkpost.com/api/v1/sending-domains/test-domain',
        status=200,
        content_type='application/json',
        body='{"results": "yay"}'
    )
    sp = SparkPost('fake-key')
    results = sp.sending_domains.update(domain='test-domain')
    assert results == 'yay'


@responses.activate
def test_fail_update():
    responses.add(
        responses.PUT,
        'https://api.sparkpost.com/api/v1/sending-domains/test-domain',
        status=500,
        content_type='application/json',
        body='{"errors": [{"message": "You failed", "description": "More Info"}]}'
    )
    with pytest.raises(SparkPostAPIException):
        sp = SparkPost('fake-key')
        sp.sending_domains.update(domain='test-domain')

@responses.activate
def test_success_find():
    responses.add(
        responses.GET,
        'https://api.sparkpost.com/api/v1/sending-domains/test-domain',
        status=200,
        content_type='application/json',
        body='{"results": {"transmission": {}}}'
    )
    sp = SparkPost('fake-key')
    results = sp.sending_domains.get('test-domain')
    assert results == {}


@responses.activate
def test_fail_find():
    responses.add(
        responses.GET,
        'https://api.sparkpost.com/api/v1/sending-domains/test-domain',
        status=404,
        content_type='application/json',
        body='{"errors": [{"message": "cant find", "description": "where you go"}]}'
    )
    with pytest.raises(SparkPostAPIException):
        sp = SparkPost('fake-key')
        sp.sending_domains.get('test-domain')


@responses.activate
def test_success_all():
    responses.add(
        responses.GET,
        'https://api.sparkpost.com/api/v1/sending-domains',
        status=200,
        content_type='application/json',
        body='{"results": []}'
    )
    sp = SparkPost('fake-key')
    response = sp.sending_domains.all()
    assert response == []


@responses.activate
def test_success_verify():
    responses.add(
        responses.POST,
        'https://api.sparkpost.com/api/v1/sending-domains/test-domain/verify',
        status=200,
        content_type='application/json',
        body='{}'
    )
    sp = SparkPost('fake-key')
    results = sp.sending_domains.verify('test-domain')
    assert results == {}


@responses.activate
def test_fail_verify():
    responses.add(
        responses.POST,
        'https://api.sparkpost.com/api/v1/sending-domains/test-domain/verify',
        status=500,
        content_type='application/json',
        body='{"errors": [{"message": "You failed", "description": "More Info"}]}'
    )
    with pytest.raises(SparkPostAPIException):
        sp = SparkPost('fake-key')
        sp.sending_domains.verify('test-domain')
