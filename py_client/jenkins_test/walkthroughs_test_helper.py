import re
import os
from typing import List, Dict


class WalkthroughTestHelper:
    @classmethod
    def _get_text_from_content(cls, filename: str) -> List[str]:
        with open(filename) as file:
            return file.readlines()

    @classmethod
    def _extract_urls_from_line(cls, line: str) -> List[str]:
        link_url_regex = "\((.*?)\)"
        link_text_regex = "\[(.*?)\]"

        regular_expression_link_in_markdown = link_text_regex + link_url_regex
        markdown_links = re.findall(regular_expression_link_in_markdown, line)
        link_urls_with_anchors = [markdown_link[1] for markdown_link in markdown_links]
        link_urls = [link_urls_with_anchor.split("#")[0] for link_urls_with_anchor in link_urls_with_anchors if link_urls_with_anchor.split("#")[0] != ""]
        return link_urls

    @classmethod
    def get_py_client_repo_root(cls) -> str:
        # set up correct path to py_client_root depending if we start test explicitly
        # or if we are started from unittest suite
        if os.getcwd().endswith("py_client\\jenkins_test"):
            path_to_py_client_repo_root = "../.."
        else:
            path_to_py_client_repo_root = "."
        return path_to_py_client_repo_root

    @classmethod
    def _compute_dictionary_of_link_url_by_line_number(cls, src_md_file_contents: List[str]) -> Dict[str, int]:
        dictionary_of_link_by_line_number = dict()
        for line_number, line in enumerate(src_md_file_contents):
            link_urls_found = cls._extract_urls_from_line(line)
            for link_url in link_urls_found:
                dictionary_of_link_by_line_number[link_url] = line_number
        return dictionary_of_link_by_line_number
