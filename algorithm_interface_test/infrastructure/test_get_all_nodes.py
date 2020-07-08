from unittest import mock, TestCase
from py_client.aidm.aidm_algorithm_classes import AlgorithmNode, AlgorithmNodeTrack
import algorithm_interface_test.test_helper.SessionMockFactory as SessionMockFactory
from py_client.algorithm_interface import algorithm_interface_factory
from algorithm_interface_test.test_helper.SessionMockTestBase import get_api_url, SessionMockTestBase


class TestGetAllNodes(TestCase):
    class GetAllNodesTestSessionMock(SessionMockTestBase):
        def get(self, request, params):
            self.__last_body = params
            self.__last_request = request
            json_string = ("[\n"
                           "  {\n"
                           "    \"ID\": 1,\n"
                           "    \"Code\": \"45ADW\",\n"
                           "    \"node_tracks\": [\n"
                           "        {\n"
                           "          \"ID\": 162,\n"
                           "          \"Code\": \"1\",\n"
                           "          \"DebugString\": \"stationtrack:85AR_{StationTrack SID = 34138}\"\n"
                           "        },\n"
                           "        {\n"
                           "          \"ID\": 163,\n"
                           "          \"Code\": \"2\",\n"
                           "          \"DebugString\": \"stationtrack:85AR_{StationTrack SID = 34140}\"\n"
                           "        }\n"
                           "       ],\n"
                           "    \"DebugString\": \"station:45ADW\"\n"
                           "  },\n"
                           "  {\n"
                           "    \"ID\": 2,\n"
                           "    \"Code\": \"45LNG\",\n"
                           "    \"node_tracks\": [],\n"
                           "    \"DebugString\": \"station:45LNG\"\n"
                           "  },\n"
                           "  {\n"
                           "    \"ID\": 3,\n"
                           "    \"Code\": \"45SIA\",\n"
                           "    \"node_tracks\": [],\n"
                           "    \"DebugString\": \"station:45SIA\"\n"
                           "  }\n"
                           "]")

            return SessionMockFactory.create_response_mock(json_string, 200)

    @mock.patch('requests.Session', side_effect=GetAllNodesTestSessionMock)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = algorithm_interface_factory.create(base_url=get_api_url())

    @mock.patch('requests.Session', side_effect=GetAllNodesTestSessionMock)
    def test_get_all_nodes_request(self, mocked_get_obj):
        self.interface_to_viriato.get_all_nodes()

        session_obj = self.interface_to_viriato._AlgorithmInterface__communication_layer.currentSession
        self.assertEqual(get_api_url() + '/nodes', session_obj._GetAllNodesTestSessionMock__last_request)
        self.assertEqual(session_obj._GetAllNodesTestSessionMock__last_body, {})

    @mock.patch('requests.Session', side_effect=GetAllNodesTestSessionMock)
    def test_get_all_nodes_response(self, mocked_get_obj):
        nodes = self.interface_to_viriato.get_all_nodes()

        self.assertIsInstance(nodes, list)
        self.assertEqual(len(nodes), 3)

        self.assertIsInstance(nodes[0], AlgorithmNode)
        self.assertEqual(nodes[0].id, 1)
        self.assertEqual(nodes[0].code, '45ADW')
        self.assertEqual(nodes[0].debug_string, "station:45ADW")
        self.assertIsInstance(nodes[0].node_tracks[0], AlgorithmNodeTrack)
        self.assertEqual(len(nodes[0].node_tracks), 2)
        self.assertEqual(nodes[0].node_tracks[0].id, 162)
        self.assertEqual(nodes[0].node_tracks[0].code, '1')
        self.assertEqual(nodes[0].node_tracks[0].debug_string, "stationtrack:85AR_{StationTrack SID = 34138}")

        self.assertIsInstance(nodes[1], AlgorithmNode)
        self.assertEqual(nodes[1].id, 2)
        self.assertEqual(nodes[1].code, '45LNG')
        self.assertEqual(nodes[1].debug_string, "station:45LNG")
        self.assertEqual(nodes[1].node_tracks, [])

    @mock.patch('requests.Session', side_effect=GetAllNodesTestSessionMock)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)
