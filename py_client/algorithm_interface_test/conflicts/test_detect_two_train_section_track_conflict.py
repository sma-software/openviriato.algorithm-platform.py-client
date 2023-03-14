import unittest
from unittest import mock
from datetime import datetime

from py_client.algorithm_interface import algorithm_interface_factory
import py_client.algorithm_interface_test.test_helper.SessionMockFactory as SessionMockFactory
from py_client.algorithm_interface_test.test_helper.SessionMockTestBase import get_api_url, SessionMockTestBase
from py_client.aidm.aidm_conflict import (
    ConflictType,
    ConflictDetectionArguments,
    AlgorithmSectionTrackConflict,
    _AlgorithmTwoTrainsSectionTrackConflict,
    AlgorithmTrainPathNodeEventType,
    AlgorithmTwoTrainsConflict,
)
from py_client.aidm.aidm_time_window_classes import TimeWindow


class TestDetectConflicts(unittest.TestCase):
    class DetectConflictsMockSession(SessionMockTestBase):
        def get(self, request, params, json):
            self.__last_body = json
            self.__last_params = params
            self.__last_request = request

            json_string = (
                "["
                "   {"
                '       "conflictType": "crossing", \n'
                '       "timeWindow": { \n'
                '       "fromTime": "2005-05-01T04:04:00", \n'
                '       "toTime": "2005-05-01T04:07:00" \n'
                "   }, \n"
                '   "sectionTrackId": 725, \n'
                '   "precedingTrainId": 1238, \n'
                '   "precedingTrainPathNodeId": 1236, \n'
                '   "preceding_train_path_node_event_type": "arrival", \n'
                '   "succeedingTrainId": 1226, \n'
                '   "succeedingTrainPathNodeId": 1225, \n'
                '   "succeeding_train_path_node_event_type": "previousDeparture" \n'
                "    }, \n"
                "   { \n"
                '       "conflictType": "headwayTime", \n'
                '       "timeWindow": { \n'
                '           "fromTime": "2005-05-01T04:12:00", \n'
                '           "toTime": "2005-05-01T04:13:00" \n'
                "       }, \n"
                '       "sectionTrackId": 659, \n'
                '       "precedingTrainId": 1224, \n'
                '       "precedingTrainPathNodeId": 2734, \n'
                '       "precedingTrainPathNodeEventType": "departure", \n'
                '       "succeedingTrainId": 1212, \n'
                '       "succeedingTrainPathNodeId": 9999, \n'
                '       "succeedingTrainPathNodeEventType": "arrival" \n'
                "   }, \n"
                "   { \n"
                '       "conflictType": "overtaking", \n'
                '       "timeWindow": { \n'
                '           "fromTime": "2005-05-01T05:24:00", \n'
                '           "toTime": "2005-05-01T05:26:00" \n'
                "       }, \n"
                '       "sectionTrackId": 734, \n'
                '       "precedingTrainId": 1227, \n'
                '       "precedingTrainPathNodeId": 5124, \n'
                '       "precedingTrainPathNodeEventType": "arrival", \n'
                '       "succeedingTrainId": 1224, \n'
                '       "succeedingTrainPathNodeId": 9829, \n'
                '       "succeedingTrainPathNodeEventType": "departure" \n'
                "   } \n"
                "]"
            )

            return SessionMockFactory.create_response_mock(json_string, 200)

    @mock.patch("requests.Session", side_effect=DetectConflictsMockSession)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = algorithm_interface_factory.create(get_api_url())

    @mock.patch("requests.Session", side_effect=DetectConflictsMockSession)
    def test_detect_conflicts_mock_session(self, mocked_get_obj):
        train_ids = [1238, 1226]
        arguments = ConflictDetectionArguments(train_ids=train_ids).with_type_filter([ConflictType.Crossing, ConflictType.HeadwayTime, ConflictType.Overtaking])

        self.interface_to_viriato.detect_conflicts(arguments=arguments)

        session_obj = self.interface_to_viriato._AlgorithmInterface__communication_layer.currentSession

        self.assertEqual(session_obj._DetectConflictsMockSession__last_request, get_api_url() + "/services/trains:detect-conflicts")

        self.assertDictEqual(
            session_obj._DetectConflictsMockSession__last_body,
            {
                "trainIds": [1238, 1226],
                "filters": {"location": {"nodeIds": None, "sectionTrackIds": None}, "conflictTypes": ["crossing", "headwayTime", "overtaking"]},
            },
        )
        self.assertDictEqual(session_obj._DetectConflictsMockSession__last_params, {})

    @mock.patch("requests.Session", side_effect=DetectConflictsMockSession)
    def test_detect_conflicts_response(self, mocked_get_obj):
        arguments = ConflictDetectionArguments(train_ids=[1238, 1226])
        list_of_algorithm_conflicts = self.interface_to_viriato.detect_conflicts(arguments=arguments)

        self.assertIsInstance(list_of_algorithm_conflicts, list)

        self.assertIsInstance(list_of_algorithm_conflicts[0], AlgorithmSectionTrackConflict)
        self.assertIsInstance(list_of_algorithm_conflicts[0], _AlgorithmTwoTrainsSectionTrackConflict)
        self.assertIsInstance(list_of_algorithm_conflicts[0].conflict_type, ConflictType)
        self.assertEqual(list_of_algorithm_conflicts[0].conflict_type, ConflictType.Crossing)
        self.assertIsInstance(list_of_algorithm_conflicts[0].time_window, TimeWindow)
        self.assertEqual(list_of_algorithm_conflicts[0].time_window.from_time, datetime(day=1, month=5, year=2005, hour=4, minute=4, second=0))
        self.assertEqual(list_of_algorithm_conflicts[0].time_window.to_time, datetime(day=1, month=5, year=2005, hour=4, minute=7, second=0))
        self.assertEqual(list_of_algorithm_conflicts[0].section_track_id, 725)
        self.assertEqual(list_of_algorithm_conflicts[0].preceding_train_id, 1238)
        self.assertEqual(list_of_algorithm_conflicts[0].preceding_train_path_node_id, 1236)
        self.assertIsInstance(list_of_algorithm_conflicts[0].preceding_train_path_node_event_type, AlgorithmTrainPathNodeEventType)
        self.assertEqual(list_of_algorithm_conflicts[0].preceding_train_path_node_event_type, AlgorithmTrainPathNodeEventType.Arrival)
        self.assertEqual(list_of_algorithm_conflicts[0].succeeding_train_id, 1226)
        self.assertEqual(list_of_algorithm_conflicts[0].succeeding_train_path_node_id, 1225)
        self.assertIsInstance(list_of_algorithm_conflicts[0].succeeding_train_path_node_event_type, AlgorithmTrainPathNodeEventType)
        self.assertEqual(list_of_algorithm_conflicts[0].succeeding_train_path_node_event_type, AlgorithmTrainPathNodeEventType.PreviousDeparture)

        self.assertIsInstance(list_of_algorithm_conflicts[1], AlgorithmSectionTrackConflict)
        self.assertIsInstance(list_of_algorithm_conflicts[1], AlgorithmTwoTrainsConflict)
        self.assertIsInstance(list_of_algorithm_conflicts[1], _AlgorithmTwoTrainsSectionTrackConflict)
        self.assertEqual(list_of_algorithm_conflicts[1].conflict_type, ConflictType.HeadwayTime)
        self.assertEqual(list_of_algorithm_conflicts[1].section_track_id, 659)
        self.assertIsInstance(list_of_algorithm_conflicts[1].succeeding_train_path_node_event_type, AlgorithmTrainPathNodeEventType)
        self.assertEqual(list_of_algorithm_conflicts[1].succeeding_train_path_node_event_type, AlgorithmTrainPathNodeEventType.Arrival)
        self.assertIsInstance(list_of_algorithm_conflicts[1].preceding_train_path_node_event_type, AlgorithmTrainPathNodeEventType)
        self.assertEqual(list_of_algorithm_conflicts[1].preceding_train_path_node_event_type, AlgorithmTrainPathNodeEventType.Departure)

        self.assertIsInstance(list_of_algorithm_conflicts[2], AlgorithmSectionTrackConflict)
        self.assertIsInstance(list_of_algorithm_conflicts[2], AlgorithmTwoTrainsConflict)
        self.assertIsInstance(list_of_algorithm_conflicts[2], _AlgorithmTwoTrainsSectionTrackConflict)
        self.assertEqual(list_of_algorithm_conflicts[2].conflict_type, ConflictType.Overtaking)
        self.assertEqual(list_of_algorithm_conflicts[2].section_track_id, 734)
        self.assertIsInstance(list_of_algorithm_conflicts[2].succeeding_train_path_node_event_type, AlgorithmTrainPathNodeEventType)
        self.assertEqual(list_of_algorithm_conflicts[2].succeeding_train_path_node_event_type, AlgorithmTrainPathNodeEventType.Departure)
        self.assertIsInstance(list_of_algorithm_conflicts[2].preceding_train_path_node_event_type, AlgorithmTrainPathNodeEventType)
        self.assertEqual(list_of_algorithm_conflicts[2].preceding_train_path_node_event_type, AlgorithmTrainPathNodeEventType.Arrival)

    @mock.patch("requests.Session", side_effect=DetectConflictsMockSession)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)
