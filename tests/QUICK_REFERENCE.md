# Quick Reference - Workflow Tests

## Run All Tests
```bash
./tests/run_tests.sh
# OR
python3 -m unittest discover tests/
```

## Test Statistics
- **97 tests** across 3 test files
- **1,487 lines** of test code
- **100% pass rate**

## Test Files Overview

| File | Tests | Focus |
|------|-------|-------|
| `test_workflow_validation.py` | 41 | Structure, configuration, steps |
| `test_workflow_integration.py` | 30 | Behavior, integration, data flow |
| `test_workflow_additional.py` | 26 | Edge cases, regressions, security |

## force_recheck Feature Coverage

✅ Input definition (type, default, description)
✅ Cache bypass behavior
✅ Conditional logic
✅ Type safety (boolean vs string)
✅ Integration with workflow steps

## Key Test Commands

```bash
# Run specific test file
python3 -m unittest tests.test_workflow_validation

# Run specific test class
python3 -m unittest tests.test_workflow_validation.TestWorkflowValidation

# Run specific test
python3 -m unittest tests.test_workflow_validation.TestWorkflowValidation.test_workflow_dispatch_inputs

# Verbose output
python3 -m unittest discover tests/ -v

# Using pytest (if installed)
pytest tests/ -v
pytest tests/ -k force_recheck  # Run only force_recheck related tests
```

## What's Tested

### Structure (20+ tests)
- YAML syntax, workflow name, triggers
- Jobs, steps, matrix configuration
- Device/variant combinations
- Action versions

### Behavior (25+ tests)
- Input handling (force_recheck)
- Cache logic (restore/save)
- Conditional execution
- Data flow between steps
- Error handling

### Security (10+ tests)
- No hardcoded secrets
- Pinned action versions
- HTTPS downloads
- Safe git operations

### Performance (8+ tests)
- Cache optimization
- Parallel downloads (aria2c)
- Matrix parallelization
- Conditional skipping

### Edge Cases (15+ tests)
- Empty results
- Missing files
- Download failures
- Network errors
- Git no-changes

### Regressions (19+ tests)
- aria2c vs wget
- python3 vs python
- Cache version explicit
- Artifact structure

## Test Success Indicators

✅ All 97 tests pass
✅ No flaky tests
✅ Fast execution (< 0.3 seconds)
✅ No external dependencies
✅ Clear error messages

## Adding New Tests

1. Add test to appropriate file:
   - Structure/config → `test_workflow_validation.py`
   - Behavior/integration → `test_workflow_integration.py`
   - Edge cases/security → `test_workflow_additional.py`

2. Follow naming convention:
   ```python
   def test_feature_description(self):
       """Brief description of what is tested."""
       # Test implementation
   ```

3. Run tests to verify:
   ```bash
   python3 -m unittest discover tests/ -v
   ```

## Troubleshooting

### YAML 'on' key issue
Tests handle the YAML parser converting `on:` to boolean `True`:
```python
if True in workflow:
    workflow['on'] = workflow.pop(True)
```

### Module not found
Install dependencies:
```bash
pip3 install -r tests/requirements.txt
```

### File path issues
Tests use relative paths from test file location:
```python
workflow_path = Path(__file__).parent.parent / '.github' / 'workflows' / 'check_arb.yml'
```

## Documentation

- Full details: `tests/README.md`
- Test summary: `tests/TEST_SUMMARY.md`
- This guide: `tests/QUICK_REFERENCE.md`