from typing import Dict, get_type_hints, Optional, List, TypeVar

from pyexpat.errors import messages

from py_client.aidm import AlgorithmDispatcherConnectionDelayReason, AlgorithmDispatcherOtherDelayReason
from py_client.aidm.aidm_train_simulation_classes import _AlgorithmDispatcherDelayReason
from py_client.communication.response_processing import AlgorithmPlatformConversionError
from py_client.conversion.converter_helpers import *
from py_client.aidm.aidm_link_classes import _AlgorithmLink, AlgorithmAwaitArrivalLink, AlgorithmRosterLink, AlgorithmConnectionLink
from py_client.aidm.aidm_routing_edge_classes import _RoutingEdgeRequest, _RoutingEdgeResponse
from py_client.aidm.aidm_routing_edge_classes import *
from abc import abstractmethod
from py_client.aidm.aidm_conflict import (
    AlgorithmConflict,
    ConflictType,
    _AlgorithmTwoTrainsSectionTrackConflict,
    _AlgorithmOneTrainSectionTrackConflict,
    _AlgorithmOneTrainNodeConflict,
    _AlgorithmTwoTrainsNodeConflict,
    _AlgorithmMultipleTrainsNodeConflict,
)
from datetime import datetime, timedelta
import isodate

T = TypeVar("T")


class _ABCJsonToAidmProcessor:
    @abstractmethod
    def is_applicable(self, json_to_process: Union[dict, Primitive, Optional[Primitive]], targeted_type: Type[object]) -> bool:
        pass

    @abstractmethod
    def process_attribute_dict(self, json_to_process: Union[dict, Primitive, Optional[Primitive]], targeted_type: Type[T]) -> T:
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
        return targeted_type is datetime

    def process_attribute_dict(self, json_to_process: Union[dict, Primitive, Optional[Primitive]], targeted_type: Type[object]) -> object:
        try:
            return datetime.fromisoformat(json_to_process.replace("%3A", ":"))
        except Exception as e:
            raise AlgorithmPlatformConversionError("Could not parse datetime, invalid datetime format: {}".format(json_to_process), e)


class TimedeltaProcessor(_ABCJsonToAidmValueProcessor):
    def is_applicable(self, json_to_process: dict, targeted_type: Type[object]) -> bool:
        return targeted_type is timedelta

    def process_attribute_dict(self, json_to_process: Union[dict, Primitive, Optional[Primitive]], targeted_type: Type[object]) -> object:
        try:
            return isodate.parse_duration(json_to_process)
        except Exception as e:
            raise AlgorithmPlatformConversionError("Could not parse duration, invalid duration format: {}".format(json_to_process), e)


class EnumProcessor(_ABCJsonToAidmValueProcessor):
    def is_applicable(self, json_to_process: Union[dict, Primitive, Optional[Primitive]], targeted_type: Type[object]) -> bool:
        return is_enum_type(targeted_type)

    def process_attribute_dict(self, json_to_process: Union[dict, Primitive, Optional[Primitive]], targeted_type: Type[object]) -> object:
        try:
            return targeted_type(json_to_process)
        except Exception as e:
            raise AlgorithmPlatformConversionError(
                "Could not parse Enum {}, invalid enum format for expected class Enum {}".format(json_to_process, targeted_type), e
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
                ("Could not populate AIDM object, AIDM class {} is unknown, has unexpected attributes or is missing attributes.").format(targeted_type), e
            )

    @staticmethod
    def unmangle(attribute_name_with_class_name: str) -> str:
        return attribute_name_with_class_name.split("__")[-1]


