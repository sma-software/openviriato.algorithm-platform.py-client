import unittest
import os

from jenkins.resolve_code_references_in_markdown import _read_src_md, _translate_source_markdown_to_output_markdown, _persist_md


class TestResolveCodeReferencesInMarkdown(unittest.TestCase):
    def test(self):
        expected_markdown_file_path = "../py_client/jenkins_tests/expected/rerouting_a_train.md"
        target_markdown_file_path = "target/rerouting_a_train.md"

        src_md_file = os.path.abspath("source/rerouting_a_train.src.md").replace("\\", "/")
        py_client_root = ".."
        src_md_file_contents = _read_src_md(src_md_file)
        src_md_file_translated = _translate_source_markdown_to_output_markdown(py_client_root, src_md_file_contents)
        _persist_md(target_markdown_file_path, src_md_file_translated)

        self.assertTrue(os.path.isfile(target_markdown_file_path))
        with open(expected_markdown_file_path) as expected_markdown_file, open(target_markdown_file_path) as target_markdown_file:
            content_expected_markdown_file = expected_markdown_file.readlines()
            content_target_markdown_file = target_markdown_file.readlines()
            self.assertListEqual(content_target_markdown_file, content_expected_markdown_file)

        os.remove(target_markdown_file_path)