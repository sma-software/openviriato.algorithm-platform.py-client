import unittest
from unittest import mock
from aidm import AlgorithmNode, AlgorithmNodeTrack
import algorithm_interface.algorithm_interface
from algorithm_interface import algorithm_interface_factory
from algorithm_interface_test.test_helper import SessionMockFactory as SessionMockFactory
from algorithm_interface_test.test_helper.SessionMockTestBase import get_api_url, SessionMockTestBase


class TestGetNeighboringNodesBetween(unittest.TestCase):
    class GetNeighboringNodesBetweenTestMock(SessionMockTestBase):
        def __init__(self):
            super().__init__()

        def get(self, request: str, params: dict):
            self.__last_body = params
            self.__last_request = request

            json_string = ("[\n"
                           "  {\n"
                           "    \"ID\": 348,\n"
                           "    \"Code\": \"85NH\",\n"
                           "    \"node_tracks\": [\n"
                           "      {\n"
                           "        \"ID\": 349,\n"
                           "        \"Code\": \"1\",\n"
                           "        \"DebugString\": \"stationtrack:85NH_1\"\n"
                           "      },\n"
                           "      {\n"
                           "        \"ID\": 350,\n"
                           "        \"Code\": \"2\",\n"
                           "        \"DebugString\": \"stationtrack:85NH_2\"\n"
                           "      }\n"
                           "    ],\n"
                           "    \"DebugString\": \"station:85NH\"\n"
                           "  },\n"
                           "  {\n"
                           "    \"ID\": 281,\n"
                           "    \"Code\": \"85JE\",\n"
                           "    \"node_tracks\": [],\n"
                           "    \"DebugString\": \"station:85JE\"\n"
                           "  }\n"
                           "]")

            return SessionMockFactory.create_response_mock(json_string, 200)

    interface_to_viriato: algorithm_interface.algorithm_interface.AlgorithmInterface

    @mock.patch('requests.Session', side_effect=GetNeighboringNodesBetweenTestMock)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = algorithm_interface_factory.create(get_api_url())

    @mock.patch('requests.Session', side_effect=GetNeighboringNodesBetweenTestMock)
    def test_get_neighboring_nodes_between_request(self, mocked_get_obj):
        from_node_id = 13
        to_node_id = 10
        self.interface_to_viriato.get_neighboring_nodes_between(from_node_id, to_node_id)

        session_obj = self.interface_to_viriato._AlgorithmInterface__communication_layer.currentSession

        self.assertEqual(session_obj._GetNeighboringNodesBetweenTestMock__last_request, get_api_url() + '/nodes')
        self.assertDictEqual(
            session_obj._GetNeighboringNodesBetweenTestMock__last_body,
            dict(HasSectionTrackFromNodeID=13, HasSectionTrackToNodeID=10))

    @mock.patch('requests.Session', side_effect=GetNeighboringNodesBetweenTestMock)
    def test_get_neighboring_nodes_between_return(self, mocked_get_obj):
        from_node_id = 1082
        to_node_id = 10
        nodes = self.interface_to_viriato.get_neighboring_nodes_between(from_node_id, to_node_id)

        self.assertIsInstance(nodes, list)
        self.assertEqual(len(nodes), 2)

        self.assertIsInstance(nodes[0], AlgorithmNode)
        self.assertEqual(nodes[0].id, 348)
        self.assertEqual(nodes[0].code, '85NH')
        self.assertEqual(nodes[0].debug_string, 'station:85NH')
        self.assertIsInstance(nodes[0].node_tracks, list)
        self.assertEqual(len(nodes[0].node_tracks), 2)
        self.assertIsInstance(nodes[0].node_tracks[0], AlgorithmNodeTrack)
        self.assertEqual(nodes[0].node_tracks[0].id, 349)
        self.assertEqual(nodes[0].node_tracks[0].code, '1')
        self.assertEqual(nodes[0].node_tracks[0].debug_string, 'stationtrack:85NH_1')

        self.assertIsInstance(nodes[1], AlgorithmNode)
        self.assertEqual(nodes[1].id, 281)
        self.assertEqual(nodes[1].code, '85JE')
        self.assertEqual(nodes[1].debug_string, 'station:85JE')
        self.assertIsInstance(nodes[1].node_tracks, list)
        self.assertEqual(nodes[1].node_tracks, [])

    @mock.patch('requests.Session', side_effect=GetNeighboringNodesBetweenTestMock)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)
