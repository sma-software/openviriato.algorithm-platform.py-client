import argparse
import os
import re

from typing import List, Optional


SOURCE_DIRECTORY = "md_source"
MD_OUTPUT_SUB_DIRECTORY = "dist"
WALKTHROUGHS_ROOT = "walkthroughs"
PY_SOURCE_DIR = "py"
CONFIG_DIR = "config"
IMAGES_DIR = "images"
PY_CLIENT_MODULE_ROOT = "py_client"

PY_CLIENT_ROOT_SYMBOLIC_PATH_TAG = "@py_client_root"
PY_SOURCE_SYMBOLIC_PATH_TAG = "@py_source"
CONFIG_SYMBOLIC_PATH_TAG = "@config"
IMAGES_SYMBOLIC_PATH_TAG = "@images"

OFFSET_FOR_GIT_HUB = 1
README_FILE_NAME = "README.md"


# naming and structure of an import marker
# @reference_name[line_selector] example:
# @twoLinesBeforeTheEndOfTheFunction[1:-2]


class MethodSignature:
    _method_arguments_as_str: str
    _return_type_as_str: str
    _method_name: str
    _line_number_start_in_source_file: int
    _line_number_stop_in_source_file: int

    def __init__(
        self,
        method_name: str,
        method_arguments_as_str: str,
        return_type_as_str: str,
        line_number_start_in_source_file: int,
        line_number_stop_in_source_file: int,
    ):
        self._method_name = method_name
        self._method_arguments_as_str = method_arguments_as_str
        self._return_type_as_str = return_type_as_str
        self._line_number_start_in_source_file = line_number_start_in_source_file
        self._line_number_stop_in_source_file = line_number_stop_in_source_file

    @property
    def method_arguments_as_str(self) -> str:
        return self._method_arguments_as_str

    @property
    def return_type_as_str(self) -> str:
        return self._return_type_as_str

    @property
    def method_name(self) -> str:
        return self._method_name

    @property
    def line_number_start_in_source_file(self) -> int:
        return self._line_number_start_in_source_file

    @property
    def line_number_stop_in_source_file(self) -> int:
        return self._line_number_stop_in_source_file


class CodeBlockWithLinesNumberInSourceCode:
    _code_block: List[str]
    _start_line_number_in_source_code: int

    def __init__(self, code_block: List[str], start_line_number_in_source_code: int):
        self._code_block = code_block
        self._start_line_number_in_source_code = start_line_number_in_source_code

    @property
    def code_block(self) -> List[str]:
        return self._code_block

    @property
    def start_line_number_in_source_code(self) -> int:
        return self._start_line_number_in_source_code

    @property
    def end_line_number_in_source_code(self) -> int:
        return self._start_line_number_in_source_code + len(self._code_block) - 1


class PythonSourceCodeImportMarker:
    _reference_name: str
    _position_line_number: int
    _line_selector_start: Optional[int]
    _line_selector_end: Optional[int]

    def __init__(self, reference_name: str, position_line_number: int, line_selector_start: Optional[int], line_selector_end: Optional[int]):
        self._reference_name = reference_name
        self._position_line_number = position_line_number
        self._line_selector_start = line_selector_start
        self._line_selector_end = line_selector_end

    @property
    def reference_name(self) -> str:
        return self._reference_name

    @property
    def position_line_number(self) -> int:
        return self._position_line_number

    @property
    def line_selector_start(self) -> Optional[int]:
        return self._line_selector_start

    @property
    def line_selector_end(self) -> Optional[int]:
        return self._line_selector_end


class ReferenceToImportMarkerInMarkDownSourceCode:
    _source_code_absolute_path: str
    _reference_name: str

    def __init__(self, reference_name: str, source_code_absolute_path: str):
        self._reference_name = reference_name
        self._source_code_absolute_path = source_code_absolute_path

    @property
    def reference_name(self) -> str:
        return self._reference_name

    @property
    def relative_path_to_source_file(self) -> str:
        return self._source_code_absolute_path


def _is_non_empty_line(line: str) -> bool:
    return line != "\n"


def _number_of_leading_spaces(code_line: str) -> int:
    return len(code_line) - len(code_line.lstrip())


def _make_relative_url_back_from_relative_path(path: str) -> str:
    path_as_posix = os.path.normpath(path)
    relative_url_syntax = str(path_as_posix).replace("\\", "/")
    split = relative_url_syntax.split("/")
    return "/".join([".." for s in split])


