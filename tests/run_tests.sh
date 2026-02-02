#!/bin/bash
# Test runner script for workflow tests

set -e

echo "Installing test dependencies..."
pip3 install -r tests/requirements.txt 2>/dev/null || pip3 install -r tests/requirements.txt --break-system-packages

echo ""
echo "Running workflow validation tests..."
python3 -m pytest tests/test_workflow_validation.py -v

echo ""
echo "Running workflow integration tests..."
python3 -m pytest tests/test_workflow_integration.py -v

echo ""
echo "All tests passed!"