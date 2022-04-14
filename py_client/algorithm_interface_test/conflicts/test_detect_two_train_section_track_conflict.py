import datetime
import unittest
from unittest import mock

from py_client.algorithm_interface.algorithm_interface import AlgorithmInterface
from py_client.algorithm_interface import algorithm_interface_factory
import py_client.algorithm_interface_test.test_helper.SessionMockFactory as SessionMockFactory
from py_client.algorithm_interface_test.test_helper.SessionMockTestBase import get_api_url, SessionMockTestBase
from py_client.aidm.aidm_conflict import _AlgorithmConflict, ConflictType, ConflictDetectionArguments, _AlgorithmSectionTrackConflict, _AlgorithmNodeConflict, AlgorithmTwoTrainSectionTrackConflict
from py_client.aidm.aidm_time_window_classes import TimeWindow

class TestDetectConflicts(unittest.TestCase):
    class DetectConflictsMockSession(SessionMockTestBase):
        def get(self, request, params):
            self.__last_body = params
            self.__last_request = request

            json_string = ( "["
                            "   {"
                            "       \"conflictType\": \"crossing\", \n"
                            "       \"timeWindow\": { \n"
                            "       \"fromTime\": \"2005-05-01T04:04:00\", \n"
                            "       \"toTime\": \"2005-05-01T04:07:00\" \n"
                            "   }, \n"
                            "   \"sectionTrackId\": 725, \n"
                            "   \"precedingTrainId\": 1238, \n"
                            "   \"precedingTrainPathNodeId\": 1236, \n"
                            "   \"succeedingTrainId\": 1226, \n"
                            "   \"succeedingTrainPathNodeId\": 1225 \n"
                            "    } \n"
                            "]"
                            )

            return SessionMockFactory.create_response_mock(json_string, 200)

    @mock.patch('requests.Session', side_effect=DetectConflictsMockSession)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = algorithm_interface_factory.create(get_api_url())

    @mock.patch('requests.Session', side_effect=DetectConflictsMockSession)
    def test_detect_conflicts_mock_session(self, mocked_get_obj):
        train_ids = [1238, 1226]
        arguments = ConflictDetectionArguments(train_ids = train_ids)

        self.interface_to_viriato.detect_conflicts(arguments = arguments)

        session_obj = self.interface_to_viriato._AlgorithmInterface__communication_layer.currentSession

        self.assertEqual(session_obj._DetectConflictsMockSession__last_request,
                         get_api_url() + "/services/trains:detect-conflicts")

        self.assertDictEqual(session_obj._DetectConflictsMockSession__last_body, {'trainIds': [1238, 1226]})

    @mock.patch('requests.Session', side_effect=DetectConflictsMockSession)
    def test_detect_conflicts_response(self, mocked_get_obj):
        arguments = ConflictDetectionArguments(train_ids = [1238, 1226])
        list_of_algorithm_conflicts = self.interface_to_viriato.detect_conflicts(arguments = arguments)

        self.assertIsInstance(
            list_of_algorithm_conflicts,
            list)

        self.assertIsInstance(
            list_of_algorithm_conflicts[0],
            _AlgorithmSectionTrackConflict)

        self.assertIsInstance(
            list_of_algorithm_conflicts[0],
            AlgorithmTwoTrainSectionTrackConflict)

        self.assertIsInstance(
            list_of_algorithm_conflicts[0].conflict_type,
            ConflictType)

        self.assertEqual(
            list_of_algorithm_conflicts[0].conflict_type,
            ConflictType.Crossing)

        self.assertIsInstance(
            list_of_algorithm_conflicts[0].time_window,
            TimeWindow)

        self.assertEqual(
            list_of_algorithm_conflicts[0].time_window.from_time,
            datetime.datetime(day=1, month=5, year=2005, hour=4, minute=4, second=0))

        self.assertEqual(
            list_of_algorithm_conflicts[0].time_window.to_time,
            datetime.datetime(day=1, month=5, year=2005, hour=4, minute=7, second=0))

        self.assertEqual(
            list_of_algorithm_conflicts[0].section_track_id,
            725)

        self.assertEqual(
            list_of_algorithm_conflicts[0].preceding_train_id,
            1238)

        self.assertEqual(
            list_of_algorithm_conflicts[0].preceding_train_path_node_id,
            1236)

        self.assertEqual(
            list_of_algorithm_conflicts[0].succeeding_train_id,
            1226)

        self.assertEqual(
            list_of_algorithm_conflicts[0].succeeding_train_path_node_id,
            1225)
        
    @mock.patch('requests.Session', side_effect=DetectConflictsMockSession)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)


