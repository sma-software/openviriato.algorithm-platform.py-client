import inspect
from py_client.aidm import *
from Conversion.converter_helpers import parse_to_datetime, parse_to_timedelta, parse_to_timedelta_or_None, \
    convert_keys_to_snake_case, convert_to_snake_case


def convert(AIDM_class_or_AIDM_class_factory, attribute_dict: dict):
    snake_case_attribute_dict = convert_keys_to_snake_case(attribute_dict)
    is_factory_method = inspect.isfunction(AIDM_class_or_AIDM_class_factory)
    if is_factory_method:
        return AIDM_class_or_AIDM_class_factory(snake_case_attribute_dict)
    else:
        return AIDM_class_or_AIDM_class_factory(**snake_case_attribute_dict)


def convert_list(AIDM_class, list_of_dict: list) -> list:
    return [convert(AIDM_class, dict_from_list) for dict_from_list in list_of_dict]


def convert_json_to_AlgorithmNode(attribute_dict: dict) -> AlgorithmNode:
    snake_case_dict = convert_keys_to_snake_case(attribute_dict)
    snake_case_dict['node_tracks'] = convert_list(AlgorithmNodeTrack, snake_case_dict['node_tracks'])
    return convert(AlgorithmNode, snake_case_dict)


def convert_json_to_AlgorithmTrainPathNode(attribute_dict: dict) -> AlgorithmTrainPathNode:
    snake_case_dict = convert_keys_to_snake_case(attribute_dict)
    stop_status_value = snake_case_dict['stop_status']
    snake_case_dict['stop_status'] = StopStatus[convert_to_snake_case(stop_status_value)]
    for key in ['arrival_time', 'departure_time']:
        snake_case_dict[key] = parse_to_datetime(snake_case_dict[key])
    snake_case_dict['minimum_run_time'] = parse_to_timedelta_or_None(snake_case_dict['minimum_run_time'])
    snake_case_dict['minimum_stop_time'] = parse_to_timedelta(snake_case_dict['minimum_stop_time'])
    return convert(AlgorithmTrainPathNode, snake_case_dict)


def convert_json_to_AlgorithmTrain(attribute_dict: dict) -> AlgorithmTrain:
    snake_case_dict = convert_keys_to_snake_case(attribute_dict)
    snake_case_dict['train_path_nodes'] = [convert_json_to_AlgorithmTrainPathNode(train_path_node)
                                           for train_path_node in snake_case_dict['train_path_nodes']]
    return convert(AlgorithmTrain, snake_case_dict)


def convert_json_to_TimeWindow(attribute_dict: dict) -> TimeWindow:
    snake_case_dict = convert_keys_to_snake_case(attribute_dict)
    for key in ['from_time', 'to_time']:
        snake_case_dict[key] = parse_to_datetime(snake_case_dict[key])
    return convert(TimeWindow, snake_case_dict)


def convert_json_to_AlgorithmSectionTrackClosure(attribute_dict: dict) -> AlgorithmSectionTrackClosure:
    snake_case_dict = convert_keys_to_snake_case(attribute_dict)
    for key in ['closure_time_window_from_node', 'closure_time_window_to_node']:
        snake_case_dict[key] = convert_json_to_TimeWindow(snake_case_dict[key])
    return convert(AlgorithmSectionTrackClosure, snake_case_dict)


def convert_json_to_AlgorithmNodeTrackClosure(attribute_dict: dict) -> AlgorithmNodeTrackClosure:
    snake_case_dict = convert_keys_to_snake_case(attribute_dict)
    snake_case_dict["closure_time_window"] = convert_json_to_TimeWindow(snake_case_dict["closure_time_window"])
    return convert(AlgorithmNodeTrackClosure, snake_case_dict)


def convert_json_to_IncomingRoutingEdgeSet(attribute_dict: dict) -> IncomingRoutingEdgeSet:
    snake_case_dict = convert_keys_to_snake_case(attribute_dict)
    snake_case_dict["incoming_edges"] = convert_list(IncomingRoutingEdge, snake_case_dict["incoming_edges"])
    return convert(IncomingRoutingEdgeSet, snake_case_dict)


def convert_json_to_OutgoingRoutingEdgeSet(attribute_dict: dict) -> OutgoingRoutingEdgeSet:
    snake_case_dict = convert_keys_to_snake_case(attribute_dict)
    snake_case_dict["outgoing_edges"] = convert_list(OutgoingRoutingEdge, snake_case_dict["outgoing_edges"])
    return convert(OutgoingRoutingEdgeSet, snake_case_dict)


def convert_json_to_CrossingRoutingEdgeSet(attribute_dict: dict) -> CrossingRoutingEdgeSet:
    snake_case_dict = convert_keys_to_snake_case(attribute_dict)
    snake_case_dict["crossing_edges"] = convert_list(CrossingRoutingEdge, snake_case_dict["crossing_edges"])
    return convert(CrossingRoutingEdgeSet, snake_case_dict)


def convert_json_to_UpdateTrainTimes(attribute_dict: dict) -> UpdateTrainTimes:
    snake_case_dict = convert_keys_to_snake_case(attribute_dict)
    snake_case_dict["times"] = convert_list(convert_json_to_UpdateTrainTimesNode, snake_case_dict["times"])
    return convert(UpdateTrainTimes, snake_case_dict)


def convert_json_to_UpdateTrainTimesNode(attribute_dict: dict) -> UpdateTrainTimesNode:
    snake_case_dict = convert_keys_to_snake_case(attribute_dict)
    for key in ['arrival_time', 'departure_time']:
        snake_case_dict[key] = parse_to_datetime(snake_case_dict[key])
    for key in ['minimum_run_time', 'minimum_stop_time']:
        snake_case_dict[key] = parse_to_timedelta_or_None(snake_case_dict[key])
    if snake_case_dict['stop_status'] is not None:
        stop_status_value = snake_case_dict['stop_status']
        snake_case_dict['stop_status'] = StopStatus[convert_to_snake_case(stop_status_value)]
    return convert(UpdateTrainTimesNode, snake_case_dict)
