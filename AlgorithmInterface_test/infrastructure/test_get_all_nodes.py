from unittest import mock, TestCase
from AIDMClasses.AIDM_Algorithm_classes import AlgorithmNode, AlgorithmNodeTrack
import AlgorithmInterface_test.test_helper.SessionMockFactory as SessionMockFactory
from AlgorithmInterface import AlgorithmInterfaceFactory
from AlgorithmInterface_test.test_helper.SessionMockTestBase import get_api_url, SessionMockTestBase


class TestGetAllNodes(TestCase):
    class GetAllNodesTestSessionMock(SessionMockTestBase):
        def get(self, request, params):
            self.__last_body = params
            self.__last_request = request
            json_string = ("[\n"
                           "  {\n"
                           "    \"ID\": 1,\n"
                           "    \"Code\": \"45ADW\",\n"
                           "    \"NodeTracks\": [\n"
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
                           "    \"NodeTracks\": [],\n"
                           "    \"DebugString\": \"station:45LNG\"\n"
                           "  },\n"
                           "  {\n"
                           "    \"ID\": 3,\n"
                           "    \"Code\": \"45SIA\",\n"
                           "    \"NodeTracks\": [],\n"
                           "    \"DebugString\": \"station:45SIA\"\n"
                           "  }\n"
                           "]")

            return SessionMockFactory.create_response_mock(json_string, 200)

    @mock.patch('requests.Session', side_effect=GetAllNodesTestSessionMock)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = AlgorithmInterfaceFactory.create(base_url=get_api_url())

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
        self.assertEqual(nodes[0].ID, 1)
        self.assertEqual(nodes[0].Code, '45ADW')
        self.assertEqual(nodes[0].DebugString, "station:45ADW")
        self.assertIsInstance(nodes[0].NodeTracks[0], AlgorithmNodeTrack)
        self.assertEqual(len(nodes[0].NodeTracks), 2)
        self.assertEqual(nodes[0].NodeTracks[0].ID, 162)
        self.assertEqual(nodes[0].NodeTracks[0].Code, '1')
        self.assertEqual(nodes[0].NodeTracks[0].DebugString, "stationtrack:85AR_{StationTrack SID = 34138}")

        self.assertIsInstance(nodes[1], AlgorithmNode)
        self.assertEqual(nodes[1].ID, 2)
        self.assertEqual(nodes[1].Code, '45LNG')
        self.assertEqual(nodes[1].DebugString, "station:45LNG")
        self.assertEqual(nodes[1].NodeTracks, [])

    @mock.patch('requests.Session', side_effect=GetAllNodesTestSessionMock)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)
