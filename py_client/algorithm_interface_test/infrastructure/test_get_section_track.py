import unittest
from unittest import mock

from py_client.aidm import AlgorithmSectionTrack
from py_client.algorithm_interface import algorithm_interface_factory
from py_client.algorithm_interface_test.test_helper import SessionMockFactory as SessionMockFactory
from py_client.algorithm_interface_test.test_helper.SessionMockTestBase import get_api_url, SessionMockTestBase


class TestGetSectionTrack(unittest.TestCase):
    class GetSectionTrackSessionTestMock(SessionMockTestBase):
        def __init__(self):
            super().__init__()

        def get(self, request: str, params: dict):
            self._last_body = params
            self._last_request = request

            json_string = ('{\n'
                           ' "id": 1082,\n'
                           ' "code": "900",\n'
                           ' "sectionCode": "70015",\n'
                           ' "distanceUnits": 10000,\n'
                           ' "debugString": "GetSectionTrackSessionTestMock"\n'
                           '}')

            return SessionMockFactory.create_response_mock(json_string, 200)

    @mock.patch('requests.Session', side_effect=GetSectionTrackSessionTestMock)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = algorithm_interface_factory.create(get_api_url())

    @mock.patch('requests.Session', side_effect=GetSectionTrackSessionTestMock)
    def test_get_section_track_request(self, mocked_get_obj):
        section_track_id = 1082
        self.interface_to_viriato.get_section_track(section_track_id)

        session_obj = self.interface_to_viriato._AlgorithmInterface__communication_layer.currentSession

        self.assertEqual(session_obj.last_request, get_api_url() + '/section-tracks/1082')
        self.assertEqual(session_obj.last_body, {})

    @mock.patch('requests.Session', side_effect=GetSectionTrackSessionTestMock)
    def test_get_section_track_return(self, mocked_get_obj):
        section_track_id = 1082
        test_section_track = self.interface_to_viriato.get_section_track(section_track_id)

        self.assertIsInstance(test_section_track, AlgorithmSectionTrack)

        self.assertEqual(test_section_track.id, 1082)
        self.assertEqual(test_section_track.code, '900')
        self.assertEqual(test_section_track.debug_string, 'GetSectionTrackSessionTestMock')
        self.assertEqual(test_section_track.section_code, '70015')
        self.assertEqual(test_section_track.distance_units, 10000)

    @mock.patch('requests.Session', side_effect=GetSectionTrackSessionTestMock)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)
