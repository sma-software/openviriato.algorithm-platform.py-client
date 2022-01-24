from typing import Type, List, Optional, Union, get_type_hints, get_origin, get_args
from py_client.communication.response_processing import AlgorithmPlatformConversionError
from py_client.aidm.aidm_base_classes import _HasID
from py_client.conversion.converter_helpers import *
from py_client.aidm.aidm_link_classes import AlgorithmConnectionLink, AlgorithmAwaitArrivalLink, AlgorithmRosterLink, LinkType
from abc import ABC, abstractmethod
import datetime
import isodate

class JsonToAidmProcessor:
    @abstractmethod
    def is_applicable(self, targeted_type: Type[object]) -> bool:
        pass

    @abstractmethod
    def process_attribute_dict(self, list:List[dict]) -> List[_HasID]:
        pass

    @abstractmethod
    def validate_that_is_optional_attribute(self, targeted_type: Type) -> None:
        if not is_optional(targeted_type):
            raise AlgorithmPlatformConversionError("The AIDM class got a None value for a non-optional field", None)

class ListProcessor(JsonToAidmProcessor):
    def is_applicable(self, targeted_type: Type[object]) -> bool:
        return is_list_type(targeted_type)

    def process_attribute_dict(self, list:List[Union[Primitive, dict]], targeted_type:Type[Union[_HasID, Primitive]]) -> List[Union[_HasID, Primitive]]:
        if is_primitive(get_type_of_list_element(targeted_type)):
            return list
        return [JsonToAidmConverter().process_json_to_aidm(element, get_type_of_list_element(targeted_type)) for element in list]

class AtomicTypeProcessor(JsonToAidmProcessor):
    def is_applicable(self, targeted_type: Type[object]) -> bool:
        return not is_list_type(targeted_type)

    def process_attribute_dict(self, attribute_dict:[Primitive, dict], targeted_type:Union[_HasID, Primitive]) -> Union[_HasID, Primitive]:
        if attribute_dict is None:
            self.validate_that_is_optional_attribute(targeted_type)
            return None
        if is_primitive(targeted_type):
            return attribute_dict

        state = convert_keys_to_snake_case(attribute_dict)

        print(targeted_type)
        object_attribute_and_attribute_type = get_type_hints(targeted_type)
        for attribute_name_with_class_name, attribute_type in object_attribute_and_attribute_type.items():
            attribute_name = self.unmangle(attribute_name_with_class_name)
            if attribute_name in state:
                state[attribute_name] = JsonToAidmConverter().process_json_to_aidm(state[attribute_name], attribute_type)
        return self.transform_processed_dict_to_aidm(targeted_type, state)

    @staticmethod
    def transform_processed_dict_to_aidm(targeted_type, snake_case_attribute_dict):
        try:
            return targeted_type(**snake_case_attribute_dict)
        except TypeError as e:
            raise AlgorithmPlatformConversionError(
                "Could not populate AIDM object, AIDM class {} is unknown, "\
                + "has unexpected attributes or is missing attributes.".format(targeted_type),
                e)

    @staticmethod
    def unmangle(attribute_name_with_class_name):
        return attribute_name_with_class_name.split("__")[-1]

class DatetimeProcessor(JsonToAidmProcessor):
    def is_applicable(self, targeted_type: Type[object]) -> bool:
        return is_of_type_or_optional_of_type(targeted_type, datetime.datetime)

    def process_attribute_dict(self, datetime_raw_str:str, targeted_type:datetime) -> datetime.datetime:
        if datetime_raw_str is None:
            self.validate_that_is_optional_attribute(targeted_type)
            return None
        try:
            return datetime.datetime.fromisoformat(datetime_raw_str)
        except Exception as e:
            raise AlgorithmPlatformConversionError(
                "Could not parse datetime, invalid datetime format: {}".format(datetime_raw_str),
                e)

class TimedeltaProcessor(JsonToAidmProcessor):
    def is_applicable(self, targeted_type: Type[object]) -> bool:
        return is_of_type_or_optional_of_type(targeted_type, datetime.timedelta)

    def process_attribute_dict(self, timedelta_raw_str:str, targeted_type:datetime) -> datetime.timedelta:
        if timedelta_raw_str is None:
            self.validate_that_is_optional_attribute(targeted_type)
            return None
        try:
            return isodate.parse_duration(timedelta_raw_str)
        except Exception as e:
            raise AlgorithmPlatformConversionError(
                "Could not parse duration, invalid duration format: {}".format(timedelta_raw_str),
                e)

class EnumProcessor(JsonToAidmProcessor):
    def is_applicable(self, targeted_type: Type[object]) -> bool:
        return is_enum_type(targeted_type)

    def process_attribute_dict(self, enum_value:str, aidm_class: Type[Enum]) -> Enum:
        try:
            return aidm_class(enum_value)
        except Exception as e:
            raise AlgorithmPlatformConversionError(
                "Could not parse Enum {}, invalid enum format for expected class Enum {}".format(enum_value, aidm_class),
                e
            )

class AlgorithmLinkProcessor(JsonToAidmProcessor):
    def is_applicable(self, targeted_type: Type[object]) -> bool:
        return targeted_type is Union[AlgorithmAwaitArrivalLink, AlgorithmConnectionLink, AlgorithmRosterLink]

    def process_attribute_dict(self, attribute_dict: dict, aidm_class: Type) -> Union[AlgorithmConnectionLink, AlgorithmAwaitArrivalLink, AlgorithmRosterLink]:
        link_type_as_str = convert_to_snake_case(attribute_dict.pop('type'))
        algorithm_link_type = self.get_link_type_from_link_type_as_str(link_type_as_str)
        return JsonToAidmConverter().process_json_to_aidm(attribute_dict, algorithm_link_type)

    def get_link_type_from_link_type_as_str(self, link_type_as_str: str):
        if link_type_as_str == LinkType.await_arrival.name:
            return AlgorithmAwaitArrivalLink
        elif link_type_as_str == LinkType.connection.name:
            return AlgorithmConnectionLink
        elif link_type_as_str == LinkType.roster.name:
            return AlgorithmRosterLink
        else:
            error_message = f"{link_type_as_str} can not be converted. Extend converter"
            raise AlgorithmPlatformConversionError(error_message, None)

class JsonToAidmConverter:
    __processors: List[JsonToAidmProcessor]

    def __init__(self):
        self.__processors = [
            ListProcessor(),
            DatetimeProcessor(),
            TimedeltaProcessor(),
            EnumProcessor(),
            AlgorithmLinkProcessor(),
            AtomicTypeProcessor()
        ]

    def process_json_to_aidm(self, attribute_dict: dict, targeted_type: Type[object]) -> _HasID:
        for processor in self.__processors:
            if (processor.is_applicable(targeted_type)):
                return processor.process_attribute_dict(attribute_dict, targeted_type)
        return attribute_dict



