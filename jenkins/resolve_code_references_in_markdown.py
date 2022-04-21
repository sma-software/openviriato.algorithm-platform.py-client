import argparse
import os
import re

from typing import List, Optional

# naming and structure of an import marker
# @reference_name[line_selector] example:
# @twoLinesBeforeTheEndOfTheFunction[1:-2]

class PythonSourceCodeImportMarker:
    _reference_name: str
    _position_line_number: int
    _line_selector_start: Optional[int]
    _line_selector_end: Optional[int]

    def __init__(self, reference_name: str, position_line_number:int, line_selector_start: Optional[int], line_selector_end: Optional[int]):
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
    def source_code_absolute_path(self) -> str:
        return self._source_code_absolute_path



def _is_non_empty_line(line: str) -> bool:
    return line != '\n'

def _number_of_leading_spaces(code_line: str) -> int:
    return len(code_line) - len(code_line.lstrip())

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

            line_selector_start = None if line_selector_start_as_string == '' else int(line_selector_start_as_string)
            line_selector_end = None if line_selector_end_as_string == '' else int(line_selector_end_as_string)
            return PythonSourceCodeImportMarker(marker, line_number, line_selector_start, line_selector_end)
    raise Error("desired import marker cannot be found in source code file. name of marker searched for: {}".format(marker))

def _extract_code_block(all_lines:List[str], line_number_code_block_start: int) -> List[str]:
    # For functions the first line is the signature, for classes it's the declaration
    # the indentation starts at the subsequent line in these cases
    # this is also working for other types of code blocks with at least two line
    # might not working in general cases
    line_number_of_first_indented_line = line_number_code_block_start + 1
    number_of_white_spaces_of_indentation = _number_of_leading_spaces(all_lines[line_number_of_first_indented_line])

    for line_number, line in enumerate(all_lines[line_number_of_first_indented_line:]):
        number_of_leading_spaces_of_the_line = _number_of_leading_spaces(line)

        # In the case of a class, an empty line with no indentation may separate two methods, but doesn't represent the end of the class
        next_code_block_detected = _is_non_empty_line(line) and number_of_leading_spaces_of_the_line < number_of_white_spaces_of_indentation
        if next_code_block_detected:
            return all_lines[line_number_code_block_start: line_number_code_block_start + line_number]
    return all_lines[line_number_code_block_start:]

def _import_code_block_from_source_file(reference: ReferenceToImportMarkerInMarkDownSourceCode) -> List[str]:
    with open(reference.source_code_absolute_path) as file:
        all_lines = file.readlines()

        import_marker = _find_import_marker(all_lines, reference.reference_name)

        # The code block starts the line after the marker
        first_line_of_the_code_block = import_marker.position_line_number + 1
        code_block = _extract_code_block(all_lines, first_line_of_the_code_block)

        return code_block[import_marker.line_selector_start : import_marker.line_selector_end]

def _write_output_markdown_file(filename: str, lines_to_write: List[str]) -> None:
    with open(filename, 'w') as textfile:
        for line_to_write in lines_to_write:
            textfile.write(line_to_write)

def _write_output_markdown_to_file(filename: str, target_directory: str) -> None:
    markdown_source_folder = os.path.dirname(filename)
    source_code_folder = markdown_source_folder
    destination_folder = target_directory

    with open(filename) as file:
        file_contents = file.readlines()
        content_of_the_result_file = _translate_source_markdown_to_output_markdown(file_contents, source_code_folder)
        output_file_name_without_src = os.path.basename(filename.replace(".src", ""))
        _write_output_markdown_file(destination_folder + '/' + output_file_name_without_src, content_of_the_result_file)


def _translate_source_markdown_to_output_markdown(file_contents: List[str], source_code_folder: str) -> List[str] :
    output_markdown_file_content = []
    for line in file_contents:
        regex_for_import_marker_in_markdown_source_code = "@Import\((.*),(.*)\)"
        import_marker_parsed_from_source_code_line = re.search(regex_for_import_marker_in_markdown_source_code, line)
        if import_marker_parsed_from_source_code_line is None:
            output_markdown_file_content.append(line)
        else:
            reference_name = import_marker_parsed_from_source_code_line.group(1)
            source_code_file_name = import_marker_parsed_from_source_code_line.group(2)
            reference_to_import_marker = ReferenceToImportMarkerInMarkDownSourceCode(reference_name, source_code_folder + "/" + source_code_file_name)

            expanded_code_listing_for_output = _read_source_code_and_format_code_for_output_markdown(reference_to_import_marker)
            output_markdown_file_content += expanded_code_listing_for_output

    return output_markdown_file_content


def _read_source_code_and_format_code_for_output_markdown(reference_to_import_marker: ReferenceToImportMarkerInMarkDownSourceCode) -> List[str]:
    code_block = _import_code_block_from_source_file(reference_to_import_marker)
    code_block = _remove_indentation_not_desired_for_output_markdown(code_block)
    expanded_code_listing_for_output = ["```python\n"] + code_block + ["\n```\n"]
    return expanded_code_listing_for_output


def _parse_file_name_from_command_line_arguments() -> str:
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument("-f", "--file", required=True)
    argument_parser.add_argument("-t", "--target_directory", required=True)

    command_line_arguments = vars(argument_parser.parse_args())
    file_to_parse: str = command_line_arguments["file"]
    target_directory: str = command_line_arguments["target_directory"]
    return file_to_parse, target_directory

def main():
    file_name, target_directory = _parse_file_name_from_command_line_arguments()
    _write_output_markdown_to_file(file_name, target_directory)

if __name__ == '__main__':
    main()