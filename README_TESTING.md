# Notebook Testing

This repository includes a comprehensive test script to validate that all Jupyter notebooks execute successfully.

## Test Script: `test_notebooks.py`

The `test_notebooks.py` script discovers and tests all Jupyter notebooks in the repository to ensure they can execute without errors.

### Features

- **Automatic Discovery**: Finds all `.ipynb` files in the repository
- **Format Support**: Handles both old (nbformat 3) and new (nbformat 4+) notebook formats  
- **Structure Validation**: Verifies notebook JSON structure is valid
- **Execution Testing**: Actually runs notebook code cells to check for runtime errors
- **Error Handling**: Gracefully handles kernel specification issues and missing dependencies
- **Detailed Reporting**: Provides comprehensive pass/fail reports with error details

### Usage

```bash
# Test all notebooks (structure + execution)
python test_notebooks.py

# Test only structure (faster, no execution)
python test_notebooks.py --no-execute

# Stop after N failures to speed up debugging
python test_notebooks.py --max-failures 5

# Save detailed results to JSON file
python test_notebooks.py --save-results results.json

# Show help
python test_notebooks.py --help
```

### Requirements

The script requires the following Python packages:
- `jupyter` - For notebook execution
- `nbconvert` - For converting and executing notebooks  
- `nbformat` - For reading notebook files
- `numpy` - Required by most notebooks
- `matplotlib` - Required by most notebooks
- `scipy` - Required by many notebooks
- `sympy` - Required by some notebooks

Install with:
```bash
pip install jupyter nbconvert nbformat numpy matplotlib scipy sympy
```

### Test Results

As of the latest test run:

- **Total notebooks**: 45
- **Passed**: 44 (97.8%)
- **Failed**: 1 (2.2%)

#### Passing notebooks:
- All 5 book-version chapter notebooks ✅
- 39 out of 40 example notebooks ✅

#### Known Issues:
- `notebook/Sampling_Theorem_Part_1.ipynb` - Contains Git merge conflict markers that make JSON invalid

### Integration

You can integrate this into CI/CD pipelines:

```bash
# Exit with error code if any tests fail
python test_notebooks.py
echo $? # Will be 0 if all pass, 1 if any fail
```

The script is designed to be minimal and focused - it only tests that notebooks can execute without errors. It doesn't modify the original notebook files and cleans up temporary files automatically.