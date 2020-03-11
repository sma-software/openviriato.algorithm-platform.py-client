import AIDM_package.AIDM_classes
from ConverterLayer.converter_helpers import parse_to_datetime, parse_to_timedelta, parse_to_timedelta_or_None


def convert_dict_to_AIDM(AIDM_class, attribute_dict: dict):
    return AIDM_class(**attribute_dict)


def from_list_of_dict_to_list_of_AIDM(AIDM_class, list_of_dict: list) -> list:
    return [convert_dict_to_AIDM(AIDM_class, dict_from_list) for dict_from_list in list_of_dict]


def convert_dict_to_AlgorithmNode(attribute_dict: dict) -> AIDM_package.AIDM_classes.AlgorithmNode:
    attribute_dict['NodeTracks'] = from_list_of_dict_to_list_of_AIDM(AIDM_package.AIDM_classes.AlgorithmNodeTrack,
                                                                     attribute_dict['NodeTracks'])
    return convert_dict_to_AIDM(AIDM_package.AIDM_classes.AlgorithmNode, attribute_dict)


# there shold be a way to get rid of this redundant function
def convert_list_of_dict_to_list_of_AlgorithmNode(list_of_dict: list) -> list:
    return [convert_dict_to_AlgorithmNode(attribute_dict) for attribute_dict in list_of_dict]


def convert_dict_to_TrainPathNode(attribute_dict: dict) -> AIDM_package.AIDM_classes.TrainPathNode:
    attribute_dict['StopStatus'] = AIDM_package.AIDM_classes.StopStatus[attribute_dict['StopStatus']]
    for key in ['ArrivalTime', 'DepartureTime']:
        attribute_dict[key] = parse_to_datetime(attribute_dict[key])
    attribute_dict['MinimumRunTime'] = parse_to_timedelta_or_None(attribute_dict['MinimumRunTime']) # some are not none!
    attribute_dict['MinimumStopTime'] = parse_to_timedelta(attribute_dict['MinimumStopTime'])
    return convert_dict_to_AIDM(AIDM_package.AIDM_classes.TrainPathNode, attribute_dict)


def convert_dict_to_AlgorithmTrain(attribute_dict: dict) -> AIDM_package.AIDM_classes.AlgorithmTrain:
    attribute_dict['TrainPathNodes'] = [convert_dict_to_TrainPathNode(train_path_node)
                                        for train_path_node in attribute_dict['TrainPathNodes']]
    return convert_dict_to_AIDM(AIDM_package.AIDM_classes.AlgorithmTrain, attribute_dict)


