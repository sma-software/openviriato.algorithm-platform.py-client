import unittest
from unittest import mock
from AIDMClasses import AlgorithmSectionTrack
import AlgorithmInterface.AlgorithmInterface
from AlgorithmInterface import AlgorithmInterfaceFactory
from AlgorithmInterface_test.test_helper import SessionMockFactory as SessionMockFactory
from AlgorithmInterface_test.test_helper.SessionMockTestBase import \
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
                           "    \"SectionCode\": \"15115\",\n"
                           "    \"Weight\": 18430,\n"
                           "    \"DebugString\": \"sectiontrack:s_15115 n_85KLW 411\"\n"
                           "  },\n"
                           "  {\n"
                           "    \"ID\": 687,\n"
                           "    \"Code\": \"311\",\n"
                           "    \"SectionCode\": \"15115\",\n"
                           "    \"Weight\": 18430,\n"
                           "    \"DebugString\": \"sectiontrack:s_15115 n_85KLW 311\"\n"
                           "  },\n"
                           "  {\n"
                           "    \"ID\": 688,\n"
                           "    \"Code\": \"712\",\n"
                           "    \"SectionCode\": \"16010\",\n"
                           "    \"Weight\": 15420,\n"
                           "    \"DebugString\": \"sectiontrack:s_16010 n_85NHOF 712\"\n"
                           "  }\n"
                           "]")

            return SessionMockFactory.create_response_mock(json_string, 200)

    interface_to_viriato: AlgorithmInterface.AlgorithmInterface.AlgorithmInterface

    @mock.patch('requests.Session', side_effect=GetAllSectionTracksSessionTestMock)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = AlgorithmInterfaceFactory.create(get_api_url())

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
        self.assertEqual(section_tracks[0].ID, 686)
        self.assertEqual(section_tracks[0].Code, '411')
        self.assertEqual(section_tracks[0].SectionCode, '15115')
        self.assertEqual(section_tracks[0].Weight, 18430)
        self.assertEqual(section_tracks[0].DebugString, 'sectiontrack:s_15115 n_85KLW 411')

        self.assertIsInstance(section_tracks[1], AlgorithmSectionTrack)
        self.assertEqual(section_tracks[1].ID, 687)
        self.assertEqual(section_tracks[1].Code, '311')
        self.assertEqual(section_tracks[1].SectionCode, '15115')
        self.assertEqual(section_tracks[1].Weight, 18430)
        self.assertEqual(section_tracks[1].DebugString, 'sectiontrack:s_15115 n_85KLW 311')

    @mock.patch('requests.Session', side_effect=GetAllSectionTracksSessionTestMock)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)
