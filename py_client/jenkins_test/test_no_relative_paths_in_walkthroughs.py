import unittest
from typing import List

import jenkins.resolve_code_references_in_markdown as resolve_code_references_in_markdown
from py_client.jenkins_test.walkthroughs_test_helper import WalkthroughTestHelper


class TestNoRelativePathsInWalkthroughs(unittest.TestCase):
    source_md_files_to_test: List[str]

    def setUp(self):
        py_client_repo_root = WalkthroughTestHelper.get_py_client_repo_root()
        self.source_md_files_to_test = resolve_code_references_in_markdown._list_walkthroughs_to_process(py_client_repo_root)
        if len(self.source_md_files_to_test) == 0:
            raise Exception(
                "did not find any files to test in {}".format("/".join((py_client_repo_root, resolve_code_references_in_markdown.WALKTHROUGHS_ROOT)))
            )

    def test_links_are_not_relative(self):
        for source_md_file_to_test in self.source_md_files_to_test:
            file_contents = WalkthroughTestHelper._get_file_contents(source_md_file_to_test)

            dictionary_of_link_url_by_line_number = WalkthroughTestHelper._compute_link_url_by_line_number_dict(file_contents)
            for link_url, line_number in dictionary_of_link_url_by_line_number.items():
                self._assert_path_is_not_relative(file_contents, link_url, line_number, source_md_file_to_test)

    def _assert_path_is_not_relative(self, text: List[str], link_url_from_source_md: str, line_number: int, output_md_files_to_test: str) -> None:
        fail_message = "link_url '{}' referenced in file {} (relative from script) should use a tag. Line {}: '{}'".format(
            link_url_from_source_md, output_md_files_to_test, line_number + 1, text[line_number]
        )
        self.assertTrue(link_url_from_source_md.startswith("@"), fail_message)
