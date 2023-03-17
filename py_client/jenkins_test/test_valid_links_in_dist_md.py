import unittest
import os
import re
from typing import List, Dict

import jenkins.resolve_code_references_in_markdown as resolve_code_references_in_markdown


class TestValidLinksInDistMd(unittest.TestCase):
    output_md_files_to_test: List[str]

    def setUp(self):
        walkthrough_repo = TestValidLinksInDistMd._get_py_walkthrough_repo()
        self.output_md_files_to_test = TestValidLinksInDistMd._list_walkthroughs_to_process(walkthrough_repo)
        if len(self.output_md_files_to_test) == 0:
            raise Exception("did not find any files to test in {}".format(walkthrough_repo))

    def test_paths_exists(self):
        for output_md_file_to_test in self.output_md_files_to_test:
            path, _ = os.path.split(output_md_file_to_test)
            text = TestValidLinksInDistMd._get_text_from_content(output_md_file_to_test)

            dictionary_of_link_url_by_line_number = TestValidLinksInDistMd._compute_dictionary_of_link_url_by_line_number(path, text)
            for link_url, line_number in dictionary_of_link_url_by_line_number.items():
                self._assert_path_exists(text, link_url, line_number, output_md_file_to_test)

    @classmethod
    def _get_py_walkthrough_repo(cls):
        # set up correct path to walkthroughs depending if we start test explicitly
        # or if we are started from unittest suite
        if os.getcwd().endswith("py_client\\jenkins_test"):
            path_to_walkthroughs_repo = "../../" + resolve_code_references_in_markdown.WALKTHROUGHS_ROOT
        else:
            path_to_walkthroughs_repo = resolve_code_references_in_markdown.WALKTHROUGHS_ROOT
        return path_to_walkthroughs_repo

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

    @classmethod
    def _get_text_from_content(cls, filename: str) -> List[str]:
        with open(filename) as file:
            return file.readlines()

    @classmethod
    def _compute_dictionary_of_link_url_by_line_number(cls, path_to_walkthrough: str, text: List[str]) -> Dict[str, int]:
        dictionary_of_link_by_line_number = dict()
        for line_number, line in enumerate(text):
            link_urls_found = cls._extract_urls_from_line(line)
            for link_url in link_urls_found:
                link_to_referenced_file = path_to_walkthrough + "/" + link_url
                dictionary_of_link_by_line_number[link_to_referenced_file] = line_number
        return dictionary_of_link_by_line_number

    @classmethod
    def _extract_urls_from_line(cls, line: str) -> List[str]:
        link_url_regex = "\((.*?)\)"
        link_text_regex = "\[(.*?)\]"

        regular_expression_link_in_markdown = link_text_regex + link_url_regex
        markdown_links = re.findall(regular_expression_link_in_markdown, line)
        link_urls_with_anchors = [markdown_link[1] for markdown_link in markdown_links]
        link_urls = [link_urls_with_anchor.split("#")[0] for link_urls_with_anchor in link_urls_with_anchors]
        return link_urls

    @classmethod
    def _get_text_from_content(cls, filename: str) -> List[str]:
        with open(filename) as file:
            return file.readlines()
