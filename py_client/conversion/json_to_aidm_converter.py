from typing import Type, List, Optional, Union, get_type_hints, get_origin, get_args
from py_client.communication.response_processing import AlgorithmPlatformConversionError
from py_client.aidm.aidm_base_classes import _HasID
from py_client.conversion.converter_helpers import *
from py_client.aidm.aidm_link_classes import _AlgorithmLink, AlgorithmAwaitArrivalLink, AlgorithmRosterLink, AlgorithmRosterLinkDefinition, AlgorithmConnectionLink
from py_client.aidm.aidm_routing_edge_classes import _RoutingEdge, CrossingRoutingEdge, IncomingRoutingEdge, OutgoingRoutingEdge, IncomingNodeTrackRoutingEdge, OutgoingNodeTrackRoutingEdge
from py_client.aidm.aidm_routing_edge_classes import *
from abc import ABC, abstractmethod
from py_client.aidm.aidm_conflict import _AlgorithmConflict, AlgorithmNodeConflict, AlgorithmSectionTrackConflict
import datetime
import isodate

class JsonToAidmProcessor:
    @abstractmethod
    def is_applicable(self, attribute_dict: dict, targeted_type: Type[object]) -> bool:
        pass

    @abstractmethod
    def process_attribute_dict(self, list:List[dict]) -> List[_HasID]:
        pass

class ListProcessor(JsonToAidmProcessor):
    def is_applicable(self, attribute_dict: dict, targeted_type: Type[object]) -> bool:
        return is_list_type(targeted_type)

    def process_attribute_dict(self, list:List[Union[Primitive, dict]], targeted_type:Type[Union[_HasID, Primitive]]) -> List[Union[_HasID, Primitive]]:
        if is_primitive(get_type_of_list_element(targeted_type)):
            return list
        return [JsonToAidmConverter().process_json_to_aidm(element, get_type_of_list_element(targeted_type)) for element in list]

class OptionalProcessor(JsonToAidmProcessor):
    def is_applicable(self, attribute_dict: dict, targeted_type: Type[object]) -> bool:
        return is_optional(targeted_type)

    def process_attribute_dict(self, optional_value:Optional[Union[Primitive, dict]], targeted_type:Type[Union[_HasID, Primitive]]) -> Optional[object]:
        if optional_value is None:
            return None
        return JsonToAidmConverter().process_json_to_aidm(optional_value, get_type_of_optional_element(targeted_type))

class AtomicTypeProcessor(JsonToAidmProcessor):
    def is_applicable(self, attribute_dict: dict, targeted_type: Type[object]) -> bool:
        return not is_list_type(targeted_type)

    def process_attribute_dict(self, attribute_dict:[Primitive, dict], targeted_type:Union[_HasID, Primitive]) -> Union[_HasID, Primitive]:
        if is_primitive(targeted_type):
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
    def is_applicable(self, attribute_dict: dict, targeted_type: Type[object]) -> bool:
        return targeted_type is datetime.datetime

    def process_attribute_dict(self, datetime_raw_str:str, targeted_type:datetime) -> datetime.datetime:
        try:
            return datetime.datetime.fromisoformat(datetime_raw_str)
        except Exception as e:
            raise AlgorithmPlatformConversionError(
                "Could not parse datetime, invalid datetime format: {}".format(datetime_raw_str),
                e)

class TimedeltaProcessor(JsonToAidmProcessor):
    def is_applicable(self, attribute_dict: dict, targeted_type: Type[object]) -> bool:
        return targeted_type is datetime.timedelta

    def process_attribute_dict(self, timedelta_raw_str:str, targeted_type:datetime) -> datetime.timedelta:
        try:
            return isodate.parse_duration(timedelta_raw_str)
        except Exception as e:
            raise AlgorithmPlatformConversionError(
                "Could not parse duration, invalid duration format: {}".format(timedelta_raw_str),
                e)

class EnumProcessor(JsonToAidmProcessor):
    def is_applicable(self, attribute_dict: dict, targeted_type: Type[object]) -> bool:
        return is_enum_type(targeted_type)

    def process_attribute_dict(self, enum_value:str, aidm_class: Type[Enum]) -> Enum:
        try:
            return aidm_class(enum_value)
        except Exception as e:
            raise AlgorithmPlatformConversionError(
                "Could not parse Enum {}, invalid enum format for expected class Enum {}".format(enum_value, aidm_class),
                e
            )


