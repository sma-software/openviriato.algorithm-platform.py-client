from typing import Dict, get_type_hints
from py_client.aidm.aidm_base_classes import _HasID
from py_client.conversion.converter_helpers import *
from py_client.aidm.aidm_link_classes import _AlgorithmLink, AlgorithmAwaitArrivalLink, AlgorithmRosterLink, AlgorithmConnectionLink
from py_client.aidm.aidm_routing_edge_classes import _RoutingEdge
from py_client.aidm.aidm_routing_edge_classes import *
from abc import abstractmethod
from py_client.aidm.aidm_conflict import AlgorithmConflict, ConflictType, _AlgorithmTwoTrainsSectionTrackConflict, _AlgorithmOneTrainSectionTrackConflict, _AlgorithmOneTrainNodeConflict, _AlgorithmTwoTrainsNodeConflict
import datetime
import isodate


class _ABCJsonToAidmProcessor:
    @abstractmethod
    def is_applicable(self, json_to_process: Union[dict, Primitive, Optional[Primitive]], targeted_type: Type[object]) -> bool:
        pass

    @abstractmethod
    def process_attribute_dict(self, json_to_process: Union[dict, Primitive, Optional[Primitive]], targeted_type: Type[object]) -> object:
        pass


class _ABCJsonToAidmValueProcessor(_ABCJsonToAidmProcessor):
    @abstractmethod
    def is_applicable(self, json_to_process: Union[dict, Primitive, Optional[Primitive]], targeted_type: Type[object]) -> bool:
        pass

    @abstractmethod
    def process_attribute_dict(self, json_to_process: Union[dict, Primitive, Optional[Primitive]], targeted_type: Type[object]) -> object:
        pass


class _ABCJsonToAidmDictProcessor(_ABCJsonToAidmProcessor):
    @abstractmethod
    def is_applicable(self, json_to_process: Union[dict, Primitive, Optional[Primitive]], targeted_type: Type[object]) -> bool:
        pass

    @abstractmethod
    def process_attribute_dict(self, json_to_process: Union[dict, Primitive, Optional[Primitive]], targeted_type: Type[object]) -> object:
        pass


class DatetimeProcessor(_ABCJsonToAidmValueProcessor):
    def is_applicable(self, json_to_process: Union[dict, Primitive, Optional[Primitive]], targeted_type: Type[object]) -> bool:
        return targeted_type is datetime.datetime

    def process_attribute_dict(self, json_to_process: Union[dict, Primitive, Optional[Primitive]], targeted_type: Type[object]) -> object:
        try:
            return datetime.datetime.fromisoformat(json_to_process)
        except Exception as e:
            raise AlgorithmPlatformConversionError(
                "Could not parse datetime, invalid datetime format: {}".format(json_to_process),
                e)


class TimedeltaProcessor(_ABCJsonToAidmValueProcessor):
    def is_applicable(self, json_to_process: dict, targeted_type: Type[object]) -> bool:
        return targeted_type is datetime.timedelta

    def process_attribute_dict(self, json_to_process: Union[dict, Primitive, Optional[Primitive]], targeted_type: Type[object]) -> object:
        try:
            return isodate.parse_duration(json_to_process)
        except Exception as e:
            raise AlgorithmPlatformConversionError(
                "Could not parse duration, invalid duration format: {}".format(json_to_process),
                e)


class EnumProcessor(_ABCJsonToAidmValueProcessor):
    def is_applicable(self, json_to_process: Union[dict, Primitive, Optional[Primitive]], targeted_type: Type[object]) -> bool:
        return is_enum_type(targeted_type)

    def process_attribute_dict(self, json_to_process: Union[dict, Primitive, Optional[Primitive]], targeted_type: Type[object]) -> object:
        try:
            return targeted_type(json_to_process)
        except Exception as e:
            raise AlgorithmPlatformConversionError(
                "Could not parse Enum {}, invalid enum format for expected class Enum {}".format(json_to_process, targeted_type),
                e
            )


class PrimitiveProcessor(_ABCJsonToAidmValueProcessor):
    def is_applicable(self, json_to_process: Union[dict, Primitive, Optional[Primitive]], targeted_type: Type[object]) -> bool:
        return is_primitive(targeted_type)

    def process_attribute_dict(self, json_to_process: Union[dict, Primitive, Optional[Primitive]], targeted_type: Type[object]) -> object:
        return json_to_process


