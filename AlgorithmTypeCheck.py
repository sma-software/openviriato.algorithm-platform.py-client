import requests
import json

# move typechecks into own module -> AlgoPlatTypeAssertions
def assert_parameter_is_str(received_object: str, object_name: str, method_name: str) -> None:
    assert isinstance(received_object, str), \
        "in method {0}, \n the parameter {0} is required to be of type str \n " \
        "but it was a instead: {2}".format(method_name, object_name, received_object.__class__)


def assert_parameter_is_int(received_object: int, object_name: str, method_name: str) -> None:
    assert isinstance(received_object, int), \
        "in method {0}, \n the parameter {0} is required to be of type int \n " \
        "but it was a instead: {2}".format(method_name, object_name, received_object.__class__)



