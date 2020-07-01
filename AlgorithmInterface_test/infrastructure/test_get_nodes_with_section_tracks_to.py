import unittest
from unittest import mock
from AIDMClasses import AlgorithmNode, AlgorithmNodeTrack
import AlgorithmInterface.AlgorithmInterface
from AlgorithmInterface import AlgorithmInterfaceFactory
from AlgorithmInterface_test.test_helper import SessionMockFactory as SessionMockFactory
from AlgorithmInterface_test.test_helper.SessionMockTestBase import get_api_url, SessionMockTestBase


class TestGetNodesWithSectionTrackTo(unittest.TestCase):
    class GetNodesWithSectionTrackToTestMock(SessionMockTestBase):
        def __init__(self):
            super().__init__()

        def get(self, request: str, params: dict):
            self.__last_body = params
            self.__last_request = request

            json_string = ("[\n"
                           "  {\n"
                           "    \"ID\": 348,\n"
                           "    \"Code\": \"85NH\",\n"
                           "    \"NodeTracks\": [\n"
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
                           "    \"NodeTracks\": [],\n"
                           "    \"DebugString\": \"station:85JE\"\n"
                           "  }\n"
                           "]")

            return SessionMockFactory.create_response_mock(json_string, 200)

    interface_to_viriato: AlgorithmInterface.AlgorithmInterface.AlgorithmInterface

    @mock.patch('requests.Session', side_effect=GetNodesWithSectionTrackToTestMock)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = AlgorithmInterfaceFactory.create(get_api_url())

    @mock.patch('requests.Session', side_effect=GetNodesWithSectionTrackToTestMock)
    def test_get_nodes_with_section_track_torequest(self, mocked_get_obj):
        node_id = 1099
        self.interface_to_viriato.get_nodes_with_section_track_to(node_id)

        session_obj = self.interface_to_viriato._AlgorithmInterface__communication_layer.currentSession

        self.assertEqual(session_obj._GetNodesWithSectionTrackToTestMock__last_request, get_api_url() + '/nodes')
        self.assertDictEqual(
            session_obj._GetNodesWithSectionTrackToTestMock__last_body,
            dict(HasSectionTrackToNodeID=1099))

    @mock.patch('requests.Session', side_effect=GetNodesWithSectionTrackToTestMock)
    def test_get_nodes_with_section_track_to_return(self, mocked_get_obj):
        node_id = 1082
        nodes = self.interface_to_viriato.get_nodes_with_section_track_to(node_id)

        self.assertIsInstance(nodes, list)
        self.assertEqual(len(nodes), 2)

        self.assertIsInstance(nodes[0], AlgorithmNode)
        self.assertEqual(nodes[0].ID, 348)
        self.assertEqual(nodes[0].Code, '85NH')
        self.assertEqual(nodes[0].DebugString, 'station:85NH')
        self.assertIsInstance(nodes[0].NodeTracks, list)
        self.assertEqual(len(nodes[0].NodeTracks), 2)
        self.assertIsInstance(nodes[0].NodeTracks[0], AlgorithmNodeTrack)
        self.assertEqual(nodes[0].NodeTracks[0].ID, 349)
        self.assertEqual(nodes[0].NodeTracks[0].Code, '1')
        self.assertEqual(nodes[0].NodeTracks[0].DebugString, 'stationtrack:85NH_1')

        self.assertIsInstance(nodes[1], AlgorithmNode)
        self.assertEqual(nodes[1].ID, 281)
        self.assertEqual(nodes[1].Code, '85JE')
        self.assertEqual(nodes[1].DebugString, 'station:85JE')
        self.assertIsInstance(nodes[1].NodeTracks, list)
        self.assertEqual(nodes[1].NodeTracks, [])

    @mock.patch('requests.Session', side_effect=GetNodesWithSectionTrackToTestMock)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)
