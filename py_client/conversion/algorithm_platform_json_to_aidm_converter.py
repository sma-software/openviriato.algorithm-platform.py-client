import inspect
from typing import Union, TypeVar, Type, Dict

from py_client.aidm import *
from py_client.communication.response_processing import AlgorithmPlatformConversionError
from py_client.conversion.converter_helpers import parse_to_datetime, parse_to_timedelta, parse_to_timedelta_or_none, \
    convert_keys_to_snake_case, convert_to_snake_case, RoutingEdgeType

EnumType = TypeVar("EnumType", bound=Enum)


def convert(aidm_class_or_aidm_class_factory, attribute_dict: dict):
    snake_case_attribute_dict = convert_keys_to_snake_case(attribute_dict)
    is_factory_method = inspect.isfunction(aidm_class_or_aidm_class_factory)
    if is_factory_method:
        return aidm_class_or_aidm_class_factory(snake_case_attribute_dict)
    else:
        try:
            return aidm_class_or_aidm_class_factory(**snake_case_attribute_dict)
        except TypeError as error_instance:
            raise AlgorithmPlatformConversionError(
                "Could not populate AIDM object, client AIDM class deviates from server AIDM class",
                error_instance)


def convert_list(aidm_class, list_of_dict: list) -> list:
    return [convert(aidm_class, dict_from_list) for dict_from_list in list_of_dict]


def convert_json_to_algorithm_node(attribute_dict: dict) -> AlgorithmNode:
    snake_case_dict = convert_keys_to_snake_case(attribute_dict)
    snake_case_dict['node_tracks'] = convert_list(AlgorithmNodeTrack, snake_case_dict['node_tracks'])
    return convert(AlgorithmNode, snake_case_dict)


def convert_json_to_algorithm_train_path_node(attribute_dict: dict) -> AlgorithmTrainPathNode:
    snake_case_dict = convert_keys_to_snake_case(attribute_dict)
    snake_case_dict['stop_status'] = StopStatus(snake_case_dict['stop_status'])
    for key in ['arrival_time', 'departure_time']:
        snake_case_dict[key] = parse_to_datetime(snake_case_dict[key])
    snake_case_dict['minimum_run_time'] = parse_to_timedelta_or_none(snake_case_dict['minimum_run_time'])
    snake_case_dict['minimum_stop_time'] = parse_to_timedelta(snake_case_dict['minimum_stop_time'])
    return convert(AlgorithmTrainPathNode, snake_case_dict)


def convert_json_to_algorithm_train(attribute_dict: dict) -> AlgorithmTrain:
    snake_case_dict = convert_keys_to_snake_case(attribute_dict)
    snake_case_dict['train_path_nodes'] = [convert_json_to_algorithm_train_path_node(train_path_node)
                                           for train_path_node in snake_case_dict['train_path_nodes']]
    return convert(AlgorithmTrain, snake_case_dict)


def convert_json_to_time_window(attribute_dict: dict) -> TimeWindow:
    snake_case_dict = convert_keys_to_snake_case(attribute_dict)
    for key in ['from_time', 'to_time']:
        snake_case_dict[key] = parse_to_datetime(snake_case_dict[key])
    return convert(TimeWindow, snake_case_dict)


def convert_json_to_algorithm_section_track_closure(attribute_dict: dict) -> AlgorithmSectionTrackClosure:
    snake_case_dict = convert_keys_to_snake_case(attribute_dict)
    for key in ['closure_time_window_from_node', 'closure_time_window_to_node']:
        snake_case_dict[key] = convert_json_to_time_window(snake_case_dict[key])
    return convert(AlgorithmSectionTrackClosure, snake_case_dict)


def convert_json_to_algorithm_node_track_closure(attribute_dict: dict) -> AlgorithmNodeTrackClosure:
    snake_case_dict = convert_keys_to_snake_case(attribute_dict)
    snake_case_dict["closure_time_window"] = convert_json_to_time_window(snake_case_dict["closure_time_window"])
    return convert(AlgorithmNodeTrackClosure, snake_case_dict)


