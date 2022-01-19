from typing import Type, List, get_type_hints
from py_client.conversion.json_to_aidm_processors import JsonToAidmProcessor
from py_client.communication.response_processing import AlgorithmPlatformConversionError
from py_client.aidm.aidm_base_classes import _HasID
from py_client.conversion.converter_helpers import convert_keys_to_snake_case

class JsonToAidmConverter:
    __processors: List[JsonToAidmProcessor]

    def __init__(self):
        self.__processors = []

    def process_json_to_aidm(self, attribute_dict: dict, aidm_class: Type[object]) -> _HasID:
        state = attribute_dict

        object_attribute_and_attribute_type = get_type_hints(aidm_class)
        for attribute_name_with_class_name, attribute_type in object_attribute_and_attribute_type.items():
            attribute_name = attribute_name_with_class_name.split("__")[-1]

            for processor in self.__processors:
                if (processor.is_applicable(self.__processors)):
                    state = processor.process_attribute_dict(state[attribute_name])
        try:
            return self.transform_processed_dict_to_aidm(aidm_class, state)
        except TypeError as e:
            raise AlgorithmPlatformConversionError(
                "Could not populate AIDM object, AIDM class {} is unknown.".format(aidm_class),
                e)

    def transform_processed_dict_to_aidm(self, aidm_class, state):
        snake_case_attribute_dict = convert_keys_to_snake_case(state)
        return aidm_class(**snake_case_attribute_dict)