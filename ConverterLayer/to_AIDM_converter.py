import inspect

import AIDMClasses.AIDM_classes
import AIDMClasses.AIDM_enum_classes
from ConverterLayer.converter_helpers import parse_to_datetime, parse_to_timedelta, parse_to_timedelta_or_None


def convert_input_to_dict(**kwargs):
    return locals()


def convert_dict_to_AIDM(AIDM_class_factory, attribute_dict: dict):
    if inspect.isfunction(AIDM_class_factory):
        obj = AIDM_class_factory(attribute_dict)
    else:
        obj = AIDM_class_factory(**attribute_dict)
    return obj


def convert_list_of_dict_to_list_of_AIDM(AIDM_class, list_of_dict: list) -> list:
    return [convert_dict_to_AIDM(AIDM_class, dict_from_list) for dict_from_list in list_of_dict]


def convert_dict_to_AlgorithmNode(attribute_dict: dict) -> AIDMClasses.AIDM_classes.AlgorithmNode:
    attribute_dict['NodeTracks'] = convert_list_of_dict_to_list_of_AIDM(AIDMClasses.AIDM_classes.AlgorithmNodeTrack,
                                                                        attribute_dict['NodeTracks'])
    return convert_dict_to_AIDM(AIDMClasses.AIDM_classes.AlgorithmNode, attribute_dict)


def convert_dict_to_TrainPathNode(attribute_dict: dict) -> AIDMClasses.AIDM_classes.TrainPathNode:
    attribute_dict['StopStatus'] = AIDMClasses.AIDM_enum_classes.StopStatus[attribute_dict['StopStatus']]
    for key in ['ArrivalTime', 'DepartureTime']:
        attribute_dict[key] = parse_to_datetime(attribute_dict[key])
    attribute_dict['MinimumRunTime'] = parse_to_timedelta_or_None(attribute_dict['MinimumRunTime'])
    attribute_dict['MinimumStopTime'] = parse_to_timedelta(attribute_dict['MinimumStopTime'])
    return convert_dict_to_AIDM(AIDMClasses.AIDM_classes.TrainPathNode, attribute_dict)


def convert_dict_to_AlgorithmTrain(attribute_dict: dict) -> AIDMClasses.AIDM_classes.AlgorithmTrain:
    attribute_dict['TrainPathNodes'] = [convert_dict_to_TrainPathNode(train_path_node)
                                        for train_path_node in attribute_dict['TrainPathNodes']]
    return convert_dict_to_AIDM(AIDMClasses.AIDM_classes.AlgorithmTrain, attribute_dict)