def _remove_indentation_not_desired_for_output_markdown(code_block: List[str]) -> List[str]:
    # we have to remove the indentation that is necessary in the source code file, but superfluous in the output
    non_empty_lines_of_code_block = [code_line for code_line in code_block if _is_non_empty_line(code_line)]
    spaces_to_remove = min([_number_of_leading_spaces(code_line) for code_line in non_empty_lines_of_code_block])
    code_line_with_removed_indentation = [code_line[spaces_to_remove:] for code_line in code_block]
    return code_line_with_removed_indentation


def _find_import_marker(all_lines: List[str], marker: str) -> PythonSourceCodeImportMarker:
    regex_for_import_marker_in_source_code = "@{}\[(.*):(.*)\]".format(marker)
    for line_number, line in enumerate(all_lines):
        retrieved_marker_with_line_numbers = re.search(regex_for_import_marker_in_source_code, line)
        if retrieved_marker_with_line_numbers is not None:
            line_selector_start_as_string = retrieved_marker_with_line_numbers.group(1)
            line_selector_end_as_string = retrieved_marker_with_line_numbers.group(2)

            line_selector_start = None if line_selector_start_as_string == "" else int(line_selector_start_as_string)
            line_selector_end = None if line_selector_end_as_string == "" else int(line_selector_end_as_string)
            return PythonSourceCodeImportMarker(marker, line_number, line_selector_start, line_selector_end)
    raise Exception("desired import marker cannot be found in source code file. name of marker searched for: {}".format(marker))


def _extract_method_signature(py_client_repo_root: str, path_to_source_file_from_py_client_root: str, method_name: str) -> MethodSignature:
    source_code_file = _resolve_path_from_py_client_repo_root(py_client_repo_root, path_to_source_file_from_py_client_root)

    if not os.path.exists(source_code_file):
        raise FileNotFoundError("Cannot find file referenced from src.md: {}".format(source_code_file))

    regex_for_signature_in_source_code = "def {}\((.*?)\) -> (.*?):".format(method_name)
    with open(source_code_file) as file:
        file_content = file.read()
        retrieved_signature_match_object = re.search(regex_for_signature_in_source_code, file_content, flags=re.DOTALL)
        if retrieved_signature_match_object is None:
            raise Exception("desired method signature '{}' cannot be found in source code file '{}'.".format(method_name, source_code_file))

        retrieved_signature = retrieved_signature_match_object.group(0)
        parameters = retrieved_signature_match_object.group(1)
        return_type = retrieved_signature_match_object.group(2)

        file_contents_before_signature = file_content.split(retrieved_signature)[0]
        line_number_start = file_contents_before_signature.count("\n")
        line_number_stop = line_number_start + retrieved_signature.count("\n")
        return MethodSignature(method_name, parameters, return_type, line_number_start, line_number_stop)


def _calculate_offset_to_first_line_number_of_code_block(lines_starting_from_marker: List[str]) -> int:
    if _contains_any_keyword(lines_starting_from_marker[0]):
        return _find_first_line_with_colon(lines_starting_from_marker)
    else:
        return 1


def _find_first_line_with_colon(lines: List[str]) -> int:
    end_of_statement_requiring_indentation_character = ":\n"
    for index, line in enumerate(lines):
        if line.find(end_of_statement_requiring_indentation_character) > -1:
            return index + 1
    raise Exception("Colon not found as expected.")


def _contains_any_keyword(line: str) -> bool:
    keywords_requiring_indentation = ["if ", "else ", "elif ", "for ", "while ", "def ", "class ", "try ", "except ", "finally ", "with "]
    for keyword in keywords_requiring_indentation:
        if line.find(keyword) > -1:
            return True
    return False


def _extract_code_block(all_lines: List[str], line_number_code_block_start: int) -> List[str]:
    # For functions the first line is the signature, for classes it's the declaration
    # the indentation starts at the subsequent line in these cases
    # this is also working for other types of code blocks with at least two line
    # might not working in general cases

    number_of_first_line_in_code_block = line_number_code_block_start + _calculate_offset_to_first_line_number_of_code_block(
        all_lines[line_number_code_block_start:]
    )
    number_of_lines_within_code_block = _calculate_number_of_lines_within_code_block(all_lines[number_of_first_line_in_code_block:])

    line_number_code_block_end = number_of_first_line_in_code_block + number_of_lines_within_code_block
    return all_lines[line_number_code_block_start:line_number_code_block_end]


