import base64
import datetime
import json
import os
import tempfile
import warnings

import pytest
import responses
import six
from mock import patch

from sparkpost import SparkPost
from sparkpost import Events
from sparkpost.exceptions import SparkPostAPIException, SparkPostException


def test_create_date_string():
    timezone_offset = -6
    source_date = datetime.datetime(year=2022, month=02, day=28, hour=12, minute=00)
    e = Events('uri', 'key')
    e.set_local_time_offset_in_hours(timezone_offset)
    ut_date_string = e.create_date_string(source_date)

    assert "2022-02-28T06:00" == ut_date_string


def test_update_list_and_date_parameters_for_list():
    e = Events('uri', 'key')
    test_key = "test"
    original_string = "item1,item2"
    test_dict = {test_key : original_string.split(",")}

    converted_dict = e._update_list_and_date_parameters(test_dict)

    assert original_string == converted_dict[test_key]


def test_update_list_and_date_parameters_for_datetime():
    e = Events('uri', 'key')
    e.set_local_time_offset_in_hours(+6)
    original_ut     = "2022-02-28T12:00"
    original_local  = "2022-02-28T06:00"
    local_datetime  = datetime.datetime.strptime(original_local, '%Y-%m-%dT%H:%M')
    test_key = "test"
    test_dict = {test_key : local_datetime}

    converted_dict = e._update_list_and_date_parameters(test_dict)

    assert original_ut == converted_dict[test_key]


@responses.activate
def test_get_no_parameters_mocked():
    responses.add(
        responses.GET,
        'https://api.sparkpost.com/api/v1/events/message',
        status=200,
        content_type='application/json',
        body='{"results":[{"mailbox_provider":"gmail","template_version":"0","friendly_from":"nobody@nowhere.com","subject":"special subject","ip_pool":"default","sending_domain":"sparkpostmail.com","rcpt_tags":[],"type":"delivery","num_retries":"0","mailbox_provider_region":"B2B - Filter","raw_rcpt_to":"someone@nowhere.com","msg_from":"msprvs1=19055EwNMpz6O=bounces-25543-4@bounces.sparkpostmail.com","recv_method":"esmtp","rcpt_to":"someone@nowhere.com","subaccount_id":0,"transmission_id":"8401419633671706792","timestamp":"2022-02-25T03:27:01.000Z","outbound_tls":"1","rcpt_meta":{},"message_id":"62167e4c1862536fd4de","ip_address":"67.231.154.162","queue_time":"6795","recipient_domain":"nowhere.com","event_id":"3693091070679284057","routing_domain":"nowhere.com","sending_ip":"192.168.0.1","template_id":"smtp_8401419633671706792","delv_method":"esmtp","customer_id":99988,"injection_time":"2022-02-25T03:26:54.000Z","msg_size":"15746"}],"total_count":1,"links":{}}'
    )
    sp = SparkPost('fake-key')
    results = sp.events.get()
    assert 1 == len(results)


@responses.activate
def test_get_by_sender_email_mocked():
    responses.add(
        responses.GET,
        'https://api.sparkpost.com/api/v1/events/message',
        status=200,
        content_type='application/json',
        body='{"results":[{"mailbox_provider":"gmail","template_version":"0","friendly_from":"nobody@nowhere.com","subject":"special subject","ip_pool":"default","sending_domain":"sparkpostmail.com","rcpt_tags":[],"type":"delivery","num_retries":"0","mailbox_provider_region":"B2B - Filter","raw_rcpt_to":"someone@nowhere.com","msg_from":"msprvs1=19055EwNMpz6O=bounces-25543-4@bounces.sparkpostmail.com","recv_method":"esmtp","rcpt_to":"someone@nowhere.com","subaccount_id":0,"transmission_id":"8401419633671706792","timestamp":"2022-02-25T03:27:01.000Z","outbound_tls":"1","rcpt_meta":{},"message_id":"62167e4c1862536fd4de","ip_address":"67.231.154.162","queue_time":"6795","recipient_domain":"nowhere.com","event_id":"3693091070679284057","routing_domain":"nowhere.com","sending_ip":"192.168.0.1","template_id":"smtp_8401419633671706792","delv_method":"esmtp","customer_id":99988,"injection_time":"2022-02-25T03:26:54.000Z","msg_size":"15746"}],"total_count":1,"links":{}}'
    )
    sp = SparkPost('fake-key')

    delivery_type = "delivery"
    sender_address = "nobody@nowhere.com"
    params = {
        "from_addresses" : sender_address,
        "from": datetime.datetime(2022, 2, 1, 0, 0),
        "to": datetime.datetime(2022, 2, 28, 23, 59),
        "events": [delivery_type]
    }
    results = sp.events.get(params)
    assert 1 == len(results)
    assert sender_address == results[0]["friendly_from"]
    assert delivery_type == results[0]["type"]
