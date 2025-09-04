#!/usr/bin/env python3
"""
Simple notebook test script using nbconvert.
Alternative to the main test_notebooks.py if timeout_decorator is not available.
"""

import os
import sys
import subprocess
import json
from pathlib import Path


def find_notebooks(directory):
    """Find all .ipynb files in directory."""
    notebook_dir = Path(directory)
    if not notebook_dir.exists():
        print(f"Directory {directory} does not exist")
        return []
    
    notebooks = list(notebook_dir.glob('*.ipynb'))
    notebooks = [nb for nb in notebooks if '.ipynb_checkpoints' not in str(nb)]
    return sorted(notebooks)


def test_notebook(notebook_path):
    """Test a single notebook using nbconvert."""
    print(f"Testing {notebook_path.name}...", end=" ")
    
    # First check if it's valid JSON
    try:
        with open(notebook_path, 'r', encoding='utf-8') as f:
            json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON: {e}")
        return False
    except Exception as e:
        print(f"❌ Error reading: {e}")
        return False
    
    # Execute the notebook
    try:
        cmd = [
            'jupyter', 'nbconvert', 
            '--to', 'notebook',
            '--execute',
            '--ExecutePreprocessor.timeout=120',
            '--ExecutePreprocessor.allow_errors=False',
            '--stdout',
            str(notebook_path)
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
        
        if result.returncode == 0:
            print("✅ PASSED")
            return True
        else:
            print("❌ FAILED")
            print(f"Error: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ TIMEOUT")
        return False
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False


def main():
    if len(sys.argv) < 2:
        print("Usage: python simple_test.py <directory>")
        sys.exit(1)
    
    directory = sys.argv[1]
    notebooks = find_notebooks(directory)
    
    if not notebooks:
        print(f"No notebooks found in {directory}")
        return
    
    print(f"Testing {len(notebooks)} notebooks in {directory}/")
    print("-" * 50)
    
    passed = 0
    failed = 0
    
    for notebook in notebooks:
        if test_notebook(notebook):
            passed += 1
        else:
            failed += 1
    
    print("-" * 50)
    print(f"Results: {passed} passed, {failed} failed")
    
    if failed > 0:
        sys.exit(1)


if __name__ == '__main__':
    main()
