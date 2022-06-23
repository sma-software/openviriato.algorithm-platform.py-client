import unittest
import os
from typing import List
import shutil

import jenkins.resolve_code_references_in_markdown as resolve_code_references_in_markdown
from jenkins.resolve_code_references_in_markdown import SOURCE_DIRECTORY, MD_OUTPUT_DIRECTORY, WALKTHROUGHS_ROOT


REGENERATE_DIRECTORY = "jenkins_tests/temp"
PY_CLIENT_ROOT = ".."


class TestGeneratedMdCorrespondToRegeneratedMd(unittest.TestCase):
    src_md_files_to_process: List[str]

    def setUp(self):
        os.makedirs("../" + REGENERATE_DIRECTORY)
        self.src_md_files_to_process = resolve_code_references_in_markdown._list_walkthroughs_to_process(PY_CLIENT_ROOT)

    def tearDown(self):
        shutil.rmtree("../" + REGENERATE_DIRECTORY)

    def testGeneratedMdCorrespondToRegeneratedMd(self):
        resolve_code_references_in_markdown._run_with_arguments(PY_CLIENT_ROOT, REGENERATE_DIRECTORY)

        for source_md_file_to_test in self.src_md_files_to_process:
            expected_md_file = TestGeneratedMdCorrespondToRegeneratedMd._retrieve_regenerated_md_from_src_md(source_md_file_to_test)
            actual_md_file = TestGeneratedMdCorrespondToRegeneratedMd._retrieve_actual_md_file_name_from_src_md_file_name(source_md_file_to_test)

            expected_lines = TestGeneratedMdCorrespondToRegeneratedMd._get_text_from_content(expected_md_file)
            actual_lines = TestGeneratedMdCorrespondToRegeneratedMd._get_text_from_content(actual_md_file)

            for expected_line, actual_line, current_line_mumber in zip(expected_lines, actual_lines, range(1, len(expected_lines) + 1)):
                self.assertEqual(expected_line, actual_line, "Walkthrough '{}' is not up to date in line {}".format(source_md_file_to_test, current_line_mumber))

    def test_dist_dir_is_sane(self):
        for src_md_file in self.src_md_files_to_process:
            actual_md_file = TestGeneratedMdCorrespondToRegeneratedMd._retrieve_actual_md_file_name_from_src_md_file_name(src_md_file)
            dist_content = os.listdir(os.path.dirname(actual_md_file))
            self.assertEqual(len(dist_content), 1, "Too many files in the directory '{}' only one markdown file should be present.".format(src_md_file))
            self.assertTrue(dist_content[0].endswith('.md'), "The file present in '{}' is not a markdown file".format(src_md_file))

    @staticmethod
    def _get_text_from_content(filename: str) -> List[str]:
        with open(filename) as file:
            return file.readlines()

    @staticmethod
    def _retrieve_actual_md_file_name_from_src_md_file_name(src_md_file):
        return src_md_file.replace('.src.md', '.md').replace(SOURCE_DIRECTORY, MD_OUTPUT_DIRECTORY)

    @staticmethod
    def _retrieve_regenerated_md_from_src_md(src_md_file):
        return src_md_file.replace('.src.md', '.md').replace(SOURCE_DIRECTORY, MD_OUTPUT_DIRECTORY).replace(WALKTHROUGHS_ROOT, REGENERATE_DIRECTORY)



