#!/usr/bin/env python3
"""
Matryoshka (Hierarchical Nesting) Analysis for Chain Reflow

Like Russian nesting dolls (matryoshka), system architectures are often nested
hierarchically rather than linked peer-to-peer. This module analyzes:

1. Hierarchy Levels: Component, System, System-of-Systems, etc.
2. Nesting Relationships: Architecture A contains Architecture B
3. Peer Relationships: At each hierarchical level
4. Missing Intermediate Levels: Gaps in the hierarchy

Key Insight:
When two architectures seem unrelated or have gaps, they may not be peers.
One might be nested inside the other, or both might be nested under an
unknown intermediate system.

Example Hierarchies:
- Component Level: Individual parts (axle, engine, transmission)
- System Level: Assemblies (drivetrain, chassis, electrical system)
- System-of-Systems Level: Complete product (vehicle)
- Enterprise Level: Fleet of products (vehicle lineup)

Relationships:
- Peer-to-peer: Same level (engine ↔ transmission)
- Parent-child: Different levels (drivetrain contains [engine, transmission])
- Nested-through-intermediate: A contains X, X peers with Y, Y contains B
"""

import json
import sys
import argparse
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple, Set
from dataclasses import dataclass, asdict
from enum import Enum
from datetime import datetime


class HierarchyLevel(Enum):
    """Standard hierarchy levels in system architectures"""
    COMPONENT = "component"  # Individual parts/modules
    SUBSYSTEM = "subsystem"  # Groups of related components
    SYSTEM = "system"  # Complete functional systems
    SYSTEM_OF_SYSTEMS = "system_of_systems"  # Multiple integrated systems
    ENTERPRISE = "enterprise"  # Organization-level architecture
    UNKNOWN = "unknown"  # Level not yet determined


class RelationshipType(Enum):
    """Types of relationships between architectures"""
    PEER = "peer"  # Same hierarchical level
    PARENT_CHILD = "parent_child"  # One contains the other
    CHILD_PARENT = "child_parent"  # Reverse of parent_child
    NESTED_INDIRECT = "nested_indirect"  # Related through intermediate levels
    UNRELATED = "unrelated"  # No hierarchical relationship


@dataclass
class HierarchyMetadata:
    """Metadata about an architecture's position in hierarchy"""
    architecture_name: str
    declared_level: Optional[str]  # User-specified level
    inferred_level: str  # System-inferred level
    confidence: float  # 0.0 to 1.0
    evidence: List[str]  # Why we think it's at this level
    scope_indicators: Dict[str, Any]  # Size, complexity, etc.

    def to_dict(self):
        return asdict(self)


@dataclass
class NestingRelationship:
    """Represents a parent-child nesting relationship"""
    id: str
    parent_architecture: str
    child_architecture: str
    parent_level: str
    child_level: str
    relationship_type: str
    evidence: List[str]
    confidence: float
    direct_containment: bool  # True if parent directly contains child

    def to_dict(self):
        return asdict(self)


@dataclass
class HierarchicalGap:
    """Represents a missing intermediate level in the hierarchy"""
    id: str
    architecture_a: str
    architecture_b: str
    level_a: str
    level_b: str
    missing_level: str
    hypothesis: str  # What the missing intermediate might be
    evidence: List[str]
    gap_type: str  # "missing_parent", "missing_intermediate", "missing_peer"

    def to_dict(self):
        return asdict(self)


