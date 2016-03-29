class SparkPostException(Exception):
    pass


class SparkPostAPIException(SparkPostException):
    "Handle 4xx and 5xx errors from the SparkPost API"
    def __init__(self, response, *args, **kwargs):
        self.response_status_code = response.status_code
        self.response_error_codes = []
        content_type = response.headers.get('content-type', '').lower()
        if 'application/json' in content_type:
            errors = response.json()['errors']
            self.response_error_codes = [e['code'] for e in errors
                                         if 'code' in e]
            errors = [e['message'] + ': ' + e.get('description', '')
                      for e in errors]
        else:
            errors = ['Not available - no JSON response']
        message = """Call to {uri} returned {status_code}, errors:

        {errors}
        """.format(
            uri=response.url,
            status_code=response.status_code,
            errors='\n'.join(errors)
        )
        super(SparkPostAPIException, self).__init__(message, *args, **kwargs)
