import unittest
import responses
from Communication import CommunicationLayer


class TestCommunicationLayerToReturnNone(unittest.TestCase):

    def setUp(self):
        base_url = "http://viriato.rest.ch/api"
        self.CommunicationLayer = CommunicationLayer.CommunicationLayer(base_url=base_url)

    @responses.activate
    def test_do_get_request_to_return_None(self):
        responses.add(**dict(
            method=responses.GET,
            url='http://viriato.rest.ch/api/get_request_that_returns_nothing',
            body='',
            status=200
        ))

        response = self.CommunicationLayer.do_get_request('get_request_that_returns_nothing')

        self.assertIsNone(response)

    @responses.activate
    def test_do_post_request_to_return_None(self):
        responses.add(**dict(
            method=responses.POST,
            url='http://viriato.rest.ch/api/post_request_that_returns_nothing',
            body='',
            status=200
        ))

        response = self.CommunicationLayer.do_post_request('post_request_that_returns_nothing')

        self.assertIsNone(response)

    @responses.activate
    def test_do_put_request_to_return_None(self):
        responses.add(**dict(
            method=responses.PUT,
            url='http://viriato.rest.ch/api/put_request_that_returns_nothing',
            body='',
            status=200
        ))

        response = self.CommunicationLayer.do_put_request('put_request_that_returns_nothing')

        self.assertIsNone(response)

    def tearDown(self) -> None:
        self.CommunicationLayer.currentSession.close()
