import unittest
from unittest import mock

import AIDMClasses.AIDM_RoutingPoint_classes
import AlgorithmInterface_test.test_helper.SessionMockFactory as APISessionMock
from AlgorithmInterface import AlgorithmInterfaceFactory
from AlgorithmInterface_test.test_helper.SessionMockTestBase import \
    get_api_url, SessionMockTestBase


class TestGetIncomingRoutingEdges(unittest.TestCase):
    class GetIncomingRoutingEdgesTestSessionMock(SessionMockTestBase):
        def get(self, request, params):
            self.__last_request = request
            self.__last_body = params

            if 'EndNodeTrackID' not in params.keys():
                json_string = ("{\n"
                               "  \"IncomingEdges\": [\n"
                               "    {\n"
                               "      \"StartSectionTrackID\": 885,\n"
                               "      \"EndNodeTrackID\": 162,\n"
                               "      \"NodeID\": 161\n"
                               "    },\n"
                               "    {\n"
                               "      \"StartSectionTrackID\": 885,\n"
                               "      \"EndNodeTrackID\": 163,\n"
                               "      \"NodeID\": 161\n"
                               "    },\n"
                               "    {\n"
                               "      \"StartSectionTrackID\": 886,\n"
                               "      \"EndNodeTrackID\": 162,\n"
                               "      \"NodeID\": 161\n"
                               "    },\n"
                               "    {\n"
                               "      \"StartSectionTrackID\": 886,\n"
                               "      \"EndNodeTrackID\": 163,\n"
                               "      \"NodeID\": 161\n"
                               "    },\n"
                               "    {\n"
                               "      \"StartSectionTrackID\": 887,\n"
                               "      \"EndNodeTrackID\": 162,\n"
                               "      \"NodeID\": 161\n"
                               "    },\n"
                               "    {\n"
                               "      \"StartSectionTrackID\": 887,\n"
                               "      \"EndNodeTrackID\": 163,\n"
                               "      \"NodeID\": 161\n"
                               "    }\n"
                               "  ]\n"
                               "}")
            else:
                json_string = ("{\n"
                               "  \"IncomingEdges\": [\n"
                               "    {\n"
                               "      \"StartSectionTrackID\": 885,\n"
                               "      \"EndNodeTrackID\": 162,\n"
                               "      \"NodeID\": 161\n"
                               "    },\n"
                               "    {\n"
                               "      \"StartSectionTrackID\": 886,\n"
                               "      \"EndNodeTrackID\": 162,\n"
                               "      \"NodeID\": 161\n"
                               "    },\n"
                               "    {\n"
                               "      \"StartSectionTrackID\": 887,\n"
                               "      \"EndNodeTrackID\": 162,\n"
                               "      \"NodeID\": 161\n"
                               "    }\n"
                               "  ]\n"
                               "}")

            return APISessionMock.create_response_mock(json_string, 200)

    @mock.patch('requests.Session', side_effect=GetIncomingRoutingEdgesTestSessionMock)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = AlgorithmInterfaceFactory.create(get_api_url())

    @mock.patch('requests.Session', side_effect=GetIncomingRoutingEdgesTestSessionMock)
    def test_get_incoming_routing_edges_request(self, mocked_get_obj):
        routing_point = AIDMClasses.AIDM_RoutingPoint_classes.RoutingPoint(nodeID=1, nodeTrackID=12)

        self.interface_to_viriato.get_incoming_routing_edges(routing_point=routing_point)

        session_obj = self.interface_to_viriato._AlgorithmicPlatformInterface__communication_layer.currentSession
        self.assertEqual(session_obj._GetIncomingRoutingEdgesTestSessionMock__last_request,
                         get_api_url() + '/nodes/1/incoming-routing-edges')
        self.assertDictEqual(session_obj._GetIncomingRoutingEdgesTestSessionMock__last_body, dict(EndNodeTrackID=12))

    @mock.patch('requests.Session', side_effect=GetIncomingRoutingEdgesTestSessionMock)
    def test_get_incoming_routing_edges_response_only_node_id(self, mocked_get_obj):
        routing_point = AIDMClasses.AIDM_RoutingPoint_classes.RoutingPoint(nodeID=161)

        routing_edges = self.interface_to_viriato.get_incoming_routing_edges(routing_point)
        self.assertIsInstance(routing_edges, AIDMClasses.IncomingRoutingEdgeSet)
        self.assertIsInstance(routing_edges.RoutingEdges[0], AIDMClasses.IncomingRoutingEdge)
        self.assertEqual(routing_edges.RoutingEdges[3].EndNodeTrackID, 163)
        self.assertEqual(routing_edges.RoutingEdges[3].StartSectionTrackID, 886)
        self.assertEqual(routing_edges.RoutingEdges[3].NodeID, 161)

    @mock.patch('requests.Session', side_effect=GetIncomingRoutingEdgesTestSessionMock)
    def test_get_incoming_routing_edges_response_node_id_and_node_track_id(self, mocked_get_obj):
        routing_point = AIDMClasses.AIDM_RoutingPoint_classes.RoutingPoint(nodeID=1, nodeTrackID=21)

        routing_edges = self.interface_to_viriato.get_incoming_routing_edges(routing_point)
        self.assertIsInstance(routing_edges, AIDMClasses.IncomingRoutingEdgeSet)
        self.assertIsInstance(routing_edges.RoutingEdges[0], AIDMClasses.IncomingRoutingEdge)
        self.assertEqual(routing_edges.RoutingEdges[1].EndNodeTrackID, 162)
        self.assertEqual(routing_edges.RoutingEdges[1].StartSectionTrackID, 886)
        self.assertEqual(routing_edges.RoutingEdges[1].NodeID, 161)

    @mock.patch('requests.Session', side_effect=GetIncomingRoutingEdgesTestSessionMock)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)


if __name__ == '__main__':
    unittest.main()
