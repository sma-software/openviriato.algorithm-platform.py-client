import unittest
from unittest import mock

import unit_testing.test_AlgorithmInterface_with_mock.SessionMockFactory as SessionMockFactory
from AlgorithmInterface import AlgorithmInterfaceFactory
from unit_testing.test_AlgorithmInterface_with_mock.unit_testing_with_mock_helpers import get_api_url, \
    SessionMockTestBase


class TestGetTrainClassifications(unittest.TestCase):
    class GetTrainClassificationsTestMockSession(SessionMockTestBase):
        # to replace session.get:
        def get(self, request, params):
            self.__last_body = params
            self.__last_request = request
            json_string = '[{ "Description": "Unknown"},{"Description": "Freight" }, { "Description": "Passenger"}]'
            return SessionMockFactory.create_response_mock(json_string, 200)

    interface_to_viriato: AlgorithmInterfaceFactory.AlgorithmicPlatformInterface

    @mock.patch('requests.Session', side_effect=GetTrainClassificationsTestMockSession)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = AlgorithmInterfaceFactory.create(get_api_url())

    @mock.patch('requests.Session', side_effect=GetTrainClassificationsTestMockSession)
    def test_get_train_classifications_request(self, mocked_get_obj):
        self.interface_to_viriato.get_train_classifications()

        session_obj = self.interface_to_viriato._AlgorithmicPlatformInterface__communication_layer.currentSession
        self.assertEqual(session_obj._GetTrainClassificationsTestMockSession__last_request,
                         get_api_url() + '/train-classifications')
        self.assertDictEqual(session_obj._GetTrainClassificationsTestMockSession__last_body, {})

    @mock.patch('requests.Session', side_effect=GetTrainClassificationsTestMockSession)
    def test_get_train_classifications_response(self, mocked_get_obj):
        train_classes = self.interface_to_viriato.get_train_classifications()

        self.assertIsInstance(train_classes, list)
        self.assertDictEqual(train_classes[0], {"Description": "Unknown"})
        self.assertDictEqual(train_classes[1], {"Description": "Freight"})
        self.assertDictEqual(train_classes[2], {"Description": "Passenger"})

    @mock.patch('requests.Session', side_effect=GetTrainClassificationsTestMockSession)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)
