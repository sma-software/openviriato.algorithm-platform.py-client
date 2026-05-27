import unittest

from py_client.aidm import (
    IncomingNodeTrackRoutingEdgeRequest,
    OutgoingNodeTrackRoutingEdgeRequest,
    CrossingRoutingEdgeRequest,
    OutgoingRoutingEdgeRequest,
    IncomingRoutingEdgeRequest,
)
from py_client.aidm.aidm_routing_edge_classes import (
    CrossingRoutingEdgeResponse,
    IncomingNodeTrackRoutingEdgeResponse,
    OutgoingNodeTrackRoutingEdgeResponse,
    RoutingEdgeSide,
)
from py_client.conversion.object_to_algorithm_platform_json_converter import convert_any_object


class MyTestCase(unittest.TestCase):
    def test_convert_routing_edges_to_algorithm_platform_json(self):
        routing_edges = [
            OutgoingRoutingEdgeRequest(node_id=7, end_section_track_id=1165),
            IncomingNodeTrackRoutingEdgeRequest(node_id=24, start_section_track_id=1165, end_node_track_id=25),
            OutgoingNodeTrackRoutingEdgeRequest(node_id=24, start_node_track_id=25, end_section_track_id=1166),
            CrossingRoutingEdgeRequest(node_id=10, start_section_track_id=1166, end_section_track_id=1212),
        ]

        routing_edges_as_json = convert_any_object(routing_edges)

        self.assertIsInstance(routing_edges_as_json, list)
        self.assertIsInstance(routing_edges_as_json[0], dict)
        self.assertDictEqual(routing_edges_as_json[0], dict(nodeId=7, endSectionTrackId=1165, type="outgoing"))
        self.assertIsInstance(routing_edges_as_json[1], dict)
        self.assertDictEqual(routing_edges_as_json[1], dict(nodeId=24, startSectionTrackId=1165, endNodeTrackId=25, type="incomingNodeTrack"))
        self.assertIsInstance(routing_edges_as_json[2], dict)
        self.assertDictEqual(
            routing_edges_as_json[2],
            dict(nodeId=24, startNodeTrackId=25, endSectionTrackId=1166, type="outgoingNodeTrack"),
        )
        self.assertIsInstance(routing_edges_as_json[3], dict)
        self.assertDictEqual(routing_edges_as_json[3], dict(nodeId=10, startSectionTrackId=1166, endSectionTrackId=1212, type="crossing"))

    def test_convert_routing_edge_responses_to_algorithm_platform_json(self):
        routing_edges = [
            IncomingNodeTrackRoutingEdgeResponse(node_id=168, start_section_track_id=936, end_node_track_id=169, incoming_side=RoutingEdgeSide.B),
            OutgoingNodeTrackRoutingEdgeResponse(node_id=168, start_node_track_id=169, end_section_track_id=936, outgoing_side=RoutingEdgeSide.B),
            CrossingRoutingEdgeResponse(node_id=291, start_section_track_id=938, end_section_track_id=939),
        ]

        routing_edges_as_json = convert_any_object(routing_edges)

        self.assertIsInstance(routing_edges_as_json, list)
        self.assertDictEqual(
            routing_edges_as_json[0],
            dict(nodeId=168, startSectionTrackId=936, incomingSide="b", endNodeTrackId=169, type="incomingNodeTrack"),
        )
        self.assertDictEqual(
            routing_edges_as_json[1],
            dict(nodeId=168, startNodeTrackId=169, outgoingSide="b", endSectionTrackId=936, type="outgoingNodeTrack"),
        )
        self.assertDictEqual(
            routing_edges_as_json[2],
            dict(nodeId=291, startSectionTrackId=938, incomingSide=None, outgoingSide=None, endSectionTrackId=939, type="crossing"),
        )


if __name__ == "__main__":
    unittest.main()
