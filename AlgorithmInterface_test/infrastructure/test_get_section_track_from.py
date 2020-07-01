import unittest
from unittest import mock
from AIDMClasses import AlgorithmSectionTrack
import AlgorithmInterface.AlgorithmInterface
from AlgorithmInterface import AlgorithmInterfaceFactory
from AlgorithmInterface_test.test_helper import SessionMockFactory as SessionMockFactory
from AlgorithmInterface_test.test_helper.SessionMockTestBase import get_api_url, SessionMockTestBase


class TestGetSectionTrackFrom(unittest.TestCase):
    class GetSectionTrackFromSessionTestMock(SessionMockTestBase):
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
                           "  },\n"
                           "  {\n"
                           "    \"ID\": 887,\n"
                           "    \"Code\": \"835\",\n"
                           "    \"SectionCode\": \"61010\",\n"
                           "    \"Weight\": 20910,\n"
                           "    \"DebugString\": \"sectiontrack:s_61010 n_85JE 835\"\n"
                           "  }\n"
                           "]")

            return SessionMockFactory.create_response_mock(json_string, 200)

    interface_to_viriato: AlgorithmInterface.AlgorithmInterface.AlgorithmInterface

    @mock.patch('requests.Session', side_effect=GetSectionTrackFromSessionTestMock)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = AlgorithmInterfaceFactory.create(get_api_url())

    @mock.patch('requests.Session', side_effect=GetSectionTrackFromSessionTestMock)
    def test_get_section_tracks_from_request(self, mocked_get_obj):
        node_id = 1082
        self.interface_to_viriato.get_section_tracks_from(node_id)

        session_obj = self.interface_to_viriato._AlgorithmInterface__communication_layer.currentSession

        self.assertEqual(
            session_obj._GetSectionTrackFromSessionTestMock__last_request,
            get_api_url() + '/section-tracks')
        self.assertEqual(session_obj._GetSectionTrackFromSessionTestMock__last_body, dict(FromNodeID=1082))

    @mock.patch('requests.Session', side_effect=GetSectionTrackFromSessionTestMock)
    def test_get_section_tracks_from_return(self, mocked_get_obj):
        node_id = 1082
        section_tracks = self.interface_to_viriato.get_section_tracks_from(node_id)

        self.assertIsInstance(section_tracks, list)
        self.assertEqual(len(section_tracks), 3)

        self.assertIsInstance(section_tracks[0], AlgorithmSectionTrack)
        self.assertEqual(section_tracks[0].ID, 885)
        self.assertEqual(section_tracks[0].Code, '838')
        self.assertEqual(section_tracks[0].DebugString, 'sectiontrack:s_61010 n_85AR 838')
        self.assertEqual(section_tracks[0].SectionCode, '61010')
        self.assertEqual(section_tracks[0].Weight, 37040)

        self.assertIsInstance(section_tracks[1], AlgorithmSectionTrack)
        self.assertEqual(section_tracks[1].ID, 886)
        self.assertEqual(section_tracks[1].Code, '2')
        self.assertEqual(section_tracks[1].DebugString, 'sectiontrack:s_61010 n_85AR 2')
        self.assertEqual(section_tracks[1].SectionCode, '61010')
        self.assertEqual(section_tracks[1].Weight, 37040)

    @mock.patch('requests.Session', side_effect=GetSectionTrackFromSessionTestMock)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)
