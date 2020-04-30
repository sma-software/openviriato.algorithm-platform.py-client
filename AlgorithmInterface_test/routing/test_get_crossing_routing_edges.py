import unittest
from unittest import mock

import AIDMClasses
import AlgorithmInterface_test.test_helper.SessionMockFactory as APISessionMock
from AlgorithmInterface import AlgorithmInterfaceFactory
from AlgorithmInterface_test.test_helper.SessionMockTestBase import get_api_url, SessionMockTestBase


class TestCrossingRoutingEdges(unittest.TestCase):
    class GetCrossingRoutingEdgesTestSessionMock(SessionMockTestBase):
        def get(self, request, params):
            self.__last_request = request
            self.__last_body = params

            json_string = ("{\n"
                           "  \"CrossingEdges\": [\n"
                           "    {\n"
                           "      \"StartSectionTrackID\": 887,\n"
                           "      \"EndSectionTrackID\": 888,\n"
                           "      \"NodeID\": 281\n"
                           "    },\n"
                           "    {\n"
                           "      \"StartSectionTrackID\": 888,\n"
                           "      \"EndSectionTrackID\": 887,\n"
                           "      \"NodeID\": 281\n"
                           "    }\n"
                           "  ]\n"
                           "}")

            return APISessionMock.create_response_mock(json_string, 200)

    @mock.patch('requests.Session', side_effect=GetCrossingRoutingEdgesTestSessionMock)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = AlgorithmInterfaceFactory.create(get_api_url())

    @mock.patch('requests.Session', side_effect=GetCrossingRoutingEdgesTestSessionMock)
    def test_get_crossing_routing_edges_request(self, mocked_get_obj):
        routing_point = AIDMClasses.RoutingPoint(nodeID=121, nodeTrackID=12)

        self.interface_to_viriato.get_crossing_routing_edges(routing_point=routing_point)

        session_obj = self.interface_to_viriato._AlgorithmicPlatformInterface__communication_layer.currentSession
        self.assertEqual(session_obj._GetCrossingRoutingEdgesTestSessionMock__last_request, get_api_url() +
                         "/nodes/121/crossing-routing-edges")
        self.assertDictEqual(session_obj._GetCrossingRoutingEdgesTestSessionMock__last_body, {})

    @mock.patch('requests.Session', side_effect=GetCrossingRoutingEdgesTestSessionMock)
    def test_get_crossing_routing_edges_response(self, mocked_get_obj):
        routing_point = AIDMClasses.RoutingPoint(nodeID=1)

        routing_edges = self.interface_to_viriato.get_crossing_routing_edges(routing_point)

        self.assertIsInstance(routing_edges, AIDMClasses.CrossingRoutingEdgeSet)
        self.assertIsInstance(routing_edges.RoutingEdges[0], AIDMClasses.CrossingRoutingEdge)
        self.assertEqual(routing_edges.RoutingEdges[0].StartSectionTrackID, 887)
        self.assertEqual(routing_edges.RoutingEdges[0].EndSectionTrackID, 888)
        self.assertEqual(routing_edges.RoutingEdges[0].NodeID, 281)

    @mock.patch('requests.Session', side_effect=GetCrossingRoutingEdgesTestSessionMock)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)


if __name__ == '__main__':
    unittest.main()
