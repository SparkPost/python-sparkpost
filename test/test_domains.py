import pytest
import responses

from sparkpost import SparkPost
from sparkpost.exceptions import SparkPostAPIException
from sparkpost.domains import SendingDomainStatus


@responses.activate
def test_success_list_sending_domains():
    responses.add(
        responses.GET,
        'https://api.sparkpost.com/api/v1/sending-domains',
        status=200,
        content_type='application/json',
        body="""{
  "results": [
    {
      "domain": "example1.com",
      "tracking_domain": "click.example1.com",
      "status": {
        "ownership_verified": true,
        "spf_status": "unverified",
        "abuse_at_status": "unverified",
        "dkim_status": "valid",
        "cname_status": "valid",
        "mx_status": "unverified",
        "compliance_status": "valid",
        "postmaster_at_status": "unverified",
        "verification_mailbox_status": "valid",
        "verification_mailbox": "susan.calvin"
      },
      "shared_with_subaccounts": false,
      "is_default_bounce_domain": false
    }
  ]
}"""
    )
    sp = SparkPost('fake-key')
    results = sp.sending_domains.list()
    assert len(results) == 1
    assert results[0]['domain'] == 'example1.com'


@responses.activate
def test_success_list_sending_domains_with_filters():
    responses.add(
        responses.GET,
        'https://api.sparkpost.com/api/v1/sending-domains?dkim_status=valid',
        status=200,
        content_type='application/json',
        match_querystring=True,
        body="""{
  "results": [
    {
      "domain": "example1.com",
      "tracking_domain": "click.example1.com",
      "status": {
        "ownership_verified": true,
        "spf_status": "unverified",
        "abuse_at_status": "unverified",
        "dkim_status": "valid",
        "cname_status": "valid",
        "mx_status": "unverified",
        "compliance_status": "valid",
        "postmaster_at_status": "unverified",
        "verification_mailbox_status": "valid",
        "verification_mailbox": "susan.calvin"
      },
      "shared_with_subaccounts": false,
      "is_default_bounce_domain": false
    }
  ]
}"""
    )
    sp = SparkPost('fake-key')
    results = sp.sending_domains.list(dkim_status=SendingDomainStatus.VALID)
    assert len(results) == 1


@responses.activate
def test_fail_list_sending_domains():
    responses.add(
        responses.GET,
        'https://api.sparkpost.com/api/v1/sending-domains',
        status=500,
        content_type='application/json',
        body="""
        {"errors": [{"message": "You failed", "description": "More Info"}]}
        """
    )
    with pytest.raises(SparkPostAPIException):
        sp = SparkPost('fake-key')
        sp.sending_domains.list()


@responses.activate
def test_success_get_sending_domain():
    responses.add(
        responses.GET,
        'https://api.sparkpost.com/api/v1/sending-domains/example1.com',
        status=200,
        content_type='application/json',
        body="""{
  "results": {
    "tracking_domain": "click.example1.com",
    "status": {
      "ownership_verified": false,
      "spf_status": "unverified",
      "abuse_at_status": "unverified",
      "dkim_status": "unverified",
      "cname_status": "unverified",
      "mx_status": "pending",
      "compliance_status": "pending",
      "postmaster_at_status": "unverified",
      "verification_mailbox_status": "unverified"
    },
    "dkim": {
      "headers": "from:to:subject:date",
      "public": "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC+W6scd3XWwvC/hPRksfDYFi3ztgyS9OSqnnjtNQeDdTSD1DRx/xFar2wjmzxp2+SnJ5pspaF77VZveN3P/HVmXZVghr3asoV9WBx/uW1nDIUxU35L4juXiTwsMAbgMyh3NqIKTNKyMDy4P8vpEhtH1iv/BrwMdBjHDVCycB8WnwIDAQAB",
      "selector": "hello_selector"
    },
    "shared_with_subaccounts": false,
    "is_default_bounce_domain": false
  }
}"""
    )
    sp = SparkPost('fake-key')
    result = sp.sending_domains.get('example1.com')
    assert result is not None


@responses.activate
def test_not_found_get_sending_domain():
    responses.add(
        responses.GET,
        'https://api.sparkpost.com/api/v1/sending-domains/foo.com',
        status=404,
        content_type='application/json',
        body="""{"errors": [{"message": "Resource could not be found"}]}"""
    )
    with pytest.raises(SparkPostAPIException):
        sp = SparkPost('fake-key')
        sp.sending_domains.get('foo.com')


