import unittest
from unittest import mock
import datetime

from py_client.algorithm_interface import algorithm_interface_factory
import py_client.algorithm_interface_test.test_helper.SessionMockFactory as SessionMockFactory
from py_client.algorithm_interface_test.test_helper.SessionMockTestBase import get_api_url, SessionMockTestBase
from py_client.aidm.aidm_conflict import ConflictDetectionArguments, ConflictType, _AlgorithmTwoTrainsSectionTrackConflict, AlgorithmConflict, AlgorithmMultipleTrainsConflict
from py_client.aidm.aidm_time_window_classes import TimeWindow

from py_client.communication.response_processing import AlgorithmPlatformConversionError


class TestDetectConflicts(unittest.TestCase):
    class DetectConflictsMockSession(SessionMockTestBase):
        def get(self, request, params, json):
            self.__last_params = params
            self.__last_body = json
            self.__last_request = request

            json_string = ( "["
                            "   {"
                            "       \"conflictType\": \"unexisting\", \n"
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
    def test_unknown_conflict(self, mocked_get_obj):
        arguments = ConflictDetectionArguments(train_ids=[6745, 6750])
        with self.assertRaises(AlgorithmPlatformConversionError) as conversion_error:
            self.interface_to_viriato.detect_conflicts(arguments=arguments)

        self.assertEqual(conversion_error.exception.message,"Could not parse Enum unexisting, invalid enum format for expected class Enum <enum 'ConflictType'>")

    @mock.patch('requests.Session', side_effect=DetectConflictsMockSession)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)


class TestDetectConflictsEmpty(unittest.TestCase):
    class DetectConflictsEmptyMockSession(SessionMockTestBase):
        def get(self, request, params, json):
            self.__last_params = params
            self.__last_body = json
            self.__last_request = request

            json_string = "[]"

            return SessionMockFactory.create_response_mock(json_string, 200)

    @mock.patch('requests.Session', side_effect=DetectConflictsEmptyMockSession)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = algorithm_interface_factory.create(get_api_url())

    @mock.patch('requests.Session', side_effect=DetectConflictsEmptyMockSession)
    def test_detect_conflicts_empty(self, mocked_get_obj):
        arguments = ConflictDetectionArguments(train_ids=[1238, 1226])

        list_of_algorithm_conflicts = self.interface_to_viriato.detect_conflicts(arguments=arguments)

        self.assertIsInstance(
            list_of_algorithm_conflicts,
            list)

        self.assertEqual(len(list_of_algorithm_conflicts), 0)

    @mock.patch('requests.Session', side_effect=DetectConflictsEmptyMockSession)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)


class TestDetectConflictsWithNonMandatoryFilters(unittest.TestCase):
    class DetectConflictsWithNonMandatoryFiltersMockSession(SessionMockTestBase):
        def get(self, request, params, json):
            self.__last_params = params
            self.__last_body = json
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
        arguments = ConflictDetectionArguments(train_ids=train_ids)\
            .with_type_filter(conflict_types)\
            .with_location_filter(filter_node_ids, filter_section_track_ids)\
            .with_train_filter(train_id)\
            .with_time_filter(time_window)

        self.interface_to_viriato.detect_conflicts(arguments=arguments)

        session_obj = self.interface_to_viriato._AlgorithmInterface__communication_layer.currentSession

        self.assertEqual(session_obj._DetectConflictsWithNonMandatoryFiltersMockSession__last_request,
                         get_api_url() + "/services/trains:detect-conflicts")

        self.assertDictEqual(session_obj._DetectConflictsWithNonMandatoryFiltersMockSession__last_body,
                             {
                                  'trainIds': [6745, 6750],
                                  'filters': {
                                      'location': {
                                          'nodeIds': [4578, 2397],
                                          'sectionTrackIds': [529, 735],
                                      },
                                      'conflictTypes': ['crossing']
                                  }
                             })

        self.assertDictEqual(session_obj._DetectConflictsWithNonMandatoryFiltersMockSession__last_params,
                             {'trainId': 1230,
                              'fromTime': '2022-01-23T23:45:00',
                              'toTime': '2022-01-24T00:15:00'})

    @mock.patch('requests.Session', side_effect=DetectConflictsWithNonMandatoryFiltersMockSession)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)


class TestConflictDetectionArguments(unittest.TestCase):
    def test_ensure_algorithm_conflict_has_subtyping_as_expected(self):
        # is a hard assumption on which we rely in the json2aidm processors (signature of method )
        self.assertTrue(issubclass(_AlgorithmTwoTrainsSectionTrackConflict, AlgorithmConflict))
        self.assertTrue(issubclass(AlgorithmMultipleTrainsConflict, AlgorithmConflict))
