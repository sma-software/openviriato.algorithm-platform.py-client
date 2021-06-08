from datetime import datetime
from unittest import mock, TestCase

from py_client.aidm import TerminationRequest
from py_client.algorithm_interface import algorithm_interface_factory
from py_client.algorithm_interface_test.test_helper import SessionMockFactory as SessionMockFactory
from py_client.algorithm_interface_test.test_helper.SessionMockTestBase import get_api_url, SessionMockTestBase


class TestGetTerminationRequest(TestCase):
    class GetTerminationRequestTestMockNoTimestamp(SessionMockTestBase):
        def get(self, request: str, params: dict):
            self._last_body = params
            self._last_request = request

            json_string = (
                "{\n"
                "  \"terminationRequestedTimestamp\": null\n"
                "}"
            )

            return SessionMockFactory.create_response_mock(json_string, 200)

    class GetTerminationRequestTestMockWithTimestamp(SessionMockTestBase):
        def get(self, request: str, params: dict):
            self._last_body = params
            self._last_request = request

            json_string = (
                "{\n"
                "  \"terminationRequestedTimestamp\": \"2003-05-01T00:10:00\" "
                "}"
            )

            return SessionMockFactory.create_response_mock(json_string, 200)

    @mock.patch('requests.Session', side_effect=GetTerminationRequestTestMockNoTimestamp)
    def test_get_get_termination_request_request(self, mocked_get_obj):
        interface_to_viriato = algorithm_interface_factory.create(get_api_url())
        interface_to_viriato.get_termination_request()

        session_obj = interface_to_viriato._AlgorithmInterface__communication_layer.currentSession

        self.assertEqual(session_obj.last_request, get_api_url() + '/user-inputs/signals')
        self.assertEqual(session_obj.last_body, {"signalType": "Termination"})

    @mock.patch('requests.Session', side_effect=GetTerminationRequestTestMockNoTimestamp)
    def test_get_termination_request_return_none_as_timestamp(self, mocked_get_obj):
        interface_to_viriato = algorithm_interface_factory.create(get_api_url())
        test_request = interface_to_viriato.get_termination_request()

        self.assertIsInstance(test_request, TerminationRequest)
        self.assertIsNone(test_request.termination_requested_timestamp)

    @mock.patch('requests.Session', side_effect=GetTerminationRequestTestMockWithTimestamp)
    def test_get_termination_request_return_datetime_as_timestamp(self, mocked_get_obj):
        interface_to_viriato = algorithm_interface_factory.create(get_api_url())
        test_request = interface_to_viriato.get_termination_request()

        self.assertIsInstance(test_request, TerminationRequest)
        self.assertIsInstance(test_request.termination_requested_timestamp, datetime)
        self.assertEqual(test_request.termination_requested_timestamp, datetime(2003, 5, 1, 0, 10, 0))
