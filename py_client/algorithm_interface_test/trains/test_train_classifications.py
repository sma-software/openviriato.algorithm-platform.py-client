import unittest
from unittest import mock

from py_client.aidm import AlgorithmTrainClassification
import py_client.algorithm_interface_test.test_helper.SessionMockFactory as SessionMockFactory
from py_client.algorithm_interface import algorithm_interface_factory
from py_client.algorithm_interface_test.test_helper.SessionMockTestBase import get_api_url, SessionMockTestBase


class TestGetTrainClassifications(unittest.TestCase):
    class GetTrainClassificationsTestMockSession(SessionMockTestBase):
        def get(self, request, params):
            self.__last_body = params
            self.__last_request = request
            json_string = '[{ "Description": "Unknown"},' \
                          '{"Description": "Freight" }, ' \
                          '{ "Description": "Passenger"}]'
            return SessionMockFactory.create_response_mock(json_string, 200)

    @mock.patch('requests.Session', side_effect=GetTrainClassificationsTestMockSession)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = algorithm_interface_factory.create(get_api_url())

    @mock.patch('requests.Session', side_effect=GetTrainClassificationsTestMockSession)
    def test_get_train_classifications_request(self, mocked_get_obj):
        self.interface_to_viriato.get_train_classifications()

        session_obj = self.interface_to_viriato._AlgorithmInterface__communication_layer.currentSession
        self.assertEqual(session_obj._GetTrainClassificationsTestMockSession__last_request,
                         get_api_url() + '/train-classifications')
        self.assertDictEqual(session_obj._GetTrainClassificationsTestMockSession__last_body, {})

    @mock.patch('requests.Session', side_effect=GetTrainClassificationsTestMockSession)
    def test_get_train_classifications_response(self, mocked_get_obj):
        train_classes = self.interface_to_viriato.get_train_classifications()

        self.assertIsInstance(train_classes, list)
        self.assertIsInstance(train_classes[0], AlgorithmTrainClassification)
        self.assertEqual(train_classes[0].description, "Unknown")
        self.assertEqual(train_classes[1].description, "Freight")

    @mock.patch('requests.Session', side_effect=GetTrainClassificationsTestMockSession)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)
