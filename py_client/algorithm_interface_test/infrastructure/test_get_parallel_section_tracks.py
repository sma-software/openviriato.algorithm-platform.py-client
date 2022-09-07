import unittest
from unittest import mock

from py_client.aidm import AlgorithmSectionTrack
from py_client.algorithm_interface import algorithm_interface_factory
from py_client.algorithm_interface_test.test_helper import SessionMockFactory as SessionMockFactory
from py_client.algorithm_interface_test.test_helper.SessionMockTestBase import get_api_url, SessionMockTestBase


class TestGetParallelSectionTracks(unittest.TestCase):
    class GetParallelSectionTracksSessionTestMock(SessionMockTestBase):
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

    @mock.patch("requests.Session", side_effect=GetParallelSectionTracksSessionTestMock)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = algorithm_interface_factory.create(get_api_url())

    # split in two tests --> one for request and one for return
    @mock.patch("requests.Session", side_effect=GetParallelSectionTracksSessionTestMock)
    def test_get_parallel_section_tracks_request(self, mocked_get_obj):
        track_id = 885

        self.interface_to_viriato.get_parallel_section_tracks(track_id)

        session_obj = self.interface_to_viriato._AlgorithmInterface__communication_layer.currentSession
        self.assertEqual(session_obj.last_request, get_api_url() + "/section-tracks")
        self.assertEqual(session_obj.last_body, dict(parallelToSectionTrackId=885))

    @mock.patch("requests.Session", side_effect=GetParallelSectionTracksSessionTestMock)
    def test_get_parallel_section_tracks_return(self, mocked_get_obj):
        track_id = 0

        parallel_section_tracks = self.interface_to_viriato.get_parallel_section_tracks(track_id)

        self.assertIsInstance(parallel_section_tracks, list)
        self.assertEqual(len(parallel_section_tracks), 2)

        self.assertIsInstance(parallel_section_tracks[0], AlgorithmSectionTrack)
        self.assertEqual(parallel_section_tracks[0].id, 885)
        self.assertEqual(parallel_section_tracks[0].code, "838")
        self.assertEqual(parallel_section_tracks[0].section_code, "61010")
        self.assertEqual(parallel_section_tracks[0].distance_units, 37040)
        self.assertEqual(parallel_section_tracks[0].debug_string, "sectiontrack:s_61010 n_85AR 838")

    @mock.patch("requests.Session", side_effect=GetParallelSectionTracksSessionTestMock)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)
