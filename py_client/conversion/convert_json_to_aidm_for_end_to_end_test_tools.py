from enum import Enum
from typing import List, Union, Dict, Type

from py_client.aidm import StopStatus, UpdateTimesTrainPathNode, UpdateStopTimesTrainPathNode, IncomingRoutingEdge, \
    OutgoingRoutingEdge, CrossingRoutingEdge, UpdateTrainRoute, StationEntryOrExit, TableDefinition, TableCellDataType, \
    TableTextCell, TableColumnDefinition, TableAlgorithmNodeCell, TableRow, TableAlgorithmTrainCell, \
    UpdateRunTimesTrainPathSegment, TimeWindow
from py_client.conversion.algorithm_platform_json_to_aidm_converter import convert
from py_client.conversion.converter_helpers import convert_keys_to_snake_case, parse_to_datetime, \
    parse_to_timedelta_or_none


def convert_list_of_json_to_update_train_times_node(attribute_dict: dict) -> List[UpdateTimesTrainPathNode]:
    return [convert_json_to_update_train_times_node(node_attributes)
            for node_attributes in attribute_dict["train_path_nodes"]]


def convert_json_to_update_train_times_node(attribute_dict: dict) -> UpdateTimesTrainPathNode:
    snake_case_dict = convert_keys_to_snake_case(attribute_dict)
    for key in ['arrival_time', 'departure_time']:
        snake_case_dict[key] = parse_to_datetime(snake_case_dict[key])
    return convert(UpdateTimesTrainPathNode, snake_case_dict)


def convert_json_to_update_stop_times_train_path_node(attribute: dict) -> UpdateStopTimesTrainPathNode:
    snake_case_dict = convert_keys_to_snake_case(attribute)
    for key in ['arrival_time', 'departure_time']:
        snake_case_dict[key] = parse_to_datetime(snake_case_dict[key])
    snake_case_dict["stop_status"] = convert_to_aidm_enum_from_string(snake_case_dict["stop_status"], StopStatus)
    return convert(UpdateStopTimesTrainPathNode, snake_case_dict)


def convert_json_to_update_run_times_train_path_segment(attribute: dict) -> UpdateRunTimesTrainPathSegment:
    snake_case_dict = convert_keys_to_snake_case(attribute)
    for key in ['to_node_arrival_time', 'from_node_departure_time']:
        snake_case_dict[key] = parse_to_datetime(snake_case_dict[key])
    snake_case_dict["minimum_run_time"] = parse_to_timedelta_or_none(snake_case_dict["minimum_run_time"])
    return convert(UpdateRunTimesTrainPathSegment, snake_case_dict)


def extract_first_dict_value(attribute_dict: dict) -> object:
    return attribute_dict[list(attribute_dict.keys())[0]]


def create_update_train_route_for_end_to_end_test(evaluated_parameter_mapping: dict) -> UpdateTrainRoute:
    train_id: int = evaluated_parameter_mapping["train_id"]
    start_train_path_node_id: int = evaluated_parameter_mapping["start_train_path_node_id"]
    end_train_path_node_id: int = evaluated_parameter_mapping["end_train_path_node_id"]
    routing_edges: List[Dict[str, Union[str, dict]]] = evaluated_parameter_mapping["routing_edges"]

    converted_routing_edges = []
    for edge_as_dict in routing_edges:
        class_fields_as_dict = convert_keys_to_snake_case(edge_as_dict)
        if all(key in class_fields_as_dict.keys() for key in {"start_node_track_id", "end_section_track_id"}):
            converted_routing_edges.append(OutgoingRoutingEdge(**class_fields_as_dict))
        elif all(key in class_fields_as_dict.keys() for key in {"start_section_track_id", "end_node_track_id"}):
            converted_routing_edges.append(IncomingRoutingEdge(**class_fields_as_dict))
        elif all(key in class_fields_as_dict.keys() for key in {"start_section_track_id", "end_section_track_id"}):
            converted_routing_edges.append(CrossingRoutingEdge(**class_fields_as_dict))
        else:
            raise TypeError("{0} is not defined as a routing edge".format(class_fields_as_dict))

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


def create_table_rows_for_end_to_end_to_test(rows_as_json: dict) -> List[TableRow]:
    table_rows = []
    for row_as_json in rows_as_json["rows"]:
        list_of_cells_to_add = convert_keys_to_snake_case(row_as_json)["row"]
        cells = []
        for cell in list_of_cells_to_add:
            cell_with_camel_case_keys = convert_keys_to_snake_case(cell)
            column_key = cell_with_camel_case_keys['column_key']
            if "value" in cell_with_camel_case_keys.keys():
                cells.append(TableTextCell(column_key, cell_with_camel_case_keys['value']))
            elif "node_id" in cell_with_camel_case_keys.keys():
                cells.append(TableAlgorithmNodeCell(column_key, cell_with_camel_case_keys['node_id']))
            elif "train_id" in cell_with_camel_case_keys.keys():
                cells.append(TableAlgorithmTrainCell(column_key, cell_with_camel_case_keys['train_id']))
        table_rows.append(TableRow(cells))
    return table_rows


def convert_to_aidm_enum_from_string(
        enum_as_string: str,
        enum_to_convert_to: Type[Union[StopStatus, StationEntryOrExit, TableCellDataType]]) -> \
        Union[StopStatus, StationEntryOrExit, TableCellDataType]:
    for member in enum_to_convert_to:
        if member.value == enum_as_string:
            return member

    raise TypeError("{0} is not defined as member of {1}".format(enum_as_string, str(enum_to_convert_to)))


def convert_string_to_stop_status(dict_with_stop_status_as_string) -> StopStatus:
    stop_status_as_string = dict_with_stop_status_as_string["stop_status_as_string"]
    return convert_to_aidm_enum_from_string(stop_status_as_string, StopStatus)


def convert_string_to_station_entry_or_exit(
        dict_with_station_entry_or_exit_as_string: Dict[str, str]) -> StationEntryOrExit:
    station_entry_or_exit_as_string = dict_with_station_entry_or_exit_as_string["station_entry_or_exit_as_string"]
    return convert_to_aidm_enum_from_string(station_entry_or_exit_as_string, StationEntryOrExit)


def convert_json_with_url_encoding_to_time_window(url_encoded_time_window_dict: Dict[str, object]) -> TimeWindow:
    for key in url_encoded_time_window_dict.keys():
        url_encoded_time_window_dict[key] = str(url_encoded_time_window_dict[key]).replace("%3A", ":")
    return convert(TimeWindow, url_encoded_time_window_dict)


class EndToEndTestParameterEnum(Enum):
    optionValue3 = "optionValue3"
