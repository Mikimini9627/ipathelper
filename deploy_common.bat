@echo off
setlocal enabledelayedexpansion

rem ============================================================
rem  Shared deploy routine for ipathelper.
rem
rem  Usage:
rem    deploy_common.bat <section> [/dryrun]
rem      <section> : a section name in ~/.pypirc (pypi or testpypi)
rem      /dryrun   : bump nothing and publish nothing (build only)
rem
rem  Called from deploy_prd.bat (pypi) and deploy_dev.bat (testpypi).
rem  Keep this file ASCII-only: the console code page is switched to
rem  UTF-8 below, and non-ASCII batch text breaks under a mismatched
rem  code page.
rem ============================================================

set "SECTION=%~1"
if "%SECTION%"=="" echo [ERROR] no target section was given. & exit /b 1

set DRYRUN=0
if /i "%~2"=="/dryrun" set DRYRUN=1

rem  pyproject.toml is UTF-8 and contains Japanese, so the console code page
rem  must be UTF-8 while the file is read back and rewritten. Otherwise the
rem  description line is re-encoded and corrupted. The original code page is
rem  restored on exit.
for /f "tokens=2 delims=:" %%c in ('chcp') do set "ORIGINAL_CP=%%c"
set "ORIGINAL_CP=%ORIGINAL_CP: =%"
chcp 65001 >nul

pushd "%~dp0"

set "TOML=pyproject.toml"
set "TOML_NEW=pyproject.toml.new"

echo [INFO] target = %SECTION%
if "%DRYRUN%"=="1" echo [INFO] dryrun: the version is not written and nothing is published.

if not exist "%TOML%" echo [ERROR] %TOML% not found. & goto FAIL

rem ============================================================
rem  Read the current version from the [project] section
rem  (a "version" key can also appear in other tables, so the
rem   section is tracked and only [project] is used)
rem ============================================================
set "CURRENT="
set "INPROJ=0"
for /f "usebackq delims=" %%L in (`findstr /n "^" "%TOML%"`) do (
    set "line=%%L"
    rem findstr /n prefixes "<number>:" - strip it so blank lines survive
    set "line=!line:*:=!"
    if "!line:~0,1!"=="[" (
        if /i "!line!"=="[project]" (set "INPROJ=1") else (set "INPROJ=0")
    )
    if "!INPROJ!"=="1" if not defined CURRENT (
        rem drop spaces and quotes, then match the key
        set "t=!line: =!"
        set t=!t:"=!
        if "!t:~0,8!"=="version=" set "CURRENT=!t:~8!"
    )
)

if not defined CURRENT echo [ERROR] version was not found in the [project] section. & goto FAIL
echo [INFO] current version = !CURRENT!

rem ---- bump the patch number ----
set "MA=" & set "MI=" & set "PA="
for /f "tokens=1,2,3 delims=." %%a in ("!CURRENT!") do (
    set "MA=%%a"
    set "MI=%%b"
    set "PA=%%c"
)
if not defined PA echo [ERROR] unexpected version format: !CURRENT! & goto FAIL

set /a PA_NEW=!PA!+1 2>nul
if errorlevel 1 echo [ERROR] the patch number is not numeric: !PA! & goto FAIL
set "NEW=!MA!.!MI!.!PA_NEW!"
echo [INFO] new version     = !NEW!

if "%DRYRUN%"=="1" goto BUILD

rem ============================================================
rem  Rewrite pyproject.toml (only the [project] version line)
rem   - findstr /n keeps blank lines
rem   - "echo(" plus delayed expansion keeps ">" in ">=3.12" literal,
rem     because redirection is parsed before the variable is expanded
rem ============================================================
if exist "%TOML_NEW%" del "%TOML_NEW%"
set "INPROJ=0"
set "DONE=0"
for /f "usebackq delims=" %%L in (`findstr /n "^" "%TOML%"`) do (
    set "line=%%L"
    set "line=!line:*:=!"
    if "!line:~0,1!"=="[" (
        if /i "!line!"=="[project]" (set "INPROJ=1") else (set "INPROJ=0")
    )
    set "HIT=0"
    if "!INPROJ!"=="1" if "!DONE!"=="0" (
        set "t=!line: =!"
        set t=!t:"=!
        if "!t:~0,8!"=="version=" set "HIT=1"
    )
    if "!HIT!"=="1" (
        echo(version = "!NEW!">>"%TOML_NEW%"
        set "DONE=1"
    ) else (
        echo(!line!>>"%TOML_NEW%"
    )
)

if not exist "%TOML_NEW%" echo [ERROR] failed to build the new %TOML%. & goto FAIL
if "!DONE!"=="0" del "%TOML_NEW%" & echo [ERROR] the version line could not be replaced. & goto FAIL

move /y "%TOML_NEW%" "%TOML%" >nul
if errorlevel 1 echo [ERROR] failed to replace %TOML%. & goto FAIL
echo [INFO] %TOML% updated to !NEW!.

:BUILD
echo.
echo [INFO] building...
if exist dist rmdir /s /q dist
uv build
if errorlevel 1 echo [ERROR] uv build failed. & goto FAIL

if "%DRYRUN%"=="1" echo. & echo [SUCCESS] dryrun finished (nothing was published). & set "EXIT_CODE=0" & goto END

echo.
echo [INFO] publishing to %SECTION%...
uv run --no-project publish.py %SECTION%
if errorlevel 1 echo [ERROR] publish failed. & goto FAIL

echo.
echo [SUCCESS] ipathelper !NEW! was published to %SECTION%.
set "EXIT_CODE=0"
goto END

:FAIL
set "EXIT_CODE=1"

:END
popd
if defined ORIGINAL_CP chcp %ORIGINAL_CP% >nul
if not defined EXIT_CODE set "EXIT_CODE=1"
echo.
pause
endlocal & exit /b %EXIT_CODE%