class MatryoshkaAnalyzer:
    """
    Analyzes hierarchical relationships between architectures
    Named after Russian nesting dolls (matryoshka)
    """

    def __init__(self):
        self.hierarchy_order = [
            HierarchyLevel.COMPONENT,
            HierarchyLevel.SUBSYSTEM,
            HierarchyLevel.SYSTEM,
            HierarchyLevel.SYSTEM_OF_SYSTEMS,
            HierarchyLevel.ENTERPRISE
        ]

        # Scope indicators for each level
        self.level_indicators = {
            HierarchyLevel.COMPONENT: {
                "typical_component_count": (1, 20),
                "keywords": ["component", "module", "part", "unit", "element"],
                "scope": "single_responsibility",
                "examples": ["axle", "bearing", "sensor", "api_endpoint"]
            },
            HierarchyLevel.SUBSYSTEM: {
                "typical_component_count": (5, 50),
                "keywords": ["subsystem", "assembly", "group", "package"],
                "scope": "related_components",
                "examples": ["drivetrain", "suspension", "auth_module", "logging_subsystem"]
            },
            HierarchyLevel.SYSTEM: {
                "typical_component_count": (10, 200),
                "keywords": ["system", "platform", "service", "application"],
                "scope": "complete_functionality",
                "examples": ["vehicle_chassis", "microservice", "database", "web_app"]
            },
            HierarchyLevel.SYSTEM_OF_SYSTEMS: {
                "typical_component_count": (50, 1000),
                "keywords": ["system_of_systems", "integrated", "enterprise", "platform"],
                "scope": "multiple_systems",
                "examples": ["vehicle", "cloud_platform", "enterprise_app", "iot_ecosystem"]
            },
            HierarchyLevel.ENTERPRISE: {
                "typical_component_count": (100, float('inf')),
                "keywords": ["enterprise", "organization", "portfolio", "fleet"],
                "scope": "organization_level",
                "examples": ["vehicle_lineup", "product_portfolio", "cloud_infrastructure"]
            }
        }

    def infer_hierarchy_level(
        self,
        arch: Dict[str, Any]
    ) -> HierarchyMetadata:
        """
        Infer the hierarchical level of an architecture

        Uses multiple indicators:
        - Declared level (if provided)
        - Component count
        - Name keywords
        - Scope description
        - Domain hints
        """
        arch_name = arch.get('name', 'Unknown')
        declared_level = arch.get('hierarchy_level')

        # If level is explicitly declared, use it (with high confidence)
        if declared_level:
            return HierarchyMetadata(
                architecture_name=arch_name,
                declared_level=declared_level,
                inferred_level=declared_level,
                confidence=0.9,
                evidence=[f"Explicitly declared as {declared_level}"],
                scope_indicators=self._extract_scope_indicators(arch)
            )

        # Otherwise, infer from indicators
        scores = {}
        evidence = []

        component_count = len(arch.get('components', []))
        name_lower = arch_name.lower()
        description_lower = arch.get('description', '').lower()

        for level in self.hierarchy_order:
            score = 0.0
            level_evidence = []
            indicators = self.level_indicators[level]

            # Check component count
            min_count, max_count = indicators['typical_component_count']
            if min_count <= component_count <= max_count:
                score += 0.4
                level_evidence.append(f"Component count ({component_count}) matches {level.value} range")

            # Check keywords in name
            for keyword in indicators['keywords']:
                if keyword in name_lower:
                    score += 0.3
                    level_evidence.append(f"Name contains '{keyword}' keyword")
                    break

            # Check keywords in description
            for keyword in indicators['keywords']:
                if keyword in description_lower:
                    score += 0.2
                    level_evidence.append(f"Description contains '{keyword}' keyword")
                    break

            # Check scope
            scope = arch.get('scope', '')
            if scope and scope.lower() == indicators['scope']:
                score += 0.1
                level_evidence.append(f"Scope matches: {scope}")

            scores[level] = score
            if level_evidence:
                evidence.extend([(level, ev) for ev in level_evidence])

        # Select level with highest score
        best_level = max(scores, key=scores.get)
        best_score = scores[best_level]
        best_evidence = [ev for level, ev in evidence if level == best_level]

        # If no clear winner, mark as unknown
        if best_score < 0.3:
            best_level = HierarchyLevel.UNKNOWN
            best_evidence = ["Insufficient evidence to determine hierarchy level"]

        return HierarchyMetadata(
            architecture_name=arch_name,
            declared_level=None,
            inferred_level=best_level.value,
            confidence=min(best_score, 1.0),
            evidence=best_evidence,
            scope_indicators=self._extract_scope_indicators(arch)
        )

    def _extract_scope_indicators(self, arch: Dict[str, Any]) -> Dict[str, Any]:
        """Extract indicators of architecture scope"""
        return {
            "component_count": len(arch.get('components', [])),
            "connection_count": len(arch.get('connections', [])),
            "domain": arch.get('domain', 'unknown'),
            "framework": arch.get('framework', 'unknown'),
            "has_external_interfaces": bool(arch.get('external_interfaces')),
            "has_subarchitectures": bool(arch.get('subarchitectures'))
        }

    def analyze_relationship(
        self,
        arch_a: Dict[str, Any],
        arch_b: Dict[str, Any],
        metadata_a: HierarchyMetadata,
        metadata_b: HierarchyMetadata
    ) -> NestingRelationship:
        """
        Analyze the hierarchical relationship between two architectures

        Determines if they are:
        - Peers (same level)
        - Parent-child (one contains the other)
        - Nested through intermediates
        """
        level_a = metadata_a.inferred_level
        level_b = metadata_b.inferred_level

        # Get level indices
        try:
            idx_a = [l.value for l in self.hierarchy_order].index(level_a)
            idx_b = [l.value for l in self.hierarchy_order].index(level_b)
        except ValueError:
            # One or both levels are unknown
            return NestingRelationship(
                id=f"rel_{arch_a['name']}_{arch_b['name']}",
                parent_architecture="unknown",
                child_architecture="unknown",
                parent_level=level_a,
                child_level=level_b,
                relationship_type=RelationshipType.UNRELATED.value,
                evidence=["Cannot determine relationship - hierarchy level unknown"],
                confidence=0.0,
                direct_containment=False
            )

        # Check if they're at the same level (peers)
        if idx_a == idx_b:
            return NestingRelationship(
                id=f"rel_{arch_a['name']}_{arch_b['name']}",
                parent_architecture=arch_a['name'],
                child_architecture=arch_b['name'],
                parent_level=level_a,
                child_level=level_b,
                relationship_type=RelationshipType.PEER.value,
                evidence=[f"Both at {level_a} level"],
                confidence=min(metadata_a.confidence, metadata_b.confidence),
                direct_containment=False
            )

        # Determine parent and child
        if idx_a < idx_b:
            # A is at higher level (parent), B is at lower level (child)
            parent_arch = arch_a
            child_arch = arch_b
            parent_meta = metadata_a
            child_meta = metadata_b
            relationship_type = RelationshipType.PARENT_CHILD
        else:
            # B is at higher level (parent), A is at lower level (child)
            parent_arch = arch_b
            child_arch = arch_a
            parent_meta = metadata_b
            child_meta = metadata_a
            relationship_type = RelationshipType.CHILD_PARENT

        # Check if relationship is direct or through intermediates
        level_gap = abs(idx_a - idx_b)
        direct = level_gap == 1

        if not direct:
            relationship_type = RelationshipType.NESTED_INDIRECT

        evidence = [
            f"{parent_arch['name']} at {parent_meta.inferred_level} level",
            f"{child_arch['name']} at {child_meta.inferred_level} level",
            f"Level gap: {level_gap} level(s)"
        ]

        if not direct:
            evidence.append(f"Indirect nesting - {level_gap - 1} intermediate level(s) may exist")

        # Check for explicit containment references
        explicit_containment = self._check_explicit_containment(parent_arch, child_arch)
        if explicit_containment:
            evidence.append("Explicit containment reference found")
            direct = True

        return NestingRelationship(
            id=f"rel_{parent_arch['name']}_{child_arch['name']}",
            parent_architecture=parent_arch['name'],
            child_architecture=child_arch['name'],
            parent_level=parent_meta.inferred_level,
            child_level=child_meta.inferred_level,
            relationship_type=relationship_type.value,
            evidence=evidence,
            confidence=min(parent_meta.confidence, child_meta.confidence),
            direct_containment=direct
        )

    def _check_explicit_containment(
        self,
        parent_arch: Dict[str, Any],
        child_arch: Dict[str, Any]
    ) -> bool:
        """Check if parent explicitly references child as subarchitecture"""
        # Check if parent has subarchitectures list
        subarchs = parent_arch.get('subarchitectures', [])
        child_name = child_arch['name']

        return any(
            sub.get('name') == child_name or sub.get('id') == child_arch.get('id')
            for sub in subarchs
        )

    def discover_hierarchical_gaps(
        self,
        architectures: List[Dict[str, Any]],
        relationships: List[NestingRelationship]
    ) -> List[HierarchicalGap]:
        """
        Discover missing intermediate levels in the hierarchy

        Cases:
        1. Two architectures at non-adjacent levels with no intermediate
        2. Multiple architectures at same level with no common parent
        3. Leaf architecture with no known parent
        """
        gaps = []

        # Infer hierarchy for all architectures
        hierarchy_metadata = {
            arch['name']: self.infer_hierarchy_level(arch)
            for arch in architectures
        }

        # Case 1: Non-adjacent levels with no intermediate
        for rel in relationships:
            if rel.relationship_type == RelationshipType.NESTED_INDIRECT.value:
                # There's a gap between parent and child
                gap = self._identify_missing_intermediate(
                    rel.parent_architecture,
                    rel.child_architecture,
                    rel.parent_level,
                    rel.child_level
                )
                if gap:
                    gaps.append(gap)

        # Case 2: Multiple peers with no common parent
        peers_by_level = {}
        for name, meta in hierarchy_metadata.items():
            level = meta.inferred_level
            if level not in peers_by_level:
                peers_by_level[level] = []
            peers_by_level[level].append(name)

        for level, peers in peers_by_level.items():
            if len(peers) > 1:
                # Check if any have a common parent
                common_parent_gap = self._check_missing_common_parent(
                    peers, level, relationships
                )
                if common_parent_gap:
                    gaps.append(common_parent_gap)

        # Case 3: Leaf architectures with no parent
        for arch in architectures:
            has_parent = any(
                rel.child_architecture == arch['name']
                for rel in relationships
            )
            if not has_parent:
                gap = self._identify_missing_parent(
                    arch['name'],
                    hierarchy_metadata[arch['name']]
                )
                if gap:
                    gaps.append(gap)

        return gaps

    def _identify_missing_intermediate(
        self,
        parent_name: str,
        child_name: str,
        parent_level: str,
        child_level: str
    ) -> Optional[HierarchicalGap]:
        """Identify missing intermediate level between parent and child"""
        # Get level indices
        try:
            idx_parent = [l.value for l in self.hierarchy_order].index(parent_level)
            idx_child = [l.value for l in self.hierarchy_order].index(child_level)
        except ValueError:
            return None

        level_gap = abs(idx_parent - idx_child)
        if level_gap <= 1:
            return None  # No gap

        # Identify missing level
        missing_idx = (idx_parent + idx_child) // 2
        missing_level = self.hierarchy_order[missing_idx].value

        return HierarchicalGap(
            id=f"gap_intermediate_{parent_name}_{child_name}",
            architecture_a=parent_name,
            architecture_b=child_name,
            level_a=parent_level,
            level_b=child_level,
            missing_level=missing_level,
            hypothesis=f"Unknown {missing_level} architecture that contains {child_name} and is contained by {parent_name}",
            evidence=[
                f"{parent_name} at {parent_level} level",
                f"{child_name} at {child_level} level",
                f"Gap of {level_gap} levels suggests {level_gap - 1} missing intermediate(s)"
            ],
            gap_type="missing_intermediate"
        )

    def _check_missing_common_parent(
        self,
        peers: List[str],
        level: str,
        relationships: List[NestingRelationship]
    ) -> Optional[HierarchicalGap]:
        """Check if peer architectures are missing a common parent"""
        # Check if any peers have a common parent
        parents = {}
        for peer in peers:
            peer_parents = [
                rel.parent_architecture
                for rel in relationships
                if rel.child_architecture == peer
            ]
            parents[peer] = peer_parents

        # If all peers have the same parent, no gap
        if all(parents[peer] for peer in peers):
            common = set(parents[peers[0]])
            for peer in peers[1:]:
                common &= set(parents[peer])
            if common:
                return None  # Have common parent

        # Missing common parent
        # Determine what level the parent should be at
        try:
            idx_current = [l.value for l in self.hierarchy_order].index(level)
            if idx_current < len(self.hierarchy_order) - 1:
                missing_level = self.hierarchy_order[idx_current + 1].value
            else:
                return None  # Already at top level
        except ValueError:
            return None

        return HierarchicalGap(
            id=f"gap_common_parent_{'_'.join(peers[:3])}",
            architecture_a=peers[0],
            architecture_b=peers[1] if len(peers) > 1 else peers[0],
            level_a=level,
            level_b=level,
            missing_level=missing_level,
            hypothesis=f"Unknown {missing_level} architecture that contains {', '.join(peers)}",
            evidence=[
                f"{len(peers)} peer architectures at {level} level",
                "No common parent identified",
                f"Expected parent at {missing_level} level"
            ],
            gap_type="missing_parent"
        )

    def _identify_missing_parent(
        self,
        arch_name: str,
        metadata: HierarchyMetadata
    ) -> Optional[HierarchicalGap]:
        """Identify missing parent for an architecture"""
        level = metadata.inferred_level

        # Don't report missing parent for top-level architectures
        if level == HierarchyLevel.ENTERPRISE.value:
            return None

        # Determine what level the parent should be at
        try:
            idx_current = [l.value for l in self.hierarchy_order].index(level)
            if idx_current < len(self.hierarchy_order) - 1:
                missing_level = self.hierarchy_order[idx_current + 1].value
            else:
                return None
        except ValueError:
            return None

        return HierarchicalGap(
            id=f"gap_parent_{arch_name}",
            architecture_a=arch_name,
            architecture_b="unknown",
            level_a=level,
            level_b="unknown",
            missing_level=missing_level,
            hypothesis=f"Unknown {missing_level} architecture that contains {arch_name}",
            evidence=[
                f"{arch_name} at {level} level",
                "No parent architecture identified",
                f"Expected parent at {missing_level} level"
            ],
            gap_type="missing_parent"
        )

    def generate_matryoshka_report(
        self,
        architectures: List[Dict[str, Any]],
        hierarchy_metadata: Dict[str, HierarchyMetadata],
        relationships: List[NestingRelationship],
        gaps: List[HierarchicalGap]
    ) -> str:
        """Generate comprehensive matryoshka analysis report"""
        report = []
        report.append("="*70)
        report.append("MATRYOSHKA (HIERARCHICAL NESTING) ANALYSIS")
        report.append("="*70)
        report.append("")
        report.append("Like Russian nesting dolls, system architectures are often nested")
        report.append("hierarchically rather than linked peer-to-peer.")
        report.append("")
        report.append("⚠️  IMPORTANT: Don't assume peer-to-peer relationships!")
        report.append("Architectures may be:")
        report.append("• At the same level (peers)")
        report.append("• At different levels (parent-child)")
        report.append("• Nested through intermediate levels")
        report.append("="*70)
        report.append("")

        # Show hierarchy levels
        report.append("DETECTED HIERARCHY LEVELS")
        report.append("-"*70)

        levels_found = {}
        for name, meta in hierarchy_metadata.items():
            level = meta.inferred_level
            if level not in levels_found:
                levels_found[level] = []
            levels_found[level].append((name, meta.confidence))

        for level in self.hierarchy_order:
            level_val = level.value
            if level_val in levels_found:
                report.append(f"\n{level_val.upper()} Level:")
                for name, confidence in levels_found[level_val]:
                    report.append(f"  • {name} (confidence: {confidence:.0%})")

        if HierarchyLevel.UNKNOWN.value in levels_found:
            report.append(f"\nUNKNOWN Level:")
            for name, confidence in levels_found[HierarchyLevel.UNKNOWN.value]:
                report.append(f"  • {name}")

        # Show relationships
        report.append("\n" + "="*70)
        report.append("HIERARCHICAL RELATIONSHIPS")
        report.append("="*70)

        peer_rels = [r for r in relationships if r.relationship_type == RelationshipType.PEER.value]
        parent_child_rels = [r for r in relationships if r.relationship_type in [RelationshipType.PARENT_CHILD.value, RelationshipType.CHILD_PARENT.value]]
        indirect_rels = [r for r in relationships if r.relationship_type == RelationshipType.NESTED_INDIRECT.value]

        if peer_rels:
            report.append("\nPeer Relationships (same level):")
            for rel in peer_rels:
                report.append(f"  {rel.parent_architecture} ↔ {rel.child_architecture}")
                report.append(f"    Level: {rel.parent_level}")

        if parent_child_rels:
            report.append("\nParent-Child Relationships (direct containment):")
            for rel in parent_child_rels:
                report.append(f"  {rel.parent_architecture} ⊃ {rel.child_architecture}")
                report.append(f"    Parent level: {rel.parent_level}")
                report.append(f"    Child level: {rel.child_level}")

        if indirect_rels:
            report.append("\nIndirect Nesting (through intermediates):")
            for rel in indirect_rels:
                report.append(f"  {rel.parent_architecture} ⊃...⊃ {rel.child_architecture}")
                report.append(f"    {rel.parent_level} → {rel.child_level}")
                report.append(f"    ⚠️  Gap: Intermediate level(s) may exist")

        # Show gaps
        if gaps:
            report.append("\n" + "="*70)
            report.append("HIERARCHICAL GAPS (Missing Levels)")
            report.append("="*70)
            report.append("")
            report.append("⚠️  KNOWLEDGE GAPS: The following intermediate levels may exist")
            report.append("but are not yet documented:")
            report.append("")

            for i, gap in enumerate(gaps, 1):
                report.append(f"{i}. {gap.gap_type.replace('_', ' ').title()}")
                report.append(f"   Hypothesis: {gap.hypothesis}")
                report.append(f"   Missing Level: {gap.missing_level}")
                report.append(f"   Evidence:")
                for ev in gap.evidence:
                    report.append(f"     • {ev}")
                report.append("")

        # Next steps
        report.append("="*70)
        report.append("RECOMMENDED NEXT STEPS")
        report.append("="*70)
        report.append("1. Verify hierarchy levels for each architecture")
        report.append("2. Investigate hierarchical gaps:")
        report.append("   • Document missing intermediate levels if they exist")
        report.append("   • Update architecture metadata if levels are incorrect")
        report.append("3. Consider hierarchical relationships when linking:")
        report.append("   • Peer-to-peer links: At same level")
        report.append("   • Parent-child links: Containment relationships")
        report.append("   • Indirect links: Through intermediate systems")
        report.append("4. Don't assume peer-to-peer - check hierarchy first!")
        report.append("")

        return "\n".join(report)