@responses.activate
def test_success_delete_sending_domain():
    responses.add(
        responses.DELETE,
        'https://api.sparkpost.com/api/v1/sending-domains/example1.com',
        status=204,
        content_type='application/json'
    )
    sp = SparkPost('fake-key')
    results = sp.sending_domains.delete('example1.com')
    assert results is True


@responses.activate
def test_not_found_delete_sending_domain():
    responses.add(
        responses.DELETE,
        'https://api.sparkpost.com/api/v1/sending-domains/foo.com',
        status=404,
        content_type='application/json',
        body="""{"errors": [{"message": "Resource could not be found"}]}"""
    )
    with pytest.raises(SparkPostAPIException):
        sp = SparkPost('fake-key')
        sp.sending_domains.delete('foo.com')


@responses.activate
def test_success_update_sending_domain():
    responses.add(
        responses.PUT,
        'https://api.sparkpost.com/api/v1/sending-domains/example1.com',
        status=200,
        content_type='application/json',
        body="""{
  "results": {
    "message": "Successfully Updated Domain.",
    "domain": "example1.com"
  }
}"""
    )

    sp = SparkPost('fake-key')
    results = sp.sending_domains.update('example1.com',
                                        tracking_domain='tr.example1.com',
                                        shared_with_subaccounts=True,
                                        is_default_bounce_domain=True)
    assert results is not None
    assert results['message'] == 'Successfully Updated Domain.'


@responses.activate
def test_success_update_dkim_sending_domain():
    responses.add(
        responses.PUT,
        'https://api.sparkpost.com/api/v1/sending-domains/example1.com',
        status=200,
        content_type='application/json',
        body="""{
  "results": {
    "message": "Successfully Updated Domain.",
    "domain": "example1.com"
  }
}"""
    )

    sp = SparkPost('fake-key')
    results = sp.sending_domains.update('example1.com',
                                        dkim_private='foo',
                                        dkim_public='bar',
                                        dkim_selector='baz')
    assert results is not None
    assert results['message'] == 'Successfully Updated Domain.'


@responses.activate
def test_failure_update_dkim_sending_domain():
    with pytest.raises(ValueError):
        sp = SparkPost('fake-key')
        results = sp.sending_domains.update('example1.com',
                                            dkim_private='foo',
                                            dkim_public='bar')


@responses.activate
def test_success_create_sending_domain():
    responses.add(
        responses.POST,
        'https://api.sparkpost.com/api/v1/sending-domains',
        status=200,
        content_type='application/json',
        body="""{
  "results": {
    "message": "Successfully Created domain.",
    "domain": "example1.com",
    "dkim": {
      "public": "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC+W6scd3XWwvC/hPRksfDYFi3ztgyS9OSqnnjtNQeDdTSD1DRx/xFar2wjmzxp2+SnJ5pspaF77VZveN3P/HVmXZVghr3asoV9WBx/uW1nDIUxU35L4juXiTwsMAbgMyh3NqIKTNKyMDy4P8vpEhtH1iv/BrwMdBjHDVCycB8WnwIDAQAB",
      "selector": "scph0316",
      "signing_domain": "example1.com",
      "headers": "from:to:subject:date"
    }
  }
}"""
    )

    sp = SparkPost('fake-key')
    results = sp.sending_domains.create('example1.com',
                                        tracking_domain='click.example1.com',
                                        shared_with_subaccounts=False)
    assert results is not None
    assert results['domain'] == 'example1.com'


@responses.activate
def test_failure_create_sending_domain_already_exists():
    responses.add(
        responses.POST,
        'https://api.sparkpost.com/api/v1/sending-domains',
        status=409,
        content_type='application/json',
        body="""{
  "errors": [
    {
      "message": "resource conflict",
      "description": "Sending Domain <example1.com> already registered",
      "code": "1602"
    }
  ]
}"""
    )

    with pytest.raises(SparkPostAPIException):
        sp = SparkPost('fake-key')
        sp.sending_domains.create('example1.com')


@responses.activate
def test_success_create_sending_domain_with_dkim():
    responses.add(
        responses.POST,
        'https://api.sparkpost.com/api/v1/sending-domains',
        status=200,
        content_type='application/json',
        body="""{
  "results": {
    "message": "Successfully Created domain.",
    "domain": "example1.com",
    "dkim": {
      "public": "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC+W6scd3XWwvC/hPRksfDYFi3ztgyS9OSqnnjtNQeDdTSD1DRx/xFar2wjmzxp2+SnJ5pspaF77VZveN3P/HVmXZVghr3asoV9WBx/uW1nDIUxU35L4juXiTwsMAbgMyh3NqIKTNKyMDy4P8vpEhtH1iv/BrwMdBjHDVCycB8WnwIDAQAB",
      "selector": "scph0316",
      "signing_domain": "example1.com",
      "headers": "from:to:subject:date"
    }
  }
}"""
    )

    sp = SparkPost('fake-key')
    results = sp.sending_domains.create('example1.com',
                                        dkim_private='foo',
                                        dkim_public='bar',
                                        dkim_selector='baz',
                                        generate_dkim=False)
    assert results is not None
    assert results['domain'] == 'example1.com'


