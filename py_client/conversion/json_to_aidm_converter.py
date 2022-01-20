from typing import Type, List, Optional, Union, get_type_hints, get_origin, get_args
from py_client.communication.response_processing import AlgorithmPlatformConversionError
from py_client.aidm.aidm_base_classes import _HasID
from py_client.conversion.converter_helpers import convert_keys_to_snake_case
from abc import ABC, abstractmethod
from py_client.aidm.aidm_aliases import Primitive, is_primitive


class JsonToAidmProcessor:
    @abstractmethod
    def is_applicable(self, aidm_class: Type[object]) -> bool:
        pass

    @abstractmethod
    def process_attribute_dict(self, list:List[dict]) -> List[_HasID]:
        pass

class ListOfAidmProcessor(JsonToAidmProcessor):
    def is_applicable(self, aidm_class: Type[object]) -> bool:
        return get_origin(aidm_class) is list

    def process_attribute_dict(self, list:List[Union[Primitive, dict]], aidm_class:Type[Union[_HasID, Primitive]]) -> List[Union[_HasID, Primitive]]:
        if is_primitive(get_args(aidm_class)[0]):
            return list
        return [JsonToAidmConverter().process_json_to_aidm(element, get_args(aidm_class)[0]) for element in list]

class AidmProcessor(JsonToAidmProcessor):
    def is_applicable(self, aidm_class: Type[object]) -> bool:
        return get_origin(aidm_class) is None

    def process_attribute_dict(self, attribute_dict:[Primitive, dict], aidm_class:Union[_HasID, Primitive]) -> Union[_HasID, Primitive]:
        if is_primitive(aidm_class) or attribute_dict is None:
            return attribute_dict

        state = convert_keys_to_snake_case(attribute_dict)

        object_attribute_and_attribute_type = get_type_hints(aidm_class)
        for attribute_name_with_class_name, attribute_type in object_attribute_and_attribute_type.items():
            attribute_name = self.unmangle(attribute_name_with_class_name)
            if attribute_name in state:
                state[attribute_name] = JsonToAidmConverter().process_json_to_aidm(state[attribute_name], attribute_type)
        return self.transform_processed_dict_to_aidm(aidm_class, state)

    @staticmethod
    def transform_processed_dict_to_aidm(aidm_class, snake_case_attribute_dict):
        try:
            return aidm_class(**snake_case_attribute_dict)
        except TypeError as e:
            raise AlgorithmPlatformConversionError(
                "Could not populate AIDM object, AIDM class {} is unknown.".format(aidm_class),
                e)

    @staticmethod
    def unmangle(attribute_name_with_class_name):
        return attribute_name_with_class_name.split("__")[-1]

class JsonToAidmConverter:
    __processors: List[JsonToAidmProcessor]

    def __init__(self):
        self.__processors = [
            ListOfAidmProcessor(),
            AidmProcessor()
        ]

    def process_json_to_aidm(self, attribute_dict: dict, aidm_class: Type[object]) -> _HasID:
        return self.process_one_attribute(aidm_class, attribute_dict)

    def process_one_attribute(self, attribute_type, unprocessed_value):
        for processor in self.__processors:
            if (processor.is_applicable(attribute_type)):
                return processor.process_attribute_dict(unprocessed_value, attribute_type)
        return unprocessed_value



