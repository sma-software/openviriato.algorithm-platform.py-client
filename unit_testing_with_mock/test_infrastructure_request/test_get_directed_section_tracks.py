import unittest
from unittest import mock

import AlgorithmInterfaceFactory
import unit_testing_with_mock.unit_testing_helpers
from AIDM_module import AIDM_classes
from unit_testing_with_mock import SessionMockFactory as SessionMockFactory
from unit_testing_with_mock.unit_testing_helpers import get_api_url


class TestGetDirectedSectionTracks(unittest.TestCase):
    class GetDirectedSectionTracksSessionTestMock(unit_testing_with_mock.unit_testing_helpers.SessionMockTestBase):
        # to replace session.get:
        def __init__(self):
            super().__init__()

        def get(self, request: str, params: dict):
            self.__last_body = params
            self.__last_request = request

            json_string = ('[\n'
                           '                {\n'
                           '                    "ID": 885,\n'
                           '                    "Code": "838",\n'
                           '                    "SectionCode": "61010",\n'
                           '                    "Weight": 37040,\n'
                           '                    "DebugString": "sectiontrack:s_61010 n_85AR 838"\n'
                           '                },\n'
                           '                {\n'
                           '                    "ID": 886,\n'
                           '                    "Code": "2",\n'
                           '                    "SectionCode": "61010",\n'
                           '                    "Weight": 37040,\n'
                           '                    "DebugString": "sectiontrack:s_61010 n_85AR 2"\n'
                           '                }\n'
                           '            ]')

            return SessionMockFactory.create_response_mock(json_string, 200)

    interface_to_viriato: AlgorithmInterfaceFactory.AlgorithmicPlatformInterface

    @mock.patch('requests.Session', side_effect=GetDirectedSectionTracksSessionTestMock)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = AlgorithmInterfaceFactory.create(get_api_url())

    @mock.patch('requests.Session', side_effect=GetDirectedSectionTracksSessionTestMock)
    def test_get_directed_section_tracks_request(self, mocked_get_obj):
        node_id_1 = 20
        node_id_2 = 500

        self.interface_to_viriato.get_directed_section_tracks(node_id_1, node_id_2)

        session_obj = self.interface_to_viriato._AlgorithmicPlatformInterface__communication_layer.currentSession
        self.assertEqual(session_obj._GetDirectedSectionTracksSessionTestMock__last_request,
                         get_api_url() + '/section-tracks-between/20/500')
        self.assertEqual(session_obj._GetDirectedSectionTracksSessionTestMock__last_body, {})

    @mock.patch('requests.Session', side_effect=GetDirectedSectionTracksSessionTestMock)
    def test_get_directed_section_tracks_return(self, mocked_get_obj):
        node_id_1 = 0
        node_id_2 = 0

        directed_section_tracks = self.interface_to_viriato.get_directed_section_tracks(node_id_1, node_id_2)

        self.assertIsInstance(directed_section_tracks[0], AIDM_classes.AlgorithmSectionTrack)
        self.assertIsInstance(directed_section_tracks[0].ID, int)
        self.assertIsInstance(directed_section_tracks[0].Code, str)
        self.assertIsInstance(directed_section_tracks[0].SectionCode, str)
        self.assertIsInstance(directed_section_tracks[0].Weight, int)
        self.assertIsInstance(directed_section_tracks[0].DebugString, str)

    @mock.patch('requests.Session', side_effect=GetDirectedSectionTracksSessionTestMock)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)
