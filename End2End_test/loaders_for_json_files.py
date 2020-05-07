import json
import os
from End2End_test.headless_runner import ViriatoHeadlessRunnerConfig


def load_test_config_file_port_number(headless_runner_config: ViriatoHeadlessRunnerConfig) -> int:
    config_file_path = os.path.join(headless_runner_config.absolute_path_to_viriato,
                                    headless_runner_config.config_file_with_relative_path)

    with open(config_file_path, encoding='utf-8-sig') as input_file:
        config_json = json.loads(input_file.read())
    return config_json['port']
