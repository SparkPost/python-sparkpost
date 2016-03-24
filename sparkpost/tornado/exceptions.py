import json

from ..exceptions import SparkPostAPIException as RequestsSparkPostAPIException


class SparkPostAPIException(RequestsSparkPostAPIException):
    def __init__(self, response, *args, **kwargs):
        errors = [response.body or ""]
        try:
            data = json.loads(response.body)
            if data:
                errors = data['errors']
                errors = [e['message'] + ': ' + e.get('description', '')
                          for e in errors]
        except:
            pass
        message = """Call to {uri} returned {status_code}, errors:

        {errors}
        """.format(
            uri=response.effective_url,
            status_code=response.code,
            errors='\n'.join(errors)
        )
        super(RequestsSparkPostAPIException, self).__init__(message, *args,
                                                            **kwargs)