import argparse
import os.path
from enum import Enum
from typing import Dict


class JobStage(Enum):
    perform_end_to_end_test = "PERFORM-END-TO-END-TEST"
    prepare_artifacts = "PREPARE-ARTIFACTS"
    check_out_and_aggregate_data_for_end_to_end_test = "CHECK-OUT-AND-AGGREGATE-DATA-FOR-END-TO-END-TEST"
    create_whl_package = "CREATE-WHL-PACKAGE"
    unit_test_py_client = "UNIT-TEST-PY-CLIENT"

    def __str__(self):
        return self.value


class ReleaseBuildConstants:
    # ToDo VPLAT-10906: See if we can derive more constants from each other
    OUTPUT_DIRECTORY = "output"
    DATABASE_DIRECTORY = "database"
    PY_CLIENT_ROOT_DIRECTORY = "algorithmplatform.pyclient"
    END_TO_END_TESTS_TOOL_ROOT_DIRECTORY = "algorithmPlatform.pyclient.endtoendtesttool"
    FILE_NAME_LICENSES_PY_CLIENT = "algorithmplatform.pyclient.licenses.txt"
    URL_JENKINS_ADDRESS = "https://jenkins.sma-partner.com"

    PATH_REMOTE_DIRECTORY_DATABASES = r"\\ZHFAS01A\\Entwicklung\Jenkins\JobData\PyClient-End2EndTests-Labs"

    ABSOLUTE_BASE_PATH_WORK_SPACE = os.getcwd()
    ABSOLUTE_PATH_OUTPUT_DIRECTORY = os.path.join(ABSOLUTE_BASE_PATH_WORK_SPACE, OUTPUT_DIRECTORY)
    ABSOLUTE_PATH_DATABASE_DIRECTORY = os.path.join(ABSOLUTE_BASE_PATH_WORK_SPACE, DATABASE_DIRECTORY)
    ABSOLUTE_PATH_PY_CLIENT_ROOT_DIRECTORY = os.path.join(ABSOLUTE_BASE_PATH_WORK_SPACE, PY_CLIENT_ROOT_DIRECTORY)
    ABSOLUTE_PATH_END_TO_END_TESTS_TOOL_ROOT_DIRECTORY = os.path.join(ABSOLUTE_BASE_PATH_WORK_SPACE, END_TO_END_TESTS_TOOL_ROOT_DIRECTORY)

    REQUIREMENTS_FILE_WITH_ABSOLUTE_PATH_PY_CLIENT = os.path.join(ABSOLUTE_PATH_PY_CLIENT_ROOT_DIRECTORY, "py_client", "py_client_requirements.txt")
    REQUIREMENTS_FILE_WITH_ABSOLUTE_PATH_PY_CLIENT_UNIT_TEST = os.path.join(
        ABSOLUTE_PATH_PY_CLIENT_ROOT_DIRECTORY, "py_client", "py_client_unit_tests_requirements.txt"
    )
    # REQUIREMENTS_FILE_WITH_PATH_END_TO_END_TEST_TOOL = "end_to_end_tests_tool/end_to_end_test_tool_requirements.txt"

    # ToDo VPLAT-10906: check if commandline arguments can be optional
    ABSOLUTE_PATH_TO_RELEASE_PACKING_SCRIPT_FOLDER = os.path.join(ABSOLUTE_PATH_PY_CLIENT_ROOT_DIRECTORY, "jenkins", "packaging")
    ABSOLUTE_PATH_TO_RELEASE_PACKING_PYTHON_ENVIRONMENT = os.path.join(ABSOLUTE_PATH_PY_CLIENT_ROOT_DIRECTORY, "packaging_env")
    ABSOLUTE_PATH_TO_PYTHON_EXE_PACKING_PYTHON_ENVIRONMENT = os.path.join(ABSOLUTE_PATH_TO_RELEASE_PACKING_PYTHON_ENVIRONMENT, "Scripts", "python.exe")
    ABSOLUTE_PATH_TO_PIP_EXE_PACKING_PYTHON_ENVIRONMENT = os.path.join(ABSOLUTE_PATH_TO_RELEASE_PACKING_PYTHON_ENVIRONMENT, "Scripts", "pip.exe")
    ABSOLUTE_FILE_PATH_SOURCE_LICENSES_PY_CLIENT = os.path.join(ABSOLUTE_PATH_TO_RELEASE_PACKING_SCRIPT_FOLDER, FILE_NAME_LICENSES_PY_CLIENT)
    COMMAND_INSTALL_WHEEL_PACKAGE_FOR_PYTHON_ENVIRONMENT_RELEASE_PACKING = (
        f"{ABSOLUTE_PATH_TO_PIP_EXE_PACKING_PYTHON_ENVIRONMENT} install wheel~=0.35.1 --no-cache-dir"
    )
    COMMAND_INSTALL_PACKAGES_FOR_PYTHON_ENVIRONMENT_RELEASE_PACKING = (
        f"{ABSOLUTE_PATH_TO_PIP_EXE_PACKING_PYTHON_ENVIRONMENT} install -r {REQUIREMENTS_FILE_WITH_ABSOLUTE_PATH_PY_CLIENT} --no-cache-dir"
    )
    COMMAND_TO_START_CREATE_PACKAGE_EXECUTABLE = f"{ABSOLUTE_PATH_TO_PYTHON_EXE_PACKING_PYTHON_ENVIRONMENT} create_release_package.py"

    ABSOLUTE_PATH_TO_TESTING_PYTHON_ENVIRONMENT = os.path.join(ABSOLUTE_PATH_PY_CLIENT_ROOT_DIRECTORY, "testing_venv")
    FILE_NAME_UNIT_TEST_REPORT = "test_results"
    ABSOLUTE_FILE_PATH_UNITTEST_RESULT = os.path.join(ABSOLUTE_PATH_OUTPUT_DIRECTORY, f"{FILE_NAME_UNIT_TEST_REPORT}.html")
    ABSOLUTE_PATH_TO_PYTHON_EXE_TESTING_PYTHON_ENVIRONMENT = os.path.join(ABSOLUTE_PATH_TO_TESTING_PYTHON_ENVIRONMENT, "Scripts", "python.exe")
    ABSOLUTE_PATH_TO_PIP_EXE_TESTING_PYTHON_ENVIRONMENT = os.path.join(ABSOLUTE_PATH_TO_TESTING_PYTHON_ENVIRONMENT, "Scripts", "pip.exe")
    COMMAND_INSTALL_PACKAGES_FOR_TESTING_PYTHON_ENVIRONMENT = f"{ABSOLUTE_PATH_TO_PIP_EXE_TESTING_PYTHON_ENVIRONMENT} install -r {REQUIREMENTS_FILE_WITH_ABSOLUTE_PATH_PY_CLIENT} -r {REQUIREMENTS_FILE_WITH_ABSOLUTE_PATH_PY_CLIENT_UNIT_TEST} --no-cache-dir"
    COMMAND_EXECUTE_UNIT_TESTS = f"{ABSOLUTE_PATH_TO_PYTHON_EXE_TESTING_PYTHON_ENVIRONMENT} {os.path.join('jenkins', 'run_all_unittests_and_generate_html_report.py')} . {ABSOLUTE_PATH_OUTPUT_DIRECTORY} {FILE_NAME_UNIT_TEST_REPORT}"
    FORMATTING_LINE_LENGTH = 160
    COMMAND_EXECUTE_FORMATTING_VERIFICATION_BLACK = f"{ABSOLUTE_PATH_TO_PYTHON_EXE_TESTING_PYTHON_ENVIRONMENT} -m black {os.path.join(ABSOLUTE_PATH_PY_CLIENT_ROOT_DIRECTORY, 'py_client')} --check --diff --line-length {FORMATTING_LINE_LENGTH}"

    FILE_NAME_END_TO_END_TEST_TOOL_REPORT = "end_to_end_test_results.txt"
    PATH_CALL_FILES_DIRECTORY_FROM_VIRIATO_ROOT = os.path.join("data", "AlgorithmPlatformService.RestSamples", "calls")
    ABSOLUTE_PATH_TO_END_TO_END_TEST_REPORT_FILE = os.path.join(ABSOLUTE_PATH_OUTPUT_DIRECTORY, FILE_NAME_END_TO_END_TEST_TOOL_REPORT)
    PATH_TO_END_TO_END_TEST_REPORT_FILE_FROM_END_TO_END_TEST_TOOL = os.path.join("..", OUTPUT_DIRECTORY, FILE_NAME_END_TO_END_TEST_TOOL_REPORT)
    RELATIVE_PATH_TO_SAMPLES_DATABASE = os.path.join(DATABASE_DIRECTORY, "Samples_Database.vstd64")
    ABSOLUTE_PATH_TO_END_TO_END_TEST_CALLS_FOLDER = os.path.join(ABSOLUTE_PATH_END_TO_END_TESTS_TOOL_ROOT_DIRECTORY, "end_to_end_tests_tool", "data", "calls")
    ABSOLUTE_PATH_TO_EXECUTABLE_END_TO_END_TESTS = os.path.join(ABSOLUTE_PATH_END_TO_END_TESTS_TOOL_ROOT_DIRECTORY, "jenkins", "run_end_to_end_test.bat")
    SUCCESS_STRING_OF_END_TO_END_TESTS_TOOL = "All End-To-End-Tests were executed successfully. There are no errors and no test fail"

    ABSOLUTE_FILE_PATH_LICENSES_PY_CLIENT = os.path.join(ABSOLUTE_PATH_OUTPUT_DIRECTORY, FILE_NAME_LICENSES_PY_CLIENT)


