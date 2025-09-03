#!/usr/bin/env python3
"""
Test runner for Jupyter notebooks.
This script executes all notebooks in specified directories to ensure they run without errors.
"""

import os
import sys
import argparse
import json
import subprocess
import tempfile
import time
import traceback
from pathlib import Path
from typing import List, Dict, Tuple

try:
    import timeout_decorator
except ImportError:
    print("Warning: timeout_decorator not installed. Notebooks may run indefinitely.")
    timeout_decorator = None


class NotebookTester:
    def __init__(self, timeout_seconds: int = 600):
        self.timeout_seconds = timeout_seconds
        self.results = {
            'passed': [],
            'failed': [],
            'errors': {}
        }
        
    def find_notebooks(self, directory: str) -> List[Path]:
        """Find all .ipynb files in the given directory."""
        notebook_dir = Path(directory)
        if not notebook_dir.exists():
            print(f"Warning: Directory {directory} does not exist")
            return []
            
        notebooks = list(notebook_dir.glob('*.ipynb'))
        # Filter out checkpoint files
        notebooks = [nb for nb in notebooks if '.ipynb_checkpoints' not in str(nb)]
        return sorted(notebooks)
    
    def validate_notebook_format(self, notebook_path: Path) -> bool:
        """Check if notebook has valid JSON format."""
        try:
            with open(notebook_path, 'r', encoding='utf-8') as f:
                json.load(f)
            return True
        except json.JSONDecodeError as e:
            self.results['errors'][str(notebook_path)] = f"Invalid JSON format: {e}"
            return False
        except Exception as e:
            self.results['errors'][str(notebook_path)] = f"Error reading file: {e}"
            return False
    
    def execute_notebook_with_timeout(self, notebook_path: Path) -> Tuple[bool, str]:
        """Execute a notebook with timeout protection."""
        if timeout_decorator and self.timeout_seconds > 0:
            @timeout_decorator.timeout(self.timeout_seconds)
            def _execute_notebook():
                return self.execute_notebook(notebook_path)
            
            try:
                return _execute_notebook()
            except timeout_decorator.TimeoutError:
                error_msg = f"Notebook execution timed out after {self.timeout_seconds} seconds"
                return False, error_msg
        else:
            return self.execute_notebook(notebook_path)
    
    def execute_notebook(self, notebook_path: Path) -> Tuple[bool, str]:
        """Execute a notebook and return success status and error message."""
        try:
            # Create a temporary file for the executed notebook
            with tempfile.NamedTemporaryFile(suffix='.ipynb', delete=False) as temp_file:
                temp_path = temp_file.name
            
            # Use nbconvert to execute the notebook
            cmd = [
                'jupyter', 'nbconvert',
                '--to', 'notebook',
                '--execute',
                '--ExecutePreprocessor.timeout=60',  # 60 seconds per cell
                '--ExecutePreprocessor.allow_errors=False',
                '--output', temp_path,
                str(notebook_path)
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=self.timeout_seconds
            )
            
            # Clean up temp file
            try:
                os.unlink(temp_path)
            except:
                pass
                
            if result.returncode == 0:
                return True, ""
            else:
                error_msg = result.stderr or result.stdout
                return False, error_msg
                
        except subprocess.TimeoutExpired:
            return False, f"Execution timed out after {self.timeout_seconds} seconds"
        except Exception as e:
            return False, f"Execution error: {str(e)}\n{traceback.format_exc()}"
    
    def test_notebook(self, notebook_path: Path) -> bool:
        """Test a single notebook."""
        print(f"Testing: {notebook_path.name}")
        
        # First validate the notebook format
        if not self.validate_notebook_format(notebook_path):
            print(f"  ❌ FAILED - Invalid format")
            self.results['failed'].append(str(notebook_path))
            return False
        
        # Then execute the notebook
        start_time = time.time()
        success, error_msg = self.execute_notebook_with_timeout(notebook_path)
        execution_time = time.time() - start_time
        
        if success:
            print(f"  ✅ PASSED ({execution_time:.1f}s)")
            self.results['passed'].append(str(notebook_path))
            return True
        else:
            print(f"  ❌ FAILED ({execution_time:.1f}s)")
            self.results['failed'].append(str(notebook_path))
            self.results['errors'][str(notebook_path)] = error_msg
            
            # Save error details to file
            error_dir = Path('test-failures')
            error_dir.mkdir(exist_ok=True)
            error_file = error_dir / f"{notebook_path.stem}_error.txt"
            with open(error_file, 'w') as f:
                f.write(f"Notebook: {notebook_path}\n")
                f.write(f"Execution time: {execution_time:.1f}s\n")
                f.write(f"Error:\n{error_msg}\n")
            
            return False
    
    def test_directory(self, directory: str) -> bool:
        """Test all notebooks in a directory."""
        notebooks = self.find_notebooks(directory)
        
        if not notebooks:
            print(f"No notebooks found in {directory}")
            return True
        
        print(f"\nTesting {len(notebooks)} notebooks in {directory}/")
        print("=" * 60)
        
        all_passed = True
        for notebook in notebooks:
            success = self.test_notebook(notebook)
            if not success:
                all_passed = False
                
        return all_passed
    
    def print_summary(self):
        """Print test summary."""
        total = len(self.results['passed']) + len(self.results['failed'])
        print("\n" + "=" * 60)
        print("SUMMARY")
        print("=" * 60)
        print(f"Total notebooks tested: {total}")
        print(f"Passed: {len(self.results['passed'])}")
        print(f"Failed: {len(self.results['failed'])}")
        
        if self.results['failed']:
            print("\nFailed notebooks:")
            for notebook in self.results['failed']:
                print(f"  • {notebook}")
                if notebook in self.results['errors']:
                    # Show first few lines of error
                    error_lines = self.results['errors'][notebook].split('\n')
                    for line in error_lines[:3]:
                        if line.strip():
                            print(f"    {line.strip()}")
                    if len(error_lines) > 3:
                        print("    ...")
        
        print(f"\nSuccess rate: {len(self.results['passed'])/total*100:.1f}%")


def main():
    parser = argparse.ArgumentParser(description='Test Jupyter notebooks')
    parser.add_argument('--directory', '-d', required=True,
                      help='Directory containing notebooks to test')
    parser.add_argument('--timeout', '-t', type=int, default=600,
                      help='Timeout in seconds for each notebook (default: 600)')
    parser.add_argument('--verbose', '-v', action='store_true',
                      help='Verbose output')
    
    args = parser.parse_args()
    
    # Create tester instance
    tester = NotebookTester(timeout_seconds=args.timeout)
    
    # Test the directory
    success = tester.test_directory(args.directory)
    
    # Print summary
    tester.print_summary()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
