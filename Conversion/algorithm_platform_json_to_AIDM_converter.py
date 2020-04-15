import inspect
import AIDMClasses
from Conversion.converter_helpers import parse_to_datetime, parse_to_timedelta, parse_to_timedelta_or_None


def convert(AIDM_class_or_AIDM_class_factory, attribute_dict: dict):
    is_factory_method = inspect.isfunction(AIDM_class_or_AIDM_class_factory)
    if is_factory_method:
        return AIDM_class_or_AIDM_class_factory(attribute_dict)
    else:
        return AIDM_class_or_AIDM_class_factory(**attribute_dict)


def convert_list(AIDM_class, list_of_dict: list) -> list:
    return [convert(AIDM_class, dict_from_list) for dict_from_list in list_of_dict]


def convert_json_to_AlgorithmNode(attribute_dict: dict) -> AIDMClasses.AlgorithmNode:
    attribute_dict['NodeTracks'] = convert_list(AIDMClasses.AlgorithmNodeTrack, attribute_dict['NodeTracks'])
    return convert(AIDMClasses.AlgorithmNode, attribute_dict)


def convert_json_to_TrainPathNode(attribute_dict: dict) -> AIDMClasses.TrainPathNode:
    attribute_dict['StopStatus'] = AIDMClasses.StopStatus[attribute_dict['StopStatus']]
    for key in ['ArrivalTime', 'DepartureTime']:
        attribute_dict[key] = parse_to_datetime(attribute_dict[key])
    attribute_dict['MinimumRunTime'] = parse_to_timedelta_or_None(attribute_dict['MinimumRunTime'])
    attribute_dict['MinimumStopTime'] = parse_to_timedelta(attribute_dict['MinimumStopTime'])
    return convert(AIDMClasses.TrainPathNode, attribute_dict)


def convert_json_to_AlgorithmTrain(attribute_dict: dict) -> AIDMClasses.AlgorithmTrain:
    attribute_dict['TrainPathNodes'] = [convert_json_to_TrainPathNode(train_path_node)
                                        for train_path_node in attribute_dict['TrainPathNodes']]
    return convert(AIDMClasses.AlgorithmTrain, attribute_dict)


def convert_json_to_TimeWindow(attribute_dict: dict) -> AIDMClasses.TimeWindow:
    for key in ['FromTime', 'ToTime']:
        attribute_dict[key] = parse_to_datetime(attribute_dict[key])
    return convert(AIDMClasses.TimeWindow, attribute_dict)


def convert_json_to_AlgorithmSectionTrackClosure(attribute_dict: dict) -> AIDMClasses.AlgorithmSectionTrackClosure:
    for key in ['ClosureTimeWindowFromNode', 'ClosureTimeWindowToNode']:
        attribute_dict[key] = convert_json_to_TimeWindow(attribute_dict[key])
    return convert(AIDMClasses.AlgorithmSectionTrackClosure, attribute_dict)


def convert_json_to_AlgorithmNodeTrackClosure(attribute_dict: dict) -> AIDMClasses.AlgorithmNodeTrackClosure:
    attribute_dict["ClosureTimeWindow"] = convert_json_to_TimeWindow(attribute_dict["ClosureTimeWindow"])
    return convert(AIDMClasses.AlgorithmNodeTrackClosure, attribute_dict)


def convert_json_to_IncomingRoutingEdgeSet(attribute_dict: dict) -> AIDMClasses.IncomingRoutingEdgeSet:
    attribute_dict["incomingEdges"] = convert_list(AIDMClasses.IncomingRoutingEdge, attribute_dict["incomingEdges"])
    return convert(AIDMClasses.IncomingRoutingEdgeSet, attribute_dict)


def convert_json_to_OutgoingRoutingEdgeSet(attribute_dict: dict) -> AIDMClasses.OutgoingRoutingEdgeSet:
    attribute_dict["outgoingEdges"] = convert_list(AIDMClasses.OutgoingRoutingEdge, attribute_dict["outgoingEdges"])
    return convert(AIDMClasses.OutgoingRoutingEdgeSet, attribute_dict)


def convert_json_to_CrossingRoutingEdgeSet(attribute_dict: dict) -> AIDMClasses.CrossingRoutingEdgeSet:
    attribute_dict["crossingEdges"] = convert_list(AIDMClasses.CrossingRoutingEdge, attribute_dict["crossingEdges"])
    return convert(AIDMClasses.CrossingRoutingEdgeSet, attribute_dict)


def convert_json_to_UpdateTrainTimes(attribute_dict: dict) -> AIDMClasses.UpdateTrainTimes:
    attribute_dict["Times"] = convert_list(convert_json_to_UpdateTrainTimesNode, attribute_dict["Times"])
    return convert(AIDMClasses.UpdateTrainTimes, attribute_dict)


def convert_json_to_UpdateTrainTimesNode(attribute_dict: dict) -> AIDMClasses.UpdateTrainTimesNode:
    for key in ['ArrivalTime', 'DepartureTime']:
        attribute_dict[key] = parse_to_datetime(attribute_dict[key])
    for key in ['MinimumRunTime', 'MinimumStopTime']:
        attribute_dict[key] = parse_to_timedelta_or_None(attribute_dict[key])
    if attribute_dict['StopStatus'] is not None:
        attribute_dict['StopStatus'] = AIDMClasses.StopStatus[attribute_dict['StopStatus']]
    return convert(AIDMClasses.UpdateTrainTimesNode, attribute_dict)