def _calculate_number_of_lines_within_code_block(lines_starting_from_code_block: List[str]):
    number_of_white_spaces_of_indentation = _number_of_leading_spaces(lines_starting_from_code_block[0])

    for line_number, line in enumerate(lines_starting_from_code_block):
        number_of_leading_spaces_of_the_line = _number_of_leading_spaces(line)

        # In the case of a class, an empty line with no indentation may separate two methods, but doesn't represent the end of the class
        next_code_block_detected = _is_non_empty_line(line) and number_of_leading_spaces_of_the_line < number_of_white_spaces_of_indentation
        if next_code_block_detected:
            return line_number

    return len(lines_starting_from_code_block)


def _import_code_block_from_source_file(
    py_client_repo_root: str, reference: ReferenceToImportMarkerInMarkDownSourceCode
) -> CodeBlockWithLinesNumberInSourceCode:
    path_to_source_code_file_with_code_block = _resolve_path_from_py_client_repo_root(py_client_repo_root, reference.relative_path_to_source_file)
    if not os.path.exists(path_to_source_code_file_with_code_block):
        raise FileNotFoundError("Cannot find file referenced from src.md: {}".format(path_to_source_code_file_with_code_block))
    with open(path_to_source_code_file_with_code_block) as file:
        all_lines = file.readlines()

        import_marker = _find_import_marker(all_lines, reference.reference_name)

        offset_code_block_start_after_line_marker = 1
        first_line_of_the_code_block = import_marker.position_line_number + offset_code_block_start_after_line_marker
        code_block = _extract_code_block(all_lines, first_line_of_the_code_block)

        code_block_content = code_block[import_marker.line_selector_start : import_marker.line_selector_end]
        return CodeBlockWithLinesNumberInSourceCode(code_block_content, first_line_of_the_code_block)


def _read_source_code_and_format_code_for_output_markdown(
    py_client_repo_root, reference_to_import_marker: ReferenceToImportMarkerInMarkDownSourceCode
) -> CodeBlockWithLinesNumberInSourceCode:
    raw_code_block_with_line_numbers = _import_code_block_from_source_file(py_client_repo_root, reference_to_import_marker)
    unindented_code_block = _remove_indentation_not_desired_for_output_markdown(raw_code_block_with_line_numbers.code_block)
    expanded_code_listing_for_output = ["```python\n"] + unindented_code_block + ["\n```\n"]
    return CodeBlockWithLinesNumberInSourceCode(expanded_code_listing_for_output, raw_code_block_with_line_numbers.start_line_number_in_source_code)


def _generate_caption(formatted_code_block_with_source_code_lines: CodeBlockWithLinesNumberInSourceCode, source_code_file_name: str, caption_text: str) -> str:
    source_code_from_py_client = _resolve_path_from_py_client_repo_root(_path_back_from_md_output_to_py_client_repo_root(), source_code_file_name)
    link_to_source_code = "{}#L{}-L{}".format(
        source_code_from_py_client,
        formatted_code_block_with_source_code_lines.start_line_number_in_source_code + OFFSET_FOR_GIT_HUB,
        formatted_code_block_with_source_code_lines.end_line_number_in_source_code - OFFSET_FOR_GIT_HUB,
    )

    source_code_basename = os.path.basename(source_code_file_name)
    return "Code listing: _{}_. ([Lines: {} - {} from file: _{}_]({})).\n".format(
        caption_text,
        formatted_code_block_with_source_code_lines.start_line_number_in_source_code + OFFSET_FOR_GIT_HUB,
        formatted_code_block_with_source_code_lines.end_line_number_in_source_code - OFFSET_FOR_GIT_HUB,
        source_code_basename,
        link_to_source_code,
    )


def _translate_source_markdown_with_code_block(py_client_repo_root: str, line: str) -> List[str]:
    pattern_for_import_marker = "@Import"
    pattern_for_source_code_file_name = "\((.*),"
    pattern_for_reference_name_in_target_file = "(.*),"
    pattern_for_caption = "(.*)\)"

    regex_for_import_marker_in_markdown_source_code = (
        pattern_for_import_marker + pattern_for_source_code_file_name + pattern_for_reference_name_in_target_file + pattern_for_caption
    )

    import_marker_parsed_from_source_code_line = re.search(regex_for_import_marker_in_markdown_source_code, line)

    if import_marker_parsed_from_source_code_line is None:
        return [line]

    source_code_file_name = import_marker_parsed_from_source_code_line.group(1)
    reference_name = import_marker_parsed_from_source_code_line.group(2)
    caption_text = import_marker_parsed_from_source_code_line.group(3)
    reference_to_import_marker = ReferenceToImportMarkerInMarkDownSourceCode(reference_name, source_code_file_name)

    formatted_code_block_with_source_code_lines = _read_source_code_and_format_code_for_output_markdown(py_client_repo_root, reference_to_import_marker)
    output_markdown_file_content = formatted_code_block_with_source_code_lines.code_block

    generated_caption = _generate_caption(formatted_code_block_with_source_code_lines, source_code_file_name, caption_text)
    output_markdown_file_content.append(generated_caption)
    return output_markdown_file_content


