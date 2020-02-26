from AIDM_module import AIDM_classes
from AIDM_module.AIDM_classes import AlgorithmTrain


def dict_to_algorithm_node_track_factory(node_track_as_dict: dict) -> AIDM_classes.AlgorithmNodeTrack:
    return AIDM_classes.AlgorithmNodeTrack(node_track_id=node_track_as_dict['ID'],
                                           code_string=node_track_as_dict['Code'],
                                           debug_string=node_track_as_dict['DebugString'])


def dict_to_algorithm_node_factory(node_as_dict: dict) -> AIDM_classes.AlgorithmNode:
    node_track_list = None
    if not node_as_dict['NodeTracks'] is None:
        node_track_list = []
        for node_track in node_as_dict['NodeTracks']:
            node_track_list.append(dict_to_algorithm_node_track_factory(node_track))
    return AIDM_classes.AlgorithmNode(node_id=node_as_dict['ID'],
                                      code_string=node_as_dict['Code'],
                                      node_tracks=node_track_list,
                                      debug_string=node_as_dict['DebugString'])


def list_of_dicts_to_algorithm_node_list_factory(list_of_nodes_as_dict: list) -> list:
    return [dict_to_algorithm_node_factory(node_as_dict) for node_as_dict in list_of_nodes_as_dict]


def dict_to_algorithm_section_track_factory(section_track_as_dict: dict) -> AIDM_classes.AlgorithmSectionTrack:
    return AIDM_classes.AlgorithmSectionTrack(section_id=section_track_as_dict['ID'],
                                              code_string=section_track_as_dict['Code'],
                                              section_code=section_track_as_dict['SectionCode'],
                                              debug_string=section_track_as_dict['DebugString'],
                                              section_weight=section_track_as_dict['Weight'])


def algorithm_section_track_list_factory(list_of_sections_dict: list) -> list:
    return [dict_to_algorithm_section_track_factory(section_as_dict) for section_as_dict in list_of_sections_dict]


def dict_to_algorithm_train_factory(json_as_dict: dict) -> AlgorithmTrain:
    return AlgorithmTrain(train_id=json_as_dict['ID'],
                          debug_string=json_as_dict['DebugString'],
                          train_path_nodes=json_as_dict['TrainPathNodes'])


def dict_to_algorithm_train_path_node_factory(json_as_dict: dict) -> AlgorithmTrain:
    return AlgorithmTrain(train_id=json_as_dict['ID'],
                          debug_string=json_as_dict['DebugString'],
                          train_path_nodes=json_as_dict['TrainPathNodes'])
