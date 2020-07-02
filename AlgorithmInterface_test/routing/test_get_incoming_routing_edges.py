import unittest
from unittest import mock

import AIDMClasses.AIDM_RoutingPoint_classes
import AlgorithmInterface_test.test_helper.SessionMockFactory as APISessionMock
from AlgorithmInterface import AlgorithmInterfaceFactory
from AlgorithmInterface_test.test_helper.SessionMockTestBase import \
    get_api_url, SessionMockTestBase


class TestGetIncomingrouting_edges(unittest.TestCase):
    class GetIncomingrouting_edgesTestSessionMock(SessionMockTestBase):
        def get(self, request, params):
            self.__last_request = request
            self.__last_body = params

            if 'EndNodeTrackID' not in params.keys():
                json_string = ("{\n"
                               "  \"IncomingEdges\": [\n"
                               "    {\n"
                               "      \"StartSectionTrackID\": 885,\n"
                               "      \"EndNodeTrackID\": 162,\n"
                               "      \"node_id\": 161\n"
                               "    },\n"
                               "    {\n"
                               "      \"StartSectionTrackID\": 885,\n"
                               "      \"EndNodeTrackID\": 163,\n"
                               "      \"node_id\": 161\n"
                               "    },\n"
                               "    {\n"
                               "      \"StartSectionTrackID\": 886,\n"
                               "      \"EndNodeTrackID\": 162,\n"
                               "      \"node_id\": 161\n"
                               "    }\n"
                               "  ]\n"
                               "}")
            else:
                json_string = ("{\n"
                               "  \"IncomingEdges\": [\n"
                               "    {\n"
                               "      \"StartSectionTrackID\": 886,\n"
                               "      \"EndNodeTrackID\": 162,\n"
                               "      \"node_id\": 161\n"
                               "    }\n"
                               "  ]\n"
                               "}")

            return APISessionMock.create_response_mock(json_string, 200)

    @mock.patch('requests.Session', side_effect=GetIncomingrouting_edgesTestSessionMock)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = AlgorithmInterfaceFactory.create(get_api_url())

    @mock.patch('requests.Session', side_effect=GetIncomingrouting_edgesTestSessionMock)
    def test_get_incoming_routing_edges_request(self, mocked_get_obj):
        routing_point = AIDMClasses.AIDM_RoutingPoint_classes.RoutingPoint(node_id=1, node_track_id=12)

        self.interface_to_viriato.get_incoming_routing_edges(routing_point=routing_point)

        session_obj = self.interface_to_viriato._AlgorithmInterface__communication_layer.currentSession
        self.assertEqual(session_obj._GetIncomingrouting_edgesTestSessionMock__last_request,
                         get_api_url() + '/nodes/1/incoming-routing-edges')
        self.assertDictEqual(session_obj._GetIncomingrouting_edgesTestSessionMock__last_body, dict(EndNodeTrackID=12))

    @mock.patch('requests.Session', side_effect=GetIncomingrouting_edgesTestSessionMock)
    def test_get_incoming_routing_edges_response_only_node_id(self, mocked_get_obj):
        routing_point = AIDMClasses.AIDM_RoutingPoint_classes.RoutingPoint(node_id=161)

        routing_edges = self.interface_to_viriato.get_incoming_routing_edges(routing_point)
        self.assertIsInstance(routing_edges, AIDMClasses.IncomingRoutingEdgeSet)
        self.assertIsInstance(routing_edges.routing_edges[0], AIDMClasses.IncomingRoutingEdge)
        self.assertEqual(routing_edges.routing_edges[0].end_node_track_id, 162)
        self.assertEqual(routing_edges.routing_edges[0].start_section_track_id, 885)
        self.assertEqual(routing_edges.routing_edges[0].node_id, 161)

        self.assertIsInstance(routing_edges.routing_edges[1], AIDMClasses.IncomingRoutingEdge)
        self.assertEqual(routing_edges.routing_edges[1].end_node_track_id, 163)
        self.assertEqual(routing_edges.routing_edges[1].start_section_track_id, 885)
        self.assertEqual(routing_edges.routing_edges[1].node_id, 161)

        self.assertIsInstance(routing_edges.routing_edges[2], AIDMClasses.IncomingRoutingEdge)
        self.assertEqual(routing_edges.routing_edges[2].end_node_track_id, 162)
        self.assertEqual(routing_edges.routing_edges[2].start_section_track_id, 886)
        self.assertEqual(routing_edges.routing_edges[2].node_id, 161)

        self.assertEqual(len(routing_edges.routing_edges), 3)

    @mock.patch('requests.Session', side_effect=GetIncomingrouting_edgesTestSessionMock)
    def test_get_incoming_routing_edges_response_node_id_and_node_track_id(self, mocked_get_obj):
        routing_point = AIDMClasses.AIDM_RoutingPoint_classes.RoutingPoint(node_id=1, node_track_id=21)

        routing_edges = self.interface_to_viriato.get_incoming_routing_edges(routing_point)
        self.assertIsInstance(routing_edges, AIDMClasses.IncomingRoutingEdgeSet)
        self.assertIsInstance(routing_edges.routing_edges[0], AIDMClasses.IncomingRoutingEdge)
        self.assertEqual(routing_edges.routing_edges[0].end_node_track_id, 162)
        self.assertEqual(routing_edges.routing_edges[0].start_section_track_id, 886)
        self.assertEqual(routing_edges.routing_edges[0].node_id, 161)

        self.assertEqual(len(routing_edges.routing_edges), 1)

    @mock.patch('requests.Session', side_effect=GetIncomingrouting_edgesTestSessionMock)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)


if __name__ == '__main__':
    unittest.main()
