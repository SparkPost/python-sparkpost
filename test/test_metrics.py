import pytest
import responses

from sparkpost import SparkPost
from sparkpost.exceptions import SparkPostAPIException


@responses.activate
def test_success_campaigns():
    responses.add(
        responses.GET,
        'https://api.sparkpost.com/api/v1/metrics/campaigns',
        status=200,
        content_type='application/json',
        body='{"results": {"campaigns": []}}'
    )
    sp = SparkPost('fake-key')
    results = sp.metrics.campaigns.list()
    assert results == []


@responses.activate
def test_fail_campaigns():
    responses.add(
        responses.GET,
        'https://api.sparkpost.com/api/v1/metrics/campaigns',
        status=500,
        content_type='application/json',
        body="""
        {"errors": [{"message": "You failed", "description": "More Info"}]}
        """
    )
    with pytest.raises(SparkPostAPIException):
        sp = SparkPost('fake-key')
        sp.metrics.campaigns.list()


@responses.activate
def test_success_domains():
    responses.add(
        responses.GET,
        'https://api.sparkpost.com/api/v1/metrics/domains',
        status=200,
        content_type='application/json',
        body='{"results": {"domains": []}}'
    )
    sp = SparkPost('fake-key')
    results = sp.metrics.domains.list()
    assert results == []


@responses.activate
def test_fail_domains():
    responses.add(
        responses.GET,
        'https://api.sparkpost.com/api/v1/metrics/domains',
        status=500,
        content_type='application/json',
        body="""
        {"errors": [{"message": "You failed", "description": "More Info"}]}
        """
    )
    with pytest.raises(SparkPostAPIException):
        sp = SparkPost('fake-key')
        sp.metrics.domains.list()
