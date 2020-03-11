import unittest
from unittest import mock

import AlgorithmInterface.AlgorithmInterface
from AIDMClasses import AIDM_classes
from AlgorithmInterface import AlgorithmInterfaceFactory
from unit_testing.test_AlgorithmInterface_with_mock import SessionMockFactory as SessionMockFactory
from unit_testing.test_AlgorithmInterface_with_mock.unit_testing_with_mock_helpers import get_api_url, \
    SessionMockTestBase


class TestGetSectionTrack(unittest.TestCase):
    class GetSectionTrackSessionTestMock(SessionMockTestBase):
        # to replace session.get:
        def __init__(self):
            super().__init__()

        def get(self, request: str, params: dict):
            self.__last_body = params
            self.__last_request = request

            json_string = ('{\n'
                           '                "ID": 1082,\n'
                           '                "Code": "900",\n'
                           '                "SectionCode": "70015",\n'
                           '                "Weight": 10000,\n'
                           '                "DebugString": "GetSectionTrackSessionTestMock"\n'
                           '            }')

            return SessionMockFactory.create_response_mock(json_string, 200)

    interface_to_viriato: AlgorithmInterface.AlgorithmInterface.AlgorithmicPlatformInterface

    @mock.patch('requests.Session', side_effect=GetSectionTrackSessionTestMock)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = AlgorithmInterfaceFactory.create(get_api_url())

    # split in two tests --> one for request and one for return
    @mock.patch('requests.Session', side_effect=GetSectionTrackSessionTestMock)
    def test_get_section_track_request(self, mocked_get_obj):
        node_id = 1082
        self.interface_to_viriato.get_section_track(node_id)

        session_obj = self.interface_to_viriato._AlgorithmicPlatformInterface__communication_layer.currentSession

        self.assertEqual(session_obj._GetSectionTrackSessionTestMock__last_request,
                         get_api_url() + '/section-tracks/1082')
        self.assertEqual(session_obj._GetSectionTrackSessionTestMock__last_body, {})

    @mock.patch('requests.Session', side_effect=GetSectionTrackSessionTestMock)
    def test_get_section_track_return(self, mocked_get_obj):
        node_id = 1082
        test_section_track = self.interface_to_viriato.get_section_track(node_id)

        self.assertIsInstance(test_section_track, AIDM_classes.AlgorithmSectionTrack)

        self.assertEqual(test_section_track.ID, 1082)
        self.assertEqual(test_section_track.DebugString, 'GetSectionTrackSessionTestMock')
        self.assertEqual(test_section_track.SectionCode, '70015')
        self.assertEqual(test_section_track.Weight, 10000)

    @mock.patch('requests.Session', side_effect=GetSectionTrackSessionTestMock)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)
