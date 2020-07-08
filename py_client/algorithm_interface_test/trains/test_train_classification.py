from unittest import mock, TestCase

from py_client.aidm import AlgorithmTrainClassification
from py_client.algorithm_interface import algorithm_interface_factory
from py_client.algorithm_interface_test.test_helper import SessionMockFactory as APISessionMock
from py_client.algorithm_interface_test.test_helper.SessionMockTestBase import get_api_url, SessionMockTestBase


class TestGetTrainClassification(TestCase):
    class GetTrainClassificationTestMockSession(SessionMockTestBase):
        def get(self, request, params):
            self.__last_body = params
            self.__last_request = request
            return APISessionMock.create_response_mock('{"Description": "Freight"}', 200)

    @mock.patch('requests.Session', side_effect=GetTrainClassificationTestMockSession)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = algorithm_interface_factory.create(get_api_url())

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

        self.assertIsInstance(train_class, AlgorithmTrainClassification)
        self.assertEqual(train_class.description, "Freight")

    @mock.patch('requests.Session', side_effect=GetTrainClassificationTestMockSession)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)
