import unittest
from unittest import mock

import py_client.algorithm_interface_test.test_helper.SessionMockFactory as APISessionMock
from py_client.aidm import RoutingPoint, CrossingRoutingEdge
from py_client.algorithm_interface import algorithm_interface_factory
from py_client.algorithm_interface_test.test_helper.SessionMockTestBase import get_api_url, SessionMockTestBase


class TestCrossingRoutingEdges(unittest.TestCase):
    class GetCrossingRoutingEdgesTestSessionMock(SessionMockTestBase):
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
                '    "startSectionTrackId": 888,\n'
                '    "endSectionTrackId": 887,\n'
                '    "nodeId": 281,\n'
                '    "type": "crossing"\n'
                "  }\n"
                "]"
            )

            return APISessionMock.create_response_mock(json_string, 200)

    @mock.patch("requests.Session", side_effect=GetCrossingRoutingEdgesTestSessionMock)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = algorithm_interface_factory.create(get_api_url())

    @mock.patch("requests.Session", side_effect=GetCrossingRoutingEdgesTestSessionMock)
    def test_get_crossing_routing_edges_request(self, mocked_get_obj):
        routing_point = RoutingPoint(node_id=121, node_track_id=12)

        self.interface_to_viriato.get_crossing_routing_edges(routing_point=routing_point)

        session_obj = self.interface_to_viriato._AlgorithmInterface__communication_layer.currentSession
        self.assertEqual(session_obj.last_request, get_api_url() + "/nodes/121/routing-edges")
        self.assertDictEqual(session_obj.last_body, {"nodeTrackId": 12, "routingEdgeType": "crossing"})

    @mock.patch("requests.Session", side_effect=GetCrossingRoutingEdgesTestSessionMock)
    def test_get_crossing_routing_edges_response(self, mocked_get_obj):
        routing_point = RoutingPoint(node_id=1)

        routing_edges = self.interface_to_viriato.get_crossing_routing_edges(routing_point)

        self.assertIsInstance(routing_edges, list)
        self.assertIsInstance(routing_edges[0], CrossingRoutingEdge)
        self.assertEqual(routing_edges[0].start_section_track_id, 887)
        self.assertEqual(routing_edges[0].end_section_track_id, 888)
        self.assertEqual(routing_edges[0].node_id, 281)

        self.assertIsInstance(routing_edges[1], CrossingRoutingEdge)
        self.assertEqual(routing_edges[1].start_section_track_id, 888)
        self.assertEqual(routing_edges[1].end_section_track_id, 887)
        self.assertEqual(routing_edges[1].node_id, 281)

        self.assertEqual(len(routing_edges), 2)

    @mock.patch("requests.Session", side_effect=GetCrossingRoutingEdgesTestSessionMock)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)


if __name__ == "__main__":
    unittest.main()