def _path_back_from_md_output_to_py_client_repo_root() -> str:
    current_path = "/".join([WALKTHROUGHS_ROOT, "walkthrough_name_placeholder", MD_OUTPUT_SUB_DIRECTORY])
    path_back_to_py_client_module_root = _make_relative_url_back_from_relative_path(current_path)
    return path_back_to_py_client_module_root


def _translate_symbolic_path_to_relative_path(line: str) -> str:
    current_state_of_line_to_process = line

    if PY_CLIENT_ROOT_SYMBOLIC_PATH_TAG in current_state_of_line_to_process:
        path_back_from_md_output_to_py_client_module_root = "/".join((_path_back_from_md_output_to_py_client_repo_root(), PY_CLIENT_MODULE_ROOT))
        current_state_of_line_to_process = current_state_of_line_to_process.replace(
            PY_CLIENT_ROOT_SYMBOLIC_PATH_TAG, path_back_from_md_output_to_py_client_module_root
        )

    path_back_to_current_walkthrough_sub_dir = _make_relative_url_back_from_relative_path(MD_OUTPUT_SUB_DIRECTORY)

    if PY_SOURCE_SYMBOLIC_PATH_TAG in current_state_of_line_to_process:
        sub_path_replacing_symbolic_tag = "/".join((path_back_to_current_walkthrough_sub_dir, PY_SOURCE_DIR))
        current_state_of_line_to_process = current_state_of_line_to_process.replace(PY_SOURCE_SYMBOLIC_PATH_TAG, sub_path_replacing_symbolic_tag)
    if CONFIG_SYMBOLIC_PATH_TAG in current_state_of_line_to_process:
        sub_path_replacing_symbolic_tag = "/".join((path_back_to_current_walkthrough_sub_dir, CONFIG_DIR))
        current_state_of_line_to_process = current_state_of_line_to_process.replace(CONFIG_SYMBOLIC_PATH_TAG, sub_path_replacing_symbolic_tag)
    if IMAGES_SYMBOLIC_PATH_TAG in current_state_of_line_to_process:
        sub_path_replacing_symbolic_tag = "/".join((path_back_to_current_walkthrough_sub_dir, IMAGES_DIR))
        current_state_of_line_to_process = current_state_of_line_to_process.replace(IMAGES_SYMBOLIC_PATH_TAG, sub_path_replacing_symbolic_tag)
    return current_state_of_line_to_process


def _translate_source_markdown_with_method_signature(py_client_repo_root: str, line: str) -> str:
    suffix_long_signature = "Long"
    suffix_short_signature = "Short"
    pattern_for_import_marker = "@ImportInline"
    pattern_for_source_code_file_name = "\((.*?),"
    pattern_for_target_signature = "(.*?)\)"

    regex_for_import_signature_in_markdown_source_code = (
        pattern_for_import_marker
        + "({}|{})".format(suffix_short_signature, suffix_long_signature)
        + pattern_for_source_code_file_name
        + pattern_for_target_signature
    )

    import_signature_parsed_from_source_code_line = re.findall(regex_for_import_signature_in_markdown_source_code, line)
    for signature_parsed in import_signature_parsed_from_source_code_line:
        tag_suffix = signature_parsed[0]
        source_code_file_name = signature_parsed[1]
        target_signature = signature_parsed[2]

        retrieved_method_signature = _extract_method_signature(py_client_repo_root, source_code_file_name, target_signature)
        source_code_from_md_source = _resolve_path_from_py_client_repo_root(_path_back_from_md_output_to_py_client_repo_root(), source_code_file_name)
        if tag_suffix == "Long":
            method_signature = "{}({}) -> {}".format(
                retrieved_method_signature.method_name, retrieved_method_signature.method_arguments_as_str, retrieved_method_signature.return_type_as_str
            )
        else:
            method_signature = "{}(...)".format(retrieved_method_signature.method_name)

        line = line.replace(
            "{}{}({},{})".format(pattern_for_import_marker, tag_suffix, source_code_file_name, target_signature),
            "[{}]({}#L{}-L{})".format(
                method_signature,
                source_code_from_md_source,
                retrieved_method_signature.line_number_start_in_source_file + OFFSET_FOR_GIT_HUB,
                retrieved_method_signature.line_number_stop_in_source_file + OFFSET_FOR_GIT_HUB,
            ),
        )
    return line


