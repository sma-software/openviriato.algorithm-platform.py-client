import unittest
from unittest import mock

import py_client.algorithm_interface_test.test_helper.SessionMockFactory as APISessionMock
from py_client.aidm import RoutingPoint, IncomingRoutingEdge, IncomingRoutingEdgeSet
from py_client.algorithm_interface import algorithm_interface_factory
from py_client.algorithm_interface_test.test_helper.SessionMockTestBase import \
    get_api_url, SessionMockTestBase


class TestGetIncomingRoutingEdges(unittest.TestCase):
    class GetIncomingRoutingEdgesTestSessionMock(SessionMockTestBase):
        def get(self, request, params):
            self.__last_request = request
            self.__last_body = params

            if 'endNodeTrackId' not in params.keys():
                json_string = ("{\n"
                               "  \"incomingEdges\": [\n"
                               "    {\n"
                               "      \"startSectionTrackId\": 885,\n"
                               "      \"endNodeTrackId\": 162,\n"
                               "      \"nodeId\": 161\n"
                               "    },\n"
                               "    {\n"
                               "      \"startSectionTrackId\": 885,\n"
                               "      \"endNodeTrackId\": 163,\n"
                               "      \"nodeId\": 161\n"
                               "    },\n"
                               "    {\n"
                               "      \"startSectionTrackId\": 886,\n"
                               "      \"endNodeTrackId\": 162,\n"
                               "      \"nodeId\": 161\n"
                               "    }\n"
                               "  ]\n"
                               "}")
            else:
                json_string = ("{\n"
                               "  \"incomingEdges\": [\n"
                               "    {\n"
                               "      \"startSectionTrackId\": 886,\n"
                               "      \"endNodeTrackId\": 162,\n"
                               "      \"nodeId\": 161\n"
                               "    }\n"
                               "  ]\n"
                               "}")

            return APISessionMock.create_response_mock(json_string, 200)

    @mock.patch('requests.Session', side_effect=GetIncomingRoutingEdgesTestSessionMock)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = algorithm_interface_factory.create(get_api_url())

    @mock.patch('requests.Session', side_effect=GetIncomingRoutingEdgesTestSessionMock)
    def test_get_incoming_routing_edges_request(self, mocked_get_obj):
        routing_point = RoutingPoint(node_id=1, node_track_id=12)

        self.interface_to_viriato.get_incoming_routing_edges(routing_point=routing_point)

        session_obj = self.interface_to_viriato._AlgorithmInterface__communication_layer.currentSession
        self.assertEqual(session_obj._GetIncomingRoutingEdgesTestSessionMock__last_request,
                         get_api_url() + '/nodes/1/incoming-routing-edges')
        self.assertDictEqual(session_obj._GetIncomingRoutingEdgesTestSessionMock__last_body, dict(endNodeTrackId=12))

    @mock.patch('requests.Session', side_effect=GetIncomingRoutingEdgesTestSessionMock)
    def test_get_incoming_routing_edges_response_only_node_id(self, mocked_get_obj):
        routing_point = RoutingPoint(node_id=161)

        routing_edges = self.interface_to_viriato.get_incoming_routing_edges(routing_point)
        self.assertIsInstance(routing_edges, IncomingRoutingEdgeSet)
        self.assertIsInstance(routing_edges.routing_edges[0], IncomingRoutingEdge)
        self.assertEqual(routing_edges.routing_edges[0].end_node_track_id, 162)
        self.assertEqual(routing_edges.routing_edges[0].start_section_track_id, 885)
        self.assertEqual(routing_edges.routing_edges[0].node_id, 161)

        self.assertIsInstance(routing_edges.routing_edges[1], IncomingRoutingEdge)
        self.assertEqual(routing_edges.routing_edges[1].end_node_track_id, 163)
        self.assertEqual(routing_edges.routing_edges[1].start_section_track_id, 885)
        self.assertEqual(routing_edges.routing_edges[1].node_id, 161)

        self.assertIsInstance(routing_edges.routing_edges[2], IncomingRoutingEdge)
        self.assertEqual(routing_edges.routing_edges[2].end_node_track_id, 162)
        self.assertEqual(routing_edges.routing_edges[2].start_section_track_id, 886)
        self.assertEqual(routing_edges.routing_edges[2].node_id, 161)

        self.assertEqual(len(routing_edges.routing_edges), 3)

    @mock.patch('requests.Session', side_effect=GetIncomingRoutingEdgesTestSessionMock)
    def test_get_incoming_routing_edges_response_node_id_and_node_track_id(self, mocked_get_obj):
        routing_point = RoutingPoint(node_id=1, node_track_id=21)

        routing_edges = self.interface_to_viriato.get_incoming_routing_edges(routing_point)
        self.assertIsInstance(routing_edges, IncomingRoutingEdgeSet)
        self.assertIsInstance(routing_edges.routing_edges[0], IncomingRoutingEdge)
        self.assertEqual(routing_edges.routing_edges[0].end_node_track_id, 162)
        self.assertEqual(routing_edges.routing_edges[0].start_section_track_id, 886)
        self.assertEqual(routing_edges.routing_edges[0].node_id, 161)

        self.assertEqual(len(routing_edges.routing_edges), 1)

    @mock.patch('requests.Session', side_effect=GetIncomingRoutingEdgesTestSessionMock)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)


if __name__ == '__main__':
    unittest.main()
