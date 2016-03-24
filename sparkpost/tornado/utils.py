from tornado.concurrent import Future


def wrap_future(future, convert):
    wrapper = Future()

    def handle_future(future):
        try:
            wrapper.set_result(convert(future.result()))
        except Exception as ex:
            wrapper.set_exception(ex)

    future.add_done_callback(handle_future)
    return wrapper