class ReleaseBuildArguments:
    __job_stage: JobStage
    __release_branch_py_client: str
    # TODO: Rename or remove
    __branch_suffix: str

    __zip_file_samples_database: str
    __path_to_samples_db_on_jenkins: str

    __root_directory_call_jsons: str
    __file_path_wheel_py_client: str
    __command_create_release_package: str

    __zip_file_name_algorithm_platform_research_release: str
    __job_name_algorithm_platform_research_release: str
    __release_url_algorithm_platform_research: str
    __build_number_algorithm_platform_research_release: int
    __target_version_algorithm_platform_research_release: str

    __zip_file_name_viriato_standard_nightly_stable_test: str
    __url_viriato_standard_nightly_stable_test: str
    __unzip_directory_viriato_nightly_stable: str
    __build_number_viriato_standard_nightly_stable: int
    __update_pip: bool

    def __init__(
        self,
        job_stage: JobStage,
        release_branch_py_client: str,
        target_version_algorithm_platform_research_release: str,
        build_number_algorithm_platform_research_release: int,
        build_number_viriato_standard_nightly_stable: int,
        unzip_directory_viriato_nightly_stable: str,
        job_name_algorithm_platform_research_release: str,
        zip_file_samples_database: str,
        file_path_wheel_py_client: str,
        zip_file_name_algorithm_platform_research_release: str,
        release_url_algorithm_platform_research: str,
        zip_file_name_viriato_standard_nightly_stable_test: str,
        url_viriato_standard_nightly_stable_test: str,
        branch_suffix: str,
        path_to_samples_db_on_jenkins: str,
        root_directory_call_jsons: str,
        command_create_release_package: str,
        update_pip: bool,
    ):
        self.__update_pip = update_pip
        self.__command_create_release_package = command_create_release_package
        self.__root_directory_call_jsons = root_directory_call_jsons
        self.__path_to_samples_db_on_jenkins = path_to_samples_db_on_jenkins
        self.__url_viriato_standard_nightly_stable_test = url_viriato_standard_nightly_stable_test
        self.__release_url_algorithm_platform_research = release_url_algorithm_platform_research
        self.__zip_file_name_viriato_standard_nightly_stable_test = zip_file_name_viriato_standard_nightly_stable_test
        self.__branch_suffix = branch_suffix
        self.__zip_file_name_algorithm_platform_research_release = zip_file_name_algorithm_platform_research_release
        self.__file_path_wheel_py_client = file_path_wheel_py_client
        self.__zip_file_samples_database = zip_file_samples_database
        self.__job_name_algorithm_platform_research_release = job_name_algorithm_platform_research_release
        self.__unzip_directory_viriato_nightly_stable = unzip_directory_viriato_nightly_stable
        self.__build_number_viriato_standard_nightly_stable = build_number_viriato_standard_nightly_stable
        self.__build_number_algorithm_platform_research_release = build_number_algorithm_platform_research_release
        self.__target_version_algorithm_platform_research_release = target_version_algorithm_platform_research_release
        self.__job_stage = job_stage
        self.__release_branch_py_client = release_branch_py_client

    @property
    def job_stage(self) -> JobStage:
        return self.__job_stage

    @property
    def release_branch_py_client(self) -> str:
        return self.__release_branch_py_client

    @property
    def algorithm_platform_release_target_version(self) -> str:
        return self.__target_version_algorithm_platform_research_release

    @property
    def build_number_algorithm_platform_research_release(self) -> int:
        return self.__build_number_algorithm_platform_research_release

    @property
    def build_number_viriato_standard_nightly_stable(self) -> int:
        return self.__build_number_viriato_standard_nightly_stable

    @property
    def unzip_directory_viriato_nightly_stable(self) -> str:
        return self.__unzip_directory_viriato_nightly_stable

    @property
    def job_name_algorithm_platform_research_release(self) -> str:
        return self.__job_name_algorithm_platform_research_release

    @property
    def zip_file_samples_database(self) -> str:
        return self.__zip_file_samples_database

    @property
    def file_path_wheel_py_client(self) -> str:
        return self.__file_path_wheel_py_client

    @property
    def zip_file_name_algorithm_platform_research_release(self) -> str:
        return self.__zip_file_name_algorithm_platform_research_release

    @property
    def branch_suffix(self) -> str:
        return self.__branch_suffix

    @property
    def zip_file_name_viriato_standard_nightly_stable_test(self):
        return self.__zip_file_name_viriato_standard_nightly_stable_test

    @property
    def release_url_algorithm_platform_research(self):
        return self.__release_url_algorithm_platform_research

    @property
    def url_viriato_standard_test_zip(self):
        return self.__url_viriato_standard_nightly_stable_test

    @property
    def path_to_samples_db_on_jenkins(self):
        return self.__path_to_samples_db_on_jenkins

    @property
    def root_directory_call_jsons(self):
        return self.__root_directory_call_jsons

    @property
    def command_create_release_package(self):
        return self.__command_create_release_package

    @property
    def update_pip(self):
        return self.__update_pip


