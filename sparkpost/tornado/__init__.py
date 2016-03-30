import sparkpost

from .exceptions import SparkPostAPIException
from .base import TornadoTransport
from .transmissions import Transmissions

__all__ = ["SparkPost", "TornadoTransport", "SparkPostAPIException",
           "Transmissions"]


class SparkPost(sparkpost.SparkPost):
    TRANSPORT_CLASS = TornadoTransport

    def __init__(self, *args, **kwargs):
        super(SparkPost, self).__init__(*args, **kwargs)
        self.transmissions = Transmissions(self.base_uri, self.api_key,
                                           self.TRANSPORT_CLASS)
        self.transmission = self.transmissions
