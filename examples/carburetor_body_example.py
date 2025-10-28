#!/usr/bin/env python3
"""
Concrete Example: Carburetor to Body of Car

This demonstrates the matryoshka analysis with the exact scenario:
User tries to link Carburetor to Body of Car - they are NOT peers!

The actual hierarchy:
Vehicle (system-of-systems)
  ├─ Body System (system level)  ← Peer to Engine System
  └─ Engine System (system level) ← KNOWLEDGE GAP! This is missing!
      └─ Carburetor (component level)

When you try to link Carburetor to Body:
1. Matryoshka detects they're at different levels
2. Identifies the missing intermediate: Engine System
3. Recognizes Engine System is the PEER to Body
4. Carburetor is part of that unknown peer system

This shows how hierarchical gaps can reveal missing peer systems, not just
missing parents or intermediates.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from matryoshka_analysis import MatryoshkaAnalyzer, HierarchyLevel


def run_example():
    """Run the carburetor-to-body example"""

    # Define the architectures
    carburetor = {
        "name": "Carburetor",
        "domain": "mechanical",
        "components": [
            {"name": "Throttle Valve"},
            {"name": "Venturi"},
            {"name": "Float Chamber"},
            {"name": "Jets"}
        ],
        "description": "Carburetor component for mixing air and fuel"
    }

    body_of_car = {
        "name": "Body of Car",
        "domain": "mechanical",
        "components": [
            {"name": "Frame"},
            {"name": "Doors"},
            {"name": "Windows"},
            {"name": "Roof"},
            {"name": "Hood"},
            {"name": "Trunk"},
            {"name": "Seats"},
            {"name": "Dashboard"},
            {"name": "Interior Panels"},
            {"name": "Exterior Panels"}
        ],
        "description": "Complete body system of the vehicle including frame and panels"
    }

    print("="*70)
    print("MATRYOSHKA ANALYSIS: Carburetor to Body of Car")
    print("="*70)
    print()
    print("Scenario: User wants to link Carburetor to Body of Car")
    print()

    # Analyze with matryoshka
    analyzer = MatryoshkaAnalyzer()

    # Infer hierarchy levels
    print("Step 1: Detect Hierarchy Levels")
    print("-"*70)

    carburetor_meta = analyzer.infer_hierarchy_level(carburetor)
    print(f"Carburetor: {carburetor_meta.inferred_level}")
    print(f"  Confidence: {carburetor_meta.confidence:.0%}")
    print(f"  Evidence:")
    for ev in carburetor_meta.evidence:
        print(f"    • {ev}")
    print()

    body_meta = analyzer.infer_hierarchy_level(body_of_car)
    print(f"Body of Car: {body_meta.inferred_level}")
    print(f"  Confidence: {body_meta.confidence:.0%}")
    print(f"  Evidence:")
    for ev in body_meta.evidence:
        print(f"    • {ev}")
    print()

    # Analyze relationship
    print("Step 2: Analyze Relationship")
    print("-"*70)

    relationship = analyzer.analyze_relationship(
        carburetor, body_of_car,
        carburetor_meta, body_meta
    )

    print(f"Relationship Type: {relationship.relationship_type}")
    print(f"Evidence:")
    for ev in relationship.evidence:
        print(f"  • {ev}")
    print()

    # The key insight
    print("⚠️  KEY INSIGHT")
    print("-"*70)
    print("Carburetor and Body are at DIFFERENT LEVELS!")
    print(f"  Carburetor: {carburetor_meta.inferred_level}")
    print(f"  Body: {body_meta.inferred_level}")
    print()
    print("They are NOT peers. Don't link them directly!")
    print()

    # Discover gaps
    print("Step 3: Discover Hierarchical Gaps")
    print("-"*70)

    architectures = [carburetor, body_of_car]
    relationships = [relationship]

    gaps = analyzer.discover_hierarchical_gaps(architectures, relationships)

    print(f"Found {len(gaps)} hierarchical gap(s):")
    print()

    for i, gap in enumerate(gaps, 1):
        print(f"{i}. {gap.gap_type.replace('_', ' ').title()}")
        print(f"   Hypothesis: {gap.hypothesis}")
        print(f"   Missing Level: {gap.missing_level}")
        print()

    # The revelation
    print("="*70)
    print("THE REVELATION: What's Actually Missing")
    print("="*70)
    print()
    print("The gap analysis reveals the missing intermediate:")
    print()
    print("Correct Hierarchy:")
    print()
    print("Vehicle (system-of-systems)")
    print("  ├─ Body System (system level)")
    print("  └─ Engine System (system level)  ← THIS IS THE KNOWLEDGE GAP!")
    print("      └─ Carburetor (component level)")
    print()
    print("Key Insights:")
    print("  1. Body System and Engine System are PEERS (both at system level)")
    print("  2. Carburetor is PART OF Engine System")
    print("  3. The missing knowledge gap is ENGINE SYSTEM")
    print("  4. Don't link Carburetor to Body - link Engine System to Body!")
    print()

    # Integration decision
    print("="*70)
    print("INTEGRATION DECISION")
    print("="*70)
    print()
    print("❌ WRONG: Link Carburetor directly to Body of Car")
    print("   (Different hierarchical levels, skips intermediate)")
    print()
    print("✓ CORRECT: Document the missing Engine System")
    print("   1. Create architecture for Engine System (system level)")
    print("   2. Link Carburetor to Engine System (parent-child)")
    print("   3. Link Engine System to Body System (peers)")
    print("   4. Both contained by Vehicle (system-of-systems)")
    print()
    print("The 'gap' between Carburetor and Body isn't a missing link -")
    print("it's a missing PEER SYSTEM (Engine) that contains Carburetor!")
    print()

    # More examples
    print("="*70)
    print("MORE EXAMPLES OF THIS PATTERN")
    print("="*70)
    print()

    examples = [
        {
            "component": "Login API Endpoint",
            "system": "E-commerce Platform",
            "missing_peer": "User Service",
            "explanation": "Login is part of User Service, which is peer to other services in the platform"
        },
        {
            "component": "Brake Caliper",
            "system": "Vehicle Chassis",
            "missing_peer": "Brake System",
            "explanation": "Caliper is part of Brake System, which is peer to Suspension, Steering, etc."
        },
        {
            "component": "Database Table",
            "system": "Web Application",
            "missing_peer": "Database Service",
            "explanation": "Table is part of Database Service, which is peer to other services"
        },
        {
            "component": "Gene",
            "system": "Organism",
            "missing_peer": "Metabolic Pathway",
            "explanation": "Gene is part of a pathway, which is peer to other pathways in the organism"
        }
    ]

    for ex in examples:
        print(f"Example: Linking {ex['component']} to {ex['system']}")
        print(f"  Missing Peer: {ex['missing_peer']}")
        print(f"  Explanation: {ex['explanation']}")
        print()

    print("In all cases, the 'gap' is the missing PEER system that contains")
    print("the component, not a direct link between component and system!")
    print()


if __name__ == '__main__':
    run_example()