def _translate_source_markdown_to_output_markdown(py_client_repo_root: str, file_contents: List[str]) -> List[str]:
    output_markdown_file_content = []

    for line in file_contents:
        translated_lines = _translate_source_markdown_with_code_block(py_client_repo_root, line)
        if translated_lines == [line]:
            translated_lines = _translate_source_markdown_with_method_signature(py_client_repo_root, line)
            translated_lines = [_translate_symbolic_path_to_relative_path(translated_lines)]
        output_markdown_file_content += translated_lines

    return output_markdown_file_content


def _persist_md(filename: str, lines_to_write: List[str]) -> None:
    if not os.path.exists(os.path.dirname(filename)):
        os.makedirs(os.path.dirname(filename))

    with open(filename, "w") as textfile:
        for line_to_write in lines_to_write:
            textfile.write(line_to_write)


def _create_walkthrough_readme(walkthrough_dist_file_path: str):
    walkthrough_file_name = os.path.basename(walkthrough_dist_file_path)
    walkthrough_dist_directory = os.path.dirname(walkthrough_dist_file_path)

    path_to_walkthrough_md_from_walkthrough_subdirectory = "/".join((MD_OUTPUT_SUB_DIRECTORY, walkthrough_file_name))
    walkthrough_sub_directory = walkthrough_dist_directory.replace(MD_OUTPUT_SUB_DIRECTORY, "")

    readme_file_in_walkthrough_subdirectory = "/".join((walkthrough_sub_directory, README_FILE_NAME))

    with open(readme_file_in_walkthrough_subdirectory, "w") as readme_file:
        readme_file.write("[Link to the walkthrough]({})".format(path_to_walkthrough_md_from_walkthrough_subdirectory))


def _read_src_md(absolute_path_src_md: str) -> List[str]:
    with open(absolute_path_src_md) as file:
        return file.readlines()


def _resolve_path_from_py_client_repo_root(py_client_repo_root: str, path_to_resolve: str) -> str:
    return py_client_repo_root + "/" + path_to_resolve


def _get_all_files_with_absolute_paths_in_directory_recursive(root_to_search_from: str) -> list[str]:
    files = []
    for root, dirs, file_names_in_current_dir in os.walk(root_to_search_from):
        files += [os.path.join(root, file) for file in file_names_in_current_dir]

    file_names_with_slashes_instead_of_backslashes = [file.replace("\\", "/") for file in files]
    return file_names_with_slashes_instead_of_backslashes


def _list_walkthroughs_to_process(py_client_repo_root: str) -> List[str]:
    walkthroughs_directory = os.path.join(py_client_repo_root, WALKTHROUGHS_ROOT).replace("\\", "/")
    filter_src_md_regex = "(.+)\.src\.md"

    file_names = _get_all_files_with_absolute_paths_in_directory_recursive(walkthroughs_directory)
    src_md_file_names = [file_name for file_name in file_names if re.match(filter_src_md_regex, file_name)]
    return src_md_file_names


def _parse_file_name_from_command_line_arguments() -> tuple[str, str]:
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument("-r", "--py_client_repo_root", required=True)
    argument_parser.add_argument("-o", "--md-output-root", required=True)

    command_line_arguments = vars(argument_parser.parse_args())
    py_client_repo_root: str = command_line_arguments["py_client_repo_root"]
    md_output_root: str = command_line_arguments["md_output_root"]

    return py_client_repo_root, md_output_root


def _run_with_arguments(py_client_repo_root: str, md_output_root: str) -> None:
    src_md_files_to_process = _list_walkthroughs_to_process(py_client_repo_root)
    if len(src_md_files_to_process) == 0:
        raise FileNotFoundError("No walkthrough found in folder '{}' please verify the given path.".format(py_client_repo_root, WALKTHROUGHS_ROOT))

    for src_md_file in src_md_files_to_process:
        src_md_file_contents = _read_src_md(src_md_file)
        src_md_file_translated = _translate_source_markdown_to_output_markdown(py_client_repo_root, src_md_file_contents)

        md_output_file = src_md_file.replace(SOURCE_DIRECTORY, MD_OUTPUT_SUB_DIRECTORY).replace(WALKTHROUGHS_ROOT, md_output_root).replace(".src.md", ".md")
        _persist_md(md_output_file, src_md_file_translated)
        _create_walkthrough_readme(md_output_file)


def main():
    py_client_repo_root, dist_directory = _parse_file_name_from_command_line_arguments()
    _run_with_arguments(py_client_repo_root, dist_directory)


if __name__ == "__main__":
    main()
