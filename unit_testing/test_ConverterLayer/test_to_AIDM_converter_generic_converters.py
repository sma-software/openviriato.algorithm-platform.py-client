import unittest

import ConverterLayer.to_AIDM_converter
from AIDMClasses import AIDM_classes


class TestToAIDMConverterGenericConversions(unittest.TestCase):

    def test_convert_dict_to_AIDM(self):
        test_section_as_dict = dict(ID=12, Code='ATest', DebugString='str', Weight=8, SectionCode='TestSection')

        test_section = ConverterLayer.to_AIDM_converter.convert_dict_to_AIDM(AIDM_classes.AlgorithmSectionTrack,
                                                                             test_section_as_dict)

        self.assertIsInstance(test_section, AIDM_classes.AlgorithmSectionTrack)
        self.assertEqual(test_section.ID, 12)
        self.assertEqual(test_section.Code, 'ATest')
        self.assertEqual(test_section.DebugString, 'str')
        self.assertEqual(test_section.Weight, 8)
        self.assertEqual(test_section.SectionCode, 'TestSection')

    def test_convert_list_of_dict_to_list_of_AIDM(self):
        test_section_as_dict = dict(ID=12, Code='ATest', DebugString='str', Weight=8, SectionCode='TestSection')
        test_section_dict_in_list = [test_section_as_dict, test_section_as_dict, test_section_as_dict]

        test_section_list = ConverterLayer.to_AIDM_converter.convert_list_of_dict_to_list_of_AIDM(
            AIDM_classes.AlgorithmSectionTrack, test_section_dict_in_list)

        self.assertIsInstance(test_section_list, list)
        self.assertIsInstance(test_section_list[0], AIDM_classes.AlgorithmSectionTrack)
        self.assertEqual(test_section_list[0].DebugString, 'str')
