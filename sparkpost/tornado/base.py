import json
from tornado import gen
from tornado.httpclient import AsyncHTTPClient, HTTPError

from .exceptions import SparkPostAPIException


class TornadoTransport(object):
    @gen.coroutine
    def request(self, method, uri, headers, **kwargs):
        if "data" in kwargs:
            kwargs["body"] = kwargs.pop("data")
        client = AsyncHTTPClient()
        try:
            response = yield client.fetch(uri, method=method, headers=headers,
                                          **kwargs)
        except HTTPError as ex:
            raise SparkPostAPIException(ex.response)
        if response.code == 204:
            raise gen.Return(True)
        if response.code == 200:
            result = None
            try:
                result = json.loads(response.body.decode("utf-8"))
            except:
                pass
            if result:
                if 'results' in result:
                    raise gen.Return(result['results'])
                raise gen.Return(result)
        raise SparkPostAPIException(response)
