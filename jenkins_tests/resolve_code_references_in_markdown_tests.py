import unittest
import os

from jenkins.resolve_code_references_in_markdown import _write_output_markdown_to_file

class TestResolveCodeReferencesInMarkdown(unittest.TestCase):
    def test(self):
        source_file = "source/rerouting_a_train.src.md"
        expected_markdown_file_path = "expected/rerouting_a_train.md"
        target_directory = "target"
        target_markdown_file_path = "target/rerouting_a_train.md"

        _write_output_markdown_to_file(source_file, target_directory)

        self.assertTrue(os.path.isfile(target_markdown_file_path))
        with open(expected_markdown_file_path) as expected_markdown_file, open(target_markdown_file_path) as target_markdown_file:
            content_expected_markdown_file = expected_markdown_file.readlines()
            content_target_markdown_file = target_markdown_file.readlines()
            self.assertListEqual(content_target_markdown_file, content_expected_markdown_file)

        os.remove(target_markdown_file_path)