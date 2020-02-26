import unittest
from unittest import mock

from AIDM import AIDM_classes
import AlgorithmPlatformPyClient
import unit_testing_with_mock.unit_testing_helpers
from unit_testing_with_mock import SessionMockFactory as SessionMockFactory
from unit_testing_with_mock.unit_testing_helpers import get_url_str


class TestGetParallelSectionTracks(unittest.TestCase):
    class GetParallelSectionTracksSessionTestMock(unit_testing_with_mock.unit_testing_helpers.SessionMockTestBase):
        # to replace session.get:
        def __init__(self):
            super().__init__()

        def get(self, request: str, params: dict):
            self.__last_body = params
            self.__last_request = request

            json_string = ("[\n"
                           "  {\n"
                           "    \"ID\": 885,\n"
                           "    \"Code\": \"838\",\n"
                           "    \"SectionCode\": \"61010\",\n"
                           "    \"Weight\": 37040,\n"
                           "    \"DebugString\": \"sectiontrack:s_61010 n_85AR 838\"\n"
                           "  },\n"
                           "  {\n"
                           "    \"ID\": 886,\n"
                           "    \"Code\": \"2\",\n"
                           "    \"SectionCode\": \"61010\",\n"
                           "    \"Weight\": 37040,\n"
                           "    \"DebugString\": \"sectiontrack:s_61010 n_85AR 2\"\n"
                           "  }\n"
                           "]")
            return SessionMockFactory.create_response_mock(json_string, 200)

    interface_to_viriato: AlgorithmPlatformPyClient.AlgorithmicPlatformInterface

    @mock.patch('requests.Session', side_effect=GetParallelSectionTracksSessionTestMock)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = AlgorithmPlatformPyClient.AlgorithmicPlatformInterface(get_url_str())

    # split in two tests --> one for request and one for return
    @mock.patch('requests.Session', side_effect=GetParallelSectionTracksSessionTestMock)
    def test_get_parallel_section_tracks_request(self, mocked_get_obj):
        self.interface_to_viriato.get_parallel_section_tracks(885)
        session_obj = self.interface_to_viriato._AlgorithmicPlatformInterface__communication_layer.currentSession
        self.assertEqual(session_obj._GetParallelSectionTracksSessionTestMock__last_request,
                         get_url_str() + '/section-tracks-parallel-to/885')
        self.assertEqual(session_obj._GetParallelSectionTracksSessionTestMock__last_body, {})

    @mock.patch('requests.Session', side_effect=GetParallelSectionTracksSessionTestMock)
    def test_get_parallel_section_tracks_return(self, mocked_get_obj):
        parallel_section_tracks = self.interface_to_viriato.get_parallel_section_tracks(0)
        self.assertIsInstance(parallel_section_tracks[0], AIDM_classes.AlgorithmSectionTrack)
        self.assertEqual(parallel_section_tracks[0].ID, 885)
        self.assertEqual(parallel_section_tracks[0].Code, '838')
        self.assertEqual(parallel_section_tracks[0].SectionCode, '61010')
        self.assertEqual(parallel_section_tracks[0].Weight, 37040)
        self.assertEqual(parallel_section_tracks[0].DebugString, 'sectiontrack:s_61010 n_85AR 838')

    def test_get_directed_section_tracks_str_parameters(self):
        with self.assertRaises(AssertionError):
            self.interface_to_viriato.get_parallel_section_tracks('A')

    @mock.patch('requests.Session', side_effect=GetParallelSectionTracksSessionTestMock)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)