class PolymorphicClassesProcessor(JsonToAidmProcessor):
    types_to_process = [_AlgorithmLink,
                        _RoutingEdge
                        ]
    aidm_types_to_create = [AlgorithmAwaitArrivalLink,
                            AlgorithmConnectionLink,
                            AlgorithmRosterLink,
                            CrossingRoutingEdge,
                            IncomingRoutingEdge,
                            IncomingNodeTrackRoutingEdge,
                            OutgoingRoutingEdge,
                            OutgoingNodeTrackRoutingEdge
                            ]

    def is_applicable(self, attribute_dict: dict, targeted_type: Type[object]) -> bool:
        if not True in [ issubclass(targeted_type, x) for x in self.types_to_process ]:
            return False
        if not 'type' in attribute_dict:
            # we can come into this branch after popping the type attribute or when we first see a polymorphic type
            # if we are for the first time here we have to have the type attribute
            if targeted_type in self.types_to_process:
                raise AlgorithmPlatformConversionError("Impossible to convert to {}. No attribute 'type' in the dictionary.".format(targeted_type), None)
            else:
                # otherwise the AtomicTypeProcessor does the conversion for us
                return False
        return True


    def process_attribute_dict(self, attribute_dict: dict, aidm_class: Type) -> object:
        # Remove the attribute type from the attribute_dict and convert it to snake case
        type_name_in_enum = convert_to_snake_case(attribute_dict.pop('type'))
        target_type = self._get_type_from_enum_value(type_name_in_enum)
        return JsonToAidmConverter().process_json_to_aidm(attribute_dict, target_type)

    def _get_type_from_enum_value(self, type_name_in_enum: str) -> Type:
        for type_to_process in self.aidm_types_to_create:
            snake_case_of_type_to_process = convert_to_snake_case(type_to_process.__name__)
            self._validate_most_specific_name_are_at_start_of_list()
            substring_start_index = snake_case_of_type_to_process.find(type_name_in_enum)
            is_targeted_type = substring_start_index != -1
            if  is_targeted_type:
                return type_to_process
        raise AlgorithmPlatformConversionError("unexisting link {} can not be converted. Extend converter".format(type_name_in_enum), None)

    def _validate_most_specific_name_are_at_start_of_list(self):
        for aidm_type in self.aidm_types_to_create:
            for aidm_type_later_in_list in self.aidm_types_to_create[self.aidm_types_to_create.index(aidm_type) + 1 :]:
                self._validate_first_is_more_specific(aidm_type, aidm_type_later_in_list)

    def _validate_first_is_more_specific(self, aidm_type, aidm_type_later_in_list):
        type_name_parts_aidm_type = convert_to_snake_case(aidm_type.__name__).split('_')
        type_name_parts_aidm_type_later_in_list = convert_to_snake_case(aidm_type_later_in_list.__name__).split('_')
        is_first_type_less_specific = set(type_name_parts_aidm_type_later_in_list).issubset(set(type_name_parts_aidm_type))
        if is_first_type_less_specific:
            raise AlgorithmPlatformConversionError(
                "The types {} is less specific than {}. They must be in the reverse order in the types_to_process list to avoid conversion error".format(
                    aidm_type,
                    aidm_type_later_in_list), None)

# TODO VPLAT-9453: Remove this processor
class ConflictProcessor(JsonToAidmProcessor):
    def is_applicable(self, attribute_dict: dict, targeted_type: Type[object]) -> bool:
        return targeted_type == _AlgorithmConflict

    def process_attribute_dict(self, attribute_dict: dict, aidm_class: Type) -> object:
        if "sectionTrackId" in attribute_dict.keys():
            return JsonToAidmConverter().process_json_to_aidm(attribute_dict, AlgorithmSectionTrackConflict)
        else:
            return JsonToAidmConverter().process_json_to_aidm(attribute_dict, AlgorithmNodeConflict)

class JsonToAidmConverter:
    __processors: List[JsonToAidmProcessor]

    def __init__(self):
        self.__processors = [
            ListProcessor(),
            OptionalProcessor(),
            DatetimeProcessor(),
            TimedeltaProcessor(),
            EnumProcessor(),
            PolymorphicClassesProcessor(),
            ConflictProcessor(),
            AtomicTypeProcessor()
        ]

    def process_json_to_aidm(self, attribute_dict: dict, targeted_type: Type[object]) -> object:
        if attribute_dict is None:
            if self.targeted_type_cannot_have_none_value(targeted_type):
                raise AlgorithmPlatformConversionError("Got a None value for a non-optional type.", None)
            return None
        for processor in self.__processors:
            if (processor.is_applicable(attribute_dict, targeted_type)):
                return processor.process_attribute_dict(attribute_dict, targeted_type)
        raise AlgorithmPlatformConversionError("Found no appropriate processor for the given response", None)

    def targeted_type_cannot_have_none_value(self, targeted_type):
        if is_optional(targeted_type):
            return False
        if is_primitive(targeted_type):
            return True
        return is_struct(targeted_type)