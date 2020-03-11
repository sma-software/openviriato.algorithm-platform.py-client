import unittest

from AIDMClasses import AIDM_classes


class TestAIDMAlgorithmNodeTrack(unittest.TestCase):

    def test_algorithm_node_track_object_init_and_attributes(self):
        node_id = 15
        code = 'someTestCode'
        debug_string = 'some string'

        test_node = AIDM_classes.AlgorithmNodeTrack(ID=node_id, Code=code, DebugString=debug_string)

        self.assertEqual(test_node.ID, 15)
        self.assertEqual(test_node.Code, 'someTestCode')
        self.assertEqual(test_node.DebugString, 'some string')
