import unittest
from unittest import mock

from py_client.aidm import AlgorithmSectionTrack
from py_client.algorithm_interface import algorithm_interface_factory
from py_client.algorithm_interface_test.test_helper import SessionMockFactory as SessionMockFactory
from py_client.algorithm_interface_test.test_helper.SessionMockTestBase import get_api_url, SessionMockTestBase


class TestGetSectionTracksBetween(unittest.TestCase):
    class GetSectionTracksBetweenSessionTestMock(SessionMockTestBase):
        def __init__(self):
            super().__init__()

        def get(self, request: str, params: dict):
            self._last_body = params
            self._last_request = request

            json_string = (
                "[\n"
                "  {\n"
                '    "id": 885,\n'
                '    "code": "838",\n'
                '    "sectionCode": "61010",\n'
                '    "distanceUnits": 37040,\n'
                '    "debugString": "sectiontrack:s_61010 n_85AR 838"\n'
                "  },\n"
                "  {\n"
                '    "id": 886,\n'
                '    "code": "2",\n'
                '    "sectionCode": "61010",\n'
                '    "distanceUnits": 37040,\n'
                '    "debugString": "sectiontrack:s_61010 n_85AR 2"\n'
                "  }\n"
                "]"
            )

            return SessionMockFactory.create_response_mock(json_string, 200)

    @mock.patch("requests.Session", side_effect=GetSectionTracksBetweenSessionTestMock)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = algorithm_interface_factory.create(get_api_url())

    @mock.patch("requests.Session", side_effect=GetSectionTracksBetweenSessionTestMock)
    def test_get_section_tracks_between_request(self, mocked_get_obj):
        from_node_id = 1082
        to_node_id = 1
        self.interface_to_viriato.get_section_tracks_between(from_node_id, to_node_id)

        session_obj = self.interface_to_viriato._AlgorithmInterface__communication_layer.currentSession

        self.assertEqual(session_obj.last_request, get_api_url() + "/section-tracks")
        self.assertEqual(session_obj.last_body, dict(fromNodeId=1082, toNodeId=1))

    @mock.patch("requests.Session", side_effect=GetSectionTracksBetweenSessionTestMock)
    def test_get_section_tracks_between_return(self, mocked_get_obj):
        from_node_id = 1082
        to_node_id = 1
        section_tracks = self.interface_to_viriato.get_section_tracks_between(from_node_id, to_node_id)

        self.assertIsInstance(section_tracks, list)
        self.assertEqual(len(section_tracks), 2)

        self.assertIsInstance(section_tracks[0], AlgorithmSectionTrack)
        self.assertEqual(section_tracks[0].id, 885)
        self.assertEqual(section_tracks[0].code, "838")
        self.assertEqual(section_tracks[0].debug_string, "sectiontrack:s_61010 n_85AR 838")
        self.assertEqual(section_tracks[0].section_code, "61010")
        self.assertEqual(section_tracks[0].distance_units, 37040)

        self.assertIsInstance(section_tracks[1], AlgorithmSectionTrack)
        self.assertEqual(section_tracks[1].id, 886)
        self.assertEqual(section_tracks[1].code, "2")
        self.assertEqual(section_tracks[1].debug_string, "sectiontrack:s_61010 n_85AR 2")
        self.assertEqual(section_tracks[1].section_code, "61010")
        self.assertEqual(section_tracks[1].distance_units, 37040)

    @mock.patch("requests.Session", side_effect=GetSectionTracksBetweenSessionTestMock)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)
