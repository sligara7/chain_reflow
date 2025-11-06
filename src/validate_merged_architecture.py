#!/usr/bin/env python3
"""
Validate Merged Architecture Tool for Chain Reflow

Validates merged system_of_systems_graph.json files for:
- Orphaned nodes (components with no connections)
- Circular dependencies
- Interface coverage (all required interfaces have providers)
- Missing interface providers
- Disconnected components

This tool addresses Issue #7 identified during integrated_reflow merge:
"Chain Reflow workflows create merged architectures but lack automated validation"

Usage:
    python3 validate_merged_architecture.py <merged_graph.json> [--format json|text]
"""

import json
import sys
import argparse
from pathlib import Path
from typing import Dict, Any, List, Set, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class ValidationIssue:
    """Represents a validation issue found in the architecture"""
    severity: str  # "critical", "warning", "info"
    category: str  # "orphan", "cycle", "interface", "connectivity"
    node_id: str = None
    description: str = ""
    recommendation: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class ArchitectureValidator:
    """
    Validates merged architectures using NetworkX-style analysis
    """

    def __init__(self, graph_path: Path, verbose: bool = False):
        self.graph_path = graph_path
        self.verbose = verbose
        self.issues: List[ValidationIssue] = []
        self.graph_data = None
        self.nodes = {}
        self.edges = []

    def load_graph(self) -> bool:
        """Load and parse graph file with format auto-detection"""
        try:
            with open(self.graph_path, 'r') as f:
                data = json.load(f)

            # Format detection (similar to matrix_gap_detection.py)
            if 'system_of_systems_graph' in data:
                self.graph_data = data['system_of_systems_graph']
            elif 'graph' in data and isinstance(data['graph'], dict):
                self.graph_data = data['graph']
            elif 'nodes' in data:
                self.graph_data = data
            else:
                raise ValueError("Unknown graph format. Expected 'system_of_systems_graph', 'graph', or 'nodes' key")

            # Load nodes
            if 'nodes' in self.graph_data:
                for node in self.graph_data['nodes']:
                    node_id = node.get('node_id', node.get('id'))
                    self.nodes[node_id] = node
            else:
                raise ValueError("No nodes found in graph")

            # Load edges
            edges_key = 'edges' if 'edges' in self.graph_data else 'links'
            if edges_key in self.graph_data:
                self.edges = self.graph_data[edges_key]

            if self.verbose:
                print(f"✓ Loaded graph: {len(self.nodes)} nodes, {len(self.edges)} edges")

            return True

        except Exception as e:
            print(f"✗ Error loading graph: {e}", file=sys.stderr)
            return False

    def check_orphaned_nodes(self) -> int:
        """
        Detect orphaned nodes (nodes with no incoming or outgoing edges)

        Returns: Number of orphans found
        """
        if self.verbose:
            print("\n[1/5] Checking for orphaned nodes...")

        # Count connections for each node
        connections = {nid: {'incoming': 0, 'outgoing': 0} for nid in self.nodes.keys()}

        for edge in self.edges:
            source = edge.get('source')
            target = edge.get('target')
            if source in connections:
                connections[source]['outgoing'] += 1
            if target in connections:
                connections[target]['incoming'] += 1

        # Find orphans (completely disconnected)
        orphans = []
        for nid, conn in connections.items():
            node = self.nodes[nid]
            node_type = node.get('node_type', node.get('type', 'unknown'))

            if conn['incoming'] == 0 and conn['outgoing'] == 0:
                # Completely orphaned
                orphans.append(nid)
                self.issues.append(ValidationIssue(
                    severity="critical",
                    category="orphan",
                    node_id=nid,
                    description=f"Node '{nid}' has no connections (orphaned)",
                    recommendation="Connect node to system or remove if unused"
                ))
            elif conn['incoming'] == 0 and node_type not in ['external', 'user']:
                # Sink node (no incoming)
                self.issues.append(ValidationIssue(
                    severity="warning",
                    category="orphan",
                    node_id=nid,
                    description=f"Node '{nid}' has no incoming edges (sink node)",
                    recommendation="Verify this is intentional (e.g., entry point)"
                ))
            elif conn['outgoing'] == 0 and node_type not in ['infrastructure', 'data_store']:
                # Source node (no outgoing)
                self.issues.append(ValidationIssue(
                    severity="warning",
                    category="orphan",
                    node_id=nid,
                    description=f"Node '{nid}' has no outgoing edges (source node)",
                    recommendation="Verify this is intentional (e.g., leaf node)"
                ))

        if self.verbose:
            if orphans:
                print(f"  ✗ Found {len(orphans)} orphaned nodes")
            else:
                print(f"  ✓ No orphaned nodes")

        return len(orphans)

    def check_circular_dependencies(self) -> int:
        """
        Detect circular dependencies using DFS cycle detection

        Returns: Number of cycles found
        """
        if self.verbose:
            print("\n[2/5] Checking for circular dependencies...")

        # Build adjacency list (only for invocation/dependency edges)
        adj = {nid: [] for nid in self.nodes.keys()}
        for edge in self.edges:
            edge_type = edge.get('edge_type', edge.get('type', 'unknown'))
            if edge_type in ['invocation', 'dependency', 'data_flow']:
                source = edge.get('source')
                target = edge.get('target')
                if source and target:
                    adj[source].append(target)

        # DFS cycle detection
        def has_cycle_from(node: str, visited: Set[str], rec_stack: Set[str]) -> bool:
            visited.add(node)
            rec_stack.add(node)

            for neighbor in adj.get(node, []):
                if neighbor not in visited:
                    if has_cycle_from(neighbor, visited, rec_stack):
                        return True
                elif neighbor in rec_stack:
                    # Cycle detected
                    return True

            rec_stack.remove(node)
            return False

        visited = set()
        cycles_found = 0

        for node in self.nodes.keys():
            if node not in visited:
                if has_cycle_from(node, visited, set()):
                    cycles_found += 1
                    self.issues.append(ValidationIssue(
                        severity="critical",
                        category="cycle",
                        node_id=node,
                        description=f"Circular dependency detected involving '{node}'",
                        recommendation="Break cycle by introducing abstraction or removing dependency"
                    ))

        if self.verbose:
            if cycles_found > 0:
                print(f"  ✗ Found {cycles_found} circular dependencies")
            else:
                print(f"  ✓ No circular dependencies (DAG structure)")

        return cycles_found

    def check_interface_coverage(self) -> int:
        """
        Validate that all required interfaces have providers

        Returns: Number of unmet interfaces
        """
        if self.verbose:
            print("\n[3/5] Checking interface coverage...")

        provided_interfaces = set()
        required_interfaces = set()

        # Collect provided and required interfaces
        for node_id, node in self.nodes.items():
            # Provided interfaces
            provided = node.get('interfaces_provided', [])
            provided_interfaces.update(provided)

            # Required interfaces
            required = node.get('interfaces_required', [])
            for iface in required:
                # Strip "(future)" markers
                clean_iface = iface.replace(' (future)', '').strip()
                required_interfaces.add(clean_iface)

        # Find unmet requirements
        unmet = required_interfaces - provided_interfaces

        # Filter out intentional future interfaces
        unmet_critical = {i for i in unmet if '(future)' not in i}

        for iface in unmet_critical:
            self.issues.append(ValidationIssue(
                severity="critical",
                category="interface",
                description=f"Interface '{iface}' is required but has no provider",
                recommendation="Implement interface provider or mark as future"
            ))

        if self.verbose:
            print(f"  Interfaces provided: {len(provided_interfaces)}")
            print(f"  Interfaces required: {len(required_interfaces)}")
            if unmet_critical:
                print(f"  ✗ {len(unmet_critical)} unmet interface requirements")
            else:
                print(f"  ✓ All required interfaces have providers")

        return len(unmet_critical)

    def check_disconnected_components(self) -> int:
        """
        Find disconnected components (subgraphs with no connections to main graph)

        Returns: Number of disconnected subgraphs
        """
        if self.verbose:
            print("\n[4/5] Checking for disconnected components...")

        # Build undirected adjacency for connectivity check
        adj = {nid: set() for nid in self.nodes.keys()}
        for edge in self.edges:
            source = edge.get('source')
            target = edge.get('target')
            if source and target:
                adj[source].add(target)
                adj[target].add(source)  # Undirected

        # Find connected components using DFS
        visited = set()
        components = []

        def dfs(node: str, component: List[str]):
            visited.add(node)
            component.append(node)
            for neighbor in adj.get(node, []):
                if neighbor not in visited:
                    dfs(neighbor, component)

        for node in self.nodes.keys():
            if node not in visited:
                component = []
                dfs(node, component)
                components.append(component)

        num_components = len(components)

        if num_components > 1:
            # Multiple disconnected subgraphs
            for i, comp in enumerate(components):
                if len(comp) > 1:
                    self.issues.append(ValidationIssue(
                        severity="warning",
                        category="connectivity",
                        description=f"Disconnected subgraph #{i+1} with {len(comp)} nodes: {', '.join(comp[:3])}{'...' if len(comp) > 3 else ''}",
                        recommendation="Connect subgraphs or split into separate architectures"
                    ))

        if self.verbose:
            if num_components > 1:
                print(f"  ✗ Found {num_components} disconnected subgraphs")
            else:
                print(f"  ✓ Graph is fully connected")

        return num_components - 1 if num_components > 0 else 0

    def check_metadata_completeness(self) -> int:
        """
        Check that nodes have required metadata fields

        Returns: Number of nodes with missing metadata
        """
        if self.verbose:
            print("\n[5/5] Checking metadata completeness...")

        required_fields = ['node_id', 'node_name', 'node_type', 'status']
        missing_count = 0

        for node_id, node in self.nodes.items():
            missing_fields = []
            for field in required_fields:
                # Check both node_id and id variants
                if field == 'node_id':
                    if 'node_id' not in node and 'id' not in node:
                        missing_fields.append(field)
                elif field == 'node_name':
                    if 'node_name' not in node and 'name' not in node:
                        missing_fields.append(field)
                elif field not in node:
                    missing_fields.append(field)

            if missing_fields:
                missing_count += 1
                self.issues.append(ValidationIssue(
                    severity="info",
                    category="metadata",
                    node_id=node_id,
                    description=f"Node '{node_id}' missing fields: {', '.join(missing_fields)}",
                    recommendation="Add missing metadata for completeness"
                ))

        if self.verbose:
            if missing_count > 0:
                print(f"  ⚠ {missing_count} nodes have incomplete metadata")
            else:
                print(f"  ✓ All nodes have complete metadata")

        return missing_count

    def validate(self) -> Dict[str, Any]:
        """
        Run all validation checks

        Returns: Validation results dictionary
        """
        if not self.load_graph():
            return {"status": "error", "message": "Failed to load graph"}

        results = {
            "timestamp": datetime.utcnow().isoformat(),
            "graph_file": str(self.graph_path),
            "graph_name": self.graph_data.get('metadata', {}).get('system_name', 'Unknown'),
            "total_nodes": len(self.nodes),
            "total_edges": len(self.edges),
            "validation_results": {
                "orphaned_nodes": self.check_orphaned_nodes(),
                "circular_dependencies": self.check_circular_dependencies(),
                "unmet_interfaces": self.check_interface_coverage(),
                "disconnected_subgraphs": self.check_disconnected_components(),
                "incomplete_metadata": self.check_metadata_completeness()
            },
            "issues": [issue.to_dict() for issue in self.issues],
            "summary": self.generate_summary()
        }

        return results

    def generate_summary(self) -> Dict[str, Any]:
        """Generate validation summary"""
        critical = sum(1 for i in self.issues if i.severity == "critical")
        warnings = sum(1 for i in self.issues if i.severity == "warning")
        info = sum(1 for i in self.issues if i.severity == "info")

        if critical > 0:
            status = "FAIL"
        elif warnings > 0:
            status = "PASS_WITH_WARNINGS"
        else:
            status = "PASS"

        return {
            "status": status,
            "total_issues": len(self.issues),
            "critical_issues": critical,
            "warnings": warnings,
            "info": info
        }


