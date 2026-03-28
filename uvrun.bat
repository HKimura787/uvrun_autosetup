@echo off
setlocal EnableExtensions
cd /d "%~dp0"

call :EnsureUv
if errorlevel 1 exit /b 1

if "%~1"=="" (
  uv run python main.py
) else (
  uv run %*
)
exit /b %ERRORLEVEL%

:EnsureUv
where uv >nul 2>&1
if not errorlevel 1 exit /b 0

if exist "%USERPROFILE%\.local\bin\uv.exe" (
  set "PATH=%USERPROFILE%\.local\bin;%PATH%"
  exit /b 0
)

if exist "%USERPROFILE%\.cargo\bin\uv.exe" (
  set "PATH=%USERPROFILE%\.cargo\bin;%PATH%"
  exit /b 0
)

echo Installing uv...
powershell -NoProfile -ExecutionPolicy Bypass -Command "irm https://astral.sh/uv/install.ps1 | iex"
if errorlevel 1 (
  echo Failed to install uv.
  exit /b 1
)

set "PATH=%USERPROFILE%\.local\bin;%USERPROFILE%\.cargo\bin;%PATH%"

where uv >nul 2>&1
if not errorlevel 1 exit /b 0

if exist "%USERPROFILE%\.local\bin\uv.exe" (
  set "PATH=%USERPROFILE%\.local\bin;%PATH%"
  where uv >nul 2>&1
  if not errorlevel 1 exit /b 0
)

if exist "%USERPROFILE%\.cargo\bin\uv.exe" (
  set "PATH=%USERPROFILE%\.cargo\bin;%PATH%"
  where uv >nul 2>&1
  if not errorlevel 1 exit /b 0
)

echo uv was installed but could not be found in PATH.
exit /b 1
