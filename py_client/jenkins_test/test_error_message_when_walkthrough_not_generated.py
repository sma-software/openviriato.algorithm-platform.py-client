import os.path
import shutil
import unittest
from typing import List

from jenkins.resolve_code_references_in_markdown import _run_with_arguments


class TestErrorMessageWhenWalkthroughNotGenerated(unittest.TestCase):
    output_md_files_to_test: List[str]

    def test_error_message_displayed_correctly(self):
        py_client_repo_root = "broken repo root"
        md_output_root = ""

        with self.assertRaises(FileNotFoundError) as raised_exception:
            _run_with_arguments(py_client_repo_root, md_output_root)
        self.assertEqual(str(raised_exception.exception), "No walkthrough found in folder 'broken repo root' please verify the given path.")

    def test_no_error_message_displayed(self):
        py_client_repo_root = TestErrorMessageWhenWalkthroughNotGenerated._get_py_walkthrough_repo()
        md_output_root = "md_output_root"

        _run_with_arguments(py_client_repo_root, md_output_root)
        created_folder = os.path.join(py_client_repo_root, md_output_root)
        self.assertTrue(os.path.exists(created_folder))

        shutil.rmtree(created_folder)

    @classmethod
    def _get_py_walkthrough_repo(cls):
        # set up correct path to walkthroughs depending if we start test explicitly
        # or if we are started from unittest suite
        if os.getcwd().endswith("py_client\\jenkins_test"):
            path_to_walkthroughs_repo = "../../"
        else:
            path_to_walkthroughs_repo = "."
        return path_to_walkthroughs_repo
