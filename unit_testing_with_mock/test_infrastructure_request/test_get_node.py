from unittest import mock, TestCase

import AlgorithmInterfaceFactory
import unit_testing_with_mock.SessionMockFactory as SessionMockFactory
import unit_testing_with_mock.unit_testing_helpers
from AIDM_module import AIDM_classes
from unit_testing_with_mock.unit_testing_helpers import get_api_url


class TestGetNode(TestCase):
    class GetNodeTestSessionMock(unit_testing_with_mock.unit_testing_helpers.SessionMockTestBase):
        # to replace session.get:
        def get(self, request, params):
            self.__last_body = params
            self.__last_request = request
            json_string = ("{\n"
                           "  \"ID\": 161,\n"
                           "  \"Code\": \"85AR\",\n"
                           "  \"NodeTracks\": [\n"
                           "    {\n"
                           "      \"ID\": 162,\n"
                           "      \"Code\": \"1\",\n"
                           "      \"DebugString\": \"stationtrack:85AR_{StationTrack SID = 34138}\"\n"
                           "    },\n"
                           "    {\n"
                           "      \"ID\": 163,\n"
                           "      \"Code\": \"2\",\n"
                           "      \"DebugString\": \"stationtrack:85AR_{StationTrack SID = 34140}\"\n"
                           "    }\n"
                           "  ],\n"
                           "  \"DebugString\": \"station:85AR\"\n"
                           "}")

            return SessionMockFactory.create_response_mock(json_string, 200)

    @mock.patch('requests.Session', side_effect=GetNodeTestSessionMock)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = AlgorithmInterfaceFactory.create(base_url=get_api_url()) # rename to api url
        #AlgorithmInterfaceFactory.AlgorithmicPlatformInterface(get_api_url())

    @mock.patch('requests.Session', side_effect=GetNodeTestSessionMock)
    def test_get_node_request(self, mocked_get_obj):
        node_id_to_query = 169

        self.interface_to_viriato.get_node(node_id_to_query)

        session_obj = self.interface_to_viriato._AlgorithmicPlatformInterface__communication_layer.currentSession
        self.assertEqual(get_api_url() + '/nodes/169', session_obj._GetNodeTestSessionMock__last_request) # there must be a way to do that smarter
        self.assertEqual(session_obj._GetNodeTestSessionMock__last_body, {})

    @mock.patch('requests.Session', side_effect=GetNodeTestSessionMock)
    def test_get_node_response(self, mocked_get_obj):
        node_id_to_query = 0

        node_from_mocked_response = self.interface_to_viriato.get_node(node_id_to_query)
        
        self.assertIsInstance(node_from_mocked_response, AIDM_classes.AlgorithmNode)
        self.assertIsInstance(node_from_mocked_response.NodeTracks[0], AIDM_classes.AlgorithmNodeTrack)
        self.assertEqual(node_from_mocked_response.ID, 161)
        self.assertEqual(node_from_mocked_response.Code, '85AR')
        self.assertEqual(node_from_mocked_response.DebugString, "station:85AR")
        self.assertEqual(node_from_mocked_response.NodeTracks[0].ID, 162)
        self.assertEqual(node_from_mocked_response.NodeTracks[0].DebugString, "stationtrack:85AR_{StationTrack SID = 34138}")

    @mock.patch('requests.Session', side_effect=GetNodeTestSessionMock)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)
