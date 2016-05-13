import responses
import pytest
from sparkpost import (
    SparkPost,
    MessageEvents
)
from sparkpost.exceptions import SparkPostAPIException


def test_format_listable_param_list():
    '''
    Tests all possible inputs for messages
    '''
    mesg = MessageEvents('uri', 'key')

    test_int_list = range(3)
    # test one. then multiple
    assert "0" == mesg._format_listable_param(test_int_list[0])
    assert "0" == mesg._format_listable_param(test_int_list[:1])
    assert "0,1,2" == mesg._format_listable_param(test_int_list)

    # now test a list of strings
    test_str_list = map(str, test_int_list)
    assert "0" == mesg._format_listable_param(test_str_list[0])
    assert "0" == mesg._format_listable_param(test_str_list[:1])
    assert "0,1,2" == mesg._format_listable_param(test_str_list)


def test_format_datetime_param():
    from datetime import datetime

    mesg = MessageEvents('uri', 'key')

    ex_time = "2014-07-20T08:00"

    assert ex_time == mesg._format_datetime_param(ex_time)

    dt_obj = datetime.strptime(ex_time, "%Y-%m-%dT%H:%M")
    assert ex_time == mesg._format_datetime_param(dt_obj)


def test_format_request_params():
    mesg = MessageEvents('uri', 'key')

    # test one kwarg
    one_kwarg = {
        "per_page": 1
    }
    formatted_kwargs = mesg._format_request_params(**one_kwarg)
    assert "per_page=1" == formatted_kwargs

    # test validator
    one_kwarg = {
        "per_page": "10000"
    }
    try:
        mesg._format_request_params(**one_kwarg)
    except ValueError:
        pass

    # test negative val
    one_kwarg = {
        "per_page": -1
    }
    try:
        mesg._format_request_params(**one_kwarg)
    except ValueError:
        pass

    # test normal
    kwargs = {
        "campaign_ids": [1, 2],
        "to_date": "now",
        "per_page": "100"
    }
    formatted_kwargs = mesg._format_request_params(**kwargs)
    assert "to=now&campaign_ids=1,2&per_page=100" == formatted_kwargs


@responses.activate
def test_fail_get():
    responses.add(
        responses.GET,
        url="""https://api.sparkpost.com/api/v1/message-events?""",
        status=404,
        content_type='application/json',
        body="""
        {"errors": [{"message": "cant find", "description": "where you go"}]}
        """
    )
    with pytest.raises(SparkPostAPIException):
        sp = SparkPost('fake-key')
        sp.message_events.get(transmission_ids=8675309)


@responses.activate
def test_success_get():
    responses.add(
        responses.GET,
        url="""https://api.sparkpost.com/api/v1/message-events?""",
        status=200,
        content_type='application/json',
        body='[]'
    )
    result_dict = {
        "results": [],
        "total_count": 0,
        "links": []
    }
    sp = SparkPost('fake-key')
    assert result_dict == sp.message_events.get(transmission_ids=8675309)
