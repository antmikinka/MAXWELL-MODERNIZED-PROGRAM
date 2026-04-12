@echo off
REM =============================================================================
REM Maxwell Quality Check Runner (Windows)
REM =============================================================================
REM Runs comprehensive quality checks on Maxwell Part IV modules.
REM
REM Usage:
REM   run_quality_checks.bat [options]
REM
REM Options:
REM   --import-only    Run only import tests
REM   --citation-only  Run only citation checks
REM   --cgs-only       Run only CGS unit tests
REM   --physics-only   Run only physics formula tests
REM   --verification   Run equation verification pipeline
REM   --all            Run all checks (default)
REM   --verbose        Show detailed output
REM   --help           Show this help message
REM
REM Exit codes:
REM   0 - All checks passed
REM   1 - One or more checks failed
REM   2 - Configuration error (missing dependencies)
REM =============================================================================

setlocal enabledelayedexpansion

REM Configuration
set "PROJECT_DIR=%~dp0"
set "MAXWELL_DIR=%PROJECT_DIR%maxwell"
set "TESTS_DIR=%PROJECT_DIR%tests"
set "PYTHON=%PYTHON:-python%"
if "%PYTHON%"=="" set "PYTHON=python"
set "VERBOSE=false"
set "MODE=all"

REM Counters
set /a TOTAL_TESTS=0
set /a PASSED_TESTS=0
set /a FAILED_TESTS=0

REM Color codes (Windows 10+)
for /F "tokens=1,2 delims=#" %%a in ('"prompt #$H#$E# & echo on & for %%b in (1) do rem"') do (
  set "DEL=%%a"
  set "COLOR_RED=%%b[31m"
  set "COLOR_GREEN=%%b[32m"
  set "COLOR_YELLOW=%%b[33m"
  set "COLOR_BLUE=%%b[34m"
  set "COLOR_RESET=%%b[0m"
)

REM =============================================================================
REM Utility Functions
REM =============================================================================

:log_info
echo [INFO] %~1
goto :eof

:log_success
echo %COLOR_GREEN%[PASS]%COLOR_RESET% %~1
goto :eof

:log_warning
echo %COLOR_YELLOW%[WARN]%COLOR_RESET% %~1
goto :eof

:log_error
echo %COLOR_RED%[FAIL]%COLOR_RESET% %~1
goto :eof

:log_header
echo.
echo ============================================================
echo %~1
echo ============================================================
goto :eof

:increment_test
set /a TOTAL_TESTS+=1
goto :eof

:record_pass
set /a PASSED_TESTS+=1
goto :eof

:record_fail
set /a FAILED_TESTS+=1
goto :eof

:print_summary
echo.
echo ============================================================
echo QUALITY CHECK SUMMARY
echo ============================================================
echo Total tests:  %TOTAL_TESTS%
echo Passed:       %PASSED_TESTS%
echo Failed:       %FAILED_TESTS%
echo.
if %FAILED_TESTS%==0 (
    echo %COLOR_GREEN%All quality checks passed!%COLOR_RESET%
    goto :eof
) else (
    echo %COLOR_RED%Some quality checks failed. Please review the errors above.%COLOR_RESET%
)
goto :eof

REM =============================================================================
REM Check 1: Import Tests
REM =============================================================================

:run_import_tests
call :log_header "PHASE 1: Module Import Tests"

set "IMPORT_FAILED=0"
set "IMPORT_TOTAL=0"

echo [INFO] Testing module imports...

REM Run Python import test
%PYTHON% -c "
import sys
import os
from pathlib import Path

project_dir = r'%PROJECT_DIR%'
maxwell_dir = os.path.join(project_dir, 'maxwell')

modules = []
for root, dirs, files in os.walk(maxwell_dir):
    for f in files:
        if f.endswith('.py') and not f.startswith('__'):
            rel = os.path.relpath(os.path.join(root, f), project_dir)
            mod = rel.replace(os.sep, '.').replace('.py', '')
            modules.append(mod)

failed = []
for mod in modules:
    try:
        __import__(mod)
        print(f'  OK: {mod}')
    except Exception as e:
        failed.append(mod)
        print(f'  FAIL: {mod} - {e}')

print(f'\nImported {len(modules) - len(failed)}/{len(modules)} modules')
if failed:
    print(f'{len(failed)} imports failed')
    sys.exit(1)
