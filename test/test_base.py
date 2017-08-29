import pytest
import responses
from mock import patch

import sparkpost
from sparkpost.base import Resource, RequestsTransport
from sparkpost.exceptions import SparkPostAPIException


fake_base_uri = 'https://fake-base.com'
fake_api_key = 'fake-api-key'
fake_resource_key = 'fake-resource-key'
fake_uri = "%s/%s" % (fake_base_uri, fake_resource_key)


def create_resource():
    resource = Resource(fake_base_uri, fake_api_key)
    resource.key = fake_resource_key
    return resource


def test_uri():
    resource = create_resource()
    assert resource.uri == fake_uri


def test_default_headers():
    expected_headers = {
        'User-Agent': 'python-sparkpost/' + sparkpost.__version__,
        'Content-Type': 'application/json',
        'Authorization': fake_api_key,
        'X-MSYS-SUBACCOUNT': 0
    }

    with patch.object(RequestsTransport,
                      'request',
                      return_value=None) as request_mock:
        resource = create_resource()
        resource.request('GET', resource.uri)
        request_mock.assert_called_with('GET', resource.uri,
                                        headers=expected_headers)


def test_subaccount_header():
    expected_headers = {
        'User-Agent': 'python-sparkpost/' + sparkpost.__version__,
        'Content-Type': 'application/json',
        'Authorization': fake_api_key,
        'X-MSYS-SUBACCOUNT': 123
    }

    with patch.object(RequestsTransport,
                      'request',
                      return_value=None) as request_mock:
        resource = create_resource()
        resource.request('GET', resource.uri, subaccount=123)
        request_mock.assert_called_with('GET', resource.uri,
                                        headers=expected_headers)


@responses.activate
def test_success_request():
    responses.add(
        responses.GET,
        fake_uri,
        status=200,
        content_type='application/json',
        body='{}'
    )
    resource = create_resource()
    results = resource.request('GET', resource.uri)
    assert results == {}


@responses.activate
def test_success_request_with_results():
    responses.add(
        responses.GET,
        fake_uri,
        status=200,
        content_type='application/json',
        body='{"results": []}'
    )
    resource = create_resource()
    results = resource.request('GET', resource.uri)
    assert results == []


@responses.activate
def test_fail_request():
    responses.add(
        responses.GET,
        fake_uri,
        status=500,
        content_type='application/json',
        body='{"errors": [{"message": "failure", "description": "desc"}]}'
    )
    resource = create_resource()
    with pytest.raises(SparkPostAPIException):
        resource.request('GET', resource.uri)


@responses.activate
def test_fail_wrongjson_request():
    responses.add(
        responses.GET,
        fake_uri,
        status=500,
        content_type='application/json',
        body='{"errors": ["Error!"]}'
    )
    resource = create_resource()
    with pytest.raises(SparkPostAPIException):
        resource.request('GET', resource.uri)


@responses.activate
def test_fail_nojson_request():
    responses.add(
        responses.GET,
        fake_uri,
        status=500,
        content_type='application/json',
        body='{"errors": '
    )
    resource = create_resource()
    with pytest.raises(SparkPostAPIException):
        resource.request('GET', resource.uri)


@responses.activate
def test_fail_no_errors():
    responses.add(
        responses.GET,
        fake_uri,
        status=500,
        content_type='application/json',
        body='no errors'
    )
    resource = create_resource()
    with pytest.raises(SparkPostAPIException):
        resource.request('GET', resource.uri)


def test_fail_get():
    resource = create_resource()
    with pytest.raises(NotImplementedError):
        resource.get()


def test_fail_list():
    resource = create_resource()
    with pytest.raises(NotImplementedError):
        resource.list()


def test_fail_create():
    resource = create_resource()
    with pytest.raises(NotImplementedError):
        resource.create()


def test_fail_update():
    resource = create_resource()
    with pytest.raises(NotImplementedError):
        resource.update()


def test_fail_delete():
    resource = create_resource()
    with pytest.raises(NotImplementedError):
        resource.delete()