def convert_to_routing_edges(
        json_edge_list: List[Dict[str, Union[str, int]]]
) -> List[Union[IncomingNodeTrackRoutingEdge, OutgoingNodeTrackRoutingEdge, CrossingRoutingEdge]]:
    edges = []
    for edge_as_dict in json_edge_list:
        edge_type = edge_as_dict.pop("type")
        if edge_type == RoutingEdgeType.incoming.value:
            edges.append(convert(IncomingRoutingEdge, edge_as_dict))
        elif edge_type == RoutingEdgeType.incoming_node_track.value:
            edges.append(convert(IncomingNodeTrackRoutingEdge, edge_as_dict))
        elif edge_type == RoutingEdgeType.outgoing.value:
            edges.append(convert(OutgoingRoutingEdge, edge_as_dict))
        elif edge_type == RoutingEdgeType.outgoing_node_track.value:
            edges.append(convert(OutgoingNodeTrackRoutingEdge, edge_as_dict))
        elif edge_type == RoutingEdgeType.crossing.value:
            edges.append(convert(CrossingRoutingEdge, edge_as_dict))
        else:
            raise AlgorithmPlatformConversionError(
                f"Cannot convert edge type {edge_type}", NotImplementedError(edge_as_dict)
            )
    return edges


def convert_json_to_update_train_times(attribute_dict: dict) -> UpdateTimesTrain:
    snake_case_dict = convert_keys_to_snake_case(attribute_dict)
    snake_case_dict["update_times_train_path_nodes"] = convert_list(
        convert_json_to_update_train_times_node,
        snake_case_dict["update_times_train_path_nodes"])
    return convert(UpdateTimesTrain, snake_case_dict)


def convert_json_to_update_train_times_node(attribute_dict: dict) -> UpdateTimesTrainPathNode:
    snake_case_dict = convert_keys_to_snake_case(attribute_dict)
    for key in ['arrival_time', 'departure_time']:
        snake_case_dict[key] = parse_to_datetime(snake_case_dict[key])
    for key in ['minimum_run_time', 'minimum_stop_time']:
        snake_case_dict[key] = parse_to_timedelta_or_none(snake_case_dict[key])
    if snake_case_dict['stop_status'] is not None:
        snake_case_dict['stop_status'] = StopStatus(snake_case_dict['stop_status'])
    return convert(UpdateTimesTrainPathNode, snake_case_dict)


def convert_json_to_algorithm_link(attribute_dict: dict) -> Union[AlgorithmConnectionLink, AlgorithmAwaitArrivalLink]:
    link_type_as_str = convert_to_snake_case(attribute_dict.pop('type'))
    snake_case_dict = convert_keys_to_snake_case(attribute_dict)
    if link_type_as_str == LinkType.await_arrival.name:
        snake_case_dict['minimum_duration'] = parse_to_timedelta(snake_case_dict['minimum_duration'])
        return convert(AlgorithmAwaitArrivalLink, snake_case_dict)
    elif link_type_as_str == LinkType.connection.name:
        snake_case_dict['minimum_duration'] = parse_to_timedelta(snake_case_dict['minimum_duration'])
        snake_case_dict['maximum_deviation'] = parse_to_timedelta_or_none(snake_case_dict['maximum_deviation'])
        return convert(AlgorithmConnectionLink, snake_case_dict)
    elif link_type_as_str == LinkType.roster.name:
        return convert(AlgorithmRosterLink, snake_case_dict)
    else:
        error_message = f"{link_type_as_str} can not be converted. Extend converter"
        raise AlgorithmPlatformConversionError(error_message, None)


def convert_algorithm_parameter_value_to_enum(
        enum_type: Type[EnumType],
        enum_algorithm_parameter_value: object) -> EnumType:
    enum_has_value_provided_by_algorithm_platform = \
        enum_algorithm_parameter_value in set(item.value for item in enum_type)
    if enum_has_value_provided_by_algorithm_platform:
        return enum_type(enum_algorithm_parameter_value)
    else:
        error_message = "{0} does not have a value {1}".format(
            enum_type,
            enum_algorithm_parameter_value)
        raise AlgorithmPlatformConversionError(error_message, None)