" 2>&1

if errorlevel 1 (
    call :record_fail
    call :log_error "Import tests failed"
    set /a IMPORT_FAILED=1
) else (
    call :record_pass
    call :log_success "All modules imported successfully"
)

set /a TOTAL_TESTS+=1
goto :eof

REM =============================================================================
REM Check 2: Citation Decorator Tests
REM =============================================================================

:run_citation_tests
call :log_header "PHASE 2: Citation Decorator Compliance"
set /a TOTAL_TESTS+=1

echo [INFO] Running citation decorator tests...

%PYTHON% -m pytest "%TESTS_DIR%\test_citation_decorator.py" -v --tb=short
if errorlevel 1 (
    call :record_fail
    call :log_error "Citation decorator tests failed"
) else (
    call :record_pass
    call :log_success "Citation decorator tests passed"
)
goto :eof

REM =============================================================================
REM Check 3: CGS Unit Tests
REM =============================================================================

:run_cgs_tests
call :log_header "PHASE 3: CGS Unit Compliance"
set /a TOTAL_TESTS+=1

echo [INFO] Running CGS unit tests...

%PYTHON% -m pytest "%TESTS_DIR%\test_cgs_units.py" -v --tb=short
if errorlevel 1 (
    call :record_fail
    call :log_error "CGS unit tests failed"
) else (
    call :record_pass
    call :log_success "CGS unit tests passed"
)
goto :eof

REM =============================================================================
REM Check 4: Physics Formula Tests
REM =============================================================================

:run_physics_tests
call :log_header "PHASE 4: Physics Formula Verification"

echo [INFO] Running Part IV electromagnetism tests...
set /a TOTAL_TESTS+=1

%PYTHON% -m pytest "%TESTS_DIR%\test_part_iv_electromagnetism.py" -v --tb=short
if errorlevel 1 (
    call :record_fail
    call :log_error "Part IV electromagnetism tests failed"
) else (
    call :record_pass
    call :log_success "Part IV electromagnetism tests passed"
)

echo [INFO] Running Part IV advanced tests...
set /a TOTAL_TESTS+=1

%PYTHON% -m pytest "%TESTS_DIR%\test_part_iv_advanced.py" -v --tb=short
if errorlevel 1 (
    call :record_fail
    call :log_error "Part IV advanced tests failed"
) else (
    call :record_pass
    call :log_success "Part IV advanced tests passed"
)
goto :eof

REM =============================================================================
REM Check 5: Equation Verification Pipeline
REM =============================================================================

:run_verification_pipeline
call :log_header "PHASE 5: Equation Verification Pipeline"

REM Check for JSON directories
if exist "%PROJECT_DIR%MAXWELL_VOLUME_1_MASTER_OUTPUT" (
    set "JSON_DIR1=%PROJECT_DIR%MAXWELL_VOLUME_1_MASTER_OUTPUT"
) else (
    set "JSON_DIR1="
)

if exist "%PROJECT_DIR%MAXWELL_VOLUME_2_MASTER_OUTPUT" (
    set "JSON_DIR2=%PROJECT_DIR%MAXWELL_VOLUME_2_MASTER_OUTPUT"
) else (
    set "JSON_DIR2="
)

if "%JSON_DIR1%"=="" if "%JSON_DIR2%"=="" (
    call :log_warning "No Mathpix JSON directories found. Skipping verification pipeline."
    call :log_info "Expected: MAXWELL_VOLUME_1_MASTER_OUTPUT, MAXWELL_VOLUME_2_MASTER_OUTPUT"
    goto :eof
)

set /a TOTAL_TESTS+=1
echo [INFO] Running equation verification pipeline...

if "%JSON_DIR2%"=="" (
    %PYTHON% "%PROJECT_DIR%run_verification.py" --json-dirs "%JSON_DIR1%" --maxwell-dir "%MAXWELL_DIR%" --output "%PROJECT_DIR%verification_report.md"
) else (
    %PYTHON% "%PROJECT_DIR%run_verification.py" --json-dirs "%JSON_DIR1%" "%JSON_DIR2%" --maxwell-dir "%MAXWELL_DIR%" --output "%PROJECT_DIR%verification_report.md"
)

