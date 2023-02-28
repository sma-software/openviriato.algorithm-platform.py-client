import datetime
import unittest
from unittest import mock

import py_client.algorithm_interface_test.test_helper.SessionMockFactory as SessionMockFactory
from py_client.algorithm_interface import algorithm_interface_factory
from py_client.algorithm_interface_test.test_helper.SessionMockTestBase import get_api_url, SessionMockTestBase


class TestCalculateMaximumHeadwayTime(unittest.TestCase):
    class CalculateMaximumHeadwayTimeTestMockSession(SessionMockTestBase):
        def get(self, request, params):
            self.__last_body = params
            self.__last_request = request
            json_string = """{ "headwayTime": "PT10M30S"}"""

            return SessionMockFactory.create_response_mock(json_string, 200)

    @mock.patch("requests.Session", side_effect=CalculateMaximumHeadwayTimeTestMockSession)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = algorithm_interface_factory.create(get_api_url())

    @mock.patch("requests.Session", side_effect=CalculateMaximumHeadwayTimeTestMockSession)
    def test_calculate_maximum_headway_time_request(self, mocked_get_obj):
        self.interface_to_viriato.calculate_maximum_headway_time()

        session_obj = self.interface_to_viriato._AlgorithmInterface__communication_layer.currentSession
        self.assertEqual(
            session_obj._CalculateMaximumHeadwayTimeTestMockSession__last_request, get_api_url() + "/section-tracks/headway-times:calculate-maximum"
        )

        self.assertDictEqual(session_obj._CalculateMaximumHeadwayTimeTestMockSession__last_body, dict())

    @mock.patch("requests.Session", side_effect=CalculateMaximumHeadwayTimeTestMockSession)
    def test_calculate_maximum_headway_time_response(self, mocked_get_obj):
        maximum_headway_time = self.interface_to_viriato.calculate_maximum_headway_time()

        self.assertIsInstance(maximum_headway_time, datetime.timedelta)
        self.assertEqual(maximum_headway_time, datetime.timedelta(minutes=10, seconds=30))

    @mock.patch("requests.Session", side_effect=CalculateMaximumHeadwayTimeTestMockSession)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)
