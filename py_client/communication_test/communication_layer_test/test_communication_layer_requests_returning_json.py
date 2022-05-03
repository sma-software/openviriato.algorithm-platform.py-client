import unittest

import responses

from py_client.communication import communication_layer


class TestCommunicationLayerToReturnJson(unittest.TestCase):

    def setUp(self):
        base_url = "http://viriato.rest.ch/api"
        self.CommunicationLayer = communication_layer.CommunicationLayer(base_url=base_url)

    @responses.activate
    def test_requests_that_return_json(self):
        responses.add(**dict(
            method=responses.GET,
            url='http://viriato.rest.ch/api/get_request_that_returns_json',
            body='{"key" : "Value"}',
            status=200
        ))

        response = self.CommunicationLayer.do_get_request_without_body('get_request_that_returns_json')

        self.assertIsInstance(response, dict)
        self.assertDictEqual(response, dict(key="Value"))

    @responses.activate
    def test_requests_with_body_that_return_json(self):
        responses.add(**dict(
            method=responses.GET,
            url='http://viriato.rest.ch/api/get_request_that_returns_json',
            body='{"key" : "Value"}',
            status=200
        ))

        response = self.CommunicationLayer.do_get_request_with_body('get_request_that_returns_json', {})

        self.assertIsInstance(response, dict)
        self.assertDictEqual(response, dict(key="Value"))

    @responses.activate
    def test_do_post_request_to_return_json(self):
        responses.add(**dict(
            method=responses.POST,
            url='http://viriato.rest.ch/api/post_request_that_returns_json',
            body='{"key" : "Value"}',
            status=200
        ))

        response = self.CommunicationLayer.do_post_request('post_request_that_returns_json')

        self.assertIsInstance(response, dict)
        self.assertDictEqual(response, dict(key="Value"))

    @responses.activate
    def test_do_put_request_to_return_json(self):
        responses.add(**dict(
            method=responses.PUT,
            url='http://viriato.rest.ch/api/put_request_that_returns_json',
            body='{"key" : "Value"}',
            status=200
        ))

        response = self.CommunicationLayer.do_put_request('put_request_that_returns_json')

        self.assertIsInstance(response, dict)
        self.assertDictEqual(response, dict(key="Value"))

    def tearDown(self) -> None:
        self.CommunicationLayer.currentSession.close()
