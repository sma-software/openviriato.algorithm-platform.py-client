import unittest
from unittest import mock

from py_client.algorithm_interface.algorithm_interface import AlgorithmInterface
from py_client.algorithm_interface import algorithm_interface_factory
import py_client.algorithm_interface_test.test_helper.SessionMockFactory as SessionMockFactory
from py_client.algorithm_interface_test.test_helper.SessionMockTestBase import get_api_url, SessionMockTestBase
from py_client.aidm import AlgorithmConflict, ConflictType
from py_client.aidm.aidm_time_window_classes import TimeWindow

class TestDetectConflicts(unittest.TestCase):
    class DetectConflictsMockSession(SessionMockTestBase):
        def get(self, request, params):
            self.__last_body = params
            self.__last_request = request

            json_string = ( "["
                            "   {"
                            "       \"sectionTrackId\": 921, \n"
                            "       \"conflictType\": \"crossing\", \n"
                            "       \"timeWindow\": { \n"
                            "           \"FromTime\": \"2003-08-04T12:17:36\", \n"
                            "           \"ToTime\": \"2003-08-04T12:18:24\" \n"
                            "       }, \n"
                            "       \"involvedTrainIds\": [ \n"
                            "           6745, \n"
                            "           6750 \n"
                            "       ] \n"
                            "   } \n"
                            "]"
                            )

            return SessionMockFactory.create_response_mock(json_string, 200)

    interface_to_viriato: AlgorithmInterface

    @mock.patch('requests.Session', side_effect=DetectConflictsMockSession)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = algorithm_interface_factory.create(get_api_url())

    @mock.patch('requests.Session', side_effect=DetectConflictsMockSession)
    def test_detect_conflicts_mock_session(self, mocked_get_obj):
        train_ids = [6745, 6750]
        self.interface_to_viriato.detect_conflicts(train_ids = train_ids)

        session_obj = self.interface_to_viriato._AlgorithmInterface__communication_layer.currentSession

        self.assertEqual(session_obj._DetectConflictsMockSession__last_request,
                         get_api_url() + "/services/trains:detect-conflicts?trainIds={}".format(','.join([str(train_id) for train_id in train_ids])))

        self.assertDictEqual(session_obj._DetectConflictsMockSession__last_body,
                             dict())

    @mock.patch('requests.Session', side_effect=DetectConflictsMockSession)
    def test_detect_conflicts_response(self, mocked_get_obj):
        train_ids = [6745, 6750]
        list_of_algorithm_conflicts = self.interface_to_viriato.detect_conflicts(train_ids = train_ids)

        self.assertIsInstance(
            list_of_algorithm_conflicts,
            list)
        self.assertIsInstance(
            list_of_algorithm_conflicts[0],
            AlgorithmConflict)

        self.assertIsInstance(
            list_of_algorithm_conflicts[0].conflict_type,
            ConflictType)

        self.assertEqual(
            list_of_algorithm_conflicts[0].conflict_type,
            ConflictType.Crossing)

        self.assertIsInstance(
            list_of_algorithm_conflicts[0].involved_train_ids,
            list)

        self.assertEqual(
            list_of_algorithm_conflicts[0].involved_train_ids[0],
            6745)

        self.assertEqual(
            list_of_algorithm_conflicts[0].involved_train_ids[1],
            6750)

        self.assertIsInstance(
            list_of_algorithm_conflicts[0].time_window,
            TimeWindow)

        self.assertIsInstance(
            list_of_algorithm_conflicts[0].section_track_id,
            int)

        self.assertEqual(
            list_of_algorithm_conflicts[0].section_track_id,
            921)

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

    interface_to_viriato: AlgorithmInterface

    @mock.patch('requests.Session', side_effect=DetectConflictsEmptyMockSession)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = algorithm_interface_factory.create(get_api_url())

    @mock.patch('requests.Session', side_effect=DetectConflictsEmptyMockSession)
    def test_detect_conflicts_empty(self, mocked_get_obj):
        train_ids = [6745, 6750]
        list_of_algorithm_conflicts = self.interface_to_viriato.detect_conflicts(train_ids=train_ids)

        self.assertIsInstance(
            list_of_algorithm_conflicts,
            list)

        self.assertEqual(len(list_of_algorithm_conflicts), 0)

    @mock.patch('requests.Session', side_effect=DetectConflictsEmptyMockSession)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)