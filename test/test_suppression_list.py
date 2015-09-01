import pytest
import responses

from sparkpost import SparkPost
from sparkpost.exceptions import SparkPostAPIException


@responses.activate
def test_success_list():
    responses.add(
        responses.GET,
        'https://api.sparkpost.com/api/v1/suppression-list',
        status=200,
        content_type='application/json',
        body='{"results": "yay"}'
    )

    sp = SparkPost('fake-key')
    results = sp.suppression_list.list()
    assert results == 'yay'


@responses.activate
def test_fail_list():
    responses.add(
        responses.GET,
        'https://api.sparkpost.com/api/v1/suppression-list',
        status=404,
        content_type='application/json',
        body="""
        {"errors": [{"message": "cant find", "description": "where you go"}]}
        """
    )
    with pytest.raises(SparkPostAPIException):
        sp = SparkPost('fake-key')
        sp.suppression_list.list()


@responses.activate
def test_success_get():
    responses.add(
        responses.GET,
        'https://api.sparkpost.com/api/v1/suppression-list/foobar',
        status=200,
        content_type='application/json',
        body='{"results": []}'
    )
    sp = SparkPost('fake-key')
    results = sp.suppression_list.get('foobar')
    assert results == []


@responses.activate
def test_fail_get():
    responses.add(
        responses.GET,
        'https://api.sparkpost.com/api/v1/suppression-list/foobar',
        status=404,
        content_type='application/json',
        body="""
        {"errors": [{"message": "cant find", "description": "where you go"}]}
        """
    )
    with pytest.raises(SparkPostAPIException):
        sp = SparkPost('fake-key')
        sp.suppression_list.get('foobar')


@responses.activate
def test_success_delete():
    responses.add(
        responses.DELETE,
        'https://api.sparkpost.com/api/v1/suppression-list/foobar',
        status=204,
        content_type='application/json'
    )
    sp = SparkPost('fake-key')
    results = sp.suppression_list.delete('foobar')
    assert results is True


@responses.activate
def test_fail_delete():
    responses.add(
        responses.DELETE,
        'https://api.sparkpost.com/api/v1/suppression-list/foobar',
        status=404,
        content_type='application/json',
        body="""
        {"errors": [{"message": "cant find", "description": "where you go"}]}
        """
    )
    with pytest.raises(SparkPostAPIException):
        sp = SparkPost('fake-key')
        sp.suppression_list.delete('foobar')


@responses.activate
def test_success_upsert():
    responses.add(
        responses.PUT,
        'https://api.sparkpost.com/api/v1/suppression-list/foobar',
        status=200,
        content_type='application/json',
        body='{"results": "yay"}'
    )

    sp = SparkPost('fake-key')
    results = sp.suppression_list._upsert({"email": "foobar"})
    assert results == 'yay'


@responses.activate
def test_success_create():
    responses.add(
        responses.PUT,
        'https://api.sparkpost.com/api/v1/suppression-list/foobar',
        status=200,
        content_type='application/json',
        body='{"results": "yay"}'
    )

    sp = SparkPost('fake-key')
    results = sp.suppression_list.create({"email": "foobar"})
    assert results == 'yay'


@responses.activate
def test_success_update():
    responses.add(
        responses.PUT,
        'https://api.sparkpost.com/api/v1/suppression-list/foobar',
        status=200,
        content_type='application/json',
        body='{"results": "yay"}'
    )

    sp = SparkPost('fake-key')
    results = sp.suppression_list.update({"email": "foobar"})
    assert results == 'yay'


@responses.activate
def test_success_upsert_bulk():
    responses.add(
        responses.PUT,
        'https://api.sparkpost.com/api/v1/suppression-list',
        status=200,
        content_type='application/json',
        body='{"results": "yay"}'
    )

    sp = SparkPost('fake-key')
    results = sp.suppression_list._upsert([
        {"email": "foobar1"}, {"email": "foobar2"}
    ])
    assert results == 'yay'


@responses.activate
def test_fail_upsert():
    responses.add(
        responses.PUT,
        'https://api.sparkpost.com/api/v1/suppression-list/foobar',
        status=404,
        content_type='application/json',
        body="""
        {"errors": [{"message": "cant find", "description": "where you go"}]}
        """
    )
    with pytest.raises(SparkPostAPIException):
        sp = SparkPost('fake-key')
        sp.suppression_list._upsert({"email": "foobar"})