class ListProcessor(_ABCJsonToAidmValueProcessor):
    def is_applicable(self, json_to_process: Union[dict, Primitive, Optional[Primitive]], targeted_type: Type[object]) -> bool:
        return is_list_type(targeted_type)

    def process_attribute_dict(self, json_to_process: Union[dict, Primitive, Optional[Primitive]], targeted_type: Type[object]) -> object:
        if is_primitive(get_type_of_list_element(targeted_type)):
            return json_to_process
        return [JsonToAidmConverter().process_json_to_aidm(element, get_type_of_list_element(targeted_type)) for element in json_to_process]


class OptionalProcessor(_ABCJsonToAidmValueProcessor):
    def is_applicable(self, json_to_process: Union[dict, Primitive, Optional[Primitive]], targeted_type: Type[object]) -> bool:
        return is_optional(targeted_type)

    def process_attribute_dict(self, json_to_process: Union[dict, Primitive, Optional[Primitive]], targeted_type: Type[object]) -> object:
        if json_to_process is None:
            return None
        return JsonToAidmConverter().process_json_to_aidm(json_to_process, get_type_of_optional_element(targeted_type))


class SingleAttributeProcessor(_ABCJsonToAidmDictProcessor):
    def is_applicable(self, json_to_process: Union[dict, Primitive, Optional[Primitive]], targeted_type: Type[object]) -> bool:
        return is_single_attribute(json_to_process, targeted_type)

    def process_attribute_dict(self, json_to_process: Union[dict, Primitive, Optional[Primitive]], targeted_type: Type[object]) -> object:
        value_of_single_attribute = list(json_to_process.values())[0]
        return JsonToAidmConverter().process_json_to_aidm(value_of_single_attribute, targeted_type)


class GeneralAidmObjectProcessor(_ABCJsonToAidmDictProcessor):
    def is_applicable(self, json_to_process: Union[dict, Primitive, Optional[Primitive]], targeted_type: Type[object]) -> bool:
        # If it is not a list, we assume it is a general object, otherwise it will fail
        # as primitives, enums, list are handled by other processors
        return not is_list_type(targeted_type)

    def process_attribute_dict(self, json_to_process: Union[dict, Primitive, Optional[Primitive]], targeted_type: Type[object]) -> object:
        state = convert_keys_to_snake_case(json_to_process)

        object_attribute_and_attribute_type = get_type_hints(targeted_type)
        for attribute_name_with_class_name, attribute_type in object_attribute_and_attribute_type.items():
            attribute_name = self.unmangle(attribute_name_with_class_name)
            if attribute_name in state:
                state[attribute_name] = JsonToAidmConverter().process_json_to_aidm(state[attribute_name], attribute_type)
        return self.transform_processed_dict_to_aidm(targeted_type, state)

    @staticmethod
    def transform_processed_dict_to_aidm(targeted_type: Type[object], snake_case_attribute_dict: dict) -> object:
        try:
            return targeted_type(**snake_case_attribute_dict)
        except TypeError as e:
            raise AlgorithmPlatformConversionError(
                "Could not populate AIDM object, AIDM class {} is unknown, "\
                + "has unexpected attributes or is missing attributes.".format(targeted_type),
                e)

    @staticmethod
    def unmangle(attribute_name_with_class_name: str) -> str:
        return attribute_name_with_class_name.split("__")[-1]


class PolymorphicClassesProcessor(_ABCJsonToAidmDictProcessor):
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

    def is_applicable(self, json_to_process: Union[dict, Primitive, Optional[Primitive]], targeted_type: Type[object]) -> bool:
        is_not_an_object = not isinstance(targeted_type, type)
        if is_not_an_object:
            return False
        if True not in [issubclass(targeted_type, x) for x in self.types_to_process]:
            return False
        if 'type' not in json_to_process:
            # we can come into this branch after popping the type attribute or when we first see a polymorphic type
            # if we are for the first time here we have to have the type attribute
            if targeted_type in self.types_to_process:
                raise AlgorithmPlatformConversionError("Impossible to convert to {}. No attribute 'type' in the dictionary.".format(targeted_type), None)
            else:
                # otherwise the AtomicTypeProcessor does the conversion for us
                return False
        return True

    def process_attribute_dict(self, json_to_process: Union[dict, Primitive, Optional[Primitive]], targeted_type: Type[object]) -> object:
        # Remove the attribute type from the attribute_dict and convert it to snake case
        type_name_in_enum = convert_to_snake_case(json_to_process.pop('type'))
        target_type = self._get_type_from_enum_value(type_name_in_enum)
        return JsonToAidmConverter().process_json_to_aidm(json_to_process, target_type)

    def _get_type_from_enum_value(self, type_name_in_enum: str) -> Type:
        for type_to_process in self.aidm_types_to_create:
            snake_case_of_type_to_process = convert_to_snake_case(type_to_process.__name__)
            self._validate_most_specific_name_are_at_start_of_list()
            substring_start_index = snake_case_of_type_to_process.find(type_name_in_enum)
            is_targeted_type = substring_start_index != -1
            if is_targeted_type:
                return type_to_process
        raise AlgorithmPlatformConversionError("unexisting link {} can not be converted. Extend converter".format(type_name_in_enum), None)

    def _validate_most_specific_name_are_at_start_of_list(self):
        for aidm_type in self.aidm_types_to_create:
            for aidm_type_later_in_list in self.aidm_types_to_create[self.aidm_types_to_create.index(aidm_type) + 1:]:
                self._validate_first_is_more_specific(aidm_type, aidm_type_later_in_list)

    @staticmethod
    def _validate_first_is_more_specific(aidm_type: object, aidm_type_later_in_list:  object):
        type_name_parts_aidm_type = convert_to_snake_case(aidm_type.__name__).split('_')
        type_name_parts_aidm_type_later_in_list = convert_to_snake_case(aidm_type_later_in_list.__name__).split('_')
        is_first_type_less_specific = set(type_name_parts_aidm_type_later_in_list).issubset(set(type_name_parts_aidm_type))
        if is_first_type_less_specific:
            raise AlgorithmPlatformConversionError(
                "The types {} is less specific than {}. They must be in the reverse order in the types_to_process list to avoid conversion error".format(
                    aidm_type,
                    aidm_type_later_in_list), None)


