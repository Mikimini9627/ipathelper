@echo off
setlocal enabledelayedexpansion

rmdir /s /q dist

REM ===== pyproject.toml のバージョンを繰り上げる(既定: パッチ / 引数で minor・major も指定可) =====
set "PART=%~1"
if "!PART!"=="" set "PART=patch"

REM 現在の version = "X.Y.Z" を取得する
set "CURVER="
for /f "usebackq tokens=2 delims==" %%A in (`findstr /b /c:"version = " "pyproject.toml"`) do set "CURVER=%%A"
if not defined CURVER (
    echo ERROR: pyproject.toml に version 行が見つかりません
    exit /b 1
)
REM 空白と引用符を取り除く
set "CURVER=!CURVER: =!"
set "CURVER=!CURVER:"=!"

REM X.Y.Z に分解する
for /f "tokens=1,2,3 delims=." %%a in ("!CURVER!") do (
    set "MAJOR=%%a"
    set "MINOR=%%b"
    set "PATCH=%%c"
)

if /i "!PART!"=="major" (
    set /a MAJOR+=1
    set "MINOR=0"
    set "PATCH=0"
) else if /i "!PART!"=="minor" (
    set /a MINOR+=1
    set "PATCH=0"
) else if /i "!PART!"=="patch" (
    set /a PATCH+=1
) else (
    echo ERROR: 不正な引数です: !PART! ^(patch / minor / major のいずれか^)
    exit /b 1
)

set "NEWVER=!MAJOR!.!MINOR!.!PATCH!"

REM version 行のみ差し替えて書き出す(空行・インデント・コメントは保持)
> "pyproject.toml.tmp" (
    for /f "usebackq delims=" %%L in (`findstr /n "^" "pyproject.toml"`) do (
        set "line=%%L"
        set "line=!line:*:=!"
        if "!line:~0,10!"=="version = " (
            echo version = "!NEWVER!"
        ) else (
            echo(!line!
        )
    )
)
move /y "pyproject.toml.tmp" "pyproject.toml" >nul

echo version: !CURVER! -^> !NEWVER! ^(!PART!^)

REM ===== ビルドして公開する =====
uv build
uv run --no-project publish.py pypi