class PolymorphicClassesProcessor(_ABCJsonToAidmDictProcessor):
    types_to_process = [_AlgorithmLink, _RoutingEdgeRequest, _RoutingEdgeResponse, _AlgorithmDispatcherDelayReason]
    aidm_types_to_create = [
        AlgorithmDispatcherConnectionDelayReason,
        AlgorithmDispatcherOtherDelayReason,
        AlgorithmAwaitArrivalLink,
        AlgorithmConnectionLink,
        AlgorithmRosterLink,
        CrossingRoutingEdgeRequest,
        IncomingRoutingEdgeRequest,
        IncomingNodeTrackRoutingEdgeRequest,
        OutgoingRoutingEdgeRequest,
        OutgoingNodeTrackRoutingEdgeRequest,
        CrossingRoutingEdgeResponse,
        IncomingNodeTrackRoutingEdgeResponse,
        OutgoingNodeTrackRoutingEdgeResponse,
    ]

    def is_applicable(self, json_to_process: Union[dict, Primitive, Optional[Primitive]], targeted_type: Type[object]) -> bool:
        is_not_an_object = not isinstance(targeted_type, type)
        if is_not_an_object:
            return False
        if True not in [issubclass(targeted_type, x) for x in self.types_to_process]:
            return False
        return True

    def process_attribute_dict(self, json_to_process: Union[dict, Primitive, Optional[Primitive]], targeted_polymorphic_type: Type[object]) -> object:

        if not json_to_process.__contains__("type"):
            raise AlgorithmPlatformConversionError("Missing 'type' property in json for class {}".format(targeted_polymorphic_type), None)

        type_name_in_enum = convert_to_snake_case(json_to_process.pop("type"))

        target_types = self._get_possible_types_from_enum_value(type_name_in_enum)
        if len(target_types) == 0:
            message = "Type '{}' for class {} is unknown. Extend PolymorphicClassesProcessor in the json_to_aidm_converter".format(
                type_name_in_enum, str(targeted_polymorphic_type)
            )
            raise AlgorithmPlatformConversionError(message, None)
        aidm_object_to_return = None
        exception_for_matching_type = None
        for targeted_type in target_types:
            try:
                if aidm_object_to_return != None:
                    raise AlgorithmPlatformConversionError("Unexpected second conversion possible.", None)
                if issubclass(targeted_type, targeted_polymorphic_type):
                    aidm_object_to_return = GeneralAidmObjectProcessor().process_attribute_dict(json_to_process, targeted_type)
            except AlgorithmPlatformConversionError as e:
                exception_for_matching_type = e
                # not every type needs to fit, just ignore then, just find one fitting
                pass

        if aidm_object_to_return is None:
            message = "Type '{}' for class {} could not be converted by the json_to_aidm_converter. Details: {}".format(
                type_name_in_enum,
                str(targeted_polymorphic_type),
                str(exception_for_matching_type.args[0]) if exception_for_matching_type is not None else "no details given",
            )
            raise AlgorithmPlatformConversionError(message, exception_for_matching_type)
        return aidm_object_to_return

    def _get_possible_types_from_enum_value(self, type_name_in_enum: str) -> List[Type]:
        found_types = []
        for type_to_process in self.aidm_types_to_create:
            snake_case_of_type_to_process = convert_to_snake_case(type_to_process.__name__)
            substring_start_index = snake_case_of_type_to_process.find(type_name_in_enum)
            is_possible_targeted_type = substring_start_index != -1
            if is_possible_targeted_type:
                found_types.append(type_to_process)
        return found_types


class ConflictTypeMappingLookup:
    __lookup: Dict[ConflictType, AlgorithmConflict] = dict()

    def __init__(self):
        self.__lookup[ConflictType.Crossing] = _AlgorithmTwoTrainsSectionTrackConflict
        self.__lookup[ConflictType.InvalidDrivingDirection] = _AlgorithmOneTrainSectionTrackConflict
        self.__lookup[ConflictType.DrivingDirectionChange] = _AlgorithmOneTrainNodeConflict
        self.__lookup[ConflictType.SimultaneousArrivalSeparationTime] = _AlgorithmTwoTrainsNodeConflict
        self.__lookup[ConflictType.SameStationTrackSeparationTime] = _AlgorithmTwoTrainsNodeConflict
        self.__lookup[ConflictType.SameSectionTrackSeparationTime] = _AlgorithmTwoTrainsNodeConflict
        self.__lookup[ConflictType.IncompatibleStationRoutes] = _AlgorithmTwoTrainsNodeConflict
        self.__lookup[ConflictType.IncompatibleJunctionRoutes] = _AlgorithmTwoTrainsNodeConflict
        self.__lookup[ConflictType.HeadwayTime] = _AlgorithmTwoTrainsSectionTrackConflict
        self.__lookup[ConflictType.Overtaking] = _AlgorithmTwoTrainsSectionTrackConflict
        self.__lookup[ConflictType.CongestedNode] = _AlgorithmMultipleTrainsNodeConflict
        self.__lookup[ConflictType.ImpossibleStationExitRoute] = _AlgorithmOneTrainNodeConflict
        self.__lookup[ConflictType.ImpossibleStationEntryRoute] = _AlgorithmOneTrainNodeConflict
        self.__lookup[ConflictType.ImpossibleJunctionRoute] = _AlgorithmOneTrainNodeConflict
        self.__lookup[ConflictType.StopInJunction] = _AlgorithmOneTrainNodeConflict
        self.__lookup[ConflictType.NoStationTrackAssigned] = _AlgorithmOneTrainNodeConflict
        self.__lookup[ConflictType.StationTrackLength] = _AlgorithmOneTrainNodeConflict
        self.__lookup[ConflictType.PlatformLength] = _AlgorithmOneTrainNodeConflict
        self.__lookup[ConflictType.LevelTrackCrossingTime] = _AlgorithmTwoTrainsNodeConflict
        self.__lookup[ConflictType.ForbiddenStationTrack] = _AlgorithmOneTrainNodeConflict

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
            GeneralAidmObjectProcessor(),
        ]

    def process_json_to_aidm(self, attribute_dict: Union[dict, Primitive, Optional[Primitive]], targeted_type: Type[T]) -> T:
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
