import sys
import os


def add_project_root_directory_to_python_path(project_root_directory):
    # python requires the root directory on its path variables to discover the modules/packages in the project
    sys.path.append(os.path.abspath(project_root_directory))


def main():
    if len(sys.argv) != 5:
        print(
            'Expected arguments: '
            '[py_client_build_number] '
            '[name_of_requirements.txt] '
            '[project_root_directory] '
            '[output_directory]',
            file=sys.stderr)
        sys.exit(1)

    # since this script is not located in the project root-directory, which is expected by setup-tools we have to add
    # the project root explicitly
    add_project_root_directory_to_python_path(project_root_directory=sys.argv[3])
    # now that we added the root-project-directory to the python path we finally can import elements from jenkins
    # package
    from jenkins.packaging.setup_tools_runner import PackagingManager
    from jenkins.packaging.setup_tools_arguments import SetupToolsArguments


    packaging_parameters = assemble_packaging_arguments(name_of_requirements, py_client_build_number, output_directory)
    PackagingManager.create_and_start_packaging_manager(packaging_parameters, project_root_directory)


if __name__ == '__main__':
    main()
