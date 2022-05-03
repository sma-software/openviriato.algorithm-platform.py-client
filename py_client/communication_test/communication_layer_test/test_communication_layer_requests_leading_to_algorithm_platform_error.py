import unittest

import responses

from py_client.communication import communication_layer, response_processing


class TestCommunicationLayerToRaiseAlgorithmPlatformError(unittest.TestCase):

    def setUp(self):
        base_url = "http://viriato.rest.ch/api"
        self.CommunicationLayer = communication_layer.CommunicationLayer(base_url=base_url)

    @responses.activate
    def test_do_get_request_to_raise_AlgorithmPlatformError(self):
        responses.add(**dict(
            method=responses.GET,
            url='http://viriato.rest.ch/api/get_request_to_raise_AlgorithmPlatformError',
            body='{"statusCode": "400", "message": "test_to_raise_AlgorithmPlatformError"}',
            status=400
        ))

        with self.assertRaises(response_processing.AlgorithmPlatformHTTPError) as algorithm_platform_error:
            self.CommunicationLayer.do_get_request_without_body('get_request_to_raise_AlgorithmPlatformError')

        self.assertIsInstance(algorithm_platform_error.exception, response_processing.AlgorithmPlatformHTTPError)
        self.assertEqual(algorithm_platform_error.exception.message, "test_to_raise_AlgorithmPlatformError")

    @responses.activate
    def test_do_get_request_with_body_to_raise_AlgorithmPlatformError(self):
        responses.add(**dict(
            method=responses.GET,
            url='http://viriato.rest.ch/api/get_request_to_raise_AlgorithmPlatformError',
            body='{"statusCode": "400", "message": "test_to_raise_AlgorithmPlatformError"}',
            status=400
        ))

        with self.assertRaises(response_processing.AlgorithmPlatformHTTPError) as algorithm_platform_error:
            self.CommunicationLayer.do_get_request_with_body('get_request_to_raise_AlgorithmPlatformError', {})

        self.assertIsInstance(algorithm_platform_error.exception, response_processing.AlgorithmPlatformHTTPError)
        self.assertEqual(algorithm_platform_error.exception.message, "test_to_raise_AlgorithmPlatformError")

    @responses.activate
    def test_do_post_request_to_raise_AlgorithmPlatformError(self):
        responses.add(**dict(
            method=responses.POST,
            url='http://viriato.rest.ch/api/post_request_to_raise_AlgorithmPlatformError',
            body='{"statusCode": "400", "message": "test_to_raise_AlgorithmPlatformError"}',
            status=400
        ))

        with self.assertRaises(response_processing.AlgorithmPlatformHTTPError) as algorithm_platform_error:
            self.CommunicationLayer.do_post_request('post_request_to_raise_AlgorithmPlatformError')

        self.assertIsInstance(algorithm_platform_error.exception, response_processing.AlgorithmPlatformHTTPError)
        self.assertEqual(algorithm_platform_error.exception.message, "test_to_raise_AlgorithmPlatformError")

    @responses.activate
    def test_do_put_request_to_raise_AlgorithmPlatformError(self):
        responses.add(**dict(
            method=responses.PUT,
            url='http://viriato.rest.ch/api/put_request_to_raise_AlgorithmPlatformError',
            body='{"statusCode": "400", "message": "test_to_raise_AlgorithmPlatformError"}',
            status=400
        ))

        with self.assertRaises(response_processing.AlgorithmPlatformHTTPError) as algorithm_platform_error:
            self.CommunicationLayer.do_put_request('put_request_to_raise_AlgorithmPlatformError')

        self.assertIsInstance(algorithm_platform_error.exception, response_processing.AlgorithmPlatformHTTPError)
        self.assertEqual(algorithm_platform_error.exception.message, "test_to_raise_AlgorithmPlatformError")

    def tearDown(self) -> None:
        self.CommunicationLayer.currentSession.close()
