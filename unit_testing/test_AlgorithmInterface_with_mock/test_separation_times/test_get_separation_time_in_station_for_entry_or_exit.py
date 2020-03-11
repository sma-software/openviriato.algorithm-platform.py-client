import datetime
import unittest
from unittest import mock

import unit_testing.test_AlgorithmInterface_with_mock.SessionMockFactory as SessionMockFactory
from AlgorithmInterface import AlgorithmInterfaceFactory
from unit_testing.test_AlgorithmInterface_with_mock.unit_testing_with_mock_helpers import get_api_url, \
    SessionMockTestBase
import AIDMClasses.AIDM_enum_classes


class TestGetSeparationTimeInStationForEntryOrExit(unittest.TestCase):
    class GetSeparationTimeInStationForEntryOrExitTestMockSession(SessionMockTestBase):
        # to replace session.get:
        def get(self, request, params):
            self.__last_body = params
            self.__last_request = request
            json_string = """{ "separationTime": "P0D"}"""

            return SessionMockFactory.create_response_mock(json_string, 200)

    interface_to_viriato: AlgorithmInterfaceFactory.AlgorithmicPlatformInterface

    @mock.patch('requests.Session', side_effect=GetSeparationTimeInStationForEntryOrExitTestMockSession)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = AlgorithmInterfaceFactory.create(get_api_url())

    @mock.patch('requests.Session', side_effect=GetSeparationTimeInStationForEntryOrExitTestMockSession)
    def test_get_separation_time_in_station_for_entry_or_exit_request(self, mocked_get_obj):
        preceding_train_path_node_id = 80
        preceding_node_track_id = 1
        preceding_station_entry_or_exit = AIDMClasses.AIDM_enum_classes.StationEntryOrExit['exit']
        succeeding_train_path_node_id = 324
        succeeding_node_track_id = 500
        succeeding_station_entry_or_exit = AIDMClasses.AIDM_enum_classes.StationEntryOrExit['entry']

        self.interface_to_viriato.get_separation_time_in_station_for_entry_or_exit(preceding_train_path_node_id,
                                                                                   preceding_node_track_id,
                                                                                   preceding_station_entry_or_exit,
                                                                                   succeeding_train_path_node_id,
                                                                                   succeeding_node_track_id,
                                                                                   succeeding_station_entry_or_exit)

        session_obj = self.interface_to_viriato._AlgorithmicPlatformInterface__communication_layer.currentSession
        self.assertEqual(session_obj._GetSeparationTimeInStationForEntryOrExitTestMockSession__last_request,
                         get_api_url() + '/station-separation-time/80/1/exit/324/500/entry')
        self.assertDictEqual(session_obj._GetSeparationTimeInStationForEntryOrExitTestMockSession__last_body, {})

    @mock.patch('requests.Session', side_effect=GetSeparationTimeInStationForEntryOrExitTestMockSession)
    def test_get_separation_time_in_station_for_entry_or_exit_response(self, mocked_get_obj):
        preceding_train_path_node_id = 999
        preceding_node_track_id = 1
        preceding_station_entry_or_exit = AIDMClasses.AIDM_enum_classes.StationEntryOrExit['exit']
        succeeding_train_path_node_id = 324
        succeeding_node_track_id = 500
        succeeding_station_entry_or_exit = AIDMClasses.AIDM_enum_classes.StationEntryOrExit['entry']

        separation_time = self.interface_to_viriato.get_separation_time_in_station_for_entry_or_exit(
            preceding_train_path_node_id, preceding_node_track_id, preceding_station_entry_or_exit,
            succeeding_train_path_node_id, succeeding_node_track_id, succeeding_station_entry_or_exit)

        self.assertIsInstance(separation_time, datetime.timedelta)
        self.assertEqual(separation_time, datetime.timedelta(seconds=0))

    @mock.patch('requests.Session', side_effect=GetSeparationTimeInStationForEntryOrExitTestMockSession)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)
