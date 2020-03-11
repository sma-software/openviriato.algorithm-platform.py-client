import unittest

from AIDMClasses import AIDM_classes


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
