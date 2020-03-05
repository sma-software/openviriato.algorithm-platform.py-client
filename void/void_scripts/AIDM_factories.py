""""

def algorithm_section_track_list_factory(list_of_sections_dict: list) -> list:
    return [AIDM_classes.AlgorithmSectionTrack.from_json_dict_factory(section_dict)
            for section_dict in list_of_sections_dict]


def dict_to_algorithm_node_track_factory(node_track_as_dict: dict) -> AIDM_classes.AlgorithmNodeTrack:
    return AIDM_classes.AlgorithmNodeTrack(ID=node_track_as_dict['ID'],
                                           Code=node_track_as_dict['Code'],
                                           DebugString=node_track_as_dict['DebugString'])
def dict_to_algorithm_node_factory(node_as_dict: dict) -> AIDM_classes.AlgorithmNode:
    node_track_list = []
    for node_track in node_as_dict['NodeTracks']:
        node_track_list.append(dict_to_algorithm_node_track_factory(node_track))
    return AIDM_classes.AlgorithmNode(ID=node_as_dict['ID'],
                                      Code=node_as_dict['Code'],
                                      NodeTracks=node_track_list,
                                      DebugString=node_as_dict['DebugString'])
                                      
                                      def list_of_dicts_to_algorithm_node_list_factory(list_of_nodes_as_dict: list) -> list:
    return [dict_to_algorithm_node_factory(node_as_dict) for node_as_dict in list_of_nodes_as_dict]
    
def dict_to_algorithm_section_track_factory(section_track_as_dict: dict) -> AIDM_classes.AlgorithmSectionTrack:
    return AIDM_classes.AlgorithmSectionTrack(ID=section_track_as_dict['ID'],
                                              Code=section_track_as_dict['Code'],
                                              SectionCode=section_track_as_dict['SectionCode'],
                                              DebugString=section_track_as_dict['DebugString'],
                                              Weight=section_track_as_dict['Weight'])

def dict_to_algorithm_train_factory(json_as_dict: dict) -> AlgorithmTrain:
    return AlgorithmTrain(ID=json_as_dict['ID'],
                          DebugString=json_as_dict['DebugString'],
                          TrainPathNodes=json_as_dict['TrainPathNodes'])


def void_dict_to_algorithm_train_path_node_factory(json_as_dict: dict) -> AlgorithmTrain:
    return AlgorithmTrain(ID=json_as_dict['ID'],
                          DebugString=json_as_dict['DebugString'],
                          TrainPathNodes=json_as_dict['TrainPathNodes'])

"""




