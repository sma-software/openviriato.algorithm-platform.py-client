from unittest import mock, TestCase

import AIDMClasses
import AlgorithmInterface.AlgorithmInterface
from AlgorithmInterface import AlgorithmInterfaceFactory
from AlgorithmInterface_test.test_helper import SessionMockFactory as APISessionMock
from AlgorithmInterface_test.test_helper.SessionMockTestBase import get_api_url, SessionMockTestBase


class TestGetTrainClassification(TestCase):
    class GetTrainClassificationTestMockSession(SessionMockTestBase):
        def get(self, request, params):
            self.__last_body = params
            self.__last_request = request
            return APISessionMock.create_response_mock('{"Description": "Freight"}', 200)

    interface_to_viriato: AlgorithmInterface.AlgorithmInterface.AlgorithmInterface

    @mock.patch('requests.Session', side_effect=GetTrainClassificationTestMockSession)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = AlgorithmInterfaceFactory.create(get_api_url())

    @mock.patch('requests.Session', side_effect=GetTrainClassificationTestMockSession)
    def test_get_train_classification_request(self, mocked_get_obj):
        train_id = 99
        self.interface_to_viriato.get_train_classification(train_id)

        session_obj = self.interface_to_viriato._AlgorithmInterface__communication_layer.currentSession

        self.assertEqual(session_obj._GetTrainClassificationTestMockSession__last_request,
                         get_api_url() + '/train-classification/99')
        self.assertDictEqual(session_obj._GetTrainClassificationTestMockSession__last_body, {})

    @mock.patch('requests.Session', side_effect=GetTrainClassificationTestMockSession)
    def test_get_train_classification_response(self, mocked_get_obj):
        train_id = 1

        train_class = self.interface_to_viriato.get_train_classification(train_id)

        self.assertIsInstance(train_class, AIDMClasses.TrainClassification)
        self.assertEqual(train_class.Description, "Freight")

    @mock.patch('requests.Session', side_effect=GetTrainClassificationTestMockSession)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)
