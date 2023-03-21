import unittest
import os
import re
from typing import List

import jenkins.resolve_code_references_in_markdown as resolve_code_references_in_markdown
from py_client.jenkins_test.walkthroughs_test_helper import WalkthroughTestHelper


class TestValidLinksInDistMd(unittest.TestCase):
    output_md_files_to_test: List[str]

    def setUp(self):
        py_client_repo_root = WalkthroughTestHelper.get_py_client_repo_root()
        walkthrough_repo = "/".join((py_client_repo_root, resolve_code_references_in_markdown.WALKTHROUGHS_ROOT))
        self.output_md_files_to_test = TestValidLinksInDistMd._list_walkthroughs_to_process(walkthrough_repo)
        if len(self.output_md_files_to_test) == 0:
            raise Exception("did not find any files to test in {}".format(walkthrough_repo))

    def test_paths_exists(self):
        for output_md_file_to_test in self.output_md_files_to_test:
            path, _ = os.path.split(output_md_file_to_test)
            text = WalkthroughTestHelper._get_text_from_content(output_md_file_to_test)

            dictionary_of_link_url_by_line_number = WalkthroughTestHelper._compute_dictionary_of_link_url_by_line_number(path, text)
            for link_url, line_number in dictionary_of_link_url_by_line_number.items():
                self._assert_path_exists(text, link_url, line_number, output_md_file_to_test)

    def _assert_path_exists(self, text: List[str], link_url: str, line_number: int, output_md_files_to_test: str) -> None:
        fail_message = "link_url '{}' (relative from dist) referenced in file {} (relative from script) does not exist. Line {}: '{}'".format(
            link_url, output_md_files_to_test, line_number + 1, text[line_number]
        )
        self.assertTrue(os.path.exists(link_url), fail_message)

    @classmethod
    def _list_walkthroughs_to_process(cls, path_to_walkthroughs: str) -> List[str]:
        filter_md_regex = "(.+)\.md"
        filter_src_md_regex = "(.+)\.src\.md"

        file_names = resolve_code_references_in_markdown._get_all_files_with_absolute_paths_in_directory_recursive(path_to_walkthroughs)
        src_md_file_names = [file_name for file_name in file_names if re.match(filter_src_md_regex, file_name)]
        md_file_names = [file_name for file_name in file_names if re.match(filter_md_regex, file_name)]
        md_file_names_without_src_md_file_names = [md_file_name for md_file_name in md_file_names if md_file_name not in src_md_file_names]
        return md_file_names_without_src_md_file_names
