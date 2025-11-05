# Chain Reflow Integration Tests

Comprehensive end-to-end integration tests for chain_reflow analysis tools.

## Test Coverage

### ✅ Analysis Tools (Priority 1)
- **Matryoshka Analysis** (5 tests) - Hierarchical nesting analysis
- **Causality Analysis** (4 tests) - Correlation vs causation detection
- **Creative Linking** (4 tests) - Orthogonal architecture linking

### ✅ Workflow Validation (2 tests)
- JSON validity of all workflow files
- Meta-analysis workflow structure validation
- Verification that workflow_runner.py references removed

### ✅ Schema Validation (2 tests)
- System-of-systems graph schema
- Analysis output schemas

### ✅ End-to-End Flow (2 tests)
- Complete analysis pipeline (all 3 tools)
- Output verification across all tools

**Total: 19 tests**

---

## Prerequisites

```bash
# Install pytest
pip3 install pytest

# Verify test data exists
ls test_architectures/specs/machine/graphs/system_of_systems_graph.json
```

---

## Running Tests

### Run All Tests
```bash
pytest tests/test_integration_end_to_end.py -v
```

### Run Specific Test Class
```bash
# Matryoshka tests only
pytest tests/test_integration_end_to_end.py::TestMatryoshkaAnalysis -v

# Causality tests only
pytest tests/test_integration_end_to_end.py::TestCausalityAnalysis -v

# Creative linking tests only
pytest tests/test_integration_end_to_end.py::TestCreativeLinking -v

# Workflow validation only
pytest tests/test_integration_end_to_end.py::TestWorkflowValidation -v

# End-to-end flow tests
pytest tests/test_integration_end_to_end.py::TestEndToEndFlow -v
```

### Run Specific Test
```bash
pytest tests/test_integration_end_to_end.py::TestMatryoshkaAnalysis::test_matryoshka_json_output -v
```

### Run with More Details
```bash
# Show print statements
pytest tests/test_integration_end_to_end.py -v -s

# Show full tracebacks
pytest tests/test_integration_end_to_end.py -v --tb=long

# Stop on first failure
pytest tests/test_integration_end_to_end.py -v -x
```

---

## Test Data

Tests use architectures in `test_architectures/`:

- **auth_service_architecture.json** - JWT authentication service
- **api_gateway_architecture.json** - API gateway and router
- **user_mgmt_architecture.json** - User CRUD operations
- **service_arch_index.json** - Index file for system-of-systems graph
- **specs/machine/graphs/system_of_systems_graph.json** - Generated graph

All services are UAF (Unified Architecture Framework) compliant.

---

## What Tests Validate

### 1. CLI Functionality (Priority 1 Verification)
- ✅ `--help` flags work for all tools
- ✅ Tools accept file paths as arguments
- ✅ Tools produce output (text, JSON, markdown)
- ✅ Error handling for missing files
- ✅ Exit codes are correct (0 = success, 1 = error)

### 2. Analysis Quality
- ✅ Matryoshka detects hierarchy levels (component, system, etc.)
- ✅ Causality identifies service dependencies
- ✅ Creative linking assesses orthogonality correctly
- ✅ Tools produce non-empty, meaningful output

### 3. Output Formats
- ✅ JSON output is valid and parseable
- ✅ JSON contains expected structure (dict with content)
- ✅ Text output contains expected keywords
- ✅ Output files are created when requested

### 4. Workflow Integration
- ✅ All workflow JSON files are valid
- ✅ Workflows have required metadata fields
- ✅ Meta-analysis workflow documents LLM-assisted execution
- ✅ No references to removed workflow_runner.py in commands

### 5. End-to-End Pipeline
- ✅ All three tools can run sequentially on same data
- ✅ Complete analysis pipeline succeeds
- ✅ Each tool produces substantial output (>100 chars)

---

## Test Architecture

```
tests/
├── __init__.py                      # Package init
├── README.md                        # This file
└── test_integration_end_to_end.py   # Main integration tests
    ├── TestMatryoshkaAnalysis       # 5 tests
    ├── TestCausalityAnalysis        # 4 tests
    ├── TestCreativeLinking          # 4 tests
    ├── TestWorkflowValidation       # 2 tests
    ├── TestOutputSchemas            # 2 tests
    └── TestEndToEndFlow             # 2 tests
```

---

## Expected Results

All 19 tests should pass:

```
============================== test session starts ==============================
...
tests/test_integration_end_to_end.py::TestMatryoshkaAnalysis::... PASSED
tests/test_integration_end_to_end.py::TestCausalityAnalysis::... PASSED
tests/test_integration_end_to_end.py::TestCreativeLinking::... PASSED
tests/test_integration_end_to_end.py::TestWorkflowValidation::... PASSED
tests/test_integration_end_to_end.py::TestOutputSchemas::... PASSED
tests/test_integration_end_to_end.py::TestEndToEndFlow::... PASSED
============================== 19 passed in ~2.3s =============================
```

---

## Continuous Integration

These tests are designed for CI/CD pipelines:

```yaml
# Example GitHub Actions workflow
name: Integration Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          pip install pytest
      - name: Run integration tests
        run: pytest tests/test_integration_end_to_end.py -v
```

---

## Adding New Tests

To add new tests:

1. **Create new test class** in `test_integration_end_to_end.py`
   ```python
   class TestNewFeature:
       """Tests for new feature"""

       def test_new_functionality(self):
           """Test description"""
           # Test code
           assert True
   ```

2. **Use existing fixtures** for common setup:
   - `test_graph_path` - Path to test graph
   - `test_graph_data` - Loaded test graph dict
   - `temp_output_file` - Temporary file for output

3. **Follow naming convention**: `test_<feature>_<scenario>`

4. **Run new tests**:
   ```bash
   pytest tests/test_integration_end_to_end.py::TestNewFeature -v
   ```

---

## Troubleshooting

### Tests fail with "File not found"
```bash
# Ensure test data exists
python3 -c "from pathlib import Path; print(Path('test_architectures/specs/machine/graphs/system_of_systems_graph.json').exists())"

# Regenerate if needed (from reflow)
cd test_architectures
python3 /path/to/reflow/tools/system_of_systems_graph_v2.py service_arch_index.json
```

### Import errors
```bash
# Ensure you're running from repo root
cd /path/to/chain_reflow
pytest tests/test_integration_end_to_end.py -v
```

### Pytest not found
```bash
pip3 install pytest
```

---

## Related Documentation

- **Priority 1**: `docs/PRIORITY_1_COMPLETION_SUMMARY.md` - CLI tool implementation
- **Priority 2**: `docs/INTEGRATION_TEST_GAP_ANALYSIS.md` - Gap analysis that motivated these tests
- **CLAUDE.md**: Workflow execution model (LLM-assisted)
- **README.md**: Main project documentation

---

**Test Suite Created**: 2025-11-05
**Priority**: 3 (Integration Testing)
**Status**: ✅ Complete - All 19 tests passing
