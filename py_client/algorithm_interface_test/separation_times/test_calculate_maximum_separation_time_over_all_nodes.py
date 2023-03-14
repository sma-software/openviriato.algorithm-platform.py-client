from datetime import timedelta
import unittest
from unittest import mock

import py_client.algorithm_interface_test.test_helper.SessionMockFactory as SessionMockFactory
from py_client.algorithm_interface import algorithm_interface_factory
from py_client.algorithm_interface_test.test_helper.SessionMockTestBase import get_api_url, SessionMockTestBase


class TestCalculateMaximumSeparationTimeOverAllNodes(unittest.TestCase):
    class CalculateMaximumSeparationTimeTestMockSession(SessionMockTestBase):
        def get(self, request, params):
            self.__last_body = params
            self.__last_request = request
            json_string = """{ "separationTime": "PT2M10S"}"""

            return SessionMockFactory.create_response_mock(json_string, 200)

    @mock.patch("requests.Session", side_effect=CalculateMaximumSeparationTimeTestMockSession)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = algorithm_interface_factory.create(get_api_url())

    @mock.patch("requests.Session", side_effect=CalculateMaximumSeparationTimeTestMockSession)
    def test_calculate_maximum_separation_time_request(self, mocked_get_obj):
        self.interface_to_viriato.calculate_maximum_separation_time()

        session_obj = self.interface_to_viriato._AlgorithmInterface__communication_layer.currentSession
        self.assertEqual(session_obj._CalculateMaximumSeparationTimeTestMockSession__last_request, get_api_url() + "/nodes/separation-times:calculate-maximum")

        self.assertDictEqual(session_obj._CalculateMaximumSeparationTimeTestMockSession__last_body, dict())

    @mock.patch("requests.Session", side_effect=CalculateMaximumSeparationTimeTestMockSession)
    def test_calculate_maximum_separation_time_response(self, mocked_get_obj):
        maximum_headway_time = self.interface_to_viriato.calculate_maximum_separation_time()

        self.assertIsInstance(maximum_headway_time, timedelta)
        self.assertEqual(maximum_headway_time, timedelta(minutes=2, seconds=10))

    @mock.patch("requests.Session", side_effect=CalculateMaximumSeparationTimeTestMockSession)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)
