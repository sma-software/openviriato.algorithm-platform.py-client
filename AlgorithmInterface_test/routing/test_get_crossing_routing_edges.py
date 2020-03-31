import unittest
from unittest import mock

import AlgorithmInterface_test.test_helper.SessionMockFactory as APISessionMock
from AIDMClasses import AIDM_classes
from AlgorithmInterface import AlgorithmInterfaceFactory
from AlgorithmInterface_test.test_helper.SessionMockTestBase import \
    get_api_url, SessionMockTestBase


class TestCrossingRoutingEdges(unittest.TestCase):
    class GetCrossingRoutingEdgesTestSessionMock(SessionMockTestBase):
        def get(self, request, params):
            self.__last_request = request
            self.__last_body = params

            json_string = ("{\n"
                           "  \"crossingEdges\": [\n"
                           "    {\n"
                           "      \"nodeID\": \"281\",\n"
                           "      \"startSectionTrack\": \"887\",\n"
                           "      \"endSectionTrack\": \"888\"\n"
                           "    },\n"
                           "    {\n"
                           "      \"nodeID\": \"281\",\n"
                           "      \"startSectionTrack\": \"888\",\n"
                           "      \"endSectionTrack\": \"887\"\n"
                           "    }\n"
                           "  ]\n"
                           "}")

            return APISessionMock.create_response_mock(json_string, 200)

    @mock.patch('requests.Session', side_effect=GetCrossingRoutingEdgesTestSessionMock)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = AlgorithmInterfaceFactory.create(get_api_url())

    @unittest.skip("VPLAT-7449")
    @mock.patch('requests.Session', side_effect=GetCrossingRoutingEdgesTestSessionMock)
    def test_get_crossing_routing_edges_request(self, mocked_get_obj):
        routing_point = AIDM_classes.RoutingPoint(nodeID=1, nodeTrackID=12)

        self.interface_to_viriato.get_crossing_routing_edges(routing_point=routing_point)

        session_obj = self.interface_to_viriato._AlgorithmicPlatformInterface__communication_layer.currentSession
        # FIXME The assertions do not match -> Bug in Doc (JSON keys != AIDM property names)
        self.assertEqual(session_obj._GetCrossingRoutingEdgesTestSessionMock__last_request, get_api_url() +
                         "/vehicles/formations/1828")
        self.assertDictEqual(session_obj._GetCrossingRoutingEdgesTestSessionMock__last_body, {"nodeTrackID": "12"})

    @unittest.skip("VPLAT-7449")
    @mock.patch('requests.Session', side_effect=GetCrossingRoutingEdgesTestSessionMock)
    def test_get_crossing_routing_edges__response(self, mocked_get_obj):
        routing_point = AIDM_classes.RoutingPoint(nodeID=1)

        routing_edges = self.interface_to_viriato.get_crossing_routing_edges(routing_point)
        # FIXME Is not implemented due to a bug in the Documentation
        raise NotImplementedError

    @mock.patch('requests.Session', side_effect=GetCrossingRoutingEdgesTestSessionMock)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)


if __name__ == '__main__':
    unittest.main()