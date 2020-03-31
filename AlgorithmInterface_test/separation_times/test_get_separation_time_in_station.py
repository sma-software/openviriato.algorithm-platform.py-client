import datetime
import unittest
from unittest import mock

import AIDMClasses.AIDM_enum_classes
import AlgorithmInterface.AlgorithmInterface
import AlgorithmInterface_test.test_helper.SessionMockFactory as SessionMockFactory
from AlgorithmInterface import AlgorithmInterfaceFactory
from AlgorithmInterface_test.test_helper.unit_testing_with_mock_helpers import \
    get_api_url, \
    SessionMockTestBase


class TestGetSeparationTimeInStation(unittest.TestCase):
    class GetTestGetSeparationTimeInStationTestMockSession(SessionMockTestBase):
        # to replace session.get:
        def get(self, request, params):
            self.__last_body = params
            self.__last_request = request
            json_string = """{ "separationTime": "PT500M"}"""

            return SessionMockFactory.create_response_mock(json_string, 200)

    interface_to_viriato: AlgorithmInterface.AlgorithmInterface.AlgorithmicPlatformInterface

    @mock.patch('requests.Session', side_effect=GetTestGetSeparationTimeInStationTestMockSession)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = AlgorithmInterfaceFactory.create(get_api_url())

    @mock.patch('requests.Session', side_effect=GetTestGetSeparationTimeInStationTestMockSession)
    def test_get_separation_time_in_station_request(self, mocked_get_obj):
        preceding_section_track_id = 999
        preceding_node_track_id = 1
        preceding_stop_status = AIDMClasses.AIDM_enum_classes.StopStatus['operationalStop']
        succeeding_section_track_id = 324
        succeeding_node_track_id = 500
        succeeding_stop_status = AIDMClasses.AIDM_enum_classes.StopStatus['passing']

        self.interface_to_viriato.get_separation_time_in_station(preceding_section_track_id, preceding_node_track_id,
                                                                 preceding_stop_status,
                                                                 succeeding_section_track_id,
                                                                 succeeding_node_track_id, succeeding_stop_status)

        session_obj = self.interface_to_viriato._AlgorithmicPlatformInterface__communication_layer.currentSession
        self.assertEqual(session_obj._GetTestGetSeparationTimeInStationTestMockSession__last_request,
                         get_api_url() + '/station-separation-time/from-section-track/999/to-node-track/1/' +
                         'operationalStop/from-section-track/324/to-node-track/500/passing')
        self.assertDictEqual(session_obj._GetTestGetSeparationTimeInStationTestMockSession__last_body, {})

    @mock.patch('requests.Session', side_effect=GetTestGetSeparationTimeInStationTestMockSession)
    def test_get_separation_time_in_station_response(self, mocked_get_obj):
        preceding_section_track_id = 9999
        preceding_node_track_id = 1
        preceding_stop_status = AIDMClasses.AIDM_enum_classes.StopStatus['operationalStop']
        succeeding_section_track_id = 324
        succeeding_node_track_id = 500
        succeeding_stop_status = AIDMClasses.AIDM_enum_classes.StopStatus['passing']

        separation_time = self.interface_to_viriato.get_separation_time_in_station(preceding_section_track_id,
                                                                                   preceding_node_track_id,
                                                                                   preceding_stop_status,
                                                                                   succeeding_section_track_id,
                                                                                   succeeding_node_track_id,
                                                                                   succeeding_stop_status)

        self.assertIsInstance(separation_time, datetime.timedelta)
        self.assertEqual(separation_time, datetime.timedelta(seconds=30000))

    @mock.patch('requests.Session', side_effect=GetTestGetSeparationTimeInStationTestMockSession)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)