class ReleaseBuildArgumentsFactory:
    @staticmethod
    def __determine_branch_suffix(branch: str) -> str:
        if branch and "Product" in branch:
            return f"-{branch}"
        return ""

    def create_instance_from_dictionary(self, command_line_arguments: Dict[str, str | int | bool]) -> ReleaseBuildArguments:
        job_stage: JobStage = JobStage(command_line_arguments["STAGE"])
        release_branch_py_client: str | None = command_line_arguments.get("RELEASE_BRANCH")
        target_version_algorithm_platform_research_release: str | None = command_line_arguments.get("ALGORITHM_PLATFORM_RELEASE_TARGET_VERSION")
        build_number_algorithm_platform_research_release: int | None = command_line_arguments.get("STD_ALGORITHM_RESEARCH_RELEASE_CREATE_PACKAGE_BUILD_NUMBER")
        build_number_viriato_standard_nightly_stable: int | None = command_line_arguments.get("STD_NIGHTLY_STABLE_BUILD_NUMBER")
        build_number_jenkins_job: int | None = command_line_arguments.get("BUILD_NUMBER")

        zip_file_name_algorithm_platform_research_release = f"AlgorithmResearch_Package-{target_version_algorithm_platform_research_release}.zip"
        zip_file_name_viriato_standard_nightly_stable_test = f"SMA.Viriato.Standard-{target_version_algorithm_platform_research_release}.test.zip"
        branch_suffix = self.__determine_branch_suffix(release_branch_py_client)

        unzip_directory_viriato_nightly_stable = f"Viriato.8-Standard-NightlyStable{branch_suffix}"
        job_name_algorithm_platform_research_release = f"Viriato.8-Standard-AlgorithmResearch-Release.CreatePackage{branch_suffix}"
        zip_file_samples_database = f"Samples_Database{branch_suffix}.zip"

        root_directory_call_jsons = os.path.join(
            unzip_directory_viriato_nightly_stable,
            ReleaseBuildConstants.PATH_CALL_FILES_DIRECTORY_FROM_VIRIATO_ROOT,
        )

        command_create_release_package = (
            f"{ReleaseBuildConstants.COMMAND_TO_START_CREATE_PACKAGE_EXECUTABLE} {target_version_algorithm_platform_research_release}.post{build_number_jenkins_job} "
            f"{ReleaseBuildConstants.REQUIREMENTS_FILE_WITH_ABSOLUTE_PATH_PY_CLIENT} "
            f"{ReleaseBuildConstants.ABSOLUTE_PATH_PY_CLIENT_ROOT_DIRECTORY} "
            f"{ReleaseBuildConstants.ABSOLUTE_PATH_OUTPUT_DIRECTORY}"
        )
        file_path_wheel_py_client = os.path.join(
            ReleaseBuildConstants.OUTPUT_DIRECTORY,
            f"sma.algorithm_platform.py_client-{target_version_algorithm_platform_research_release}.post{build_number_jenkins_job}-py3-none-any.whl",
        )

        release_url_algorithm_platform_research = (
            f"{ReleaseBuildConstants.URL_JENKINS_ADDRESS}/job/{job_name_algorithm_platform_research_release}/"
            f"{build_number_algorithm_platform_research_release}/artifact/dist/dist/{zip_file_name_algorithm_platform_research_release}"
        )
        url_viriato_standard_nightly_stable_test = (
            f"{ReleaseBuildConstants.URL_JENKINS_ADDRESS}/job/{unzip_directory_viriato_nightly_stable}/"
            f"{build_number_viriato_standard_nightly_stable}/artifact/stable/dist/{zip_file_name_viriato_standard_nightly_stable_test}"
        )
        path_to_samples_db_on_jenkins = os.path.join(
            ReleaseBuildConstants.PATH_REMOTE_DIRECTORY_DATABASES,
            zip_file_samples_database,
        )

        update_pip: bool = command_line_arguments["UPDATE_PIP"]

        return ReleaseBuildArguments(
            job_stage=job_stage,
            build_number_algorithm_platform_research_release=build_number_algorithm_platform_research_release,
            build_number_viriato_standard_nightly_stable=build_number_viriato_standard_nightly_stable,
            target_version_algorithm_platform_research_release=target_version_algorithm_platform_research_release,
            release_branch_py_client=release_branch_py_client,
            unzip_directory_viriato_nightly_stable=unzip_directory_viriato_nightly_stable,
            job_name_algorithm_platform_research_release=job_name_algorithm_platform_research_release,
            zip_file_samples_database=zip_file_samples_database,
            file_path_wheel_py_client=file_path_wheel_py_client,
            zip_file_name_algorithm_platform_research_release=zip_file_name_algorithm_platform_research_release,
            zip_file_name_viriato_standard_nightly_stable_test=zip_file_name_viriato_standard_nightly_stable_test,
            branch_suffix=branch_suffix,
            release_url_algorithm_platform_research=release_url_algorithm_platform_research,
            url_viriato_standard_nightly_stable_test=url_viriato_standard_nightly_stable_test,
            path_to_samples_db_on_jenkins=path_to_samples_db_on_jenkins,
            root_directory_call_jsons=root_directory_call_jsons,
            command_create_release_package=command_create_release_package,
            update_pip=update_pip,
        )


