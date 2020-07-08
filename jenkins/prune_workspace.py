import os
import sys
import shutil
import stat


def make_deletable(path_to_workspace: str, output_directory: str):
    for root, directories, files in os.walk(path_to_workspace):
        for file_or_directory_name in directories + files:
            if output_directory not in file_or_directory_name:
                absolute_path = os.path.join(root, file_or_directory_name)
                os.chmod(absolute_path, stat.S_IRWXU)


def delete_everything_in_workspace_except_output(path_to_workspace: str, output_directory: str):
    top_level_files_and_directories = os.listdir(path_to_workspace)
    for file_or_dir in top_level_files_and_directories:
        absolute_path = os.path.join(path_to_workspace, file_or_dir)
        if output_directory not in absolute_path:
            if os.path.isdir(absolute_path):
                shutil.rmtree(absolute_path)
            else:
                os.remove(absolute_path)


def main():
    if len(sys.argv) != 3:
        print('Expected arguments: [path_to_workspace] [output_directory]', file=sys.stderr)
        sys.exit(1)

    path_to_workspace = sys.argv[1]
    output_directory = sys.argv[2]
    if "/" in output_directory:
        print('Output directory has to be direct descendant of workspace')
        return sys.exit(1)

    make_deletable(path_to_workspace, output_directory)
    delete_everything_in_workspace_except_output(path_to_workspace, output_directory)


if __name__ == '__main__':
    main()
