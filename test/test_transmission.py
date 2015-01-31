import pytest
import responses
from sparkpost import transmission


@responses.activate
def test_success_send():
  responses.add(responses.POST,'https://api-staging.sparkpost.com/api/v1/transmissions', status=200, content_type='application/json', body='{"results": "yay"}')
  t = transmission.Transmission()
  response = t.send()
  assert response == { 'results': 'yay' }

@responses.activate
def test_fail_send():
  responses.add(responses.POST,'https://api-staging.sparkpost.com/api/v1/transmissions', status=500, content_type='application/json', body='{"errors": "You failed"}')
  t = transmission.Transmission()
  response = t.send()
  assert response == 'You failed'

@responses.activate
def test_success_find():
  responses.add(responses.GET,'https://api-staging.sparkpost.com/api/v1/transmissions', status=200, content_type='application/json', body='{"results": []}')
  t = transmission.Transmission()
  response = t.find('foobar')
  assert response == { 'results': [] }

@responses.activate
def test_fail_find():
  responses.add(responses.GET,'https://api-staging.sparkpost.com/api/v1/transmissions', status=404, content_type='application/json', body='{"errors": "cant find"}')
  t = transmission.Transmission()
  response = t.find('foobar')
  assert response == 'cant find'

@responses.activate
def test_success_list():
  responses.add(responses.GET,'https://api-staging.sparkpost.com/api/v1/transmissions', status=200, content_type='application/json', body='{"results": []}')
  t = transmission.Transmission()
  response = t.list_all()
  assert response == { 'results': [] }
