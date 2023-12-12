import glob
import re
import shutil
from zipfile import ZipFile
import os
import requests

FILE_VERSION_REGEX = re.compile(r"(\d+\.\d+\.\d+)")  # => 1.2.3


def get_matching_single_filename_from_directory(directory: str, filename_pattern: str) -> str:
    files = glob.glob(filename_pattern, root_dir=directory)
    if len(files) != 1:
        raise FileNotFoundError(f"Could not find exactly one file with pattern {filename_pattern} in the directory {directory}.")

    return files[0]


def get_version_number_from_file_name(filename: str) -> str:
    match = FILE_VERSION_REGEX.search(filename)
    if match:
        return match.group(1)
    else:
        raise Exception(f"The file provided {filename} does not have a version number.")


def download_zip_and_return_file_path(url: str, filename: str, target_directory: str) -> str:
    if not os.path.isdir(target_directory):
        os.mkdir(target_directory)
        print("Created directory for downloaded zip at: ", os.path.abspath(target_directory))

    zip_file_path = os.path.join(target_directory, filename)

    request = requests.get(url, stream=True)
    if not request.ok:
        raise Exception(f"Could not download '{url}. Code {request.status_code}. \nText: \n{request.text}'")

    with open(zip_file_path, "wb") as fd:
        for chunk in request.iter_content(chunk_size=128):
            fd.write(chunk)

    return zip_file_path


def extract_zip_file(path_zip_file: str, target_directory: str) -> str:
    with ZipFile(path_zip_file, "r") as zip_file:
        zip_file.extractall(path=target_directory)

    return target_directory


def copy_file_and_return_file_path(source_path: str, target_directory: str):
    # create output directory if not available
    if not os.path.isdir(target_directory):
        os.mkdir(target_directory)
        print("Created output directory at: ", os.path.abspath(target_directory))

    zip_file_path_local_copy_db = shutil.copy2(source_path, target_directory)
    return zip_file_path_local_copy_db


def is_string_in_file_content(search_string: str, file_path: str) -> bool:
    with open(file_path, "r") as file:
        file_content = file.read()
        return search_string in file_content
