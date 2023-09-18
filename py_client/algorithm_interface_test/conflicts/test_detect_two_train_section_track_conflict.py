import unittest
from unittest import mock
from datetime import datetime

from py_client.aidm import AlgorithmTrainPathNodeReference
from py_client.algorithm_interface import algorithm_interface_factory
import py_client.algorithm_interface_test.test_helper.SessionMockFactory as SessionMockFactory
from py_client.algorithm_interface_test.test_helper.SessionMockTestBase import get_api_url, SessionMockTestBase
from py_client.aidm.aidm_conflict import (
    ConflictType,
    ConflictDetectionArguments,
    AlgorithmSectionTrackConflict,
    _AlgorithmTwoTrainsSectionTrackConflict,
    AlgorithmConflictDetectionEventType,
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
                '   "causingTrainPathNode": { \n'
                '       "trainId": 1238, \n'
                '       "trainPathNodeId": 1236 \n'
                "    }, \n"
                '    "causingEventType": "arrival", \n'
                '    "affectedTrainPathNode": { \n'
                '        "trainId": 1226, \n'
                '        "trainPathNodeId": 1225 \n'
                "     }, \n"
                '     "affectedEventType": "previousDeparture" \n'
                "    }, \n"
                "   { \n"
                '       "conflictType": "headwayTime", \n'
                '       "timeWindow": { \n'
                '           "fromTime": "2005-05-01T04:12:00", \n'
                '           "toTime": "2005-05-01T04:13:00" \n'
                "       }, \n"
                '       "sectionTrackId": 659, \n'
                '       "causingTrainPathNode": { \n'
                '           "trainId": 1224, \n'
                '           "trainPathNodeId": 2734 \n'
                "        }, \n"
                '        "causingEventType": "departure", \n'
                '       "affectedTrainPathNode": { \n'
                '           "trainId": 1212, \n'
                '           "trainPathNodeId": 9999 \n'
                "       }, \n"
                '       "affectedEventType": "arrival" \n'
                "   }, \n"
                "   { \n"
                '       "conflictType": "overtaking", \n'
                '       "timeWindow": { \n'
                '           "fromTime": "2005-05-01T05:24:00", \n'
                '           "toTime": "2005-05-01T05:26:00" \n'
                "       }, \n"
                '       "sectionTrackId": 734, \n'
                '       "causingTrainPathNode": { \n'
                '           "trainId": 1227, \n'
                '           "trainPathNodeId": 5124 \n'
                "        }, \n"
                '        "causingEventType": "arrival", \n'
                '       "affectedTrainPathNode": { \n'
                '           "trainId": 1224, \n'
                '           "trainPathNodeId": 9829 \n'
                "       }, \n"
                '       "affectedEventType": "departure" \n'
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
        self.assertEqual(list_of_algorithm_conflicts[0].causing_train_path_node.train_path_node_id, 1236)
        self.assertIsInstance(list_of_algorithm_conflicts[0].causing_event_type, AlgorithmConflictDetectionEventType)
        self.assertEqual(list_of_algorithm_conflicts[0].causing_event_type, AlgorithmConflictDetectionEventType.Arrival)
        affected_train_path_node = list_of_algorithm_conflicts[0].affected_train_path_node
        self.assertIsInstance(affected_train_path_node, AlgorithmTrainPathNodeReference)
        self.assertEqual(affected_train_path_node.train_id, 1226)
        self.assertEqual(affected_train_path_node.train_path_node_id, 1225)
        self.assertIsInstance(list_of_algorithm_conflicts[0].affected_event_type, AlgorithmConflictDetectionEventType)
        self.assertEqual(list_of_algorithm_conflicts[0].affected_event_type, AlgorithmConflictDetectionEventType.PreviousDeparture)

        self.assertIsInstance(list_of_algorithm_conflicts[1], AlgorithmSectionTrackConflict)
        self.assertIsInstance(list_of_algorithm_conflicts[1], AlgorithmTwoTrainsConflict)
        self.assertIsInstance(list_of_algorithm_conflicts[1], _AlgorithmTwoTrainsSectionTrackConflict)
        self.assertEqual(list_of_algorithm_conflicts[1].conflict_type, ConflictType.HeadwayTime)
        self.assertEqual(list_of_algorithm_conflicts[1].section_track_id, 659)
        self.assertIsInstance(list_of_algorithm_conflicts[1].affected_event_type, AlgorithmConflictDetectionEventType)
        self.assertEqual(list_of_algorithm_conflicts[1].affected_event_type, AlgorithmConflictDetectionEventType.Arrival)
        self.assertIsInstance(list_of_algorithm_conflicts[1].causing_event_type, AlgorithmConflictDetectionEventType)
        self.assertEqual(list_of_algorithm_conflicts[1].causing_event_type, AlgorithmConflictDetectionEventType.Departure)

        self.assertIsInstance(list_of_algorithm_conflicts[2], AlgorithmSectionTrackConflict)
        self.assertIsInstance(list_of_algorithm_conflicts[2], AlgorithmTwoTrainsConflict)
        self.assertIsInstance(list_of_algorithm_conflicts[2], _AlgorithmTwoTrainsSectionTrackConflict)
        self.assertEqual(list_of_algorithm_conflicts[2].conflict_type, ConflictType.Overtaking)
        self.assertEqual(list_of_algorithm_conflicts[2].section_track_id, 734)
        self.assertIsInstance(list_of_algorithm_conflicts[2].affected_event_type, AlgorithmConflictDetectionEventType)
        self.assertEqual(list_of_algorithm_conflicts[2].affected_event_type, AlgorithmConflictDetectionEventType.Departure)
        self.assertIsInstance(list_of_algorithm_conflicts[2].causing_event_type, AlgorithmConflictDetectionEventType)
        self.assertEqual(list_of_algorithm_conflicts[2].causing_event_type, AlgorithmConflictDetectionEventType.Arrival)

    @mock.patch("requests.Session", side_effect=DetectConflictsMockSession)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)
