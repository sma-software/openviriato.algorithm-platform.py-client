from abc import ABC, abstractmethod
from typing import Type, Tuple
from py_client.aidm import AlgorithmSectionTrack
from py_client.conversion.converter_helpers import convert_keys_to_snake_case

class JsonToAidmProcessor:
    @classmethod
    @abstractmethod
    def is_applicable(cls, aidm_class: Type[object]) -> bool:
        pass

    @classmethod
    @abstractmethod
    def process_attribute_dict(cls, aidm_class: Type[object], attribute_dictionary: dict) -> None:
        pass

class SectionTrackProcessor(JsonToAidmProcessor):
    @classmethod
    def is_applicable(cls, aidm_class: Type[object]) -> bool:
        return aidm_class is AlgorithmSectionTrack

    @classmethod
    def process_attribute_dict(cls, aidm_class: Type[object], attribute_dictionary: dict) -> AlgorithmSectionTrack:
        snake_case_attribute_dict = convert_keys_to_snake_case(attribute_dictionary)
        return aidm_class(**snake_case_attribute_dict)
