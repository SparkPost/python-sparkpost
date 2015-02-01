class SparkPostException(Exception):
    pass


class SparkPostAPIException(SparkPostException):
    "Handle 4xx and 5xx errors from the SparkPost API"
    pass
