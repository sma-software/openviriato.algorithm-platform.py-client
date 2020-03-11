import unittest

import ConverterLayer.to_AIDM_converter
from AIDM_package import AIDM_classes


class TestAIDMAlgorithmNode(unittest.TestCase):

    def test_algorithm_node_object(self):
        node_id = 15
        code_string = 'someTestNodeID'
        debug_string = 'AAA'
        node_tracks = []

        test_node = AIDM_classes.AlgorithmNode(node_id, code_string, debug_string, node_tracks)

        self.assertEqual(test_node.ID, 15)
        self.assertEqual(test_node.Code, 'someTestNodeID')
        self.assertEqual(test_node.DebugString, 'AAA')
        self.assertEqual(test_node.NodeTracks, [])

    def test_algorithm_node_object_factory(self):
        test_node_json_dict = dict(ID=15, Code='A', DebugString='test123', NodeTracks=[])

        test_node = ConverterLayer.to_AIDM_converter.convert_dict_to_AlgorithmNode(test_node_json_dict)

        self.assertEqual(test_node.ID, 15)
        self.assertEqual(test_node.Code, 'A')
        self.assertEqual(test_node.DebugString, 'test123')
        self.assertEqual(test_node.NodeTracks, [])
