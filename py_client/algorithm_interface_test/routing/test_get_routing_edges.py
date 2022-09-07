import unittest
from unittest import mock

import py_client.algorithm_interface_test.test_helper.SessionMockFactory as APISessionMock
from py_client.aidm import RoutingPoint, CrossingRoutingEdge, IncomingNodeTrackRoutingEdge, OutgoingNodeTrackRoutingEdge
from py_client.algorithm_interface import algorithm_interface_factory
from py_client.algorithm_interface_test.test_helper.SessionMockTestBase import get_api_url, SessionMockTestBase


class TestRoutingEdges(unittest.TestCase):
    class GetRoutingEdgesTestSessionMock(SessionMockTestBase):
        def get(self, request, params):
            self._last_request = request
            self._last_body = params

            json_string = (
                "[\n"
                "  {\n"
                '    "startSectionTrackId": 887,\n'
                '    "endSectionTrackId": 888,\n'
                '    "nodeId": 281,\n'
                '    "type": "crossing"\n'
                "  },\n"
                "  {\n"
                '    "startNodeTrackId": 162,\n'
                '    "endSectionTrackId": 885,\n'
                '    "nodeId": 281,\n'
                '    "type": "outgoingNodeTrack"\n'
                "  },\n"
                "  {\n"
                '    "startSectionTrackId": 888,\n'
                '    "endSectionTrackId": 887,\n'
                '    "nodeId": 281,\n'
                '    "type": "crossing"\n'
                "  },\n"
                "  {\n"
                '    "startSectionTrackId": 885,\n'
                '    "endNodeTrackId": 162,\n'
                '    "nodeId": 281,\n'
                '    "type": "incomingNodeTrack"\n'
                "  },\n"
                "  {\n"
                '    "startSectionTrackId": 885,\n'
                '    "endNodeTrackId": 163,\n'
                '    "nodeId": 281,\n'
                '    "type": "incomingNodeTrack"\n'
                "  },\n"
                "  {\n"
                '    "startSectionTrackId": 886,\n'
                '    "endNodeTrackId": 162,\n'
                '    "nodeId": 281,\n'
                '    "type": "incomingNodeTrack"\n'
                "  }\n"
                "]"
            )

            return APISessionMock.create_response_mock(json_string, 200)

    @mock.patch("requests.Session", side_effect=GetRoutingEdgesTestSessionMock)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = algorithm_interface_factory.create(get_api_url())

    @mock.patch("requests.Session", side_effect=GetRoutingEdgesTestSessionMock)
    def test_get_routing_edges_request(self, mocked_get_obj):
        routing_point = RoutingPoint(node_id=121, node_track_id=12)

        self.interface_to_viriato.get_routing_edges(routing_point=routing_point)

        session_obj = self.interface_to_viriato._AlgorithmInterface__communication_layer.currentSession
        self.assertEqual(session_obj.last_request, get_api_url() + "/nodes/121/routing-edges")
        self.assertDictEqual(session_obj.last_body, {"nodeTrackId": 12, "routingEdgeType": None})

    @mock.patch("requests.Session", side_effect=GetRoutingEdgesTestSessionMock)
    def test_get_crossing_routing_edges_response(self, mocked_get_obj):
        routing_point = RoutingPoint(node_id=1)

        routing_edges = self.interface_to_viriato.get_crossing_routing_edges(routing_point)

        self.assertIsInstance(routing_edges, list)
        self.assertIsInstance(routing_edges[0], CrossingRoutingEdge)
        self.assertIsInstance(routing_edges[1], OutgoingNodeTrackRoutingEdge)
        self.assertIsInstance(routing_edges[2], CrossingRoutingEdge)
        self.assertIsInstance(routing_edges[3], IncomingNodeTrackRoutingEdge)
        self.assertIsInstance(routing_edges[4], IncomingNodeTrackRoutingEdge)
        self.assertIsInstance(routing_edges[5], IncomingNodeTrackRoutingEdge)

        self.assertEqual(len(routing_edges), 6)

    @mock.patch("requests.Session", side_effect=GetRoutingEdgesTestSessionMock)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)


if __name__ == "__main__":
    unittest.main()
