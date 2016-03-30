try:
    from urllib.parse import urlparse
except:
    from urlparse import urlparse

import pytest
import responses

from sparkpost import SparkPost
from sparkpost import Templates
from sparkpost.exceptions import SparkPostAPIException


def test_translate_keys_with_id():
    t = Templates('uri', 'key')
    results = t._translate_keys(id='test_id')
    assert results['id'] == 'test_id'


@responses.activate
def test_success_create():
    responses.add(
        responses.POST,
        'https://api.sparkpost.com/api/v1/templates',
        status=200,
        content_type='application/json',
        body='{"results": "yay"}'
    )

    sp = SparkPost('fake-key')
    results = sp.templates.create()
    assert results == 'yay'


@responses.activate
def test_fail_create():
    responses.add(
        responses.POST,
        'https://api.sparkpost.com/api/v1/templates',
        status=500,
        content_type='application/json',
        body="""
        {"errors": [{"message": "You failed", "description": "More Info"}]}
        """
    )
    with pytest.raises(SparkPostAPIException):
        sp = SparkPost('fake-key')
        sp.templates.create()


@responses.activate
def test_success_update():
    responses.add(
        responses.PUT,
        'https://api.sparkpost.com/api/v1/templates/foobar',
        status=200,
        content_type='application/json',
        body='{"results": "yay"}'
    )

    sp = SparkPost('fake-key')
    results = sp.templates.update('foobar', name='foobar')
    assert results == 'yay'


@responses.activate
def test_fail_update():
    responses.add(
        responses.PUT,
        'https://api.sparkpost.com/api/v1/templates/foobar',
        status=500,
        content_type='application/json',
        body="""
        {"errors": [{"message": "You failed", "description": "More Info"}]}
        """
    )
    with pytest.raises(SparkPostAPIException):
        sp = SparkPost('fake-key')
        sp.templates.update('foobar', name='foobar')


@responses.activate
def test_success_delete():
    responses.add(
        responses.DELETE,
        'https://api.sparkpost.com/api/v1/templates/foobar',
        status=200,
        content_type='application/json',
        body='{"results": "yay"}'
    )

    sp = SparkPost('fake-key')
    results = sp.templates.delete('foobar')
    assert results == 'yay'


@responses.activate
def test_fail_delete():
    responses.add(
        responses.DELETE,
        'https://api.sparkpost.com/api/v1/templates/foobar',
        status=500,
        content_type='application/json',
        body="""
        {"errors": [{"message": "You failed", "description": "More Info"}]}
        """
    )
    with pytest.raises(SparkPostAPIException):
        sp = SparkPost('fake-key')
        sp.templates.delete('foobar')


@responses.activate
def test_success_get():
    responses.add(
        responses.GET,
        'https://api.sparkpost.com/api/v1/templates/foobar',
        status=200,
        content_type='application/json',
        body='{"results": {}}'
    )
    sp = SparkPost('fake-key')
    results = sp.templates.get('foobar')
    assert results == {}


@responses.activate
def test_success_get_with_is_draft():
    responses.add(
        responses.GET,
        'https://api.sparkpost.com/api/v1/templates/foobar?draft=true',
        match_querystring=True,
        status=200,
        content_type='application/json',
        body='{"results": {}}'
    )
    sp = SparkPost('fake-key')
    results = sp.templates.get('foobar', True)
    assert results == {}


@responses.activate
def test_fail_get():
    responses.add(
        responses.GET,
        'https://api.sparkpost.com/api/v1/templates/foobar',
        status=404,
        content_type='application/json',
        body="""
        {"errors": [{"message": "cant find", "description": "where you go"}]}
        """
    )
    with pytest.raises(SparkPostAPIException):
        sp = SparkPost('fake-key')
        sp.templates.get('foobar')


@responses.activate
def test_success_list():
    responses.add(
        responses.GET,
        'https://api.sparkpost.com/api/v1/templates',
        status=200,
        content_type='application/json',
        body='{"results": []}'
    )
    sp = SparkPost('fake-key')
    response = sp.templates.list()
    assert response == []


@responses.activate
def test_success_preview():
    responses.add(
        responses.POST,
        'https://api.sparkpost.com/api/v1/templates/foobar/preview',
        status=200,
        content_type='application/json',
        body='{"results": {}}'
    )
    sp = SparkPost('fake-key')
    results = sp.templates.preview('foobar', {})
    assert responses.calls[0].request.body == '{"substitution_data": {}}'
    assert results == {}


@responses.activate
def test_success_preview_with_draft():
    responses.add(
        responses.POST,
        'https://api.sparkpost.com/api/v1/templates/foobar/preview?draft=true',
        match_querystring=True,
        status=200,
        content_type='application/json',
        body='{"results": {}}'
    )
    sp = SparkPost('fake-key')
    results = sp.templates.preview('foobar', {}, True)
    parsed = urlparse(responses.calls[0].request.url)
    assert parsed.query == 'draft=true'
    assert results == {}


@responses.activate
def test_fail_preview():
    responses.add(
        responses.POST,
        'https://api.sparkpost.com/api/v1/templates/foobar/preview',
        status=404,
        content_type='application/json',
        body="""
        {"errors": [{"message": "cant find", "description": "where you go"}]}
        """
    )
    with pytest.raises(SparkPostAPIException):
        sp = SparkPost('fake-key')
        sp.templates.preview('foobar', {})