def format_text_report(results: Dict[str, Any]) -> str:
    """Format validation results as human-readable text"""
    lines = []
    lines.append("=" * 80)
    lines.append("ARCHITECTURE VALIDATION REPORT")
    lines.append("=" * 80)
    lines.append(f"")
    lines.append(f"Timestamp: {results['timestamp']}")
    lines.append(f"Graph File: {results['graph_file']}")
    lines.append(f"System Name: {results['graph_name']}")
    lines.append(f"Nodes: {results['total_nodes']}, Edges: {results['total_edges']}")
    lines.append(f"")

    # Validation Results
    lines.append("-" * 80)
    lines.append("VALIDATION RESULTS")
    lines.append("-" * 80)
    vr = results['validation_results']
    lines.append(f"Orphaned nodes:          {vr['orphaned_nodes']}")
    lines.append(f"Circular dependencies:   {vr['circular_dependencies']}")
    lines.append(f"Unmet interfaces:        {vr['unmet_interfaces']}")
    lines.append(f"Disconnected subgraphs:  {vr['disconnected_subgraphs']}")
    lines.append(f"Incomplete metadata:     {vr['incomplete_metadata']}")
    lines.append(f"")

    # Summary
    summary = results['summary']
    lines.append("-" * 80)
    lines.append("SUMMARY")
    lines.append("-" * 80)
    lines.append(f"Status: {summary['status']}")
    lines.append(f"Total Issues: {summary['total_issues']}")
    lines.append(f"  Critical: {summary['critical_issues']}")
    lines.append(f"  Warnings: {summary['warnings']}")
    lines.append(f"  Info: {summary['info']}")
    lines.append(f"")

    # Issues Detail
    if results['issues']:
        lines.append("-" * 80)
        lines.append("ISSUES DETAIL")
        lines.append("-" * 80)
        for i, issue in enumerate(results['issues'], 1):
            lines.append(f"")
            lines.append(f"[{i}] {issue['severity'].upper()} - {issue['category']}")
            if issue.get('node_id'):
                lines.append(f"    Node: {issue['node_id']}")
            lines.append(f"    Issue: {issue['description']}")
            lines.append(f"    Fix: {issue['recommendation']}")

    lines.append(f"")
    lines.append("=" * 80)

    if summary['status'] == "PASS":
        lines.append("✓ VALIDATION PASSED")
    elif summary['status'] == "PASS_WITH_WARNINGS":
        lines.append("⚠ VALIDATION PASSED WITH WARNINGS")
    else:
        lines.append("✗ VALIDATION FAILED")
    lines.append("=" * 80)

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Validate merged architecture for orphans, cycles, interface coverage"
    )
    parser.add_argument(
        "graph_file",
        type=Path,
        help="Path to merged system_of_systems_graph.json file"
    )
    parser.add_argument(
        "--format", "-f",
        choices=["json", "text"],
        default="text",
        help="Output format (default: text)"
    )
    parser.add_argument(
        "--output", "-o",
        type=Path,
        help="Output file path (optional, default: stdout)"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Verbose output"
    )

    args = parser.parse_args()

    # Validate
    validator = ArchitectureValidator(args.graph_file, verbose=args.verbose)
    results = validator.validate()

    # Format output
    if args.format == "json":
        output = json.dumps(results, indent=2)
    else:
        output = format_text_report(results)

    # Write output
    if args.output:
        with open(args.output, 'w') as f:
            f.write(output)
        print(f"✓ Validation report written to: {args.output}")
    else:
        print(output)

    # Exit code
    summary = results['summary']
    if summary['status'] == "FAIL":
        sys.exit(1)
    elif summary['status'] == "PASS_WITH_WARNINGS":
        sys.exit(0)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
