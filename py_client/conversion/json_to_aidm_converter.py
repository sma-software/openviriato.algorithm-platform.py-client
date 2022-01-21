from typing import Type, List, Optional, Union, get_type_hints, get_origin, get_args
from py_client.communication.response_processing import AlgorithmPlatformConversionError
from py_client.aidm.aidm_base_classes import _HasID
from py_client.conversion.converter_helpers import convert_keys_to_snake_case
from abc import ABC, abstractmethod
from py_client.aidm.aidm_aliases import Primitive, is_primitive
import datetime
import isodate

class JsonToAidmProcessor:
    @abstractmethod
    def is_applicable(self, targeted_type: Type[object]) -> bool:
        pass

    @abstractmethod
    def process_attribute_dict(self, list:List[dict]) -> List[_HasID]:
        pass

class ListProcessor(JsonToAidmProcessor):
    def is_applicable(self, targeted_type: Type[object]) -> bool:
        return get_origin(targeted_type) is list

    def process_attribute_dict(self, list:List[Union[Primitive, dict]], targeted_type:Type[Union[_HasID, Primitive]]) -> List[Union[_HasID, Primitive]]:
        if is_primitive(get_args(targeted_type)[0]):
            return list
        return [JsonToAidmConverter().process_json_to_aidm(element, get_args(targeted_type)[0]) for element in list]

class AtomicTypeProcessor(JsonToAidmProcessor):
    def is_applicable(self, targeted_type: Type[object]) -> bool:
        return get_origin(targeted_type) is None

    def process_attribute_dict(self, attribute_dict:[Primitive, dict], targeted_type:Union[_HasID, Primitive]) -> Union[_HasID, Primitive]:
        if is_primitive(targeted_type) or attribute_dict is None:
            return attribute_dict

        state = convert_keys_to_snake_case(attribute_dict)

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
        return targeted_type in [datetime.datetime, Optional[datetime.datetime]]

    def process_attribute_dict(self, datetime_raw_str:str, targeted_type:datetime) -> datetime.datetime:
        if datetime_raw_str is None:
            return datetime_raw_str
        return datetime.datetime.fromisoformat(datetime_raw_str)

class TimedeltaProcessor(JsonToAidmProcessor):
    def is_applicable(self, targeted_type: Type[object]) -> bool:
        return targeted_type in [datetime.timedelta, Optional[datetime.timedelta]]

    def process_attribute_dict(self, timedelta_raw_str:str, targeted_type:datetime) -> datetime.timedelta:
        if timedelta_raw_str is None:
            return timedelta_raw_str
        return isodate.parse_duration(timedelta_raw_str)

class JsonToAidmConverter:
    __processors: List[JsonToAidmProcessor]

    def __init__(self):
        self.__processors = [
            ListProcessor(),
            DatetimeProcessor(),
            TimedeltaProcessor(),
            AtomicTypeProcessor()
        ]

    def process_json_to_aidm(self, attribute_dict: dict, targeted_type: Type[object]) -> _HasID:
        for processor in self.__processors:
            if (processor.is_applicable(targeted_type)):
                return processor.process_attribute_dict(attribute_dict, targeted_type)
        return attribute_dict



