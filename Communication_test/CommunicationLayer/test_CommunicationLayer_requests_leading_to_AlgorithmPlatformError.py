import unittest
import responses
from Communication import CommunicationLayer, ResponseProcessing


class TestCommunicationLayerToRaiseAlgorithmPlatformError(unittest.TestCase):

    def setUp(self):
        base_url = "http://viriato.rest.ch/api"
        self.CommunicationLayer = CommunicationLayer.CommunicationLayer(base_url=base_url)

    @responses.activate
    def test_do_get_request_to_raise_AlgorithmPlatformError(self):
        responses.add(**dict(
            method=responses.GET,
            url='http://viriato.rest.ch/api/get_request_to_raise_AlgorithmPlatformError',
            body='{"statusCode": "400", "message": "test_to_raise_AlgorithmPlatformError"}',
            status=400
        ))

        with self.assertRaises(ResponseProcessing.AlgorithmPlatformError) as algorithm_platform_error:
            self.CommunicationLayer.do_get_request('get_request_to_raise_AlgorithmPlatformError')

        self.assertIsInstance(algorithm_platform_error.exception, ResponseProcessing.AlgorithmPlatformError)
        self.assertEqual(algorithm_platform_error.exception.message, "test_to_raise_AlgorithmPlatformError")

    @responses.activate
    def test_do_post_request_to_raise_AlgorithmPlatformError(self):
        responses.add(**dict(
            method=responses.POST,
            url='http://viriato.rest.ch/api/post_request_to_raise_AlgorithmPlatformError',
            body='{"statusCode": "400", "message": "test_to_raise_AlgorithmPlatformError"}',
            status=400
        ))

        with self.assertRaises(ResponseProcessing.AlgorithmPlatformError) as algorithm_platform_error:
            self.CommunicationLayer.do_post_request('post_request_to_raise_AlgorithmPlatformError')

        self.assertIsInstance(algorithm_platform_error.exception, ResponseProcessing.AlgorithmPlatformError)
        self.assertEqual(algorithm_platform_error.exception.message, "test_to_raise_AlgorithmPlatformError")

    @responses.activate
    def test_do_put_request_to_raise_AlgorithmPlatformError(self):
        responses.add(**dict(
            method=responses.PUT,
            url='http://viriato.rest.ch/api/put_request_to_raise_AlgorithmPlatformError',
            body='{"statusCode": "400", "message": "test_to_raise_AlgorithmPlatformError"}',
            status=400
        ))

        with self.assertRaises(ResponseProcessing.AlgorithmPlatformError) as algorithm_platform_error:
            self.CommunicationLayer.do_put_request('put_request_to_raise_AlgorithmPlatformError')

        self.assertIsInstance(algorithm_platform_error.exception, ResponseProcessing.AlgorithmPlatformError)
        self.assertEqual(algorithm_platform_error.exception.message, "test_to_raise_AlgorithmPlatformError")

    def tearDown(self) -> None:
        self.CommunicationLayer.currentSession.close()
