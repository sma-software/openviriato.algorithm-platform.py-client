from typing import List, Union, Optional

from py_client.aidm import RoutingPoint, TimeWindow
from py_client.aidm.aidm_routing_edge_classes import _RoutingEdge, IncomingNodeTrackRoutingEdge, OutgoingNodeTrackRoutingEdge, AnyRoutingEdgeIncomingOrOutgoing, AnyRoutingEdgeIncomingOrCrossingOrOutgoing, IncomingRoutingEdge, OutgoingRoutingEdge
from py_client.aidm.aidm_link_classes import LinkType, AlgorithmRosterLink, AlgorithmAwaitArrivalLink, AlgorithmConnectionLink, _AlgorithmLink
from py_client.communication.communication_layer import CommunicationLayer
from py_client.conversion.converter_helpers import RoutingEdgeType
from py_client.conversion.object_to_algorithm_platform_json_converter import convert_any_object
from py_client.conversion.json_to_aidm_converter import JsonToAidmConverter


def merge_query_parameters(query_parameter_dictionaries: List[dict]) -> dict:
    return {parameter: value
            for parameter_dict in query_parameter_dictionaries
            for parameter, value in parameter_dict.items()}


def create_query_parameters_from_preceding_and_succeeding_routing_edge(
        preceding_routing_edge: AnyRoutingEdgeIncomingOrOutgoing,
        succeeding_routing_edge: AnyRoutingEdgeIncomingOrOutgoing
) -> dict:
    if isinstance(preceding_routing_edge, IncomingRoutingEdge):
        preceding_query_parameters = dict(precedingFromSectionTrackId=preceding_routing_edge.start_section_track_id)
    elif isinstance(preceding_routing_edge, IncomingNodeTrackRoutingEdge):
        preceding_query_parameters = dict(
            precedingFromSectionTrackId=preceding_routing_edge.start_section_track_id,
            precedingToNodeTrackId=preceding_routing_edge.end_node_track_id,
        )
    elif isinstance(preceding_routing_edge, OutgoingRoutingEdge):
        preceding_query_parameters = dict(precedingToSectionTrackId=preceding_routing_edge.end_section_track_id)
    elif isinstance(preceding_routing_edge, OutgoingNodeTrackRoutingEdge):
        preceding_query_parameters = dict(
            precedingToSectionTrackId=preceding_routing_edge.end_section_track_id,
            precedingFromNodeTrackId=preceding_routing_edge.start_node_track_id,
        )
    else:
        raise TypeError(f"{preceding_routing_edge} is not an {AnyRoutingEdgeIncomingOrOutgoing}")

    if isinstance(succeeding_routing_edge, IncomingRoutingEdge):
        succeeding_query_parameters = dict(succeedingFromSectionTrackId=succeeding_routing_edge.start_section_track_id)
    elif isinstance(succeeding_routing_edge, IncomingNodeTrackRoutingEdge):
        succeeding_query_parameters = dict(
            succeedingFromSectionTrackId=succeeding_routing_edge.start_section_track_id,
            succeedingToNodeTrackId=succeeding_routing_edge.end_node_track_id,
        )
    elif isinstance(succeeding_routing_edge, OutgoingRoutingEdge):
        succeeding_query_parameters = dict(succeedingToSectionTrackId=succeeding_routing_edge.end_section_track_id)
    elif isinstance(succeeding_routing_edge, OutgoingNodeTrackRoutingEdge):
        succeeding_query_parameters = dict(
            succeedingToSectionTrackId=succeeding_routing_edge.end_section_track_id,
            succeedingFromNodeTrackId=succeeding_routing_edge.start_node_track_id,
        )
    else:
        raise TypeError(f"{succeeding_routing_edge} is not an {AnyRoutingEdgeIncomingOrOutgoing}")
    return merge_query_parameters([preceding_query_parameters, succeeding_query_parameters])


def do_get_routing_edges_request(
        communication_layer: CommunicationLayer,
        routing_point: RoutingPoint,
        routing_edge_type: Optional[RoutingEdgeType]
) -> List[AnyRoutingEdgeIncomingOrCrossingOrOutgoing]:
    url_to_resource = "nodes/{0}/routing-edges".format(routing_point.node_id)
    get_request_params = dict(
        routingEdgeType=None if routing_edge_type is None else routing_edge_type.value,
        nodeTrackId=routing_point.node_track_id,
    )
    response_list = communication_layer.do_get_request(url_to_resource, get_request_params)
    return JsonToAidmConverter().process_json_to_aidm(response_list, List[_RoutingEdge])


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
    return JsonToAidmConverter().process_json_to_aidm(response_dict, List[_AlgorithmLink])