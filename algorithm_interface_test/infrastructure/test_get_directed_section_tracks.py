import unittest
from unittest import mock

import aidm.aidm_algorithm_classes
import algorithm_interface.algorithm_interface
from algorithm_interface import algorithm_interface_factory
from algorithm_interface_test.test_helper import SessionMockFactory as SessionMockFactory
from algorithm_interface_test.test_helper.SessionMockTestBase import \
    get_api_url, \
    SessionMockTestBase


class TestGetDirectedSectionTracks(unittest.TestCase):
    class GetDirectedSectionTracksSessionTestMock(SessionMockTestBase):
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
                           '                    "section_code": "61010",\n'
                           '                    "Weight": 37040,\n'
                           '                    "DebugString": "sectiontrack:s_61010 n_85AR 838"\n'
                           '                },\n'
                           '                {\n'
                           '                    "ID": 886,\n'
                           '                    "Code": "2",\n'
                           '                    "section_code": "61010",\n'
                           '                    "Weight": 37040,\n'
                           '                    "DebugString": "sectiontrack:s_61010 n_85AR 2"\n'
                           '                }\n'
                           '            ]')

            return SessionMockFactory.create_response_mock(json_string, 200)

    interface_to_viriato: algorithm_interface.algorithm_interface.AlgorithmInterface

    @mock.patch('requests.Session', side_effect=GetDirectedSectionTracksSessionTestMock)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = algorithm_interface_factory.create(get_api_url())

    @mock.patch('requests.Session', side_effect=GetDirectedSectionTracksSessionTestMock)
    def test_get_directed_section_tracks_request(self, mocked_get_obj):
        node_id_1 = 20
        node_id_2 = 500

        self.interface_to_viriato.get_directed_section_tracks(node_id_1, node_id_2)

        session_obj = self.interface_to_viriato._AlgorithmInterface__communication_layer.currentSession
        self.assertEqual(session_obj._GetDirectedSectionTracksSessionTestMock__last_request,
                         get_api_url() + '/section-tracks-between/20/500')
        self.assertEqual(session_obj._GetDirectedSectionTracksSessionTestMock__last_body, {})

    @mock.patch('requests.Session', side_effect=GetDirectedSectionTracksSessionTestMock)
    def test_get_directed_section_tracks_return(self, mocked_get_obj):
        node_id_1 = 0
        node_id_2 = 0

        directed_section_tracks = self.interface_to_viriato.get_directed_section_tracks(node_id_1, node_id_2)

        self.assertIsInstance(directed_section_tracks[0], aidm.aidm_algorithm_classes.AlgorithmSectionTrack)
        self.assertIsInstance(directed_section_tracks[0].id, int)
        self.assertIsInstance(directed_section_tracks[0].code, str)
        self.assertIsInstance(directed_section_tracks[0].section_code, str)
        self.assertIsInstance(directed_section_tracks[0].weight, int)
        self.assertIsInstance(directed_section_tracks[0].debug_string, str)

    @mock.patch('requests.Session', side_effect=GetDirectedSectionTracksSessionTestMock)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)
