import unittest
from unittest import mock

import AIDMClasses
import AlgorithmInterface_test.test_helper.SessionMockFactory as APISessionMock
from AlgorithmInterface import AlgorithmInterfaceFactory
from AlgorithmInterface_test.test_helper.SessionMockTestBase import get_api_url, SessionMockTestBase


class TestGetOutgoingRoutingEdges(unittest.TestCase):
    class GetOutgoingRoutingEdgesTestSessionMock(SessionMockTestBase):
        def get(self, request, params):
            self.__last_request = request
            self.__last_body = params

            if "StartNodeTrackID" not in params.keys():
                json_string = ("{\n"
                               "  \"OutgoingEdges\": [\n"
                               "    {\n"
                               "      \"StartNodeTrackID\": 21,\n"
                               "      \"EndSectionTrackID\": 885,\n"
                               "      \"NodeID\": 154\n"
                               "    },\n"
                               "    {\n"
                               "      \"StartNodeTrackID\": 21,\n"
                               "      \"EndSectionTrackID\": 886,\n"
                               "      \"NodeID\": 154\n"
                               "    },\n"
                               "    {\n"
                               "      \"StartNodeTrackID\": 21,\n"
                               "      \"EndSectionTrackID\": 887,\n"
                               "      \"NodeID\": 154\n"
                               "    }\n"
                               "  ]\n"
                               "}")
            else:
                json_string = ("{\n"
                               "  \"OutgoingEdges\": [\n"
                               "    {\n"
                               "      \"StartNodeTrackID\": 162,\n"
                               "      \"EndSectionTrackID\": 885,\n"
                               "      \"NodeID\": 45\n"
                               "    }\n"
                               "  ]\n"
                               "}")

            return APISessionMock.create_response_mock(json_string, 200)

    @mock.patch('requests.Session', side_effect=GetOutgoingRoutingEdgesTestSessionMock)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = AlgorithmInterfaceFactory.create(get_api_url())

    @mock.patch('requests.Session', side_effect=GetOutgoingRoutingEdgesTestSessionMock)
    def test_get_outgoing_routing_edges_request(self, mocked_get_obj):
        routing_point = AIDMClasses.RoutingPoint(nodeID=1, nodeTrackID=12)

        self.interface_to_viriato.get_outgoing_routing_edges(routing_point=routing_point)

        session_obj = self.interface_to_viriato._AlgorithmicPlatformInterface__communication_layer.currentSession
        self.assertEqual(get_api_url() + "/nodes/1/outgoing-routing-edges",
                         session_obj._GetOutgoingRoutingEdgesTestSessionMock__last_request)
        self.assertDictEqual(session_obj._GetOutgoingRoutingEdgesTestSessionMock__last_body, {"StartNodeTrackID": 12})

    @mock.patch('requests.Session', side_effect=GetOutgoingRoutingEdgesTestSessionMock)
    def test_get_outgoing_routing_edges_response_only_node_id(self, mocked_get_obj):
        routing_point = AIDMClasses.RoutingPoint(nodeID=161)

        routing_edges = self.interface_to_viriato.get_outgoing_routing_edges(routing_point)
        self.assertIsInstance(routing_edges, AIDMClasses.OutgoingRoutingEdgeSet)
        self.assertIsInstance(routing_edges.RoutingEdges[0], AIDMClasses.OutgoingRoutingEdge)
        self.assertEqual(routing_edges.RoutingEdges[0].StartNodeTrackID, 21)
        self.assertEqual(routing_edges.RoutingEdges[0].EndSectionTrackID, 885)
        self.assertEqual(routing_edges.RoutingEdges[0].NodeID, 154)

        self.assertIsInstance(routing_edges.RoutingEdges[1], AIDMClasses.OutgoingRoutingEdge)
        self.assertEqual(routing_edges.RoutingEdges[1].StartNodeTrackID, 21)
        self.assertEqual(routing_edges.RoutingEdges[1].EndSectionTrackID, 886)
        self.assertEqual(routing_edges.RoutingEdges[1].NodeID, 154)

        self.assertIsInstance(routing_edges.RoutingEdges[2], AIDMClasses.OutgoingRoutingEdge)
        self.assertEqual(routing_edges.RoutingEdges[2].StartNodeTrackID, 21)
        self.assertEqual(routing_edges.RoutingEdges[2].EndSectionTrackID, 887)
        self.assertEqual(routing_edges.RoutingEdges[2].NodeID, 154)

        self.assertEqual(len(routing_edges.RoutingEdges), 3)

    @mock.patch('requests.Session', side_effect=GetOutgoingRoutingEdgesTestSessionMock)
    def test_get_outgoing_routing_edges_response_node_id_response_and_node_track_id(self, mocked_get_obj):
        routing_point = AIDMClasses.RoutingPoint(nodeID=1, nodeTrackID=21)

        routing_edges = self.interface_to_viriato.get_outgoing_routing_edges(routing_point)

        self.assertIsInstance(routing_edges, AIDMClasses.OutgoingRoutingEdgeSet)
        self.assertIsInstance(routing_edges.RoutingEdges[0], AIDMClasses.OutgoingRoutingEdge)
        self.assertEqual(routing_edges.RoutingEdges[0].StartNodeTrackID, 162)
        self.assertEqual(routing_edges.RoutingEdges[0].EndSectionTrackID, 885)
        self.assertEqual(routing_edges.RoutingEdges[0].NodeID, 45)

        self.assertEqual(len(routing_edges.RoutingEdges), 1)

    @mock.patch('requests.Session', side_effect=GetOutgoingRoutingEdgesTestSessionMock)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)


if __name__ == '__main__':
    unittest.main()