class TestDetectConflictsEmpty(unittest.TestCase):
    class DetectConflictsEmptyMockSession(SessionMockTestBase):
        def get(self, request, params):
            self.__last_body = params
            self.__last_request = request

            json_string = "[]"

            return SessionMockFactory.create_response_mock(json_string, 200)

    @mock.patch('requests.Session', side_effect=DetectConflictsEmptyMockSession)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = algorithm_interface_factory.create(get_api_url())

    @mock.patch('requests.Session', side_effect=DetectConflictsEmptyMockSession)
    def test_detect_conflicts_empty(self, mocked_get_obj):
        arguments = ConflictDetectionArguments(train_ids = [1238, 1226])

        list_of_algorithm_conflicts = self.interface_to_viriato.detect_conflicts(arguments = arguments)

        self.assertIsInstance(
            list_of_algorithm_conflicts,
            list)

        self.assertEqual(len(list_of_algorithm_conflicts), 0)

    @mock.patch('requests.Session', side_effect=DetectConflictsEmptyMockSession)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)

class TestDetectConflictsWithNonMandatoryFilters(unittest.TestCase):
    class DetectConflictsWithNonMandatoryFiltersMockSession(SessionMockTestBase):
        def get(self, request, params):
            self.__last_body = params
            self.__last_request = request

            json_string = "[]"

            return SessionMockFactory.create_response_mock(json_string, 200)

    @mock.patch('requests.Session', side_effect=DetectConflictsWithNonMandatoryFiltersMockSession)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = algorithm_interface_factory.create(get_api_url())

    @mock.patch('requests.Session', side_effect=DetectConflictsWithNonMandatoryFiltersMockSession)
    def test_detect_conflicts_with_non_mandatory_filters_session(self, mocked_get_obj):
        train_ids = [6745, 6750]
        train_id = 1230
        time_window = TimeWindow(datetime.datetime(year=2022, month=1, day=23, hour=23, minute=45), datetime.datetime(year=2022, month=1, day=24, hour=0, minute=15))
        filter_node_ids = [4578, 2397]
        filter_section_track_ids = [529, 735]
        conflict_types = [ConflictType.Crossing]
        arguments = ConflictDetectionArguments(train_ids=train_ids )\
            .with_type_filter(conflict_types)\
            .with_location_filter(filter_node_ids,filter_section_track_ids)\
            .with_train_filter(train_id)\
            .with_time_filter(time_window)

        self.interface_to_viriato.detect_conflicts(arguments=arguments)

        session_obj = self.interface_to_viriato._AlgorithmInterface__communication_layer.currentSession

        self.assertEqual(session_obj._DetectConflictsWithNonMandatoryFiltersMockSession__last_request,
                         get_api_url() + "/services/trains:detect-conflicts")

        self.assertDictEqual(session_obj._DetectConflictsWithNonMandatoryFiltersMockSession__last_body,
                             {'nodeIds':[4578, 2397],
                              'sectionTrackIds': [529, 735],
                              'trainIds': [6745, 6750],
                              'trainId': 1230,
                              'timeWindow': {'fromTime': '2022-01-23T23:45:00',
                                             'toTime': '2022-01-24T00:15:00'},
                              'types': ['crossing']})

    @mock.patch('requests.Session', side_effect=DetectConflictsWithNonMandatoryFiltersMockSession)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)