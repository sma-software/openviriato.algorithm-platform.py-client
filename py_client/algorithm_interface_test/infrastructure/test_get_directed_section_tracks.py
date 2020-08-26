import unittest
from unittest import mock

import py_client.aidm.aidm_algorithm_classes
from py_client import algorithm_interface
from py_client.algorithm_interface import algorithm_interface_factory
from py_client.algorithm_interface_test.test_helper import SessionMockFactory as SessionMockFactory
from py_client.algorithm_interface_test.test_helper.SessionMockTestBase import \
    get_api_url, \
    SessionMockTestBase


class TestGetDirectedSectionTracks(unittest.TestCase):
    class GetDirectedSectionTracksSessionTestMock(SessionMockTestBase):
        def get(self, request: str, params: dict):
            self.__last_body = params
            self.__last_request = request

            json_string = ('[\n'
                           '                {\n'
                           '                    "id": 885,\n'
                           '                    "code": "838",\n'
                           '                    "sectionCode": "61010",\n'
                           '                    "weight": 37040,\n'
                           '                    "debugString": "sectiontrack:s_61010 n_85AR 838"\n'
                           '                },\n'
                           '                {\n'
                           '                    "id": 886,\n'
                           '                    "code": "2",\n'
                           '                    "sectionCode": "61010",\n'
                           '                    "weight": 37040,\n'
                           '                    "debugString": "sectiontrack:s_61010 n_85AR 2"\n'
                           '                }\n'
                           '            ]')

            return SessionMockFactory.create_response_mock(json_string, 200)

    interface_to_viriato: py_client.algorithm_interface.algorithm_interface.AlgorithmInterface

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

        self.assertIsInstance(directed_section_tracks[0], py_client.aidm.aidm_algorithm_classes.AlgorithmSectionTrack)
        self.assertIsInstance(directed_section_tracks[0].id, int)
        self.assertIsInstance(directed_section_tracks[0].code, str)
        self.assertIsInstance(directed_section_tracks[0].section_code, str)
        self.assertIsInstance(directed_section_tracks[0].weight, int)
        self.assertIsInstance(directed_section_tracks[0].debug_string, str)

    @mock.patch('requests.Session', side_effect=GetDirectedSectionTracksSessionTestMock)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)