def load_graph(file_path: str) -> dict:
    """Load system_of_systems_graph.json file"""
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: File not found: {file_path}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in {file_path}: {e}", file=sys.stderr)
        sys.exit(1)


def graph_to_architectures(graph: dict) -> List[dict]:
    """
    Convert system_of_systems_graph nodes to architecture format expected by analyzer

    Maps from graph node format to the format expected by MatryoshkaAnalyzer:
    - node.name → architecture.name
    - node.raw.description → architecture.description
    - node.raw.hierarchical_tier → architecture.hierarchy_level
    - node.functions → architecture.components (for counting)
    - node.raw.framework → architecture.framework
    """
    nodes = graph.get('graph', {}).get('nodes', [])
    architectures = []

    for node in nodes:
        raw = node.get('raw', {})

        # Map hierarchical_tier to standard hierarchy levels
        tier_to_level = {
            'tier_0_components': 'component',
            'tier_1_systems': 'system',
            'tier_2_system_of_systems': 'system_of_systems',
            'tier_3_enterprise': 'enterprise',
            'component': 'component',
            'subsystem': 'subsystem',
            'system': 'system',
            'system_of_systems': 'system_of_systems',
            'enterprise': 'enterprise'
        }

        hierarchical_tier = raw.get('hierarchical_tier', '')
        hierarchy_level = tier_to_level.get(hierarchical_tier, None)

        # Use functions as components for counting purposes
        functions = node.get('functions', [])

        # Build architecture dict
        arch = {
            'name': node.get('name', 'Unknown'),
            'description': raw.get('description', ''),
            'framework': raw.get('framework', 'unknown'),
            'components': functions,  # Use functions as components
            'domain': raw.get('domain', 'unknown'),
        }

        # Add hierarchy_level if it was declared
        if hierarchy_level:
            arch['hierarchy_level'] = hierarchy_level

        # Add dependencies if present
        if 'dependencies' in node:
            arch['dependencies'] = node['dependencies']

        # Add interfaces for additional context
        if 'interfaces' in node:
            arch['interfaces'] = node['interfaces']

        architectures.append(arch)

    return architectures


