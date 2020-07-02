from unittest import mock, TestCase

import AIDMClasses.AIDM_Algorithm_classes
import AlgorithmInterface_test.test_helper.SessionMockFactory as SessionMockFactory
from AlgorithmInterface import AlgorithmInterfaceFactory
from AlgorithmInterface_test.test_helper.SessionMockTestBase import \
    get_api_url, \
    SessionMockTestBase


class TestGetNode(TestCase):
    class GetNodeTestSessionMock(SessionMockTestBase):
        # to replace session.get:
        def get(self, request, params):
            self.__last_body = params
            self.__last_request = request
            json_string = ("{\n"
                           "  \"ID\": 161,\n"
                           "  \"Code\": \"85AR\",\n"
                           "  \"node_tracks\": [\n"
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
        self.interface_to_viriato = AlgorithmInterfaceFactory.create(base_url=get_api_url())

    @mock.patch('requests.Session', side_effect=GetNodeTestSessionMock)
    def test_get_node_request(self, mocked_get_obj):
        node_id_to_query = 169

        self.interface_to_viriato.get_node(node_id_to_query)

        session_obj = self.interface_to_viriato._AlgorithmInterface__communication_layer.currentSession
        self.assertEqual(get_api_url() + '/nodes/169', session_obj._GetNodeTestSessionMock__last_request)
        self.assertEqual(session_obj._GetNodeTestSessionMock__last_body, {})

    @mock.patch('requests.Session', side_effect=GetNodeTestSessionMock)
    def test_get_node_response(self, mocked_get_obj):
        node_id_to_query = 0

        node_from_mocked_response = self.interface_to_viriato.get_node(node_id_to_query)
        
        self.assertIsInstance(node_from_mocked_response, AIDMClasses.AIDM_Algorithm_classes.AlgorithmNode)
        self.assertIsInstance(node_from_mocked_response.node_tracks[0],
                              AIDMClasses.AIDM_Algorithm_classes.AlgorithmNodeTrack)
        self.assertEqual(node_from_mocked_response.id, 161)
        self.assertEqual(node_from_mocked_response.code, '85AR')
        self.assertEqual(node_from_mocked_response.debug_string, "station:85AR")
        self.assertEqual(node_from_mocked_response.node_tracks[0].id, 162)
        self.assertEqual(node_from_mocked_response.node_tracks[0].debug_string, "stationtrack:85AR_{StationTrack SID = 34138}")

    @mock.patch('requests.Session', side_effect=GetNodeTestSessionMock)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)
