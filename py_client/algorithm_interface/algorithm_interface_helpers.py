from typing import List, Union
from py_client.aidm import IncomingRoutingEdge, OutgoingRoutingEdge


def merge_query_parameters(query_parameter_dictionaries: List[dict]) -> dict:
    return {parameter: value
            for parameter_dict in query_parameter_dictionaries
            for parameter, value in parameter_dict.items()}


def create_query_parameters_from_preceding_and_succeeding_routing_edge(
        preceding_routing_edge: Union[IncomingRoutingEdge, OutgoingRoutingEdge],
        succeeding_routing_edge: Union[IncomingRoutingEdge, OutgoingRoutingEdge]) -> dict:

    if isinstance(preceding_routing_edge, IncomingRoutingEdge):
        preceding_query_parameters = dict(
            PrecedingFromSectionTrackID=preceding_routing_edge.start_section_track_id,
            PrecedingToNodeTrackID=preceding_routing_edge.end_node_track_id)
    elif isinstance(preceding_routing_edge, OutgoingRoutingEdge):
        preceding_query_parameters = dict(
            PrecedingToSectionTrackID=preceding_routing_edge.end_section_track_id,
            PrecedingFromNodeTrackID=preceding_routing_edge.start_node_track_id)

    if isinstance(succeeding_routing_edge, IncomingRoutingEdge):
        succeeding_query_parameters = dict(
            SucceedingFromSectionTrackID=succeeding_routing_edge.start_section_track_id,
            SucceedingToNodeTrackID=succeeding_routing_edge.end_node_track_id)
    elif isinstance(succeeding_routing_edge, OutgoingRoutingEdge):
        succeeding_query_parameters = dict(
            SucceedingToSectionTrackID=succeeding_routing_edge.end_section_track_id,
            SucceedingFromNodeTrackID=succeeding_routing_edge.start_node_track_id)

    return merge_query_parameters([preceding_query_parameters, succeeding_query_parameters])