class ArgumentParserFactory:
    @staticmethod
    def _strict_parse_str_to_bool(val: str) -> bool:
        val = val.lower()
        if val == "true":
            return True
        elif val == "false":
            return False
        else:
            raise ValueError("invalid truth value %r" % (val,))

    @staticmethod
    def _is_string_not_empty_and_not_just_white_spaces(val: str) -> str:
        if val and val.strip(" ") != "":
            return val
        raise ValueError(f"invalid string value: {val}")

    @staticmethod
    def _add_arguments_algorithm_platform_release_target_version_and_build_number_to_parser(parser):
        parser.add_argument(
            "--ALGORITHM-PLATFORM-RELEASE-TARGET-VERSION", type=ArgumentParserFactory._is_string_not_empty_and_not_just_white_spaces, required=True
        )
        parser.add_argument("--BUILD-NUMBER", type=int, required=True)

    @staticmethod
    def create_instance() -> argparse.ArgumentParser:
        argument_parser = argparse.ArgumentParser()
        # ToDo VPLAT 10906: make this a flag and not a input value: https://stackoverflow.com/questions/15008758/parsing-boolean-values-with-argparse
        argument_parser.add_argument("--UPDATE-PIP", type=ArgumentParserFactory._strict_parse_str_to_bool, required=True)

        # ToDo VPLAT 10906: maybe add more granular subparsers
        subparsers = argument_parser.add_subparsers(
            dest="STAGE", title="STAGE", metavar=[e.value for e in JobStage], required=True, help="Help: [STAGE-NAME] -h"
        )
        subparsers.add_parser("UNIT-TEST-PY-CLIENT")

        whl_package_parser = subparsers.add_parser("CREATE-WHL-PACKAGE")
        ArgumentParserFactory._add_arguments_algorithm_platform_release_target_version_and_build_number_to_parser(whl_package_parser)

        subparser_complex_stages = subparsers.add_parser(
            "PERFORM-END-TO-END-TEST",
            aliases=["PREPARE-ARTIFACTS", "CHECK-OUT-AND-AGGREGATE-DATA-FOR-END-TO-END-TEST"],
        )
        ArgumentParserFactory._add_arguments_algorithm_platform_release_target_version_and_build_number_to_parser(subparser_complex_stages)
        subparser_complex_stages.add_argument("--RELEASE-BRANCH", type=ArgumentParserFactory._is_string_not_empty_and_not_just_white_spaces, required=True)
        subparser_complex_stages.add_argument("--STD-ALGORITHM-RESEARCH-RELEASE-CREATE-PACKAGE-BUILD-NUMBER", type=int, required=True)
        subparser_complex_stages.add_argument("--STD-NIGHTLY-STABLE-BUILD-NUMBER", type=int, required=True)

        return argument_parser
