class SparkPostException(Exception):
    pass


class SparkPostAPIException(SparkPostException):
    "Handle 4xx and 5xx errors from the SparkPost API"
    def __init__(self, response, *args, **kwargs):
        errors = response.json()['errors']
        errors = [e['message'] + ': ' + e.get('description','') for e in errors]
        message = """Call to {uri} returned {status_code}, errors:

        {errors}
        """.format(
            uri=response.url,
            status_code=response.status_code,
            errors='\n'.join(errors)
        )
        super(SparkPostAPIException, self).__init__(message, *args, **kwargs)
