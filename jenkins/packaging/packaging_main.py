from jenkins.packaging.packaging_manager import PackagingManager
from jenkins.packaging.packaging_arguments import assemble_packaging_arguments
import sys


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

    py_client_build_number = sys.argv[1]
    name_of_requirements = sys.argv[2]
    project_root_directory = sys.argv[3]
    output_directory = sys.argv[4]

    packaging_parameters = assemble_packaging_arguments(name_of_requirements, py_client_build_number, output_directory)
    PackagingManager.create_and_start_packaging_manager(packaging_parameters, project_root_directory)


if __name__ == '__main__':
    main()
