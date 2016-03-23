from .utils import wrap_future
from ..transmissions import Transmissions as SyncTransmissions


class Transmissions(SyncTransmissions):
    def get(self, transmission_id):
        results = self._fetch_get(transmission_id)
        return wrap_future(results, lambda f: f["transmission"])
