from datetime import datetime

import pytest
import responses
from Crypto.PublicKey import RSA
from mock import MagicMock, patch

from sparkpost import SparkPost
from sparkpost.sending_domains import SendingDomains
from sparkpost.exceptions import SparkPostAPIException


base_uri = SparkPost('fake-key').sending_domains.uri


def test_generate_key_pair():
    # we're not asserting here, just making sure the generated key pair does
    # not raise an exception
    sp = SparkPost('fake-key')
    private, public = sp.sending_domains._generate_key_pair()
    RSA.importKey(private)
    RSA.importKey(public)


def test_generate_selector():
    sp = SparkPost('fake-key')
    result = sp.sending_domains._generate_selector()
    assert result == 'scph%s' % datetime.now().strftime('%m%d')


@patch.object(SendingDomains, 'request')
def test_create_params_with_defaults(mock_request):
    sp = SparkPost('fake-key')
    sp.sending_domains._generate_selector = MagicMock(return_value='sel')
    sp.sending_domains.create('fake.com')
    sp.sending_domains._generate_selector.assert_called_once()


@responses.activate
def test_create_domain_only():
    responses.add(
        responses.POST,
        base_uri,
        status=200,
        content_type='application/json',
        body='{"results": {}}'
    )
    sp = SparkPost('fake-key')
    results = sp.sending_domains.create('fake.com')
    assert results == {}


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
