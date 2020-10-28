import inspect

from py_client.aidm import *
from py_client.communication.response_processing import AlgorithmPlatformConversionError
from py_client.conversion.converter_helpers import parse_to_datetime, parse_to_timedelta, parse_to_timedelta_or_none, \
    convert_keys_to_snake_case, convert_to_snake_case


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
    stop_status_value = snake_case_dict['stop_status']
    snake_case_dict['stop_status'] = StopStatus[convert_to_snake_case(stop_status_value)]
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


def convert_json_to_incoming_routing_edge_set(attribute_dict: dict) -> IncomingRoutingEdgeSet:
    snake_case_dict = convert_keys_to_snake_case(attribute_dict)
    snake_case_dict["incoming_edges"] = convert_list(IncomingRoutingEdge, snake_case_dict["incoming_edges"])
    return convert(IncomingRoutingEdgeSet, snake_case_dict)


def convert_json_to_outgoing_routing_edge_set(attribute_dict: dict) -> OutgoingRoutingEdgeSet:
    snake_case_dict = convert_keys_to_snake_case(attribute_dict)
    snake_case_dict["outgoing_edges"] = convert_list(OutgoingRoutingEdge, snake_case_dict["outgoing_edges"])
    return convert(OutgoingRoutingEdgeSet, snake_case_dict)


def convert_json_to_crossing_routing_edge_set(attribute_dict: dict) -> CrossingRoutingEdgeSet:
    snake_case_dict = convert_keys_to_snake_case(attribute_dict)
    snake_case_dict["crossing_edges"] = convert_list(CrossingRoutingEdge, snake_case_dict["crossing_edges"])
    return convert(CrossingRoutingEdgeSet, snake_case_dict)


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
        stop_status_value = snake_case_dict['stop_status']
        snake_case_dict['stop_status'] = StopStatus[convert_to_snake_case(stop_status_value)]
    return convert(UpdateTimesTrainPathNode, snake_case_dict)
