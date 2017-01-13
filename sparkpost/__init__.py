import os

from .base import RequestsTransport
from .exceptions import SparkPostException
from .metrics import Metrics
from .recipient_lists import RecipientLists
from .suppression_list import SuppressionList
from .templates import Templates
from .transmissions import Transmissions


__version__ = '1.3.3'


class SparkPost(object):
    TRANSPORT_CLASS = RequestsTransport

    def __init__(self, api_key=None, base_uri='https://api.sparkpost.com',
                 version='1'):
        "Set up the SparkPost API client"
        if not api_key:
            api_key = self.get_api_key()
            if not api_key:
                raise SparkPostException("No API key. Improve message.")

        self.base_uri = base_uri + '/api/v' + version
        self.api_key = api_key

        self.metrics = Metrics(self.base_uri, self.api_key,
                               self.TRANSPORT_CLASS)
        self.recipient_lists = RecipientLists(self.base_uri, self.api_key,
                                              self.TRANSPORT_CLASS)
        self.suppression_list = SuppressionList(self.base_uri, self.api_key,
                                                self.TRANSPORT_CLASS)
        self.templates = Templates(self.base_uri, self.api_key,
                                   self.TRANSPORT_CLASS)
        self.transmissions = Transmissions(self.base_uri, self.api_key,
                                           self.TRANSPORT_CLASS)
        # Keeping self.transmission for backwards compatibility.
        # Will be removed in a future release.
        self.transmission = self.transmissions

    def get_api_key(self):
        "Get API key from environment variable"
        return os.environ.get('SPARKPOST_API_KEY', None)
