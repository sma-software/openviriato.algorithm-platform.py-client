import unittest
from unittest import mock

from py_client.aidm import AlgorithmSectionTrack
from py_client.algorithm_interface import algorithm_interface_factory
from py_client.algorithm_interface_test.test_helper import SessionMockFactory as SessionMockFactory
from py_client.algorithm_interface_test.test_helper.SessionMockTestBase import \
    get_api_url, \
    SessionMockTestBase


class TestGetAllSectionTracks(unittest.TestCase):
    class GetAllSectionTracksSessionTestMock(SessionMockTestBase):
        def __init__(self):
            super().__init__()

        def get(self, request: str, params: dict):
            self.__last_body = params
            self.__last_request = request
            json_string = ("[\n"
                           "  {\n"
                           "    \"ID\": 686,\n"
                           "    \"Code\": \"411\",\n"
                           "    \"section_code\": \"15115\",\n"
                           "    \"Weight\": 18430,\n"
                           "    \"DebugString\": \"sectiontrack:s_15115 n_85KLW 411\"\n"
                           "  },\n"
                           "  {\n"
                           "    \"ID\": 687,\n"
                           "    \"Code\": \"311\",\n"
                           "    \"section_code\": \"15115\",\n"
                           "    \"Weight\": 18430,\n"
                           "    \"DebugString\": \"sectiontrack:s_15115 n_85KLW 311\"\n"
                           "  },\n"
                           "  {\n"
                           "    \"ID\": 688,\n"
                           "    \"Code\": \"712\",\n"
                           "    \"section_code\": \"16010\",\n"
                           "    \"Weight\": 15420,\n"
                           "    \"DebugString\": \"sectiontrack:s_16010 n_85NHOF 712\"\n"
                           "  }\n"
                           "]")

            return SessionMockFactory.create_response_mock(json_string, 200)

    @mock.patch('requests.Session', side_effect=GetAllSectionTracksSessionTestMock)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = algorithm_interface_factory.create(get_api_url())

    @mock.patch('requests.Session', side_effect=GetAllSectionTracksSessionTestMock)
    def test_get_all_section_tracks_request(self, mocked_get_obj):
        self.interface_to_viriato.get_all_section_tracks()

        session_obj = self.interface_to_viriato._AlgorithmInterface__communication_layer.currentSession

        self.assertEqual(
            session_obj._GetAllSectionTracksSessionTestMock__last_request,
            get_api_url() + '/section-tracks')
        self.assertEqual(session_obj._GetAllSectionTracksSessionTestMock__last_body, {})

    @mock.patch('requests.Session', side_effect=GetAllSectionTracksSessionTestMock)
    def test_get_all_section_tracks_return(self, mocked_get_obj):
        section_tracks = self.interface_to_viriato.get_all_section_tracks()

        self.assertIsInstance(section_tracks, list)
        self.assertEqual(len(section_tracks), 3)

        self.assertIsInstance(section_tracks[0], AlgorithmSectionTrack)
        self.assertEqual(section_tracks[0].id, 686)
        self.assertEqual(section_tracks[0].code, '411')
        self.assertEqual(section_tracks[0].section_code, '15115')
        self.assertEqual(section_tracks[0].weight, 18430)
        self.assertEqual(section_tracks[0].debug_string, 'sectiontrack:s_15115 n_85KLW 411')

        self.assertIsInstance(section_tracks[1], AlgorithmSectionTrack)
        self.assertEqual(section_tracks[1].id, 687)
        self.assertEqual(section_tracks[1].code, '311')
        self.assertEqual(section_tracks[1].section_code, '15115')
        self.assertEqual(section_tracks[1].weight, 18430)
        self.assertEqual(section_tracks[1].debug_string, 'sectiontrack:s_15115 n_85KLW 311')

    @mock.patch('requests.Session', side_effect=GetAllSectionTracksSessionTestMock)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)
