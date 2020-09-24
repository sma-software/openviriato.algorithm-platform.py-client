import json
import os
from typing import Optional

from End_to_end_tests_tool.runner.tests_runner_config import TestsRunnerConfig


def read_headless_runner_config_from_config_file(
        config_file_on_relative_path: str,
        relative_path_to_viriato: Optional[str],
        relative_path_to_test_database: Optional[str]
) -> TestsRunnerConfig:
    with open(os.path.abspath(config_file_on_relative_path), encoding='utf-8-sig') as input_file:
        json_config = json.loads(input_file.read())

        if relative_path_to_viriato is None:
            relative_path_to_viriato = json_config['absolutePathToViriato']

        if relative_path_to_test_database is None:
            relative_path_to_test_database = json_config['relative_path_to_test_database']

        return TestsRunnerConfig(
            data_root_path_relative=json_config['dataRootPathRelative'],
            config_file_on_relative_path=json_config['relativeConfigFilePath'],
            absolute_path_to_viriato=relative_path_to_viriato,
            algorithm_interface_port_nr=json_config['port'],
            absolute_path_to_test_db=os.path.abspath(relative_path_to_test_database),
            headless_executable=json_config['headlessExecutable'],
            connection_attempts_number=json_config["retryAttempts"],
            connection_retry_wait_seconds=json_config["retryWaitingTime"])