def convert_to_routing_edge_pair(attribute_dict: dict) -> RoutingEdgePair:
    incoming_routing_edge: dict = attribute_dict["incoming_routing_edge"]
    if incoming_routing_edge is None:
        incoming_node_track_routing_edge = None
    else:
        incoming_routing_edge.pop("type")
        incoming_node_track_routing_edge = convert(IncomingNodeTrackRoutingEdge, incoming_routing_edge)
    outgoing_routing_edge: dict = attribute_dict["outgoing_routing_edge"]
    if outgoing_routing_edge is None:
        outgoing_node_track_routing_edge = None
    else:
        outgoing_routing_edge.pop("type")
        outgoing_node_track_routing_edge = convert(OutgoingNodeTrackRoutingEdge, outgoing_routing_edge)
    return RoutingEdgePair(incoming_node_track_routing_edge, outgoing_node_track_routing_edge)


def convert_to_termination_request(attribute_dict: dict) -> TerminationRequest:
    snake_case_dict = convert_keys_to_snake_case(attribute_dict)
    if snake_case_dict["termination_requested_timestamp"] is None:
        return TerminationRequest(None)
    else:
        return TerminationRequest(parse_to_datetime(snake_case_dict["termination_requested_timestamp"]))

def convert_json_to_algorithm_section_running_time_penalty(attribute_dict: dict) -> List[AlgorithmSectionRunningTimePenalty]:
    snake_case_dict = convert_keys_to_snake_case(attribute_dict)
    snake_case_dict['total_penalty'] = parse_to_timedelta(snake_case_dict['total_penalty'])
    snake_case_dict['affected_section_tracks'] = convert_list(
        convert_json_to_algorithm_section_running_time_penalty_track,
        snake_case_dict['affected_section_tracks'])
    return convert(AlgorithmSectionRunningTimePenalty, snake_case_dict)

def convert_json_to_algorithm_section_running_time_penalty_track(attribute_dict: dict) -> List[AlgorithmSectionRunningTimePenaltyTrack]:
    snake_case_dict = convert_keys_to_snake_case(attribute_dict)
    for key in ['from_node_time_window', 'to_node_time_window']:
        snake_case_dict[key] = convert_json_to_time_window(snake_case_dict[key])
    return convert(AlgorithmSectionRunningTimePenaltyTrack, snake_case_dict)

def convert_json_to_algorithm_train_simulation_train(attribute_dict: dict) -> AlgorithmTrainSimulationTrain:
    snake_case_dict = convert_keys_to_snake_case(attribute_dict)
    snake_case_dict['train_path_nodes'] = convert_list(
        convert_json_to_algorithm_train_simulation_path_node,
        snake_case_dict['train_path_nodes'])
    return convert(AlgorithmTrainSimulationTrain, snake_case_dict)

def convert_json_to_algorithm_train_simulation_path_node(attribute_dict: dict) -> AlgorithmTrainSimulationTrainPathNode:
    snake_case_dict = convert_keys_to_snake_case(attribute_dict)
    for key in ['arrival_time', 'departure_time']:
        snake_case_dict[key] = parse_to_datetime(snake_case_dict[key])
    return convert(AlgorithmTrainSimulationTrainPathNode, snake_case_dict)

def convert_json_to_algorithm_train_simulation_event(attribute_dict: dict) -> AlgorithmTrainSimulationEvent:
    snake_case_dict = convert_keys_to_snake_case(attribute_dict)
    snake_case_dict['type'] = AlgorithmTrainSimulationEventType(snake_case_dict['type'])
    snake_case_dict['absolute_time'] = parse_to_datetime(snake_case_dict['absolute_time'])
    return convert(AlgorithmTrainSimulationEvent, snake_case_dict)
