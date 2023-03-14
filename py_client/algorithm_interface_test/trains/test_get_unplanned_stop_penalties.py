from datetime import timedelta
import unittest
from unittest import mock

import py_client.algorithm_interface_test.test_helper.SessionMockFactory as SessionMockFactory
from py_client.aidm import AlgorithmUnplannedStopPenalties
from py_client.algorithm_interface import algorithm_interface_factory
from py_client.algorithm_interface_test.test_helper.SessionMockTestBase import get_api_url, SessionMockTestBase


class TestGetUnplannedStopPenalties(unittest.TestCase):
    class GetUnplannedStopPenaltiesTestMockSession(SessionMockTestBase):
        def get(self, request, params):
            self.__last_body = params
            self.__last_request = request
            json_string = (
                "{ \n" '    "decelerationPenalty": "PT30S", \n' '    "minimumDurationUnplannedStop": "PT1M30S", \n' '    "accelerationPenalty": "PT45S" \n' "}"
            )

            return SessionMockFactory.create_response_mock(json_string, 200)

    @mock.patch("requests.Session", side_effect=GetUnplannedStopPenaltiesTestMockSession)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = algorithm_interface_factory.create(get_api_url())

    @mock.patch("requests.Session", side_effect=GetUnplannedStopPenaltiesTestMockSession)
    def test_get_unplanned_stop_penalties_request(self, mocked_get_obj):
        train_id = 1245
        self.interface_to_viriato.get_unplanned_stop_penalties(train_id)

        session_obj = self.interface_to_viriato._AlgorithmInterface__communication_layer.currentSession
        self.assertEqual(session_obj._GetUnplannedStopPenaltiesTestMockSession__last_request, get_api_url() + "/trains/1245/unplanned-stop-penalties")
        self.assertDictEqual(session_obj._GetUnplannedStopPenaltiesTestMockSession__last_body, dict())

    @mock.patch("requests.Session", side_effect=GetUnplannedStopPenaltiesTestMockSession)
    def test_get_trains_cut_to_time_range_driving_any_node_response(self, mocked_get_obj):
        train_id = 1245
        unplanned_stop_penalties = self.interface_to_viriato.get_unplanned_stop_penalties(train_id)

        self.assertIsInstance(unplanned_stop_penalties, AlgorithmUnplannedStopPenalties)

        self.assertIsInstance(unplanned_stop_penalties.minimum_duration_unplanned_stop, timedelta)
        self.assertEqual(unplanned_stop_penalties.minimum_duration_unplanned_stop, timedelta(minutes=1, seconds=30))

        self.assertIsInstance(unplanned_stop_penalties.deceleration_penalty, timedelta)
        self.assertEqual(unplanned_stop_penalties.deceleration_penalty, timedelta(seconds=30))

        self.assertIsInstance(unplanned_stop_penalties.acceleration_penalty, timedelta)
        self.assertEqual(unplanned_stop_penalties.acceleration_penalty, timedelta(seconds=45))

    @mock.patch("requests.Session", side_effect=GetUnplannedStopPenaltiesTestMockSession)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)
