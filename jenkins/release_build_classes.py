import argparse
import os.path
from enum import Enum
from typing import Dict


class JobStage(Enum):
    perform_end_to_end_test = "PERFORM-END-TO-END-TEST"
    prepare_artifacts = "PREPARE-ARTIFACTS"
    check_out_and_aggregate_data_for_end_to_end_test = "CHECK-OUT-AND-AGGREGATE-DATA-FOR-END-TO-END-TEST"

    def __str__(self):
        return self.value


class ReleaseBuildConstants:
    OUTPUT_DIRECTORY = "output"
    DATABASE_DIRECTORY = "database"

    URL_JENKINS_ADDRESS = "https://jenkins.sma-partner.com"

    FILE_NAME_SAMPLES_DATABASE = "Samples_Database.vstd64"
    PATH_REMOTE_DIRECTORY_DATABASES = r"\\ZHFAS01A\\Entwicklung\Jenkins\JobData\PyClient-End2EndTests-Labs"

    REQUIREMENTS_FILE_WITH_PATH_PY_CLIENT = "py_client/py_client_requirements.txt"
    REQUIREMENTS_FILE_WITH_PATH_PY_CLIENT_UNIT_TEST = "py_client/py_client_unit_tests_requirements.txt"
    REQUIREMENTS_FILE_WITH_PATH_END_TO_END_TEST_TOOL = "end_to_end_tests_tool/end_to_end_test_tool_requirements.txt"

    FILE_NAME_UNIT_TEST_REPORT = "test_results"

    PATH_CALL_FILES_DIRECTORY_FROM_VIRIATO_ROOT = "data\\AlgorithmPlatformService.RestSamples\\calls"
    PATH_TO_END_TO_END_TEST_REPORT_FILE = os.path.join(OUTPUT_DIRECTORY, "end_to_end_test_results.txt")
    PATH_TO_END_TO_END_TEST_CALLS_FOLDER = "algorithmplatform.pyclient.endtoendtesttool\\end_to_end_tests_tool\\data\\calls"
    FOLDER_NAME_END_TO_END_TESTS_TOOL_ROOT = "algorithmPlatform.pyclient.endtoendtesttool"
    PATH_TO_EXECUTABLE_END_TO_END_TESTS = "jenkins\\run_end_to_end_test.bat"
    UPDATE_PIP_IN_END_TO_END_TESTS_PYTHON_ENVIRONMENT = False
    SUCCESS_STRING_OF_END_TO_END_TESTS_TOOL = "All End-To-End-Tests were executed successfully. There are no errors and no test fail"

    # ALGORITHM_PLATFORM_RESEARCH_RELEASE_PACKAGE_WILDCARD = "AlgorithmResearch_Package*.zip"
    # VIRIATO_STANDARD_TEST_ZIP_WILDCARD = "SMA.Viriato.Standard-*test.zip"

    FILE_PATH_LICENSES_PY_CLIENT = os.path.join(OUTPUT_DIRECTORY, "algorithmplatform.pyclient.licenses.txt")


class ReleaseBuildArguments:
    __job_stage: JobStage
    __release_branch_py_client: str
    # TODO: Rename or remove
    __branch_suffix: str

    __zip_file_samples_database: str
    __path_to_samples_db_on_jenkins: str

    __root_directory_call_jsons: str
    __file_path_wheel_py_client: str

    __zip_file_name_algorithm_platform_research_release: str
    __job_name_algorithm_platform_research_release: str
    __release_url_algorithm_platform_research: str
    __build_number_algorithm_platform_research_release: int
    __target_version_algorithm_platform_research_release: str

    __zip_file_name_viriato_standard_nightly_stable_test: str
    __url_viriato_standard_nightly_stable_test: str
    __unzip_directory_viriato_nightly_stable: str
    __build_number_viriato_standard_nightly_stable: int

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
    ):
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


class ReleaseBuildArgumentsFactory:
    @staticmethod
    def __determine_branch_suffix(branch: str) -> str:
        if "Product" in branch:
            return f"-{branch}"
        return ""

    def create_instance_from_dictionary(self, command_line_arguments: Dict[str, str | int | JobStage]) -> ReleaseBuildArguments:
        job_stage: JobStage = command_line_arguments["STAGE"]
        release_branch_py_client: str = command_line_arguments["RELEASE_BRANCH"]
        target_version_algorithm_platform_research_release = command_line_arguments["ALGORITHM_PLATFORM_RELEASE_TARGET_VERSION"]
        build_number_algorithm_platform_research_release = command_line_arguments["STD_ALGORITHM_RESEARCH_RELEASE_CREATE_PACKAGE_BUILD_NUMBER"]
        build_number_viriato_standard_nightly_stable = command_line_arguments["STD_NIGHTLY_STABLE_BUILD_NUMBER"]

        build_number_jenkins_job = command_line_arguments["BUILD_NUMBER"]

        zip_file_name_algorithm_platform_research_release = f"AlgorithmResearch_Package-{target_version_algorithm_platform_research_release}.zip"
        zip_file_name_viriato_standard_nightly_stable_test = f"SMA.Viriato.Standard-{target_version_algorithm_platform_research_release}.test.zip"
        branch_suffix = self.__determine_branch_suffix(release_branch_py_client)

        unzip_directory_viriato_nightly_stable = f"Viriato.8-Standard-NightlyStable{branch_suffix}"
        job_name_algorithm_platform_research_release = f"Viriato.8-Standard-AlgorithmResearch-Release.CreatePackage{branch_suffix}"
        zip_file_samples_database = f"Samples_Database{branch_suffix}.zip"

        root_directory_call_jsons = os.path.join(
            unzip_directory_viriato_nightly_stable,
            # f"SMA.Viriato.Standard-{target_version_algorithm_platform_research_release}",
            ReleaseBuildConstants.PATH_CALL_FILES_DIRECTORY_FROM_VIRIATO_ROOT,
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
        path_to_samples_db_on_jenkins = os.path.join(ReleaseBuildConstants.PATH_REMOTE_DIRECTORY_DATABASES, zip_file_samples_database)

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
        )


class ArgumentParserFactory:
    @staticmethod
    def create_instance() -> argparse.ArgumentParser:
        argument_parser = argparse.ArgumentParser()
        argument_parser.add_argument("--STAGE", type=JobStage, choices=list(JobStage), required=True)
        argument_parser.add_argument("--RELEASE-BRANCH", type=str, required=True)
        argument_parser.add_argument("--ALGORITHM-PLATFORM-RELEASE-TARGET-VERSION", type=str, required=True)
        argument_parser.add_argument("--STD-ALGORITHM-RESEARCH-RELEASE-CREATE-PACKAGE-BUILD-NUMBER", type=int, required=True)
        argument_parser.add_argument("--STD-NIGHTLY-STABLE-BUILD-NUMBER", type=int, required=True)
        argument_parser.add_argument("--BUILD-NUMBER", type=int, required=True)

        return argument_parser
