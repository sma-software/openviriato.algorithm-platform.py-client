from unittest import mock, TestCase

import py_client.algorithm_interface_test.test_helper.SessionMockFactory as SessionMockFactory
from py_client.aidm.aidm_algorithm_classes import AlgorithmNode, AlgorithmNodeTrack
from py_client.algorithm_interface import algorithm_interface_factory
from py_client.algorithm_interface_test.test_helper.SessionMockTestBase import get_api_url, SessionMockTestBase


class TestGetNeighborNode(TestCase):
    class GetNeighborNodeTestSessionMock(SessionMockTestBase):
        def get(self, request, params):
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
                '    "debugString": "GetNeighborNodeTestSessionMock:85NH"\n'
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

    @mock.patch("requests.Session", side_effect=GetNeighborNodeTestSessionMock)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = algorithm_interface_factory.create(get_api_url())

    @mock.patch("requests.Session", side_effect=GetNeighborNodeTestSessionMock)
    def test_get_neighbor_nodes_request(self, mocked_get_obj):
        node_id = 161
        self.interface_to_viriato.get_neighbor_nodes(node_id)

        session_obj = self.interface_to_viriato._AlgorithmInterface__communication_layer.currentSession

        self.assertEqual(get_api_url() + "/neighbor-nodes/161", session_obj._GetNeighborNodeTestSessionMock__last_request)
        self.assertEqual(session_obj._GetNeighborNodeTestSessionMock__last_body, {})

    @mock.patch("requests.Session", side_effect=GetNeighborNodeTestSessionMock)
    def test_get_neighbor_nodes_response(self, mocked_get_obj):
        node_id = 1

        mock_return_neighbor_nodes = self.interface_to_viriato.get_neighbor_nodes(node_id)

        self.assertIsInstance(mock_return_neighbor_nodes[0], AlgorithmNode)
        self.assertEqual(mock_return_neighbor_nodes[0].debug_string, "GetNeighborNodeTestSessionMock:85NH")
        self.assertIsInstance(mock_return_neighbor_nodes[0].node_tracks[0], AlgorithmNodeTrack)

    @mock.patch("requests.Session", side_effect=GetNeighborNodeTestSessionMock)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)
