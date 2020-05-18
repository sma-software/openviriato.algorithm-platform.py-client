import unittest

from AlgorithmInterface import AlgorithmInterface, AlgorithmInterfaceFactory


class TestObjectInitialisation(unittest.TestCase):
    def test_initialisation_in_with(self):
        url_str = 'http://localhost:8080'

        with AlgorithmInterface.AlgorithmInterface(url_str) as interface_to_viriato:
            self.assertEqual(interface_to_viriato.base_url, url_str)

    def test_initialisation_from_factory_in_with(self):
        url_str = 'http://localhost:8080'

        with AlgorithmInterfaceFactory.create(url_str) as interface_to_viriato:
            self.assertEqual(interface_to_viriato.base_url, url_str)


if __name__ == '__main__':
    unittest.main()
