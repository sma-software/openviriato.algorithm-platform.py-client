from abc import ABC, abstractmethod
from typing import Type, Tuple
from py_client.aidm.aidm_base_classes import _HasID
from typing import get_type_hints, Optional, List

class JsonToAidmProcessor:
    @abstractmethod
    def is_applicable(self, aidm_class: Type[object]) -> bool:
        pass

    @abstractmethod
    def process_attribute_dict(self, attribute_dictionary: dict, aidm_class: Type[object]) -> None:
        pass