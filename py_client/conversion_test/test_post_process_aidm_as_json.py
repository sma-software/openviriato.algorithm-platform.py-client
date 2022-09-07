import unittest

from py_client.aidm import IncomingNodeTrackRoutingEdge, OutgoingNodeTrackRoutingEdge, CrossingRoutingEdge, OutgoingRoutingEdge, IncomingRoutingEdge
from py_client.conversion.object_to_algorithm_platform_json_converter import convert_any_object


class MyTestCase(unittest.TestCase):
    def test_convert_routing_edges_to_algorithm_platform_json(self):
        routing_edges = [
            OutgoingRoutingEdge(node_id=7, end_section_track_id=1165),
            IncomingNodeTrackRoutingEdge(node_id=24, start_section_track_id=1165, end_node_track_id=25),
            OutgoingNodeTrackRoutingEdge(node_id=24, start_node_track_id=25, end_section_track_id=1166),
            CrossingRoutingEdge(node_id=10, start_section_track_id=1166, end_section_track_id=1212),
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


if __name__ == "__main__":
    unittest.main()
