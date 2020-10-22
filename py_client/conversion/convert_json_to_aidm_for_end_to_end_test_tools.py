from typing import List, Union, Dict, Type

from py_client.aidm import StopStatus, UpdateTimesTrainPathNode, UpdateTrainStopTimesNode, IncomingRoutingEdge, \
    OutgoingRoutingEdge, CrossingRoutingEdge, UpdateTrainRoute, StationEntryOrExit, TableDefinition, TableCellDataType, \
    TableTextCell, TableColumnDefinition
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


def create_table_definition_for_end_to_end_to_test(object_as_json: dict) -> TableDefinition:
    json_with_snake_case_keys = convert_keys_to_snake_case(object_as_json)["table_definition"]
    table_name = json_with_snake_case_keys["name"]
    columns = []
    for cell_definition in json_with_snake_case_keys["columns"]:
        cell_definition_with_snake_case_keys = convert_keys_to_snake_case(cell_definition)
        key = cell_definition_with_snake_case_keys["key"]
        header = TableTextCell(key, cell_definition_with_snake_case_keys["header"])
        header_data_type = convert_to_aidm_enum_from_string(
            cell_definition_with_snake_case_keys["header_data_type"],
            TableCellDataType)
        column_data_type = convert_to_aidm_enum_from_string(
            cell_definition_with_snake_case_keys["column_data_type"],
            TableCellDataType)
        columns.append(TableColumnDefinition(key, header, header_data_type, column_data_type))
    return TableDefinition(table_name, columns)


def convert_to_aidm_enum_from_string(
        enum_as_string: str,
        enum_to_convert_to: Type[Union[StopStatus, StationEntryOrExit, TableCellDataType]]) -> \
        Union[StopStatus, StationEntryOrExit, TableCellDataType]:
    enum_as_snake_case_string = convert_to_snake_case(enum_as_string)
    for member in enum_to_convert_to:
        if member.name == enum_as_snake_case_string:
            return member

    raise TypeError("{0} is not defined as member of {1}".format(enum_as_string, str(enum_to_convert_to)))


def convert_string_to_stop_status(dict_with_stop_status_as_string) -> StopStatus:
    stop_status_as_string = convert_to_snake_case(dict_with_stop_status_as_string["stop_status_as_string"])
    return convert_to_aidm_enum_from_string(stop_status_as_string, StopStatus)


def convert_string_to_station_entry_or_exit(
        dict_with_station_entry_or_exit_as_string: Dict[str, str]) -> StationEntryOrExit:
    station_entry_or_exit_as_string = convert_to_snake_case(
        dict_with_station_entry_or_exit_as_string["station_entry_or_exit_as_string"])
    return convert_to_aidm_enum_from_string(station_entry_or_exit_as_string, StationEntryOrExit)
