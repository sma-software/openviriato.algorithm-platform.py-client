import unittest
from unittest import mock

import py_client.aidm.aidm_algorithm_classes
import py_client.algorithm_interface_test.test_helper.SessionMockFactory as SessionMockFactory
from py_client import algorithm_interface
from py_client.aidm import aidm_train_path_node_classes
from py_client.algorithm_interface import algorithm_interface_factory
from py_client.algorithm_interface_test.test_helper.SessionMockTestBase import get_api_url, SessionMockTestBase


class TestPersistTrains(unittest.TestCase):
    class PersistTrainsTestMockSession(SessionMockTestBase):
        def post(self, request, json):
            self.__last_body = json
            self.__last_request = request
            json_string = """
                {
                  "scenarioCode": "ByAlgo01"
                }
                """
            return SessionMockFactory.create_response_mock(json_string, 200)

    @mock.patch("requests.Session", side_effect=PersistTrainsTestMockSession)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = algorithm_interface_factory.create(get_api_url())

    @mock.patch("requests.Session", side_effect=PersistTrainsTestMockSession)
    def test_persist_trains_request(self, mocked_get_obj):
        scenario_description = "my description"
        self.interface_to_viriato.persist_trains(scenario_description=scenario_description)

        session_obj = self.interface_to_viriato._AlgorithmInterface__communication_layer.currentSession
        self.assertEqual(session_obj._PersistTrainsTestMockSession__last_request, get_api_url() + "/services/trains:persist")
        self.assertDictEqual(session_obj._PersistTrainsTestMockSession__last_body, dict(description=scenario_description))

    @mock.patch("requests.Session", side_effect=PersistTrainsTestMockSession)
    def test_clone_train_response(self, mocked_get_obj):
        scenario_description = "my description"
        test_scenario_code = self.interface_to_viriato.persist_trains(scenario_description=scenario_description)

        self.assertIsInstance(test_scenario_code, str)
        self.assertEqual(test_scenario_code, "ByAlgo01")

    @mock.patch("requests.Session", side_effect=PersistTrainsTestMockSession)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)
