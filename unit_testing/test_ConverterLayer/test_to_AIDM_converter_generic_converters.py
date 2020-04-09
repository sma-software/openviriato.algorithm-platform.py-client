import unittest

import AIDMClasses.AIDM_Algorithm_classes
import Conversion.algorithm_platform_json_to_AIDM_converter



class TestToAIDMConverterGenericConversions(unittest.TestCase):

    def test_convert_dict_to_AIDM(self):
        test_section_as_dict = dict(ID=12, Code='ATest', DebugString='str', Weight=8, SectionCode='TestSection')

        test_section = Conversion.algorithm_platform_json_to_AIDM_converter.convert(
            AIDMClasses.AIDM_Algorithm_classes.AlgorithmSectionTrack,
            test_section_as_dict)

        self.assertIsInstance(test_section, AIDMClasses.AIDM_Algorithm_classes.AlgorithmSectionTrack)
        self.assertEqual(test_section.ID, 12)
        self.assertEqual(test_section.Code, 'ATest')
        self.assertEqual(test_section.DebugString, 'str')
        self.assertEqual(test_section.Weight, 8)
        self.assertEqual(test_section.SectionCode, 'TestSection')

    def test_convert_list_of_dict_to_list_of_AIDM(self):
        test_section_as_dict = dict(ID=12, Code='ATest', DebugString='str', Weight=8, SectionCode='TestSection')
        test_section_dict_in_list = [test_section_as_dict, test_section_as_dict, test_section_as_dict]

        test_section_list = Conversion.algorithm_platform_json_to_AIDM_converter.convert_list(
            AIDMClasses.AIDM_Algorithm_classes.AlgorithmSectionTrack, test_section_dict_in_list)

        self.assertIsInstance(test_section_list, list)
        self.assertIsInstance(test_section_list[0], AIDMClasses.AIDM_Algorithm_classes.AlgorithmSectionTrack)
        self.assertEqual(test_section_list[0].DebugString, 'str')
