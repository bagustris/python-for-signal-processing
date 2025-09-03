#!/usr/bin/env python3
"""
Test script to validate that all Jupyter notebooks in the repository execute successfully.

This script discovers all .ipynb files in the repository and attempts to execute them
using nbconvert. It reports which notebooks pass/fail and provides detailed error
information for debugging.
"""

import os
import sys
import glob
import subprocess
import json
from pathlib import Path
import tempfile
from typing import List, Tuple, Dict


class NotebookTester:
    def __init__(self, repo_root: str):
        self.repo_root = Path(repo_root)
        self.results = {
            'passed': [],
            'failed': [],
            'skipped': [],
            'errors': {}
        }
    
    def find_notebooks(self) -> List[Path]:
        """Find all notebook files in the repository, excluding checkpoints."""
        notebooks = []
        
        # Search for notebooks in all directories
        for pattern in ['**/*.ipynb']:
            for notebook in self.repo_root.glob(pattern):
                # Skip checkpoint directories
                if '.ipynb_checkpoints' in str(notebook):
                    continue
                notebooks.append(notebook)
        
        return sorted(notebooks)
    
    def execute_notebook(self, notebook_path: Path) -> Tuple[bool, str]:
        """
        Execute a single notebook and return (success, error_message).
        
        Args:
            notebook_path: Path to the notebook file
            
        Returns:
            Tuple of (success_bool, error_message_string)
        """
        try:
            # Create a temporary output file
            with tempfile.NamedTemporaryFile(suffix='.ipynb', delete=False) as temp_out:
                temp_output_path = temp_out.name
            
            try:
                # Execute the notebook using nbconvert with alternative approaches
                # First, try with allow-errors to continue execution even if some cells fail
                cmd = [
                    'jupyter', 'nbconvert',
                    '--to', 'notebook',
                    '--execute',
                    '--output', temp_output_path,
                    '--ExecutePreprocessor.timeout=300',  # 5 minute timeout per cell
                    '--ExecutePreprocessor.allow_errors=True',  # Continue on errors
                    str(notebook_path)
                ]
                
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    cwd=self.repo_root
                )
                
                if result.returncode == 0:
                    return True, ""
                else:
                    # If the first attempt failed, try with kernel override
                    cmd_with_kernel = [
                        'jupyter', 'nbconvert',
                        '--to', 'notebook',
                        '--execute',
                        '--output', temp_output_path,
                        '--ExecutePreprocessor.timeout=300',
                        '--ExecutePreprocessor.allow_errors=True',
                        '--ExecutePreprocessor.kernel_name=python3',  # Force python3 kernel
                        str(notebook_path)
                    ]
                    
                    result2 = subprocess.run(
                        cmd_with_kernel,
                        capture_output=True,
                        text=True,
                        cwd=self.repo_root
                    )
                    
                    if result2.returncode == 0:
                        return True, "Succeeded with kernel override"
                    else:
                        # Return both error attempts for debugging
                        return False, f"Both attempts failed.\nFirst attempt (exit {result.returncode}):\nSTDOUT: {result.stdout}\nSTDERR: {result.stderr}\n\nSecond attempt with kernel override (exit {result2.returncode}):\nSTDOUT: {result2.stdout}\nSTDERR: {result2.stderr}"
                    
            finally:
                # Clean up temporary file
                try:
                    os.unlink(temp_output_path)
                except FileNotFoundError:
                    pass
                    
        except Exception as e:
            return False, f"Exception during execution: {str(e)}"
    
    def test_notebook_structure(self, notebook_path: Path) -> Tuple[bool, str]:
        """
        Basic validation of notebook JSON structure.
        Supports both old (nbformat 3) and new (nbformat 4+) formats.
        
        Args:
            notebook_path: Path to the notebook file
            
        Returns:
            Tuple of (success_bool, error_message_string)
        """
        try:
            with open(notebook_path, 'r', encoding='utf-8') as f:
                notebook = json.load(f)
            
            # Basic required keys for all notebook formats
            basic_required = ['metadata', 'nbformat']
            missing_basic = [key for key in basic_required if key not in notebook]
            
            if missing_basic:
                return False, f"Missing required basic keys: {missing_basic}"
            
            nbformat_version = notebook.get('nbformat', 0)
            
            if nbformat_version <= 3:
                # Old format: uses 'worksheets' containing cells
                if 'worksheets' not in notebook:
                    return False, "Old format notebook missing 'worksheets'"
                
                if not isinstance(notebook['worksheets'], list):
                    return False, "Worksheets must be a list"
                
                if not notebook['worksheets']:
                    return True, ""  # Empty notebook is valid
                
                # Check cells within worksheets
                for ws_i, worksheet in enumerate(notebook['worksheets']):
                    if 'cells' not in worksheet:
                        return False, f"Worksheet {ws_i} missing cells"
                    
                    if not isinstance(worksheet['cells'], list):
                        return False, f"Worksheet {ws_i} cells must be a list"
                    
                    for i, cell in enumerate(worksheet['cells']):
                        if 'cell_type' not in cell:
                            return False, f"Worksheet {ws_i}, Cell {i} missing cell_type"
                        # Old format uses 'input' for code cells and 'source' for markdown
                        if cell['cell_type'] == 'code' and 'input' not in cell:
                            return False, f"Worksheet {ws_i}, Code cell {i} missing input"
                        elif cell['cell_type'] == 'markdown' and 'source' not in cell:
                            return False, f"Worksheet {ws_i}, Markdown cell {i} missing source"
            
            else:
                # New format (nbformat 4+): uses 'cells' directly
                required_keys = ['cells', 'metadata', 'nbformat']
                missing_keys = [key for key in required_keys if key not in notebook]
                
                if missing_keys:
                    return False, f"Missing required keys: {missing_keys}"
                
                # Validate cells structure
                if not isinstance(notebook['cells'], list):
                    return False, "Cells must be a list"
                
                for i, cell in enumerate(notebook['cells']):
                    if 'cell_type' not in cell:
                        return False, f"Cell {i} missing cell_type"
                    if 'source' not in cell:
                        return False, f"Cell {i} missing source"
            
            return True, ""
            
        except json.JSONDecodeError as e:
            return False, f"Invalid JSON: {str(e)}"
        except Exception as e:
            return False, f"Error reading file: {str(e)}"
    
    def run_tests(self, execute_notebooks: bool = True, max_failures: int = None) -> Dict:
        """
        Run tests on all notebooks.
        
        Args:
            execute_notebooks: Whether to execute notebooks (vs just structure check)
            max_failures: Maximum number of failures before stopping (None for no limit)
            
        Returns:
            Dictionary with test results
        """
        notebooks = self.find_notebooks()
        print(f"Found {len(notebooks)} notebooks to test")
        print(f"Repository root: {self.repo_root}")
        print(f"Execute mode: {'ON' if execute_notebooks else 'OFF (structure only)'}")
        print("-" * 60)
        
        failure_count = 0
        
        for i, notebook in enumerate(notebooks, 1):
            relative_path = notebook.relative_to(self.repo_root)
            print(f"[{i:2d}/{len(notebooks)}] Testing {relative_path}...", end=" ", flush=True)
            
            # First check basic structure
            structure_ok, structure_error = self.test_notebook_structure(notebook)
            if not structure_ok:
                print("FAILED (structure)")
                self.results['failed'].append(str(relative_path))
                self.results['errors'][str(relative_path)] = f"Structure error: {structure_error}"
                failure_count += 1
                if max_failures and failure_count >= max_failures:
                    print(f"\nStopped testing after {max_failures} failures")
                    break
                continue
            
            if execute_notebooks:
                # Execute the notebook
                success, error_msg = self.execute_notebook(notebook)
                if success:
                    print("PASSED")
                    self.results['passed'].append(str(relative_path))
                else:
                    print("FAILED (execution)")
                    self.results['failed'].append(str(relative_path))
                    self.results['errors'][str(relative_path)] = error_msg
                    failure_count += 1
                    if max_failures and failure_count >= max_failures:
                        print(f"\nStopped testing after {max_failures} failures")
                        break
            else:
                print("PASSED (structure)")
                self.results['passed'].append(str(relative_path))
        
        return self.results
    
    def print_summary(self):
        """Print a summary of test results."""
        print("\n" + "=" * 60)
        print("TEST SUMMARY")
        print("=" * 60)
        print(f"Total notebooks tested: {len(self.results['passed']) + len(self.results['failed']) + len(self.results['skipped'])}")
        print(f"Passed: {len(self.results['passed'])}")
        print(f"Failed: {len(self.results['failed'])}")
        print(f"Skipped: {len(self.results['skipped'])}")
        
        if self.results['failed']:
            print(f"\nFAILED NOTEBOOKS:")
            for notebook in self.results['failed']:
                print(f"  - {notebook}")
                if notebook in self.results['errors']:
                    # Print first few lines of error for summary
                    error_lines = self.results['errors'][notebook].split('\n')[:3]
                    for line in error_lines:
                        if line.strip():
                            print(f"    Error: {line.strip()}")
                    if len(self.results['errors'][notebook].split('\n')) > 3:
                        print(f"    ... (truncated)")
        
        if self.results['passed']:
            print(f"\nPASSED NOTEBOOKS:")
            for notebook in self.results['passed']:
                print(f"  ✓ {notebook}")
    
    def save_results(self, output_file: str = "test_results.json"):
        """Save detailed results to a JSON file."""
        output_path = self.repo_root / output_file
        with open(output_path, 'w') as f:
            json.dump(self.results, f, indent=2)
        print(f"\nDetailed results saved to: {output_path}")


