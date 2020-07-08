import unittest
from unittest import mock

import aidm
import algorithm_interface_test.test_helper.SessionMockFactory as APISessionMock
from algorithm_interface import algorithm_interface_factory
from algorithm_interface_test.test_helper.SessionMockTestBase import get_api_url, SessionMockTestBase


class TestGetOutgoingrouting_edges(unittest.TestCase):
    class GetOutgoingrouting_edgesTestSessionMock(SessionMockTestBase):
        def get(self, request, params):
            self.__last_request = request
            self.__last_body = params

            if "StartNodeTrackID" not in params.keys():
                json_string = ("{\n"
                               "  \"OutgoingEdges\": [\n"
                               "    {\n"
                               "      \"StartNodeTrackID\": 21,\n"
                               "      \"EndSectionTrackID\": 885,\n"
                               "      \"node_id\": 154\n"
                               "    },\n"
                               "    {\n"
                               "      \"StartNodeTrackID\": 21,\n"
                               "      \"EndSectionTrackID\": 886,\n"
                               "      \"node_id\": 154\n"
                               "    },\n"
                               "    {\n"
                               "      \"StartNodeTrackID\": 21,\n"
                               "      \"EndSectionTrackID\": 887,\n"
                               "      \"node_id\": 154\n"
                               "    }\n"
                               "  ]\n"
                               "}")
            else:
                json_string = ("{\n"
                               "  \"OutgoingEdges\": [\n"
                               "    {\n"
                               "      \"StartNodeTrackID\": 162,\n"
                               "      \"EndSectionTrackID\": 885,\n"
                               "      \"node_id\": 45\n"
                               "    }\n"
                               "  ]\n"
                               "}")

            return APISessionMock.create_response_mock(json_string, 200)

    @mock.patch('requests.Session', side_effect=GetOutgoingrouting_edgesTestSessionMock)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = algorithm_interface_factory.create(get_api_url())

    @mock.patch('requests.Session', side_effect=GetOutgoingrouting_edgesTestSessionMock)
    def test_get_outgoing_routing_edges_request(self, mocked_get_obj):
        routing_point = aidm.RoutingPoint(node_id=1, node_track_id=12)

        self.interface_to_viriato.get_outgoing_routing_edges(routing_point=routing_point)

        session_obj = self.interface_to_viriato._AlgorithmInterface__communication_layer.currentSession
        self.assertEqual(get_api_url() + "/nodes/1/outgoing-routing-edges",
                         session_obj._GetOutgoingrouting_edgesTestSessionMock__last_request)
        self.assertDictEqual(session_obj._GetOutgoingrouting_edgesTestSessionMock__last_body, {"StartNodeTrackID": 12})

    @mock.patch('requests.Session', side_effect=GetOutgoingrouting_edgesTestSessionMock)
    def test_get_outgoing_routing_edges_response_only_node_id(self, mocked_get_obj):
        routing_point = aidm.RoutingPoint(node_id=161)

        routing_edges = self.interface_to_viriato.get_outgoing_routing_edges(routing_point)
        self.assertIsInstance(routing_edges, aidm.OutgoingRoutingEdgeSet)
        self.assertIsInstance(routing_edges.routing_edges[0], aidm.OutgoingRoutingEdge)
        self.assertEqual(routing_edges.routing_edges[0].start_node_track_id, 21)
        self.assertEqual(routing_edges.routing_edges[0].end_section_track_id, 885)
        self.assertEqual(routing_edges.routing_edges[0].node_id, 154)

        self.assertIsInstance(routing_edges.routing_edges[1], aidm.OutgoingRoutingEdge)
        self.assertEqual(routing_edges.routing_edges[1].start_node_track_id, 21)
        self.assertEqual(routing_edges.routing_edges[1].end_section_track_id, 886)
        self.assertEqual(routing_edges.routing_edges[1].node_id, 154)

        self.assertIsInstance(routing_edges.routing_edges[2], aidm.OutgoingRoutingEdge)
        self.assertEqual(routing_edges.routing_edges[2].start_node_track_id, 21)
        self.assertEqual(routing_edges.routing_edges[2].end_section_track_id, 887)
        self.assertEqual(routing_edges.routing_edges[2].node_id, 154)

        self.assertEqual(len(routing_edges.routing_edges), 3)

    @mock.patch('requests.Session', side_effect=GetOutgoingrouting_edgesTestSessionMock)
    def test_get_outgoing_routing_edges_response_node_id_response_and_node_track_id(self, mocked_get_obj):
        routing_point = aidm.RoutingPoint(node_id=1, node_track_id=21)

        routing_edges = self.interface_to_viriato.get_outgoing_routing_edges(routing_point)

        self.assertIsInstance(routing_edges, aidm.OutgoingRoutingEdgeSet)
        self.assertIsInstance(routing_edges.routing_edges[0], aidm.OutgoingRoutingEdge)
        self.assertEqual(routing_edges.routing_edges[0].start_node_track_id, 162)
        self.assertEqual(routing_edges.routing_edges[0].end_section_track_id, 885)
        self.assertEqual(routing_edges.routing_edges[0].node_id, 45)

        self.assertEqual(len(routing_edges.routing_edges), 1)

    @mock.patch('requests.Session', side_effect=GetOutgoingrouting_edgesTestSessionMock)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)


if __name__ == '__main__':
    unittest.main()
