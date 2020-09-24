import os
import sys


def make_this_file_executable_from_command_line_without_breaking_module_imports(project_root_dir: str):
    allow_python_to_discover_all_modules_by_appending_the_project_root_path(project_root_dir)


def allow_python_to_discover_all_modules_by_appending_the_project_root_path(project_root_dir: str):
    sys.path.append(project_root_dir)


def main():
    if not len(sys.argv) == 6:
        print("expected syntax: python.exe {0} ["
              "relative_path_to_python_project_root_dir, "
              "relative_path_to_end_to_end_configuration_file.json, "
              "relative_path_to_viriato_folder, "
              "relative_path_to_test_data_base.mdb, "
              "log_file_name_with_relative_path.log ]".format(__file__))
        return sys.exit(1)

    absolute_project_root_dir = os.path.abspath(os.path.join(os.getcwd(), sys.argv[1]))
    make_this_file_executable_from_command_line_without_breaking_module_imports(absolute_project_root_dir)
    from End_to_end_tests_tool.runner import tests_runner

    with open(file=sys.argv[5], mode='w') as log_file:
        tests_runner.run_end_to_end_tests(
            configuration_file_path=sys.argv[2],
            relative_path_to_viriato_folder=sys.argv[3],
            relative_path_to_test_data_base=sys.argv[4],
            file_to_store_test_results=log_file)


if __name__ == '__main__':
    main()
