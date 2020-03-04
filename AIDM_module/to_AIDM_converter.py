import AIDM_module.AIDM_classes


def convert_dict_to_AIDM(AIDM_class, attribute_dict: dict):
    return AIDM_class(**attribute_dict)


def from_list_of_dict_to_list_of_AIDM(AIDM_class, list_of_dict: list) -> list:
    return [convert_dict_to_AIDM(AIDM_class, dict_from_list) for dict_from_list in list_of_dict]


def convert_dict_to_AlgorithmNode(attribute_dict: dict) -> AIDM_module.AIDM_classes.AlgorithmNode:
    attribute_dict['NodeTracks'] = from_list_of_dict_to_list_of_AIDM(AIDM_module.AIDM_classes.AlgorithmNodeTrack,
                                                                     attribute_dict['NodeTracks'])
    return convert_dict_to_AIDM(AIDM_module.AIDM_classes.AlgorithmNode, attribute_dict)


def convert_list_of_dict_to_AlgorithmNode(list_of_dict: list) -> list:
    return [convert_dict_to_AlgorithmNode(attribute_dict) for attribute_dict in list_of_dict]


def convert_dict_to_TrainPathNode(attribute_dict: dict) -> AIDM_module.AIDM_classes.AlgorithmNode:
    attribute_dict['StopStatus'] = AIDM_module.AIDM_classes.StopStatus[attribute_dict['StopStatus']]
    return convert_dict_to_AIDM(AIDM_module.AIDM_classes.TrainPathNode, attribute_dict)


def convert_dict_to_AlgorithmTrain(attribute_dict: dict) -> AIDM_module.AIDM_classes.AlgorithmTrain:
    attribute_dict['TrainPathNodes'] = [convert_dict_to_TrainPathNode(train_path_node)
                                        for train_path_node in attribute_dict['TrainPathNodes']]
    return convert_dict_to_AIDM(AIDM_module.AIDM_classes.AlgorithmTrain, attribute_dict)
