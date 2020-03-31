from unittest import mock, TestCase

import AlgorithmInterface_test.test_helper.SessionMockFactory as SessionMockFactory
from AIDMClasses import AIDM_classes
from AlgorithmInterface import AlgorithmInterfaceFactory
from AlgorithmInterface_test.test_helper.SessionMockTestBase import \
    get_api_url, \
    SessionMockTestBase


class TestGetNeighborNode(TestCase):
    class GetNeighborNodeTestSessionMock(SessionMockTestBase):
        # to replace session.get:
        def get(self, request, params):
            self.__last_body = params
            self.__last_request = request
            json_string = ('[\n'
                           '  {\n'
                           '    "ID": 348,\n'
                           '    "Code": "85NH",\n'
                           '    "NodeTracks": [\n'
                           '      {\n'
                           '        "ID": 349,\n'
                           '        "Code": "1",\n'
                           '        "DebugString": "stationtrack:85NH_1"\n'
                           '      },\n'
                           '      {\n'
                           '        "ID": 350,\n'
                           '        "Code": "2",\n'
                           '        "DebugString": "stationtrack:85NH_2"\n'
                           '      }\n'
                           '    ],\n'
                           '    "DebugString": "GetNeighborNodeTestSessionMock:85NH"\n'
                           '  },\n'
                           '  {\n'
                           '    "ID": 281,\n'
                           '    "Code": "85JE",\n'
                           '    "NodeTracks": [],\n'
                           '    "DebugString": "station:85JE"\n'
                           '  }\n'
                           ']')

            return SessionMockFactory.create_response_mock(json_string, 200)

    @mock.patch('requests.Session', side_effect=GetNeighborNodeTestSessionMock)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = AlgorithmInterfaceFactory.create(get_api_url())

    @mock.patch('requests.Session', side_effect=GetNeighborNodeTestSessionMock)
    def test_get_neighbor_nodes_request(self, mocked_get_obj):
        node_id = 161
        self.interface_to_viriato.get_neighbor_nodes(node_id)

        session_obj = self.interface_to_viriato._AlgorithmicPlatformInterface__communication_layer.currentSession

        self.assertEqual(get_api_url() + '/neighbor-nodes/161',
                         session_obj._GetNeighborNodeTestSessionMock__last_request)
        self.assertEqual(session_obj._GetNeighborNodeTestSessionMock__last_body, {})

    @mock.patch('requests.Session', side_effect=GetNeighborNodeTestSessionMock)
    def test_get_neighbor_nodes_response(self, mocked_get_obj):
        node_id = 1

        mock_return_neighbor_nodes = self.interface_to_viriato.get_neighbor_nodes(node_id)

        self.assertIsInstance(mock_return_neighbor_nodes[0], AIDM_classes.AlgorithmNode)
        self.assertEqual(mock_return_neighbor_nodes[0].DebugString, "GetNeighborNodeTestSessionMock:85NH")
        self.assertIsInstance(mock_return_neighbor_nodes[0].NodeTracks[0], AIDM_classes.AlgorithmNodeTrack)

    @mock.patch('requests.Session', side_effect=GetNeighborNodeTestSessionMock)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)
