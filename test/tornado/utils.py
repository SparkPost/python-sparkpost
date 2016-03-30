from __future__ import print_function
from collections import namedtuple

from responses import RequestsMock
from tornado import ioloop
from tornado.concurrent import Future
from tornado.httpclient import HTTPRequest, HTTPResponse, HTTPError

Request = namedtuple("Request", ["url", "method", "headers", "body"])


class ResponseGenerator(object):
    def get_adapter(self, url):
        return self

    def build_response(self, request, response):
        resp = HTTPResponse(request, response.status, headers=response.headers,
                            effective_url=request.url, error=None, buffer="")
        resp._body = response.data
        f = Future()
        f.content = None
        if response.status < 200 or response.status >= 300:
            resp.error = HTTPError(response.status, response=resp)
            ioloop.IOLoop().current().add_callback(f.set_exception, resp.error)
        else:
            ioloop.IOLoop().current().add_callback(f.set_result, resp)
        return f


class AsyncClientMock(RequestsMock):
    def start(self):
        import mock

        def unbound_on_send(client, request, callback=None, **kwargs):
            if not isinstance(request, HTTPRequest):
                request = Request(request,
                                  kwargs.get("method", "GET"),
                                  kwargs.get("headers", []),
                                  kwargs.get("body", ""))
            return self._on_request(ResponseGenerator(), request)
        self._patcher = mock.patch('tornado.httpclient.AsyncHTTPClient.fetch',
                                   unbound_on_send)
        self._patcher.start()

    def stop(self):
        self._patcher.stop()
