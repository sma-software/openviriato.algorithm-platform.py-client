from py_client.aidm.aidm_update_classes import UpdateTrainTimesNode
from py_client.conversion.converter_helpers import convert_keys_to_snake_case, parse_to_datetime
from py_client.conversion.algorithm_platform_json_to_aidm_converter import convert
from typing import List


def convert_list_of_json_to_update_train_times_node(attribute_dict: dict) -> List[UpdateTrainTimesNode]:
    return [convert_json_to_update_train_times_node(node_attributes) for node_attributes in attribute_dict[
        "train_path_nodes"]]


def convert_json_to_update_train_times_node(attribute_dict: dict) -> UpdateTrainTimesNode:
    snake_case_dict = convert_keys_to_snake_case(attribute_dict)
    for key in ['arrival_time', 'departure_time']:
        snake_case_dict[key] = parse_to_datetime(snake_case_dict[key])
    return convert(UpdateTrainTimesNode, snake_case_dict)