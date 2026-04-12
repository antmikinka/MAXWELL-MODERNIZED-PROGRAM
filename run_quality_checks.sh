#!/usr/bin/env bash
#
# Maxwell Quality Check Runner
# ============================
# Runs comprehensive quality checks on Maxwell Part IV modules.
#
# Usage:
#   ./run_quality_checks.sh [options]
#
# Options:
#   --import-only    Run only import tests
#   --citation-only  Run only citation checks
#   --cgs-only       Run only CGS unit tests
#   --physics-only   Run only physics formula tests
#   --verification   Run equation verification pipeline
#   --all            Run all checks (default)
#   --verbose        Show detailed output
#   --help           Show this help message
#
# Exit codes:
#   0 - All checks passed
#   1 - One or more checks failed
#   2 - Configuration error (missing dependencies)

set -euo pipefail

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
MAXWELL_DIR="$PROJECT_DIR/maxwell"
TESTS_DIR="$PROJECT_DIR/tests"
PYTHON="${PYTHON:-python}"
VERBOSE="${VERBOSE:-false}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Counters
TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0

# ── Utility Functions ─────────────────────────────────────────────

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[PASS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[FAIL]${NC} $1"
}

log_header() {
    echo ""
    echo "============================================================"
    echo "$1"
    echo "============================================================"
}

increment_test() {
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
}

record_pass() {
    PASSED_TESTS=$((PASSED_TESTS + 1))
}

record_fail() {
    FAILED_TESTS=$((FAILED_TESTS + 1))
}

print_summary() {
    echo ""
    echo "============================================================"
    echo "QUALITY CHECK SUMMARY"
    echo "============================================================"
    echo "Total tests:  $TOTAL_TESTS"
    echo -e "Passed:       ${GREEN}$PASSED_TESTS${NC}"
    echo -e "Failed:       ${RED}$FAILED_TESTS${NC}"
    echo ""

    if [ $FAILED_TESTS -eq 0 ]; then
        echo -e "${GREEN}All quality checks passed!${NC}"
        return 0
    else
        echo -e "${RED}Some quality checks failed. Please review the errors above.${NC}"
        return 1
    fi
}

# ── Check 1: Import Tests ─────────────────────────────────────────