@responses.activate
def test_failure_create_sending_domain_with_dkim():
    with pytest.raises(ValueError):
        sp = SparkPost('fake-key')
        results = sp.sending_domains.create('example1.com',
                                            dkim_private='foo',
                                            dkim_public='bar',
                                            generate_dkim=False)


@responses.activate
def test_success_list_tracking_domains():
    responses.add(
        responses.GET,
        'https://api.sparkpost.com/api/v1/tracking-domains',
        status=200,
        content_type='application/json',
        body="""{
  "results": [
    {
      "port": 443,
      "domain": "example.domain.com",
      "secure": true,
      "default": true,
      "status": {
        "verified": false,
        "cname_status": "pending",
        "compliance_status": "pending"
      }
    },
    {
      "port": 80,
      "domain": "example2.domain.com",
      "secure": false,
      "default": false,
      "status": {
        "verified": true,
        "cname_status": "valid",
        "compliance_status": "valid"
      },
      "subaccount_id": 215
    }
  ]
}"""
    )
    sp = SparkPost('fake-key')
    results = sp.tracking_domains.list()
    assert len(results) == 2
    assert results[0]['domain'] == 'example.domain.com'


@responses.activate
def test_success_list_tracking_domains_subaccounts():
    responses.add(
        responses.GET,
        'https://api.sparkpost.com/api/v1/tracking-domains?subaccounts=foo,bar',
        status=200,
        content_type='application/json',
        match_querystring=True,
        body="""{
  "results": [
    {
      "port": 80,
      "domain": "example2.domain.com",
      "secure": false,
      "default": false,
      "status": {
        "verified": true,
        "cname_status": "valid",
        "compliance_status": "valid"
      },
      "subaccount_id": 215
    }
  ]
}"""
    )
    sp = SparkPost('fake-key')
    results = sp.tracking_domains.list(subaccounts=['foo', 'bar'])
    assert len(results) == 1
    assert results[0]['domain'] == 'example2.domain.com'


@responses.activate
def test_fail_list_tracking_domains():
    responses.add(
        responses.GET,
        'https://api.sparkpost.com/api/v1/tracking-domains',
        status=500,
        content_type='application/json',
        body="""
        {"errors": [{"message": "You failed", "description": "More Info"}]}
        """
    )
    with pytest.raises(SparkPostAPIException):
        sp = SparkPost('fake-key')
        sp.tracking_domains.list()


@responses.activate
def test_success_get_tracking_domain():
    responses.add(
        responses.GET,
        'https://api.sparkpost.com/api/v1/tracking-domains/example1.com',
        status=200,
        content_type='application/json',
        body="""{
  "results": {
    "port": 443,
    "domain": "example.domain.com",
    "secure": true,
    "default": true,
    "status": {
      "verified": false,
      "cname_status": "pending",
      "compliance_status": "pending"
    }
  }
}"""
    )
    sp = SparkPost('fake-key')
    result = sp.tracking_domains.get('example1.com')
    assert result is not None


@responses.activate
def test_not_found_get_tracking_domain():
    responses.add(
        responses.GET,
        'https://api.sparkpost.com/api/v1/tracking-domains/foo.com',
        status=404,
        content_type='application/json',
        body="""{"errors": [{"message": "Resource could not be found"}]}"""
    )
    with pytest.raises(SparkPostAPIException):
        sp = SparkPost('fake-key')
        sp.tracking_domains.get('foo.com')


@responses.activate
def test_success_delete_tracking_domain():
    responses.add(
        responses.DELETE,
        'https://api.sparkpost.com/api/v1/tracking-domains/example1.com',
        status=204,
        content_type='application/json'
    )
    sp = SparkPost('fake-key')
    results = sp.tracking_domains.delete('example1.com')
    assert results is True


@responses.activate
def test_not_found_delete_tracking_domain():
    responses.add(
        responses.DELETE,
        'https://api.sparkpost.com/api/v1/tracking-domains/foo.com',
        status=404,
        content_type='application/json',
        body="""{"errors": [{"message": "Resource could not be found"}]}"""
    )
    with pytest.raises(SparkPostAPIException):
        sp = SparkPost('fake-key')
        sp.tracking_domains.delete('foo.com')
