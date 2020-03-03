from unittest import mock, TestCase

import AlgorithmInterfaceFactory
import unit_testing_with_mock.unit_testing_helpers
from unit_testing_with_mock import SessionMockFactory as APISessionMock
from unit_testing_with_mock.unit_testing_helpers import get_api_url


class TestGetTrainClassification(TestCase):
    class GetTrainClassificationTestMockSession(unit_testing_with_mock.unit_testing_helpers.SessionMockTestBase):
        # to replace session.get:
        def get(self, request, params):
            self.__last_body = params
            self.__last_request = request
            return APISessionMock.create_response_mock('{"Description": "Freight"}', 200)

    interface_to_viriato: AlgorithmInterfaceFactory.AlgorithmicPlatformInterface

    @mock.patch('requests.Session', side_effect=GetTrainClassificationTestMockSession)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = AlgorithmInterfaceFactory.AlgorithmicPlatformInterface(get_api_url())

    @mock.patch('requests.Session', side_effect=GetTrainClassificationTestMockSession)
    def test_get_train_classification_request(self, mocked_get_obj):
        self.interface_to_viriato.get_train_classification(99)
        session_obj = self.interface_to_viriato._AlgorithmicPlatformInterface__communication_layer.currentSession
        self.assertEqual(session_obj._GetTrainClassificationTestMockSession__last_request,
                         get_api_url() + '/train-classification/99')
        self.assertEqual(session_obj._GetTrainClassificationTestMockSession__last_body, {})

    @mock.patch('requests.Session', side_effect=GetTrainClassificationTestMockSession)
    def test_get_train_classification_response(self, mocked_get_obj):
        train_class = self.interface_to_viriato.get_train_classification(1)
        self.assertIsInstance(train_class, dict)
        self.assertEqual(train_class, {"Description": "Freight"})

    def test_get_train_classification_with_str(self):
        with self.assertRaises(AssertionError):
            self.interface_to_viriato.get_train_classification('b')
            NotImplementedError('accepted str for train number')

    @mock.patch('requests.Session', side_effect=GetTrainClassificationTestMockSession)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)
