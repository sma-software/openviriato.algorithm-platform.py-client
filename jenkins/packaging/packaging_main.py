import sys
import os


def add_project_root_directory_to_python_path(project_root_directory):
    # python requires the root directory on its path variables to discover the modules/packages in the project
    sys.path.append(os.path.abspath(project_root_directory))


def main():
    if len(sys.argv) != 5:
        print(
            'Expected arguments: '
            '[py_client_version_number] '
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


    setup_tools_arguments = SetupToolsArguments(
        py_client_version_number=sys.argv[1],
        release_package_requirements_on_relative_path=sys.argv[2],
        project_root_directory=sys.argv[3],
        output_directory=sys.argv[4])

    PackagingManager().make_package(setup_tools_arguments)


if __name__ == '__main__':
    main()
