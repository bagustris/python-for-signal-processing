#!/bin/bash
# Quick test runner for CI/CD environments
# This script installs dependencies and runs the notebook tests

set -e

echo "=== Notebook Testing Runner ==="
echo "Installing required dependencies..."

# Install Python dependencies
pip install -q jupyter nbconvert nbformat numpy matplotlib scipy sympy

echo "Dependencies installed successfully."
echo ""

# Run the tests
echo "Running notebook tests..."
python test_notebooks.py --save-results ci_test_results.json

# Check the exit code
if [ $? -eq 0 ]; then
    echo ""
    echo "✅ All notebook tests passed!"
else
    echo ""
    echo "❌ Some notebook tests failed. Check the output above for details."
    exit 1
fi