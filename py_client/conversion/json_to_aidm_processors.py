from abc import ABC, abstractmethod
from typing import Type, Tuple
from py_client.aidm import AlgorithmSectionTrack
from py_client.conversion.converter_helpers import convert_keys_to_snake_case
from typing import get_type_hints, Optional, List

class JsonToAidmProcessor:
    @abstractmethod
    def is_applicable(cls, aidm_class: Type[object]) -> bool:
        pass

    @abstractmethod
    def process_attribute_dict(cls, aidm_class: Type[object], attribute_dictionary: dict) -> None:
        pass

class AidmWithOnlyPrimitivesProcessor(JsonToAidmProcessor):
    def is_applicable(cls, aidm_class: Type[object]) -> bool:
        attributeTypes = [attrType for _, attrType in get_type_hints(aidm_class).items()]
        builtInTypes = [str, int, bool, Optional[str], Optional[int], Optional[bool]]
        return all([a in builtInTypes for a in attributeTypes])

    def process_attribute_dict(cls, aidm_class: Type[object], attribute_dictionary: dict) -> AlgorithmSectionTrack:
        snake_case_attribute_dict = convert_keys_to_snake_case(attribute_dictionary)
        return aidm_class(**snake_case_attribute_dict)