def write_output(results: dict, output_path: Optional[str], format: str):
    """Write analysis results to file or stdout"""
    if format == 'json':
        output = json.dumps(results, indent=2)
    elif format == 'markdown':
        output = results['report']  # Already formatted as text, could enhance for markdown
    else:  # text
        output = results['report']

    if output_path:
        try:
            with open(output_path, 'w') as f:
                f.write(output)
            print(f"Analysis written to: {output_path}", file=sys.stderr)
        except IOError as e:
            print(f"Error writing to {output_path}: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        print(output)


def analyze_graph(graph_file: str, output_path: Optional[str] = None, format: str = 'text'):
    """
    Analyze a system_of_systems_graph.json file for hierarchical relationships

    Args:
        graph_file: Path to system_of_systems_graph.json
        output_path: Optional path to write results (default: stdout)
        format: Output format - 'text', 'json', or 'markdown'
    """
    # Load graph
    graph = load_graph(graph_file)

    # Convert to architecture format
    architectures = graph_to_architectures(graph)

    if not architectures:
        print("Error: No architectures found in graph", file=sys.stderr)
        sys.exit(1)

    # Run analysis
    analyzer = MatryoshkaAnalyzer()

    # Infer hierarchy levels
    hierarchy_metadata = {}
    for arch in architectures:
        meta = analyzer.infer_hierarchy_level(arch)
        hierarchy_metadata[arch['name']] = meta

    # Analyze relationships
    relationships = []
    for i, arch_a in enumerate(architectures):
        for arch_b in architectures[i+1:]:
            rel = analyzer.analyze_relationship(
                arch_a, arch_b,
                hierarchy_metadata[arch_a['name']],
                hierarchy_metadata[arch_b['name']]
            )
            relationships.append(rel)

    # Discover gaps
    gaps = analyzer.discover_hierarchical_gaps(architectures, relationships)

    # Generate report
    report = analyzer.generate_matryoshka_report(
        architectures,
        hierarchy_metadata,
        relationships,
        gaps
    )

    # Prepare results
    results = {
        'report': report,
        'summary': {
            'num_architectures': len(architectures),
            'num_relationships': len(relationships),
            'num_gaps': len(gaps),
            'hierarchy_levels': {
                name: meta.inferred_level
                for name, meta in hierarchy_metadata.items()
            }
        },
        'hierarchy_metadata': {
            name: meta.to_dict()
            for name, meta in hierarchy_metadata.items()
        },
        'relationships': [rel.to_dict() for rel in relationships],
        'gaps': [gap.to_dict() for gap in gaps]
    }

    # Write output
    write_output(results, output_path, format)


def parse_args():
    """Parse command-line arguments"""
    parser = argparse.ArgumentParser(
        description='Matryoshka (hierarchical nesting) analysis for system architectures',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze a graph and output to stdout
  %(prog)s system_of_systems_graph.json

  # Save JSON output to file
  %(prog)s system_of_systems_graph.json --output report.json --format json

  # Run demo with hardcoded test data
  %(prog)s --demo
"""
    )

    parser.add_argument(
        'graph_file',
        nargs='?',
        type=str,
        help='Path to system_of_systems_graph.json file'
    )

    parser.add_argument(
        '--output', '-o',
        type=str,
        default=None,
        help='Output file path (default: stdout)'
    )

    parser.add_argument(
        '--format', '-f',
        choices=['text', 'json', 'markdown'],
        default='text',
        help='Output format (default: text)'
    )

    parser.add_argument(
        '--demo',
        action='store_true',
        help='Run demonstration with hardcoded test data'
    )

    return parser.parse_args()


def demo():
    """Demo of matryoshka analysis with hardcoded test data"""
    print("Running matryoshka analysis demo...\n", file=sys.stderr)

    # Example: Multi-level vehicle architectures
    architectures = [
        {
            "name": "Axle Component",
            "domain": "mechanical",
            "components": [
                {"name": "Shaft"},
                {"name": "Bearing"},
                {"name": "Housing"}
            ],
            "description": "Individual axle component for vehicle"
        },
        {
            "name": "Drivetrain System",
            "domain": "mechanical",
            "components": [
                {"name": "Engine"},
                {"name": "Transmission"},
                {"name": "Driveshaft"},
                {"name": "Differential"},
                {"name": "Axles"}
            ],
            "description": "Complete drivetrain system including power transmission"
        },
        {
            "name": "Vehicle Platform",
            "domain": "mechanical",
            "components": list(range(150)),  # Many components
            "description": "Complete vehicle platform integrating all systems"
        },
        {
            "name": "Suspension Component",
            "domain": "mechanical",
            "components": [
                {"name": "Spring"},
                {"name": "Shock Absorber"}
            ],
            "description": "Suspension component for vehicle"
        }
    ]

    analyzer = MatryoshkaAnalyzer()

    # Infer hierarchy levels
    hierarchy_metadata = {}
    for arch in architectures:
        meta = analyzer.infer_hierarchy_level(arch)
        hierarchy_metadata[arch['name']] = meta
        print(f"{arch['name']}: {meta.inferred_level} (confidence: {meta.confidence:.0%})")
    print()

    # Analyze relationships
    relationships = []
    for i, arch_a in enumerate(architectures):
        for arch_b in architectures[i+1:]:
            rel = analyzer.analyze_relationship(
                arch_a, arch_b,
                hierarchy_metadata[arch_a['name']],
                hierarchy_metadata[arch_b['name']]
            )
            relationships.append(rel)
            print(f"{rel.parent_architecture} <-> {rel.child_architecture}: {rel.relationship_type}")
    print()

    # Discover gaps
    gaps = analyzer.discover_hierarchical_gaps(architectures, relationships)
    print(f"Discovered {len(gaps)} hierarchical gap(s)\n")

    # Generate report
    report = analyzer.generate_matryoshka_report(
        architectures,
        hierarchy_metadata,
        relationships,
        gaps
    )
    print(report)


def main():
    """Main entry point - handles CLI arguments or runs demo"""
    args = parse_args()

    if args.demo:
        # Run demo with hardcoded test data
        demo()
    elif args.graph_file:
        # Analyze provided graph file
        analyze_graph(args.graph_file, args.output, args.format)
    else:
        # No arguments provided
        print("Error: Please provide a graph file or use --demo flag", file=sys.stderr)
        print("Run with --help for usage information", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
