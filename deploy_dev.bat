@echo off
rem  Publish to TestPyPI (development).
rem  The version bump / build / publish logic lives in deploy_common.bat.
rem  Pass /dryrun to build without bumping the version or publishing.
call "%~dp0deploy_common.bat" testpypi %*
exit /b %ERRORLEVEL%