class ConflictTypeMappingLookup:
    __lookup: Dict[ConflictType, AlgorithmConflict] = dict()

    def __init__(self):
        self.__lookup[ConflictType.Crossing] = _AlgorithmTwoTrainsSectionTrackConflict
        self.__lookup[ConflictType.Trafficability] = _AlgorithmOneTrainSectionTrackConflict
        self.__lookup[ConflictType.TravelDirectionChange] = _AlgorithmOneTrainNodeConflict
        self.__lookup[ConflictType.SimultaneousArrival] = _AlgorithmTwoTrainsNodeConflict
        self.__lookup[ConflictType.SameStationTrack] = _AlgorithmTwoTrainsNodeConflict
        self.__lookup[ConflictType.SameSectionTrack] = _AlgorithmTwoTrainsNodeConflict
        self.__lookup[ConflictType.IncompatibleStationRoutes] = _AlgorithmTwoTrainsNodeConflict
        self.__lookup[ConflictType.IncompatibleJunctionRoutes] = _AlgorithmTwoTrainsNodeConflict

    def get_conflict_type_mapping(self, enum_conflict_type: ConflictType) -> Type[AlgorithmConflict]:
        return self.__lookup[enum_conflict_type]


class ConflictProcessor(_ABCJsonToAidmProcessor):
    def is_applicable(self, json_to_process: Union[dict, Primitive, Optional[Primitive]], targeted_type: Type[object]) -> bool:
        return targeted_type == AlgorithmConflict

    def process_attribute_dict(self, json_to_process: Union[dict, Primitive, Optional[Primitive]], targeted_type: Type[object]) -> object:
        conflict_type_as_enum = JsonToAidmConverter().process_json_to_aidm(json_to_process["conflictType"], ConflictType)
        targeted_type = ConflictTypeMappingLookup().get_conflict_type_mapping(conflict_type_as_enum)
        return JsonToAidmConverter().process_json_to_aidm(json_to_process, targeted_type)


class JsonToAidmConverter:
    __processors: List[_ABCJsonToAidmProcessor]

    def __init__(self):
        self.__processors = [
            ListProcessor(),
            SingleAttributeProcessor(),
            OptionalProcessor(),
            DatetimeProcessor(),
            TimedeltaProcessor(),
            EnumProcessor(),
            PolymorphicClassesProcessor(),
            ConflictProcessor(),
            PrimitiveProcessor(),
            GeneralAidmObjectProcessor()
        ]

    def process_json_to_aidm(self, attribute_dict: Union[dict, Primitive, Optional[Primitive]], targeted_type: Type[object]) -> object:
        if attribute_dict is None:
            if self.targeted_type_cannot_have_none_value(targeted_type):
                raise AlgorithmPlatformConversionError("Got a None value for a non-optional type.", None)
            return None
        for processor in self.__processors:
            if processor.is_applicable(attribute_dict, targeted_type):
                return processor.process_attribute_dict(attribute_dict, targeted_type)
        raise AlgorithmPlatformConversionError("Found no appropriate processor for the given response", None)

    @staticmethod
    def targeted_type_cannot_have_none_value(targeted_type: Type[object]) -> bool:
        if is_optional(targeted_type):
            return False
        if is_primitive(targeted_type):
            return True
        return is_struct(targeted_type)
