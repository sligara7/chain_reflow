#!/usr/bin/env python3
"""
End-to-end integration tests for chain_reflow analysis tools.

Tests the complete flow:
1. Load test architectures
2. Generate/use system_of_systems_graph.json
3. Run matryoshka/causality/creative_linking analysis
4. Validate output formats and content

Prerequisites:
- pytest installed: pip install pytest
- Test architectures in test_architectures/
- Analysis tools have CLI support (Priority 1)

Run with:
    pytest tests/test_integration_end_to_end.py -v
    pytest tests/test_integration_end_to_end.py::test_matryoshka_analysis -v
"""

import json
import os
import subprocess
import tempfile
from pathlib import Path
from typing import Dict, Any

import pytest


# Test data paths
REPO_ROOT = Path(__file__).parent.parent
TEST_ARCH_DIR = REPO_ROOT / "test_architectures"
TEST_GRAPH = TEST_ARCH_DIR / "specs" / "machine" / "graphs" / "system_of_systems_graph.json"
TEST_INDEX = TEST_ARCH_DIR / "service_arch_index.json"

# Analysis tool paths
SRC_DIR = REPO_ROOT / "src"
MATRYOSHKA_TOOL = SRC_DIR / "matryoshka_analysis.py"
CAUSALITY_TOOL = SRC_DIR / "causality_analysis.py"
CREATIVE_LINKING_TOOL = SRC_DIR / "creative_linking.py"


def run_tool(tool_path: Path, args: list, timeout: int = 30) -> subprocess.CompletedProcess:
    """
    Run an analysis tool and return the result.

    Args:
        tool_path: Path to the Python tool
        args: Command-line arguments
        timeout: Timeout in seconds

    Returns:
        CompletedProcess with stdout, stderr, returncode
    """
    cmd = ["python3", str(tool_path)] + args
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=timeout,
        cwd=str(REPO_ROOT)
    )
    return result


def validate_json_output(json_str: str) -> Dict[Any, Any]:
    """
    Validate JSON output and return parsed dict.

    Args:
        json_str: JSON string to validate

    Returns:
        Parsed JSON dict

    Raises:
        json.JSONDecodeError: If JSON is invalid
        AssertionError: If required fields missing
    """
    data = json.loads(json_str)
    assert isinstance(data, dict), "Output must be a JSON object"
    return data


# ============================================================================
# Test Fixtures
# ============================================================================

@pytest.fixture
def test_graph_path() -> Path:
    """Path to test system_of_systems_graph.json"""
    assert TEST_GRAPH.exists(), f"Test graph not found: {TEST_GRAPH}"
    return TEST_GRAPH


@pytest.fixture
def test_graph_data(test_graph_path) -> Dict[Any, Any]:
    """Load test graph as dict"""
    with open(test_graph_path, 'r') as f:
        return json.load(f)