run_import_tests() {
    log_header "PHASE 1: Module Import Tests"

    # Discover all Python modules in maxwell/
    local modules=()
    while IFS= read -r -d '' file; do
        # Convert file path to module name
        local rel_path="${file#$MAXWELL_DIR/}"
        local module_path="${rel_path//\//.}"
        module_path="${module_path%.py}"
        module_path="${module_path/__init__/}"
        module_path="${module_path%.}"

        # Skip empty or invalid module names
        if [[ -n "$module_path" && ! "$module_path" =~ ^__ ]]; then
            modules+=("$module_path")
        fi
    done < <(find "$MAXWELL_DIR" -name "*.py" -type f -print0)

    log_info "Found ${#modules[@]} modules to test"

    local failed_imports=()

    for module in "${modules[@]}"; do
        increment_test

        if [ "$VERBOSE" = true ]; then
            log_info "Testing import: maxwell.$module"
        fi

        if $PYTHON -c "import sys; sys.path.insert(0, '$PROJECT_DIR'); import maxwell.$module" 2>/dev/null; then
            record_pass
            [ "$VERBOSE" = true ] && log_success "maxwell.$module"
        else
            record_fail
            log_error "Failed to import: maxwell.$module"
            failed_imports+=("maxwell.$module")
        fi
    done

    if [ ${#failed_imports[@]} -eq 0 ]; then
        log_success "All ${#modules[@]} modules imported successfully"
    else
        log_error "${#failed_imports[@]} modules failed to import"
    fi

    return ${#failed_imports[@]}
}

# ── Check 2: Citation Decorator Tests ─────────────────────────────

run_citation_tests() {
    log_header "PHASE 2: Citation Decorator Compliance"

    increment_test

    log_info "Running citation decorator tests..."

    if $PYTHON -m pytest "$TESTS_DIR/test_citation_decorator.py" -v --tb=short 2>&1; then
        record_pass
        log_success "Citation decorator tests passed"
    else
        record_fail
        log_error "Citation decorator tests failed"
    fi
}

# ── Check 3: CGS Unit Tests ───────────────────────────────────────

run_cgs_tests() {
    log_header "PHASE 3: CGS Unit Compliance"

    increment_test

    log_info "Running CGS unit tests..."

    if $PYTHON -m pytest "$TESTS_DIR/test_cgs_units.py" -v --tb=short 2>&1; then
        record_pass
        log_success "CGS unit tests passed"
    else
        record_fail
        log_error "CGS unit tests failed"
    fi
}

# ── Check 4: Physics Formula Tests ────────────────────────────────

run_physics_tests() {
    log_header "PHASE 4: Physics Formula Verification"

    increment_test

    log_info "Running Part IV electromagnetism tests..."

    if $PYTHON -m pytest "$TESTS_DIR/test_part_iv_electromagnetism.py" -v --tb=short 2>&1; then
        record_pass
        log_success "Part IV electromagnetism tests passed"
    else
        record_fail
        log_error "Part IV electromagnetism tests failed"
    fi

    increment_test

    log_info "Running Part IV advanced tests..."

    if $PYTHON -m pytest "$TESTS_DIR/test_part_iv_advanced.py" -v --tb=short 2>&1; then
        record_pass
        log_success "Part IV advanced tests passed"
    else
        record_fail
        log_error "Part IV advanced tests failed"
    fi
}

# ── Check 5: Equation Verification Pipeline ───────────────────────

run_verification_pipeline() {
    log_header "PHASE 5: Equation Verification Pipeline"

    # Check if JSON directories exist
    local json_dirs=()
    for dir in MAXWELL_VOLUME_1_MASTER_OUTPUT MAXWELL_VOLUME_2_MASTER_OUTPUT; do
        if [ -d "$PROJECT_DIR/$dir" ]; then
            json_dirs+=("$PROJECT_DIR/$dir")
        fi
    done

    if [ ${#json_dirs[@]} -eq 0 ]; then
        log_warning "No Mathpix JSON directories found. Skipping verification pipeline."
        log_info "Expected directories: MAXWELL_VOLUME_1_MASTER_OUTPUT, MAXWELL_VOLUME_2_MASTER_OUTPUT"
        return 0
    fi

    increment_test

    log_info "Running equation verification pipeline..."

    local json_dir_args=""
    for dir in "${json_dirs[@]}"; do
        json_dir_args="$json_dir_args --json-dirs $dir"
    done

    if $PYTHON "$PROJECT_DIR/run_verification.py" \
        $json_dir_args \
        --maxwell-dir "$MAXWELL_DIR" \
        --output "$PROJECT_DIR/verification_report.md" 2>&1; then
        record_pass
        log_success "Equation verification pipeline completed"
        log_info "Report: $PROJECT_DIR/verification_report.md"
    else
        record_fail
        log_error "Equation verification pipeline failed"
    fi
}

# ── Check 6: Custom Quality Script ────────────────────────────────

run_custom_quality_checks() {
    log_header "PHASE 6: Custom Quality Checks"

    # Run custom Python quality checks
    local quality_script="$TESTS_DIR/run_quality_checks.py"

    if [ -f "$quality_script" ]; then
        increment_test
        log_info "Running custom quality checks..."

        if $PYTHON "$quality_script" 2>&1; then
            record_pass
            log_success "Custom quality checks passed"
        else
            record_fail
            log_error "Custom quality checks failed"
        fi
    else
        log_info "No custom quality script found. Skipping."
    fi
}

# ── Main Execution ────────────────────────────────────────────────

show_help() {
    cat << EOF
Maxwell Quality Check Runner
============================

Usage: $(basename "$0") [options]

Options:
  --import-only    Run only import tests
  --citation-only  Run only citation checks
  --cgs-only       Run only CGS unit tests
  --physics-only   Run only physics formula tests
  --verification   Run equation verification pipeline
  --all            Run all checks (default)
  --verbose        Show detailed output
  --help           Show this help message

Examples:
  $(basename "$0")              # Run all checks
  $(basename "$0") --verbose    # Run all checks with detailed output
  $(basename "$0") --import-only  # Run only import tests

Exit codes:
  0 - All checks passed
  1 - One or more checks failed
  2 - Configuration error
EOF
}

main() {
    local mode="all"

    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --import-only)
                mode="import"
                shift
                ;;
            --citation-only)
                mode="citation"
                shift
                ;;
            --cgs-only)
                mode="cgs"
                shift
                ;;
            --physics-only)
                mode="physics"
                shift
                ;;
            --verification)
                mode="verification"
                shift
                ;;
            --all)
                mode="all"
                shift
                ;;
            --verbose)
                VERBOSE=true
                shift
                ;;
            --help|-h)
                show_help
                exit 0
                ;;
            *)
                log_error "Unknown option: $1"
                show_help
                exit 2
                ;;
        esac
    done

    # Verify Python is available
    if ! command -v "$PYTHON" &> /dev/null; then
        log_error "Python not found. Set PYTHON environment variable or install Python."
        exit 2
    fi

    # Verify project structure
    if [ ! -d "$MAXWELL_DIR" ]; then
        log_error "Maxwell directory not found: $MAXWELL_DIR"
        exit 2
    fi

    if [ ! -d "$TESTS_DIR" ]; then
        log_error "Tests directory not found: $TESTS_DIR"
        exit 2
    fi

    # Run checks based on mode
    case $mode in
        import)
            run_import_tests
            ;;
        citation)
            run_citation_tests
            ;;
        cgs)
            run_cgs_tests
            ;;
        physics)
            run_physics_tests
            ;;
        verification)
            run_verification_pipeline
            ;;
        all)
            run_import_tests || true
            run_citation_tests || true
            run_cgs_tests || true
            run_physics_tests || true
            run_verification_pipeline || true
            run_custom_quality_checks || true
            ;;
    esac

    print_summary
}

# Run main function
main "$@"
