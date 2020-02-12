import requests
import json

def assert_parameter_is_str(received_object: str, object_name: str, method_name: str) -> None:
    assert isinstance(received_object, str), \
        "in method {0}, \n the parameter {0} is required to be of type str \n " \
        "but it was a instead: {2}".format(method_name, object_name, received_object.__class__)


def assert_parameter_is_int(received_object: int, object_name: str, method_name: str) -> None:
    assert isinstance(received_object, int), \
        "in method {0}, \n the parameter {0} is required to be of type int \n " \
        "but it was a instead: {2}".format(method_name, object_name, received_object.__class__)


def check_if_request_successful(api_return: requests.Response) -> None:
    """
    not all HTTPError Messages are completely indicative, depends on how the API is configured
    we therefore display the returned json in an additional error if it is a HTTPError
    # note that the connection will remain open if no error
    :param api_return: the raw objected returned by the api-request
    """
    try:
        api_return.raise_for_status()
    except requests.HTTPError:
        # if there is an error, the algorithm platform supplies us with more information (hopefully)
        try:
            rest_feedback = api_return.json()
        except json.decoder.JSONDecodeError:
            # there was no information/json, back to the previous error
            api_return.raise_for_status()
        raise AlgorithmPlatformError(rest_feedback['statusCode'], rest_feedback['message'])


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
