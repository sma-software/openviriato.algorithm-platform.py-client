import unittest
from unittest import mock

from py_client.aidm import AlgorithmNode, AlgorithmNodeTrack
from py_client.algorithm_interface import algorithm_interface_factory
from py_client.algorithm_interface_test.test_helper import SessionMockFactory as SessionMockFactory
from py_client.algorithm_interface_test.test_helper.SessionMockTestBase import get_api_url, SessionMockTestBase


class TestGetNodesWithSectionTrackFrom(unittest.TestCase):
    class GetNodesWithSectionTrackFromTestMock(SessionMockTestBase):
        def __init__(self):
            super().__init__()

        def get(self, request: str, params: dict):
            self.__last_body = params
            self.__last_request = request

            json_string = (
                "[\n"
                "  {\n"
                '    "id": 348,\n'
                '    "code": "85NH",\n'
                '    "nodeTracks": [\n'
                "      {\n"
                '        "id": 349,\n'
                '        "code": "1",\n'
                '        "debugString": "stationtrack:85NH_1"\n'
                "      },\n"
                "      {\n"
                '        "id": 350,\n'
                '        "code": "2",\n'
                '        "debugString": "stationtrack:85NH_2"\n'
                "      }\n"
                "    ],\n"
                '    "debugString": "station:85NH"\n'
                "  },\n"
                "  {\n"
                '    "id": 281,\n'
                '    "code": "85JE",\n'
                '    "nodeTracks": [],\n'
                '    "debugString": "station:85JE"\n'
                "  }\n"
                "]"
            )

            return SessionMockFactory.create_response_mock(json_string, 200)

    @mock.patch("requests.Session", side_effect=GetNodesWithSectionTrackFromTestMock)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = algorithm_interface_factory.create(get_api_url())

    @mock.patch("requests.Session", side_effect=GetNodesWithSectionTrackFromTestMock)
    def test_get_nodes_with_section_track_from_request(self, mocked_get_obj):
        node_id = 1082
        self.interface_to_viriato.get_nodes_with_section_track_from(node_id)

        session_obj = self.interface_to_viriato._AlgorithmInterface__communication_layer.currentSession

        self.assertEqual(session_obj._GetNodesWithSectionTrackFromTestMock__last_request, get_api_url() + "/nodes")
        self.assertDictEqual(session_obj._GetNodesWithSectionTrackFromTestMock__last_body, dict(hasSectionTrackFromNodeId=1082))

    @mock.patch("requests.Session", side_effect=GetNodesWithSectionTrackFromTestMock)
    def test_get_nodes_with_section_track_from_return(self, mocked_get_obj):
        node_id = 1082
        nodes = self.interface_to_viriato.get_nodes_with_section_track_from(node_id)

        self.assertIsInstance(nodes, list)
        self.assertEqual(len(nodes), 2)

        self.assertIsInstance(nodes[0], AlgorithmNode)
        self.assertEqual(nodes[0].id, 348)
        self.assertEqual(nodes[0].code, "85NH")
        self.assertEqual(nodes[0].debug_string, "station:85NH")
        self.assertIsInstance(nodes[0].node_tracks, list)
        self.assertEqual(len(nodes[0].node_tracks), 2)
        self.assertIsInstance(nodes[0].node_tracks[0], AlgorithmNodeTrack)
        self.assertEqual(nodes[0].node_tracks[0].id, 349)
        self.assertEqual(nodes[0].node_tracks[0].code, "1")
        self.assertEqual(nodes[0].node_tracks[0].debug_string, "stationtrack:85NH_1")

        self.assertIsInstance(nodes[1], AlgorithmNode)
        self.assertEqual(nodes[1].id, 281)
        self.assertEqual(nodes[1].code, "85JE")
        self.assertEqual(nodes[1].debug_string, "station:85JE")
        self.assertIsInstance(nodes[1].node_tracks, list)
        self.assertEqual(nodes[1].node_tracks, [])

    @mock.patch("requests.Session", side_effect=GetNodesWithSectionTrackFromTestMock)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)
