# Workflow Tests

Comprehensive test suite for the `check_arb.yml` GitHub Actions workflow.

## Test Structure

### `test_workflow_validation.py`
Unit tests that validate the workflow structure and configuration:
- Workflow name, triggers, and inputs
- Job configurations and matrix setup
- Step definitions and dependencies
- Cache configuration
- Artifact handling
- Edge cases and boundary conditions
- Regression tests

### `test_workflow_integration.py`
Integration tests that verify workflow behavior:
- Script integration and data flow
- Conditional logic
- Error handling
- Data flow between steps
- Security best practices
- Performance optimizations

## Running Tests

### Using the test runner script:
```bash
./tests/run_tests.sh
```

### Using Python directly:
```bash
# Install dependencies first
pip3 install -r tests/requirements.txt

# Run all tests
python3 -m unittest discover tests/

# Run specific test file
python3 -m unittest tests.test_workflow_validation
python3 -m unittest tests.test_workflow_integration

# Run with verbose output
python3 -m unittest tests.test_workflow_validation -v
```

### Using pytest (if available):
```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_workflow_validation.py -v

# Run specific test class
pytest tests/test_workflow_validation.py::TestWorkflowValidation -v

# Run specific test method
pytest tests/test_workflow_validation.py::TestWorkflowValidation::test_workflow_name_exists -v
```

## Test Coverage

The test suite covers:

1. **Workflow Structure** (40+ tests)
   - YAML syntax validation
   - Trigger configuration (workflow_dispatch, schedule)
   - Input definitions
   - Job definitions and dependencies
   - Matrix strategy and combinations

2. **Job Configuration** (20+ tests)
   - Runner configuration
   - Error handling (continue-on-error, fail-fast)
   - Matrix devices and variants
   - Matrix exclusions and inclusions
   - Device metadata completeness

3. **Step Validation** (30+ tests)
   - Checkout and dependency installation
   - Tool setup (arbextract, payload-dumper)
   - Firmware fetching and downloading
   - Cache restore and save
   - Firmware analysis
   - History updates
   - Artifact uploads
   - Cleanup operations

4. **Conditional Logic** (15+ tests)
   - force_recheck input handling
   - Cache hit/miss behavior
   - File existence checks
   - CN variant special handling
   - Skip file logic

5. **Integration & Data Flow** (20+ tests)
   - Script input/output formats
   - Environment variables
   - Data passing between steps
   - Artifact generation and consumption
   - Error propagation

6. **Edge Cases** (15+ tests)
   - Matrix combination counting
   - Cache key uniqueness
   - Empty results handling
   - Download failures and retries
   - Git operations with no changes

7. **Security & Best Practices** (10+ tests)
   - No hardcoded secrets
   - Pinned action versions
   - Secure external downloads (HTTPS)
   - Safe git configuration
   - File permissions

8. **Performance** (8+ tests)
   - Cache utilization
   - Parallel downloads (aria2c)
   - Matrix parallel execution
   - Conditional step optimization

9. **Regression Tests** (10+ tests)
   - Workflow file existence
   - YAML syntax validation
   - No deprecated actions
   - Script file existence
   - Output variable format

## Key Tests for force_recheck Feature

The test suite includes specific tests for the new `force_recheck` input:

- `test_workflow_dispatch_inputs`: Validates input definition
- `test_force_recheck_bypasses_cache`: Verifies cache bypass behavior
- `test_force_recheck_condition`: Tests conditional logic
- `test_cache_restore_step`: Validates conditional cache restore

## Test Philosophy

These tests follow best practices:
- **Comprehensive**: Cover normal cases, edge cases, and error conditions
- **Maintainable**: Clear test names and documentation
- **Fast**: No external dependencies, use mocks where appropriate
- **Reliable**: Deterministic, no flaky tests
- **Focused**: Each test validates one specific behavior

## Adding New Tests

When adding new workflow features:

1. Add structural validation tests in `test_workflow_validation.py`
2. Add behavior tests in `test_workflow_integration.py`
3. Add edge case tests for the new feature
4. Add regression tests to prevent future breakage
5. Update this README with new test coverage

## Continuous Integration

These tests should be run:
- Before committing workflow changes
- In pull request CI checks
- After deploying workflow updates
- As part of regular test suite runs