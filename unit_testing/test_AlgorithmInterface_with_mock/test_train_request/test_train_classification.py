from unittest import mock, TestCase

import AlgorithmInterface.AlgorithmInterface
from AlgorithmInterface import AlgorithmInterfaceFactory
from unit_testing.test_AlgorithmInterface_with_mock import SessionMockFactory as APISessionMock
from unit_testing.test_AlgorithmInterface_with_mock.unit_testing_with_mock_helpers import get_api_url, \
    SessionMockTestBase


class TestGetTrainClassification(TestCase):
    class GetTrainClassificationTestMockSession(SessionMockTestBase):
        # to replace session.get:
        def get(self, request, params):
            self.__last_body = params
            self.__last_request = request
            return APISessionMock.create_response_mock('{"Description": "Freight"}', 200)

    interface_to_viriato: AlgorithmInterface.AlgorithmInterface.AlgorithmicPlatformInterface

    @mock.patch('requests.Session', side_effect=GetTrainClassificationTestMockSession)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = AlgorithmInterfaceFactory.create(get_api_url())

    @mock.patch('requests.Session', side_effect=GetTrainClassificationTestMockSession)
    def test_get_train_classification_request(self, mocked_get_obj):
        train_id = 99
        self.interface_to_viriato.get_train_classification(train_id)

        session_obj = self.interface_to_viriato._AlgorithmicPlatformInterface__communication_layer.currentSession

        self.assertEqual(session_obj._GetTrainClassificationTestMockSession__last_request,
                         get_api_url() + '/train-classification/99')
        self.assertDictEqual(session_obj._GetTrainClassificationTestMockSession__last_body, {})

    @mock.patch('requests.Session', side_effect=GetTrainClassificationTestMockSession)
    def test_get_train_classification_response(self, mocked_get_obj):
        train_id = 1

        train_class = self.interface_to_viriato.get_train_classification(train_id)

        self.assertIsInstance(train_class, dict)
        self.assertDictEqual(train_class, {"Description": "Freight"})

    @mock.patch('requests.Session', side_effect=GetTrainClassificationTestMockSession)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)
