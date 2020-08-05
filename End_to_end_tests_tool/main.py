import sys
import os
from End_to_end_tests_tool.runner import tests_runner


def main():
    if len(sys.argv) != 2:
        print("expected syntax: python.exe pyclient_end_to_end_runner ["
              "relative_path_to_end_to_end_configuration_file.json]")
        return
    absolute_root_path = os.path.dirname(sys.argv[0])
    configuration_file_relative_path = sys.argv[1]
    tests_runner.run_end_to_end_tests(absolute_root_path, configuration_file_relative_path)


if __name__ == '__main__':
    main()
