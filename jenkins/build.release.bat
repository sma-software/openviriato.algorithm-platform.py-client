@echo off

set BUILDTOOL=python algorithmplatform.pyclient\\jenkins\\release_build_script.py
set PY_CLIENT_REQUIREMENTS_FILE_WITH_PATH=algorithmplatform.pyclient\\jenkins\\release_build_requirements.txt
set ACTIVATE_VENV_BAT_SCRIPT=venv_jenkins_build_job\\Scripts\\activate.bat

if "%8" == "" (
    if "%7" neq "" goto stages
)

echo "USAGE: algorithmplatform.pyclient\jenkins\build.release.bat [STAGE] [RELEASE-BRANCH] [ALGORITHM-PLATFORM-RELEASE-TARGET-VERSION] [STD-ALGORITHM-RESEARCH-RELEASE-CREATE-PACKAGE-BUILD-NUMBER] [STD-NIGHTLY-STABLE-BUILD-NUMBER] [BUILD-NUMBER] [UPDATE-PIP]
echo "Example call: algorithmplatform.pyclient\jenkins\build.release.bat CHECK-OUT-AND-AGGREGATE-DATA-FOR-END-TO-END-TEST Product-43 8.43.33 33 29 1 false"
exit /b 1


:stages
if %1 == "INSTALL-PYTHON-ENVIRONMENT" (
    echo "Running stage INSTALL_PYTHON_ENVIRONMENT"

    echo "Step: make local environment"
    python -m venv venv_jenkins_build_job

    echo "Step: activating local environment"
    call %ACTIVATE_VENV_BAT_SCRIPT%

    echo "Installing requirements"
    call pip install -r %PY_CLIENT_REQUIREMENTS_FILE_WITH_PATH% --no-cache-dir

    exit /b 0
)

echo "Step: activating local environment"
call %ACTIVATE_VENV_BAT_SCRIPT%

echo "Executing stage."
%BUILDTOOL% --STAGE=%1 --RELEASE-BRANCH=%2 --ALGORITHM-PLATFORM-RELEASE-TARGET-VERSION=%3 --STD-ALGORITHM-RESEARCH-RELEASE-CREATE-PACKAGE-BUILD-NUMBER=%4 --STD-NIGHTLY-STABLE-BUILD-NUMBER=%5 --BUILD-NUMBER=%6 --UPDATE-PIP=%7

if %ERRORLEVEL% neq 0 (
    echo "An error occurred during executing the stage."
    exit /b 1
)

echo "Stage successfully completed."
exit /b 0
