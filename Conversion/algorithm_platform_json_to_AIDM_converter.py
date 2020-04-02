import inspect

import AIDMClasses.AIDM_Algorithm_classes
import AIDMClasses.AIDM_RoutingEdge_classes
import AIDMClasses.AIDM_TimeWindow_classes
import AIDMClasses.AIDM_TrackClosure_classes
import AIDMClasses.AIDM_TrainPathNode_classes as AIDM_classes
import AIDMClasses.AIDM_Update_classes
import AIDMClasses.AIDM_enum_classes as AIDM_enum_classes
from Conversion.converter_helpers import parse_to_datetime, parse_to_timedelta, parse_to_timedelta_or_None


def convert(AIDM_class_factory, attribute_dict: dict):
    if inspect.isfunction(AIDM_class_factory):
        return AIDM_class_factory(attribute_dict)
    else:
        return AIDM_class_factory(**attribute_dict)


def convert_list(AIDM_class, list_of_dict: list) -> list:
    return [convert(AIDM_class, dict_from_list) for dict_from_list in list_of_dict]


def convert_dict_to_AlgorithmNode(attribute_dict: dict) -> AIDMClasses.AIDM_Algorithm_classes.AlgorithmNode:
    attribute_dict['NodeTracks'] = convert_list(AIDMClasses.AIDM_Algorithm_classes.AlgorithmNodeTrack,
                                                attribute_dict['NodeTracks'])
    return convert(AIDMClasses.AIDM_Algorithm_classes.AlgorithmNode, attribute_dict)


def convert_dict_to_TrainPathNode(attribute_dict: dict) -> AIDM_classes.TrainPathNode:
    attribute_dict['StopStatus'] = AIDM_enum_classes.StopStatus[attribute_dict['StopStatus']]
    for key in ['ArrivalTime', 'DepartureTime']:
        attribute_dict[key] = parse_to_datetime(attribute_dict[key])
    attribute_dict['MinimumRunTime'] = parse_to_timedelta_or_None(attribute_dict['MinimumRunTime'])
    attribute_dict['MinimumStopTime'] = parse_to_timedelta(attribute_dict['MinimumStopTime'])
    return convert(AIDM_classes.TrainPathNode, attribute_dict)


def convert_json_to_AlgorithmTrain(attribute_dict: dict) -> AIDMClasses.AIDM_Algorithm_classes.AlgorithmTrain:
    attribute_dict['TrainPathNodes'] = [convert_dict_to_TrainPathNode(train_path_node)
                                        for train_path_node in attribute_dict['TrainPathNodes']]
    return convert(AIDMClasses.AIDM_Algorithm_classes.AlgorithmTrain, attribute_dict)


def convert_dict_to_TimeWindow(attribute_dict: dict) -> AIDMClasses.AIDM_TimeWindow_classes.TimeWindow:
    for key in ['FromTime', 'ToTime']:
        attribute_dict[key] = parse_to_datetime(attribute_dict[key])
    return convert(AIDMClasses.AIDM_TimeWindow_classes.TimeWindow, attribute_dict)


def convert_dict_to_AlgorithmSectionTrackClosure(attribute_dict: dict) -> AIDMClasses.AIDM_TrackClosure_classes.AlgorithmSectionTrackClosure:
    for key in ['ClosureTimeWindowFromNode', 'ClosureTimeWindowToNode']:
        attribute_dict[key] = convert_dict_to_TimeWindow(attribute_dict[key])
    return convert(AIDMClasses.AIDM_TrackClosure_classes.AlgorithmSectionTrackClosure, attribute_dict)


def convert_dict_to_AlgorithmNodeTrackClosure(attribute_dict: dict) -> AIDMClasses.AIDM_TrackClosure_classes.AlgorithmNodeTrackClosure:
    attribute_dict["ClosureTimeWindow"] = convert_dict_to_TimeWindow(attribute_dict["ClosureTimeWindow"])
    return convert(AIDMClasses.AIDM_TrackClosure_classes.AlgorithmNodeTrackClosure, attribute_dict)


def convert_dict_to_IncomingRoutingEdgeSet(attribute_dict: dict) -> AIDMClasses.AIDM_RoutingEdge_classes.IncomingRoutingEdgeSet:
    attribute_dict["incomingEdges"] = convert_list(AIDMClasses.AIDM_RoutingEdge_classes.IncomingRoutingEdge,
                                                   attribute_dict["incomingEdges"])
    return convert(AIDMClasses.AIDM_RoutingEdge_classes.IncomingRoutingEdgeSet, attribute_dict)


def convert_dict_to_OutgoingRoutingEdgeSet(attribute_dict: dict) -> AIDMClasses.AIDM_RoutingEdge_classes.OutgoingRoutingEdgeSet:
    attribute_dict["outgoingEdges"] = convert_list(AIDMClasses.AIDM_RoutingEdge_classes.OutgoingRoutingEdge,
                                                   attribute_dict["outgoingEdges"])
    return convert(AIDMClasses.AIDM_RoutingEdge_classes.OutgoingRoutingEdgeSet, attribute_dict)


def convert_dict_to_CrossingRoutingEdgeSet(attribute_dict: dict) -> AIDMClasses.AIDM_RoutingEdge_classes.CrossingRoutingEdgeSet:
    attribute_dict["crossingEdges"] = convert_list(AIDMClasses.AIDM_RoutingEdge_classes.CrossingRoutingEdge,
                                                   attribute_dict["crossingEdges"])
    return convert(AIDMClasses.AIDM_RoutingEdge_classes.CrossingRoutingEdgeSet, attribute_dict)


def convert_dict_to_UpdateTrainTimes(attribute_dict: dict) -> AIDMClasses.AIDM_Update_classes.UpdateTrainTimes:
    attribute_dict["Times"] = convert_list(AIDMClasses.AIDM_Update_classes.UpdateTrainTimesNode,
                                           attribute_dict["Times"])
    return convert(AIDMClasses.AIDM_Update_classes.UpdateTrainTimes, attribute_dict)