if errorlevel 1 (
    call :record_fail
    call :log_error "Equation verification pipeline failed"
) else (
    call :record_pass
    call :log_success "Equation verification pipeline completed"
    call :log_info "Report: %PROJECT_DIR%verification_report.md"
)
goto :eof

REM =============================================================================
REM Check 6: Custom Quality Script
REM =============================================================================

:run_custom_quality_checks
call :log_header "PHASE 6: Custom Quality Checks"

if exist "%TESTS_DIR%\run_quality_checks.py" (
    set /a TOTAL_TESTS+=1
    echo [INFO] Running custom quality checks...

    %PYTHON% "%TESTS_DIR%\run_quality_checks.py"
    if errorlevel 1 (
        call :record_fail
        call :log_error "Custom quality checks failed"
    ) else (
        call :record_pass
        call :log_success "Custom quality checks passed"
    )
) else (
    call :log_info "No custom quality script found. Skipping."
)
goto :eof

REM =============================================================================
REM Help Display
REM =============================================================================

:show_help
echo Maxwell Quality Check Runner (Windows)
echo ======================================
echo.
echo Usage: run_quality_checks.bat [options]
echo.
echo Options:
echo   --import-only    Run only import tests
echo   --citation-only  Run only citation checks
echo   --cgs-only       Run only CGS unit tests
echo   --physics-only   Run only physics formula tests
echo   --verification   Run equation verification pipeline
echo   --all            Run all checks ^(default^)
echo   --verbose        Show detailed output
echo   --help           Show this help message
echo.
echo Examples:
echo   run_quality_checks.bat              REM Run all checks
echo   run_quality_checks.bat --verbose    REM Run all with detailed output
echo   run_quality_checks.bat --import-only  REM Run only import tests
echo.
echo Exit codes:
echo   0 - All checks passed
echo   1 - One or more checks failed
echo   2 - Configuration error
goto :eof

REM =============================================================================
REM Main Entry Point
REM =============================================================================

:main
REM Parse arguments
:parse_args
if "%~1"=="" goto :run_checks
if /i "%~1"=="--import-only" set "MODE=import" & shift & goto :parse_args
if /i "%~1"=="--citation-only" set "MODE=citation" & shift & goto :parse_args
if /i "%~1"=="--cgs-only" set "MODE=cgs" & shift & goto :parse_args
if /i "%~1"=="--physics-only" set "MODE=physics" & shift & goto :parse_args
if /i "%~1"=="--verification" set "MODE=verification" & shift & goto :parse_args
if /i "%~1"=="--all" set "MODE=all" & shift & goto :parse_args
if /i "%~1"=="--verbose" set "VERBOSE=true" & shift & goto :parse_args
if /i "%~1"=="--help" call :show_help & exit /b 0
echo %COLOR_RED%Unknown option: %~1%COLOR_RESET%
call :show_help
exit /b 2

:run_checks
REM Verify Python
where %PYTHON% >nul 2>&1
if errorlevel 1 (
    call :log_error "Python not found. Set PYTHON environment variable or install Python."
    exit /b 2
)

REM Verify directories
if not exist "%MAXWELL_DIR%" (
    call :log_error "Maxwell directory not found: %MAXWELL_DIR%"
    exit /b 2
)

if not exist "%TESTS_DIR%" (
    call :log_error "Tests directory not found: %TESTS_DIR%"
    exit /b 2
)

REM Run checks based on mode
if "%MODE%"=="import" call :run_import_tests & goto :print_summary_and_exit
if "%MODE%"=="citation" call :run_citation_tests & goto :print_summary_and_exit
if "%MODE%"=="cgs" call :run_cgs_tests & goto :print_summary_and_exit
if "%MODE%"=="physics" call :run_physics_tests & goto :print_summary_and_exit
if "%MODE%"=="verification" call :run_verification_pipeline & goto :print_summary_and_exit
if "%MODE%"=="all" (
    call :run_import_tests || true
    call :run_citation_tests || true
    call :run_cgs_tests || true
    call :run_physics_tests || true
    call :run_verification_pipeline || true
    call :run_custom_quality_checks || true
)

:print_summary_and_exit
call :print_summary
if %FAILED_TESTS%==0 (
    exit /b 0
) else (
    exit /b 1
)

REM Run main
call :main %*
