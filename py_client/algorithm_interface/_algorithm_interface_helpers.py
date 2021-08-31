from typing import List, Union, Optional

from py_client.aidm import IncomingNodeTrackRoutingEdge, \
    OutgoingNodeTrackRoutingEdge, ABCIncomingRoutingEdge, ABCOutgoingRoutingEdge, RoutingPoint, CrossingRoutingEdge, \
    TimeWindow, LinkType, AlgorithmRosterLink, AlgorithmAwaitArrivalLink, AlgorithmConnectionLink
from py_client.communication.communication_layer import CommunicationLayer
from py_client.conversion import algorithm_platform_json_to_aidm_converter
from py_client.conversion.algorithm_platform_json_to_aidm_converter import convert_json_to_algorithm_link
from py_client.conversion.converter_helpers import RoutingEdgeType
from py_client.conversion.object_to_algorithm_platform_json_converter import convert_any_object


def merge_query_parameters(query_parameter_dictionaries: List[dict]) -> dict:
    return {parameter: value
            for parameter_dict in query_parameter_dictionaries
            for parameter, value in parameter_dict.items()}


def create_query_parameters_from_preceding_and_succeeding_routing_edge(
        preceding_routing_edge: Union[ABCIncomingRoutingEdge, ABCOutgoingRoutingEdge],
        succeeding_routing_edge: Union[ABCIncomingRoutingEdge, ABCOutgoingRoutingEdge]
) -> dict:
    if isinstance(preceding_routing_edge, ABCIncomingRoutingEdge):
        preceding_query_parameters = dict(precedingFromSectionTrackId=preceding_routing_edge.start_section_track_id)
        if isinstance(preceding_routing_edge, IncomingNodeTrackRoutingEdge):
            preceding_query_parameters["precedingToNodeTrackId"] = preceding_routing_edge.end_node_track_id
    elif isinstance(preceding_routing_edge, ABCOutgoingRoutingEdge):
        preceding_query_parameters = dict(precedingToSectionTrackId=preceding_routing_edge.end_section_track_id)
        if isinstance(preceding_routing_edge, OutgoingNodeTrackRoutingEdge):
            preceding_query_parameters["precedingFromNodeTrackId"] = preceding_routing_edge.start_node_track_id
    else:
        raise TypeError(
            f"{preceding_routing_edge} is not an {ABCIncomingRoutingEdge.__name__} or {ABCIncomingRoutingEdge.__name__}"
        )

    if isinstance(succeeding_routing_edge, ABCIncomingRoutingEdge):
        succeeding_query_parameters = dict(succeedingFromSectionTrackId=succeeding_routing_edge.start_section_track_id)
        if isinstance(succeeding_routing_edge, IncomingNodeTrackRoutingEdge):
            succeeding_query_parameters["succeedingToNodeTrackId"] = succeeding_routing_edge.end_node_track_id
    elif isinstance(succeeding_routing_edge, ABCOutgoingRoutingEdge):
        succeeding_query_parameters = dict(succeedingToSectionTrackId=succeeding_routing_edge.end_section_track_id)
        if isinstance(succeeding_routing_edge, OutgoingNodeTrackRoutingEdge):
            succeeding_query_parameters["succeedingFromNodeTrackId"] = succeeding_routing_edge.start_node_track_id
    else:
        raise TypeError(
            f"{preceding_routing_edge} is not an {ABCIncomingRoutingEdge.__name__} or {ABCIncomingRoutingEdge.__name__}"
        )

    return merge_query_parameters([preceding_query_parameters, succeeding_query_parameters])


def do_get_routing_edges_request(
        communication_layer: CommunicationLayer,
        routing_point: RoutingPoint,
        routing_edge_type: Optional[RoutingEdgeType]
) -> List[Union[IncomingNodeTrackRoutingEdge, OutgoingNodeTrackRoutingEdge, CrossingRoutingEdge]]:
    url_to_resource = "nodes/{0}/routing-edges".format(routing_point.node_id)
    get_request_params = dict(
        routingEdgeType=None if routing_edge_type is None else routing_edge_type.value,
        nodeTrackId=routing_point.node_track_id,
    )
    response_list = communication_layer.do_get_request(url_to_resource, get_request_params)
    return algorithm_platform_json_to_aidm_converter.convert_to_routing_edges(response_list)


def do_get_any_parameter(
        communication_layer: CommunicationLayer,
        key: str
) -> Optional[Union[bool, dict, int, list, str]]:
    url_to_resource = "parameters/{0}".format(key)
    return communication_layer.do_get_request(url_to_resource)["value"]


def do_get_any_link(
        communication_layer: CommunicationLayer,
        time_window: TimeWindow,
        link_type_filter: Optional[LinkType],
        node_id_filter: Optional[List[int]],
) -> List[Union[AlgorithmAwaitArrivalLink, AlgorithmConnectionLink, AlgorithmRosterLink]]:
    url_to_resource = "links"
    link_type = None if link_type_filter is None else convert_any_object(link_type_filter)
    node_filter = None if node_id_filter is None else node_id_filter
    query_parameters = merge_query_parameters(
        [convert_any_object(time_window), dict(linkType=link_type, nodeFilter=node_filter)]
    )
    response_dict = communication_layer.do_get_request(url_to_resource, query_parameters)
    return algorithm_platform_json_to_aidm_converter.convert_list(convert_json_to_algorithm_link, response_dict)
