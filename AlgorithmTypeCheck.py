import datetime


# move typechecks into own module -> AlgoPlatTypeAssertions
def assert_parameter_is_str(received_object: str, object_name: str, method_name: str) -> None:
    assert isinstance(received_object, str), \
        "in method {0}, \n the parameter {0} is required to be of type str \n " \
        "but it was a instead: {2}".format(method_name, object_name, received_object.__class__)


def assert_parameter_is_int(received_object: int, object_name: str, method_name: str) -> None:
    assert isinstance(received_object, int), \
        "in method {0}, \n the parameter {0} is required to be of type int \n " \
        "but it was a instead: {2}".format(method_name, object_name, received_object.__class__)


def assert_non_negative_weight(weight: int):
    assert not (weight < 0), 'only non-negative values for weights permitted'


def assert_datetime(date_time_obj: datetime.datetime):
    assert isinstance(date_time_obj, datetime.datetime), 'value has to be a datetime object'


def check_attributes_by_list(obj, attribute_names: list):
    for attribute_name in attribute_names:
        assert (hasattr(obj, attribute_name)), 'attribute {0} is missing'.format(attribute_name)