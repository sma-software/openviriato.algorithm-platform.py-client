import datetime
import typing
from enum import unique, Enum
from typing import List, Optional, Union, get_origin, get_args, Type
from py_client.communication.response_processing import AlgorithmPlatformConversionError
import isodate


def _convert_to_camel_case(snake_case_key: str):
    split_by_underscore = snake_case_key.split('_')
    split_by_underscore_camel_case = [*map(str.title, split_by_underscore)]
    camel_case_with_first_letter_upper_case = ''.join(split_by_underscore_camel_case)
    return camel_case_with_first_letter_upper_case[:1].lower() + camel_case_with_first_letter_upper_case[1:]


def _translate_id(any_key: str) -> str:
    if any_key.endswith("ID"):
        leading_underscore_if_needed = "_" if (any_key.__len__() > 2) else ""
        return any_key.rstrip("ID") + leading_underscore_if_needed + "id"
    if any_key.endswith("IDs"):
        leading_underscore_if_needed = "_" if (any_key.__len__() > 3) else ""
        return any_key.rstrip("IDs") + leading_underscore_if_needed + "ids"
    else:
        return any_key


def convert_to_snake_case(any_key: str) -> str:
    snake_case_key = ""
    for character in any_key:
        leading_underscore_if_needed = "_" if character.isupper() else ""
        snake_case_key += leading_underscore_if_needed + character.lower()
    return snake_case_key.lstrip('_')


def _translate_key(key: str) -> str:
    key_with_correct_id = _translate_id(key)
    return convert_to_snake_case(key_with_correct_id)


def convert_keys_to_snake_case(json_with_camel_case_keys: dict) -> dict:
    snake_case_keys_and_camel_case_keys = [(_translate_key(key), key) for key in json_with_camel_case_keys.keys()]
    return {snake_case_key: json_with_camel_case_keys[camel_case_key] for snake_case_key, camel_case_key in
            snake_case_keys_and_camel_case_keys}


def parse_to_datetime(datetime_raw_str: str) -> datetime.datetime:
    return datetime.datetime.fromisoformat(datetime_raw_str)


def parse_to_timedelta(timedelta_raw_str: str) -> datetime.timedelta:
    return isodate.parse_duration(timedelta_raw_str)


def parse_to_timedelta_or_none(timedelta_raw_str: (str, None)) -> (datetime.timedelta, None):
    if timedelta_raw_str is not None:
        return parse_to_timedelta(timedelta_raw_str)
    else:
        return None


def convert_to_datetime_format_or_return_self(obj):
    if isinstance(obj, datetime.datetime):
        return obj.isoformat()
    elif isinstance(obj, datetime.timedelta):
        return isodate.duration_isoformat(obj)
    else:
        return obj

def is_optional(actual_type: Type) -> bool:
    return get_origin(actual_type) is Union and type(None) in get_args(actual_type)

def is_list_type(type: Type) -> bool:
    return get_origin(type) is list

def is_enum_type(received_type: Type) -> bool:
    return isinstance(received_type, type) and issubclass(received_type, Enum)

def get_type_of_list_element(type: Type) -> Type:
    if not is_list_type(type):
        raise TypeError("The targeted type is not a list.")
    return get_args(type)[0]

def get_type_of_optional_element(type: Type) -> Type:
    if not is_optional(type):
        raise TypeError("The targeted type is not optional.")
    return get_args(type)[0]

Primitive = Union[int, str, bool]
def is_primitive(value: object):
    list_of_primitive = Primitive.__args__
    return value in list_of_primitive or (is_optional(value) and get_type_of_optional_element(value) in list_of_primitive)

Struct = Union[datetime.datetime, datetime.timedelta]
def is_struct(value: object):
    list_of_struct = Struct.__args__
    return value in list_of_struct or (is_optional(value) and get_type_of_optional_element(value) in list_of_struct)

@unique
class RoutingEdgeType(Enum):
    incoming = "incoming"
    incoming_node_track = "incomingNodeTrack"
    outgoing = "outgoing"
    outgoing_node_track = "outgoingNodeTrack"
    crossing = "crossing"