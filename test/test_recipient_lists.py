import pytest
import responses

from sparkpost import SparkPost
from sparkpost import RecipientLists
from sparkpost.exceptions import SparkPostAPIException


def test_translate_keys_with_id():
    t = RecipientLists('uri', 'key')
    results = t._translate_keys(id='test_id')
    assert results['id'] == 'test_id'


@responses.activate
def test_success_create():
    responses.add(
        responses.POST,
        'https://api.sparkpost.com/api/v1/recipient-lists',
        status=200,
        content_type='application/json',
        body='{"results": "yay"}'
    )

    sp = SparkPost('fake-key')
    results = sp.recipient_lists.create()
    assert results == 'yay'


@responses.activate
def test_fail_create():
    responses.add(
        responses.POST,
        'https://api.sparkpost.com/api/v1/recipient-lists',
        status=500,
        content_type='application/json',
        body="""
        {"errors": [{"message": "You failed", "description": "More Info"}]}
        """
    )
    with pytest.raises(SparkPostAPIException):
        sp = SparkPost('fake-key')
        sp.recipient_lists.create()


@responses.activate
def test_success_update():
    responses.add(
        responses.PUT,
        'https://api.sparkpost.com/api/v1/recipient-lists/foobar',
        status=200,
        content_type='application/json',
        body='{"results": "yay"}'
    )

    sp = SparkPost('fake-key')
    results = sp.recipient_lists.update('foobar', name='foobar')
    assert results == 'yay'


@responses.activate
def test_fail_update():
    responses.add(
        responses.PUT,
        'https://api.sparkpost.com/api/v1/recipient-lists/foobar',
        status=500,
        content_type='application/json',
        body="""
        {"errors": [{"message": "You failed", "description": "More Info"}]}
        """
    )
    with pytest.raises(SparkPostAPIException):
        sp = SparkPost('fake-key')
        sp.recipient_lists.update('foobar', name='foobar')


@responses.activate
def test_success_delete():
    responses.add(
        responses.DELETE,
        'https://api.sparkpost.com/api/v1/recipient-lists/foobar',
        status=200,
        content_type='application/json',
        body='{"results": "yay"}'
    )

    sp = SparkPost('fake-key')
    results = sp.recipient_lists.delete('foobar')
    assert results == 'yay'


@responses.activate
def test_fail_delete():
    responses.add(
        responses.DELETE,
        'https://api.sparkpost.com/api/v1/recipient-lists/foobar',
        status=500,
        content_type='application/json',
        body="""
        {"errors": [{"message": "You failed", "description": "More Info"}]}
        """
    )
    with pytest.raises(SparkPostAPIException):
        sp = SparkPost('fake-key')
        sp.recipient_lists.delete('foobar')


@responses.activate
def test_success_get():
    responses.add(
        responses.GET,
        'https://api.sparkpost.com/api/v1/recipient-lists/foobar',
        status=200,
        content_type='application/json',
        body='{"results": "yay"}'
    )
    sp = SparkPost('fake-key')
    results = sp.recipient_lists.get('foobar')
    assert results == "yay"


@responses.activate
def test_success_get_with_recipients():
    responses.add(
        responses.GET,
        'https://api.sparkpost.com/api/v1/recipient-lists/foobar',
        status=200,
        content_type='application/json',
        body='{"results": "yay"}'
    )
    sp = SparkPost('fake-key')
    results = sp.recipient_lists.get('foobar', True)
    assert results == "yay"


@responses.activate
def test_fail_get():
    responses.add(
        responses.GET,
        'https://api.sparkpost.com/api/v1/recipient-lists/foobar',
        status=404,
        content_type='application/json',
        body="""
        {"errors": [{"message": "cant find", "description": "where you go"}]}
        """
    )
    with pytest.raises(SparkPostAPIException):
        sp = SparkPost('fake-key')
        sp.recipient_lists.get('foobar')


@responses.activate
def test_success_list():
    responses.add(
        responses.GET,
        'https://api.sparkpost.com/api/v1/recipient-lists',
        status=200,
        content_type='application/json',
        body='{"results": "yay"}'
    )
    sp = SparkPost('fake-key')
    response = sp.recipient_lists.list()
    assert response == "yay"