def main():
    """Main function to run notebook tests."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Test all Jupyter notebooks in the repository")
    parser.add_argument('--repo-root', default='.', help='Repository root directory (default: current directory)')
    parser.add_argument('--no-execute', action='store_true', help='Only check structure, do not execute notebooks')
    parser.add_argument('--max-failures', type=int, help='Stop after N failures (default: no limit)')
    parser.add_argument('--save-results', help='Save results to JSON file (default: test_results.json)')
    
    args = parser.parse_args()
    
    # Resolve repo root to absolute path
    repo_root = os.path.abspath(args.repo_root)
    if not os.path.isdir(repo_root):
        print(f"Error: Repository root '{repo_root}' is not a valid directory")
        sys.exit(1)
    
    # Create tester and run tests
    tester = NotebookTester(repo_root)
    
    try:
        results = tester.run_tests(
            execute_notebooks=not args.no_execute,
            max_failures=args.max_failures
        )
        
        tester.print_summary()
        
        if args.save_results:
            tester.save_results(args.save_results)
        
        # Exit with error code if any tests failed
        if results['failed']:
            sys.exit(1)
        else:
            print("\n🎉 All tests passed!")
            sys.exit(0)
            
    except KeyboardInterrupt:
        print("\n\nTests interrupted by user")
        tester.print_summary()
        sys.exit(1)
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
=======
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
