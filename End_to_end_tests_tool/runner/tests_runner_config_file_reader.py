import json
import os
from End_to_end_tests_tool.runner.tests_runner_config import TestsRunnerConfig


def read_headless_runner_config_from_config_file(
        absolute_path_to_viriato: str,
        config_file_on_relative_path: str
) -> TestsRunnerConfig:

    config_file_path = os.path.join(absolute_path_to_viriato, config_file_on_relative_path)

    with open(config_file_path, encoding='utf-8-sig') as input_file:
        json_config = json.loads(input_file.read())
        return TestsRunnerConfig(
            data_root_path_relative=json_config['dataRootPathRelative'],
            config_file_on_relative_path=json_config['relativeConfigFilePath'],
            absolute_path_to_viriato=json_config['absolutePathToViriato'],
            algorithm_interface_port_nr=json_config['port'],
            absolute_path_to_test_db=json_config['databasePath'],
            headless_executable=json_config['headlessExecutable'],
            connection_attempts_number=json_config["retryAttempts"],
            connection_retry_wait_seconds=json_config["retryWaitingTime"]
        )
