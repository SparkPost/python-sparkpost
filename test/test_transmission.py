import pytest
import responses

from sparkpost import SparkPost
from sparkpost import Transmission
from sparkpost.exceptions import SparkPostAPIException



def test_translate_keys_with_list():
    t = Transmission('uri', 'key')
    results = t._translate_keys(recipient_list = 'test')
    assert results['return_path'] == 'default@sparkpostmail.com'
    assert results['options']['open_tracking'] == True
    assert results['options']['click_tracking'] == True
    assert results['content']['use_draft_template'] == False
    assert results['recipients'] == { 'list_id': 'test' }

def test_translate_keys_with_recips():
    t = Transmission('uri', 'key')
    results = t._translate_keys(recipients = ['test', {'key': 'value'}, 'foobar' ])
    assert results['recipients'] == [ { 'address': {'email': 'test'} },
      {'key': 'value'}, {'address': {'email': 'foobar'}}]

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
def test_fail_send():
    responses.add(
        responses.POST,
        'https://api.sparkpost.com/api/v1/transmissions',
        status=500,
        content_type='application/json',
        body='{"errors": [{"message": "You failed", "description": "More Info"}]}'
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
        body='{"errors": [{"message": "cant find", "description": "where you go"}]}'
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
