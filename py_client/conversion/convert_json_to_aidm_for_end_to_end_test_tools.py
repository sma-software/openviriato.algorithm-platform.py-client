from typing import List, Union, Dict

from py_client.aidm import StopStatus, UpdateTimesTrainPathNode, UpdateTrainStopTimesNode, IncomingRoutingEdge, \
    OutgoingRoutingEdge, CrossingRoutingEdge, UpdateTrainRoute, StationEntryOrExit
from py_client.conversion.algorithm_platform_json_to_aidm_converter import convert
from py_client.conversion.converter_helpers import convert_keys_to_snake_case, parse_to_datetime, convert_to_snake_case


def convert_list_of_json_to_update_train_times_node(attribute_dict: dict) -> List[UpdateTimesTrainPathNode]:
    return [convert_json_to_update_train_times_node(node_attributes)
            for node_attributes in attribute_dict["train_path_nodes"]]


def convert_json_to_update_train_times_node(attribute_dict: dict) -> UpdateTimesTrainPathNode:
    snake_case_dict = convert_keys_to_snake_case(attribute_dict)
    for key in ['arrival_time', 'departure_time']:
        snake_case_dict[key] = parse_to_datetime(snake_case_dict[key])
    return convert(UpdateTimesTrainPathNode, snake_case_dict)


def convert_json_to_update_train_stop_times_node(attribute: dict) -> UpdateTrainStopTimesNode:
    snake_case_dict = convert_keys_to_snake_case(attribute)
    for key in ['arrival_time', 'departure_time']:
        snake_case_dict[key] = parse_to_datetime(snake_case_dict[key])
    snake_case_dict["stop_status"] = StopStatus[snake_case_dict["stop_status"]]
    return convert(UpdateTimesTrainPathNode, snake_case_dict)


def extract_first_dict_value(attribute_dict: dict) -> object:
    return attribute_dict[list(attribute_dict.keys())[0]]


def create_update_train_route_for_end_to_end_test(object_as_json: dict) -> UpdateTrainRoute:
    train_id: int = object_as_json["train_id"]
    start_train_path_node_id: int = object_as_json["start_train_path_node_id"]
    end_train_path_node_id: int = object_as_json["end_train_path_node_id"]
    routing_edges: List[Dict[str, Union[str, dict]]] = object_as_json["routing_edges"]
    converted_routing_edges = []
    for edge_as_dict in routing_edges:
        class_fields_as_dict = convert_keys_to_snake_case(edge_as_dict["fields"])
        if edge_as_dict["class"] == OutgoingRoutingEdge.__name__:
            converted_routing_edges.append(OutgoingRoutingEdge(**class_fields_as_dict))
        elif edge_as_dict["class"] == IncomingRoutingEdge.__name__:
            converted_routing_edges.append(IncomingRoutingEdge(**class_fields_as_dict))
        elif edge_as_dict["class"] == CrossingRoutingEdge.__name__:
            converted_routing_edges.append(CrossingRoutingEdge(**class_fields_as_dict))
        else:
            raise TypeError("{0} is not defined as a routing edge".format(edge_as_dict["class"]))

    return UpdateTrainRoute(train_id, end_train_path_node_id, converted_routing_edges, start_train_path_node_id)


def convert_string_to_stop_status(dict_with_stop_status_as_string) -> StopStatus:
    stop_status_as_string = convert_to_snake_case(dict_with_stop_status_as_string["stop_status_as_string"])
    for status in StopStatus:
        if status.name == stop_status_as_string:
            return StopStatus[stop_status_as_string]

    raise TypeError("{0} is not defined as a Stop Status".format(stop_status_as_string))


def convert_string_to_station_entry_or_exit(
        dict__with_station_entry_or_exit_as_string: Dict[str, str]) -> StationEntryOrExit:
    station_entry_or_exit_as_string = convert_to_snake_case(
        dict__with_station_entry_or_exit_as_string["station_entry_or_exit_as_string"])
    for status in StationEntryOrExit:
        if status.name == station_entry_or_exit_as_string:
            return StationEntryOrExit[station_entry_or_exit_as_string]

    raise TypeError("{0} is not defined as a EntryOrExit".format(station_entry_or_exit_as_string))