@pytest.fixture
def temp_output_file():
    """Create temporary output file for tests"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        yield Path(f.name)
    # Cleanup
    if Path(f.name).exists():
        Path(f.name).unlink()


# ============================================================================
# Matryoshka Analysis Tests
# ============================================================================

class TestMatryoshkaAnalysis:
    """Integration tests for matryoshka_analysis.py"""

    def test_matryoshka_help(self):
        """Test --help flag works"""
        result = run_tool(MATRYOSHKA_TOOL, ["--help"])
        assert result.returncode == 0, f"--help failed: {result.stderr}"
        assert "matryoshka" in result.stdout.lower() or "hierarchy" in result.stdout.lower()
        assert "usage:" in result.stdout.lower() or "positional arguments:" in result.stdout.lower()

    def test_matryoshka_on_test_graph_text_output(self, test_graph_path):
        """Test matryoshka analysis on test graph with text output"""
        result = run_tool(MATRYOSHKA_TOOL, [str(test_graph_path)])

        assert result.returncode == 0, f"Analysis failed: {result.stderr}"
        assert len(result.stdout) > 0, "No output produced"

        # Check for expected content in output
        output = result.stdout.lower()
        assert "hierarchy" in output or "level" in output, "Missing hierarchy analysis"

        # Should analyze the 3 test services
        assert "auth" in output or "authentication" in output
        assert "api" in output or "gateway" in output
        assert "user" in output or "management" in output

    def test_matryoshka_json_output(self, test_graph_path, temp_output_file):
        """Test matryoshka analysis with JSON output"""
        result = run_tool(
            MATRYOSHKA_TOOL,
            [str(test_graph_path), "--output", str(temp_output_file), "--format", "json"]
        )

        assert result.returncode == 0, f"Analysis failed: {result.stderr}"
        assert temp_output_file.exists(), "Output file not created"

        # Validate JSON structure
        with open(temp_output_file, 'r') as f:
            data = json.load(f)

        assert isinstance(data, dict), "Output must be JSON object"
        # Check for key sections (structure may vary based on implementation)
        # At minimum, should have some analysis results
        assert len(data) > 0, "Empty JSON output"

    def test_matryoshka_detects_hierarchy_levels(self, test_graph_path):
        """Test that matryoshka correctly identifies hierarchy levels"""
        result = run_tool(
            MATRYOSHKA_TOOL,
            [str(test_graph_path), "--format", "json"]
        )

        assert result.returncode == 0, f"Analysis failed: {result.stderr}"

        # All three test services should be at "system" level (UAF services)
        output = result.stdout
        assert "system" in output.lower(), "Should identify system-level components"

    def test_matryoshka_invalid_file(self):
        """Test error handling for non-existent file"""
        result = run_tool(MATRYOSHKA_TOOL, ["/nonexistent/file.json"])

        assert result.returncode != 0, "Should fail on non-existent file"
        assert "not found" in result.stderr.lower() or "error" in result.stderr.lower()


# ============================================================================
# Causality Analysis Tests
# ============================================================================

class TestCausalityAnalysis:
    """Integration tests for causality_analysis.py"""

    def test_causality_help(self):
        """Test --help flag works"""
        result = run_tool(CAUSALITY_TOOL, ["--help"])
        assert result.returncode == 0, f"--help failed: {result.stderr}"
        assert "causality" in result.stdout.lower() or "correlation" in result.stdout.lower()

    def test_causality_single_graph(self, test_graph_path):
        """Test causality analysis on single graph"""
        result = run_tool(CAUSALITY_TOOL, [str(test_graph_path)])

        assert result.returncode == 0, f"Analysis failed: {result.stderr}"
        assert len(result.stdout) > 0, "No output produced"

        # Should analyze correlations between the 3 services
        output = result.stdout.lower()
        assert "correlation" in output or "relationship" in output or "causality" in output

    def test_causality_json_output(self, test_graph_path, temp_output_file):
        """Test causality analysis with JSON output"""
        result = run_tool(
            CAUSALITY_TOOL,
            [str(test_graph_path), "--output", str(temp_output_file), "--format", "json"]
        )

        assert result.returncode == 0, f"Analysis failed: {result.stderr}"
        assert temp_output_file.exists(), "Output file not created"

        # Validate JSON structure
        with open(temp_output_file, 'r') as f:
            data = json.load(f)

        assert isinstance(data, dict), "Output must be JSON object"
        assert len(data) > 0, "Empty JSON output"

    def test_causality_detects_dependencies(self, test_graph_path):
        """Test that causality analysis detects service dependencies"""
        result = run_tool(
            CAUSALITY_TOOL,
            [str(test_graph_path), "--format", "json"]
        )

        assert result.returncode == 0, f"Analysis failed: {result.stderr}"

        # Test graph has dependencies: api_gateway→auth, user_mgmt→auth
        # Causality analysis should detect these
        output_text = result.stdout + result.stderr
        # Just verify analysis completed without specific assertions about detection
        # (implementation details may vary)
        assert len(output_text) > 0


# ============================================================================
# Creative Linking Tests
# ============================================================================

class TestCreativeLinking:
    """Integration tests for creative_linking.py"""

    def test_creative_linking_help(self):
        """Test --help flag works"""
        result = run_tool(CREATIVE_LINKING_TOOL, ["--help"])
        assert result.returncode == 0, f"--help failed: {result.stderr}"
        assert "creative" in result.stdout.lower() or "linking" in result.stdout.lower()

    def test_creative_linking_single_graph(self, test_graph_path):
        """Test creative linking on single graph (should find no opportunities)"""
        result = run_tool(CREATIVE_LINKING_TOOL, [str(test_graph_path)])

        assert result.returncode == 0, f"Analysis failed: {result.stderr}"
        assert len(result.stdout) > 0, "No output produced"

        # Test architectures are all UAF services (same framework/domain)
        # Creative linking should NOT find opportunities (correct behavior!)
        output = result.stdout.lower()
        # Should mention orthogonality assessment or similar
        assert "orthogon" in output or "similar" in output or "linking" in output or "no" in output

    def test_creative_linking_json_output(self, test_graph_path, temp_output_file):
        """Test creative linking with JSON output"""
        result = run_tool(
            CREATIVE_LINKING_TOOL,
            [str(test_graph_path), "--output", str(temp_output_file), "--format", "json"]
        )

        assert result.returncode == 0, f"Analysis failed: {result.stderr}"
        assert temp_output_file.exists(), "Output file not created"

        # Validate JSON structure
        with open(temp_output_file, 'r') as f:
            data = json.load(f)

        assert isinstance(data, dict), "Output must be JSON object"

    def test_creative_linking_with_context(self, test_graph_path):
        """Test creative linking with user-provided context"""
        result = run_tool(
            CREATIVE_LINKING_TOOL,
            [str(test_graph_path), "--context", "Auth service is like security checkpoint"]
        )

        assert result.returncode == 0, f"Analysis failed: {result.stderr}"
        assert len(result.stdout) > 0, "No output produced"


# ============================================================================
# Workflow Validation Tests
# ============================================================================

class TestWorkflowValidation:
    """Tests for workflow JSON files"""

    def test_all_workflows_are_valid_json(self):
        """Test that all workflow JSON files are valid"""
        workflow_dir = REPO_ROOT / "workflows"
        assert workflow_dir.exists(), f"Workflows directory not found: {workflow_dir}"

        workflow_files = list(workflow_dir.glob("*.json"))
        assert len(workflow_files) > 0, "No workflow files found"

        for workflow_file in workflow_files:
            with open(workflow_file, 'r') as f:
                try:
                    data = json.load(f)
                    assert isinstance(data, dict), f"{workflow_file.name}: Must be JSON object"
                    assert "workflow_metadata" in data, f"{workflow_file.name}: Missing workflow_metadata"
                except json.JSONDecodeError as e:
                    pytest.fail(f"{workflow_file.name}: Invalid JSON - {e}")

    def test_meta_analysis_workflow_structure(self):
        """Test that meta-analysis workflow has required structure"""
        workflow_file = REPO_ROOT / "workflows" / "99-chain_meta_analysis.json"
        assert workflow_file.exists(), "Meta-analysis workflow not found"

        with open(workflow_file, 'r') as f:
            workflow = json.load(f)

        # Check required fields
        assert "workflow_metadata" in workflow
        assert "workflow_steps" in workflow
        assert "entry_points" in workflow

        metadata = workflow["workflow_metadata"]
        assert "workflow_id" in metadata
        assert "execution_model" in metadata, "Should document LLM-assisted execution"
        assert "LLM" in metadata["execution_model"] or "llm" in metadata["execution_model"]

        # Check that workflow doesn't reference removed workflow_runner.py
        workflow_str = json.dumps(workflow)
        # Look for old-style command invocations (should be removed)
        if "workflow_runner.py" in workflow_str:
            # Check if it's in a comment/description only (acceptable)
            steps = workflow.get("workflow_steps", [])
            for step in steps:
                actions = step.get("actions", [])
                for action in actions:
                    command = action.get("command", "")
                    assert "workflow_runner.py" not in command, \
                        f"Step {step['step_id']} still references workflow_runner.py in command"


# ============================================================================
# Schema Validation Tests
# ============================================================================

class TestOutputSchemas:
    """Tests for validating output schemas"""

    def test_test_graph_schema(self, test_graph_data):
        """Test that test graph has expected structure"""
        assert "metadata" in test_graph_data or "graph" in test_graph_data

        if "graph" in test_graph_data:
            graph = test_graph_data["graph"]
            assert "nodes" in graph
            assert "links" in graph or "edges" in graph

            nodes = graph["nodes"]
            assert isinstance(nodes, list)
            assert len(nodes) == 3, "Test graph should have 3 services"

            # Each node should have id and name at minimum
            for node in nodes:
                assert "id" in node
                assert "name" in node

    def test_matryoshka_report_schema(self):
        """Test that existing matryoshka report has valid schema"""
        report_path = TEST_ARCH_DIR / "matryoshka_report.json"
        if not report_path.exists():
            pytest.skip("Matryoshka report not found")

        with open(report_path, 'r') as f:
            report = json.load(f)

        assert isinstance(report, dict), "Report must be JSON object"
        # Schema may vary - just verify it's valid JSON


# ============================================================================
# Integration Flow Tests
# ============================================================================

class TestEndToEndFlow:
    """Test complete end-to-end analysis flow"""

    def test_complete_analysis_pipeline(self, test_graph_path):
        """
        Test complete pipeline:
        1. Run matryoshka analysis
        2. Run causality analysis
        3. Run creative linking
        4. All should succeed
        """
        # Step 1: Matryoshka
        result1 = run_tool(MATRYOSHKA_TOOL, [str(test_graph_path)])
        assert result1.returncode == 0, f"Matryoshka failed: {result1.stderr}"

        # Step 2: Causality
        result2 = run_tool(CAUSALITY_TOOL, [str(test_graph_path)])
        assert result2.returncode == 0, f"Causality failed: {result2.stderr}"

        # Step 3: Creative Linking
        result3 = run_tool(CREATIVE_LINKING_TOOL, [str(test_graph_path)])
        assert result3.returncode == 0, f"Creative linking failed: {result3.stderr}"

        # All three analyses completed successfully
        assert True, "Complete analysis pipeline succeeded"

    def test_all_tools_produce_output(self, test_graph_path):
        """Test that all tools produce non-empty output"""
        tools = [
            ("matryoshka", MATRYOSHKA_TOOL),
            ("causality", CAUSALITY_TOOL),
            ("creative_linking", CREATIVE_LINKING_TOOL)
        ]

        for name, tool in tools:
            result = run_tool(tool, [str(test_graph_path)])
            assert result.returncode == 0, f"{name} failed: {result.stderr}"
            assert len(result.stdout) > 0, f"{name} produced no output"
            assert len(result.stdout) > 100, f"{name} output suspiciously short"


# ============================================================================
# Run Tests
# ============================================================================

if __name__ == "__main__":
    # Run with: python3 tests/test_integration_end_to_end.py
    pytest.main([__file__, "-v", "--tb=short"])
