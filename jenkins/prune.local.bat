@echo off
setlocal enabledelayedexpansion
set "folders=database output Viriato.8-Standard-NightlyStable-Product-43 Viriato.8-Standard-NightlyStable venv_jenkins_build_job algorithmplatform.pyclient\packaging_env algorithmplatform.pyclient\testing_venv algorithmplatform.pyclient\build algorithmplatform.pyclient\sma.algorithm_platform.py_client.egg-info"
echo The following folders will be deleted:
for %%i in (%folders%) do (
    echo - %%i
)
set /p "confirm=Are you sure you want to delete all folders? (y/n): "
if /i "%confirm%"=="y" (
    for %%i in (%folders%) do (
        if exist %%i (
            echo Deleting %%i...
            rmdir /S /Q %%i
        ) else (
            echo Directory %%i does not exist.
        )
    )
) else (
    echo "Operation cancelled."
)
endlocal

