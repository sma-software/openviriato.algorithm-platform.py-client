import requests


def verify_parameter_is_str(received_object: object, object_name: str, method_name: str):
    assert isinstance(received_object, str), \
        "in method {0}, \n the parameter {0} is required to be of type str \n " \
        "but it was a instead: {2}".format(method_name, object_name, received_object.__class__)


def verify_parameter_is_int(received_object: object, object_name: str, method_name: str):
    assert isinstance(received_object, int), \
        "in method {0}, \n the parameter {0} is required to be of type int \n " \
        "but it was a instead: {2}".format(method_name, object_name, received_object.__class__)


def check_if_request_successful(api_return: requests.Response):
    """
    not all HTTPError Messages are completely indicative, depends on how the API is configured
    we therefore display the returned json in an additional error if it is a HTTPError
    :param api_return: the raw objected returned by the api-request
    """
    try:
        api_return.raise_for_status()
    except requests.HTTPError:
        # if there is an error, the algorithm platform supplies us with more information (hopefully)
        rest_feedback = api_return.json()
        raise AlgorithmPlatformError(rest_feedback['statusCode'], rest_feedback['message'])
    # note that the connection will remain open


class Error(Exception):
    """Base class for exceptions in this module."""
    pass


class AlgorithmPlatformError(Error):
    """Exception raised for errors in the input.

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, expression: str, message: str):
        self.expression = 'HTTPError {0}'.format(expression)
        self.message = message
