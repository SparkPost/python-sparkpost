import pytest

from sparkpost import SparkPost
from sparkpost.exceptions import SparkPostException


def test_no_api_key():
    with pytest.raises(SparkPostException):
        SparkPost()
