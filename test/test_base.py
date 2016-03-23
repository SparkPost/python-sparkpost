import pytest
import responses

from sparkpost.base import Resource
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
