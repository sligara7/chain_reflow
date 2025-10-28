#!/usr/bin/env python3
"""
Interactive Workflow Executor for Chain Reflow
Handles user interaction and LLM-guided workflow execution
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime


class InteractiveExecutor:
    """Interactive workflow executor with user prompts and guidance"""

    def __init__(self, workflow_file: str, system_root: Optional[str] = None):
        self.workflow_file = Path(workflow_file)
        self.system_root = Path(system_root) if system_root else Path.cwd()
        self.context_dir = self.system_root / "context"
        self.workflow_data = None
        self.working_memory = {}
        self.framework_selected = None

        self._load_workflow()
        self._init_context()

    def _load_workflow(self):
        """Load workflow JSON"""
        with open(self.workflow_file, 'r') as f:
            self.workflow_data = json.load(f)

    def _init_context(self):
        """Initialize context directory"""
        self.context_dir.mkdir(parents=True, exist_ok=True)

        working_memory_file = self.context_dir / "working_memory.json"
        if working_memory_file.exists():
            with open(working_memory_file, 'r') as f:
                self.working_memory = json.load(f)
        else:
            self.working_memory = {
                "system_name": None,
                "workflow_id": self.workflow_data['workflow_metadata']['workflow_id'],
                "workflow_version": self.workflow_data['workflow_metadata']['version'],
                "started_at": datetime.now().isoformat(),
                "paths": {
                    "system_root": str(self.system_root.absolute()),
                    "reflow_root": None,
                    "tools_path": None,
                    "templates_path": None,
                    "workflow_steps_path": None,
                    "definitions_path": None
                },
                "framework_configuration": {},
                "current_step": None,
                "operations_since_refresh": 0
            }

    def _save_working_memory(self):
        """Save working memory"""
        working_memory_file = self.context_dir / "working_memory.json"
        with open(working_memory_file, 'w') as f:
            json.dump(self.working_memory, f, indent=2)

    def run_step_s01_path_configuration(self):
        """Execute S-01: Path Configuration"""
        print("\n" + "="*70)
        print("STEP S-01: Path Configuration")
        print("="*70)
        print("\nThis step configures all required paths for workflow operation.")
        print("\nPath configuration is critical for tool invocations.")
        print("All paths must be absolute for proper operation.\n")

        # S-01-A01: Identify reflow_root
        print("-" * 70)
        print("Action S-01-A01: Identify and validate reflow_root path")
        print("-" * 70)

        reflow_root = input("\nEnter the path to reflow installation (reflow_root): ").strip()
        reflow_root = Path(reflow_root).absolute()

        # Verify reflow_root structure
        required_dirs = ["tools/", "templates/", "definitions/", "workflows/", "workflow_steps/"]
        print(f"\nVerifying reflow_root structure at: {reflow_root}")

        for dir_name in required_dirs:
            dir_path = reflow_root / dir_name.rstrip('/')
            if dir_path.exists():
                print(f"  ✓ Found: {dir_name}")
            else:
                print(f"  ✗ Missing: {dir_name}")
                print(f"\n⚠️  Warning: reflow_root may not be correctly configured")

        self.working_memory['paths']['reflow_root'] = str(reflow_root)

        # S-01-A02: Identify system_root
        print("\n" + "-" * 70)
        print("Action S-01-A02: Identify or create system_root path")
        print("-" * 70)

        print(f"\nCurrent system_root: {self.system_root}")
        use_current = input("Use current directory as system_root? [Y/n]: ").strip().lower()

        if use_current != 'n':
            system_root = self.system_root
        else:
            system_root = input("Enter path for system_root: ").strip()
            system_root = Path(system_root).absolute()
            system_root.mkdir(parents=True, exist_ok=True)

        self.working_memory['paths']['system_root'] = str(system_root)

        # S-01-A03: Derive tool paths
        print("\n" + "-" * 70)
        print("Action S-01-A03: Derive and store all tool paths")
        print("-" * 70)

        self.working_memory['paths']['tools_path'] = str(reflow_root / "tools")
        self.working_memory['paths']['templates_path'] = str(reflow_root / "templates")
        self.working_memory['paths']['workflow_steps_path'] = str(reflow_root / "workflow_steps")
        self.working_memory['paths']['definitions_path'] = str(reflow_root / "definitions")

        print("\nDerived paths:")
        for key, value in self.working_memory['paths'].items():
            print(f"  {key}: {value}")

        # Save working memory
        self._save_working_memory()
        print("\n✓ Path configuration saved to context/working_memory.json")

        # S-01-A04: Validation (simulated)
        print("\n" + "-" * 70)
        print("Action S-01-A04: Run validation (simulated)")
        print("-" * 70)
        print(f"\nWould execute: python3 {reflow_root}/tools/validate_reflow_setup.py {system_root}")
        print("✓ Path configuration complete")

    def run_step_s01a_framework_selection(self):
        """Execute S-01A: Architectural Framework Selection"""
        print("\n" + "="*70)
        print("STEP S-01A: Architectural Framework Selection")
        print("="*70)
        print("\nFramework selection is an ARCHITECTURAL DECISION.")
        print("The wrong framework leads to wrong insights.\n")

        # S-01A-A01: System characteristics analysis
        print("-" * 70)
        print("Action S-01A-A01: Analyze system domain and characteristics")
        print("-" * 70)

        print("\nSemantic Matching Questionnaire:")
        print("\nThis questionnaire helps match your system to the appropriate framework.")

        # Question 1
        print("\n1. What are your primary entities (nodes)?")
        print("   a) Services that communicate via APIs")
        print("   b) States in a process with transitions")
        print("   c) Agents with relationships")
        print("   d) Species in an ecosystem")
        print("   e) Genes, proteins, or molecules")
        print("   f) Adaptive agents that learn")
        print("   g) Other")

        q1 = input("\nYour answer (a-g): ").strip().lower()

        # Question 2
        print("\n2. What are your connections (edges)?")
        print("   a) API calls or data interfaces")
        print("   b) State transitions with conditions")
        print("   c) Social relationships or interactions")
        print("   d) Energy/matter flow or species interactions")
        print("   e) Molecular interactions (activation, inhibition)")
        print("   f) Adaptive interactions with feedback")
        print("   g) Other")

        q2 = input("\nYour answer (a-g): ").strip().lower()

        # Question 3
        print("\n3. Do edges have conditions or branching?")
        print("   a) Yes, if/else routing or decision points")
        print("   b) Yes, but based on agent decisions")
        print("   c) No, always connected")
        print("   d) Yes, based on environmental factors")

        q3 = input("\nYour answer (a-d): ").strip().lower()

        # Question 4
        print("\n4. Are cycles expected behavior or errors?")
        print("   a) Expected - feedback loops are essential")
        print("   b) Expected - rework loops are normal")
        print("   c) Errors - circular dependencies are bad")
        print("   d) Neither - cycles not relevant")

        q4 = input("\nYour answer (a-d): ").strip().lower()

        # Recommend framework based on answers
        framework_recommendation = self._recommend_framework(q1, q2, q3, q4)

        # S-01A-A04 & A05: Present recommendation and get confirmation
        print("\n" + "-" * 70)
        print("Framework Recommendation")
        print("-" * 70)

        print(f"\nRecommended: {framework_recommendation['name']}")
        print(f"\nRationale: {framework_recommendation['rationale']}")
        print(f"\nThis framework reveals:")
        for insight in framework_recommendation['reveals']:
            print(f"  • {insight}")

        print(f"\nNetworkX analyses enabled:")
        for analysis in framework_recommendation['enabled_analyses']:
            print(f"  • {analysis}")

        print("\n⚠️  IMPORTANT: Framework selection determines entire analysis approach.")
        print("Switching later requires re-doing all architecture files.")

        confirmation = input(f"\nProceed with {framework_recommendation['name']}? [Y/n]: ").strip().lower()

        if confirmation != 'n':
            self.framework_selected = framework_recommendation['id']
            self.working_memory['framework_configuration'] = {
                "framework_id": framework_recommendation['id'],
                "framework_name": framework_recommendation['name'],
                "component_term": framework_recommendation.get('component_term', 'component'),
                "connection_term": framework_recommendation.get('connection_term', 'connection'),
                "user_confirmed": True,
                "confirmation_timestamp": datetime.now().isoformat()
            }
            self._save_working_memory()
            print(f"\n✓ Framework selected: {framework_recommendation['name']}")
        else:
            print("\n⚠️  Framework selection cancelled. Please re-run framework selection.")

    def _recommend_framework(self, q1, q2, q3, q4) -> Dict[str, Any]:
        """Recommend framework based on questionnaire answers"""

        # Simple rule-based recommendation
        if q1 == 'b' and q2 == 'b':
            return {
                "id": "decision_flow",
                "name": "Decision Flow Framework",
                "rationale": "Your system has states with conditional transitions, which is the core abstraction of Decision Flow.",
                "reveals": [
                    "Critical paths through the workflow",
                    "Bottlenecks and rework loops",
                    "Decision points with highest impact"
                ],
                "enabled_analyses": [
                    "Flow analysis (with transition probabilities)",
                    "Cycle detection (rework loops)",
                    "Critical path analysis",
                    "Centrality analysis"
                ],
                "component_term": "state",
                "connection_term": "transition"
            }
        elif q1 == 'a' and q2 == 'a':
            return {
                "id": "uaf",
                "name": "Unified Architecture Framework (UAF)",
                "rationale": "Your system has services communicating via APIs, which maps to UAF's service-oriented architecture.",
                "reveals": [
                    "Service dependencies",
                    "Interface contracts",
                    "Deployment architecture"
                ],
                "enabled_analyses": [
                    "DAG analysis (verify no circular dependencies)",
                    "Centrality analysis (identify critical services)",
                    "Component analysis"
                ],
                "component_term": "service",
                "connection_term": "interface"
            }
        elif q1 == 'c' and q2 == 'c':
            return {
                "id": "social_network",
                "name": "Social Network Analysis Framework",
                "rationale": "Your system has agents with relationships, which is the core abstraction of social networks.",
                "reveals": [
                    "Influential agents",
                    "Communities and clusters",
                    "Information flow patterns"
                ],
                "enabled_analyses": [
                    "Centrality analysis (identify key agents)",
                    "Community detection",
                    "Clustering analysis",
                    "Network topology"
                ],
                "component_term": "agent",
                "connection_term": "relationship"
            }
        elif q1 == 'e' and q2 == 'e':
            return {
                "id": "systems_biology",
                "name": "Systems Biology Framework",
                "rationale": "Your system has molecular interactions with regulation, which maps to systems biology networks.",
                "reveals": [
                    "Regulatory feedback loops",
                    "Key regulatory molecules",
                    "Pathway dynamics"
                ],
                "enabled_analyses": [
                    "Cycle detection (feedback loops)",
                    "Flow analysis (reaction rates)",
                    "Centrality analysis (key regulators)",
                    "Pathway analysis"
                ],
                "component_term": "molecule",
                "connection_term": "interaction"
            }
        else:
            # Default to custom framework
            return {
                "id": "custom",
                "name": "Custom Framework",
                "rationale": "Your system doesn't clearly match standard frameworks. A custom framework will be created.",
                "reveals": [
                    "System-specific patterns",
                    "Domain-specific insights"
                ],
                "enabled_analyses": [
                    "Basic graph analysis",
                    "Topology analysis"
                ],
                "component_term": "component",
                "connection_term": "connection"
            }

    def run_step_s02_directory_structure(self):
        """Execute S-02: Directory Structure Creation"""
        print("\n" + "="*70)
        print("STEP S-02: Directory Structure Creation")
        print("="*70)

        required_dirs = ["context", "specs", "services", "docs", "architectures"]

        print("\nCreating directory structure...")
        for dir_name in required_dirs:
            dir_path = self.system_root / dir_name
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"  ✓ Created: {dir_name}/")

        print("\n✓ Directory structure created")

    def run_step_s03_foundational_documents(self):
        """Execute S-03: Foundational Documents"""
        print("\n" + "="*70)
        print("STEP S-03: Foundational Documents")
        print("="*70)

        # Get system name
        system_name = input("\nEnter system name: ").strip()
        self.working_memory['system_name'] = system_name

        # Mission statement
        print("\n" + "-" * 70)
        print("Creating Mission Statement")
        print("-" * 70)

        mission = input("\nEnter mission statement (or press Enter for guided creation): ").strip()

        if not mission:
            print("\nGuided Mission Statement Creation:")
            purpose = input("  What is the system's primary purpose? ").strip()
            users = input("  Who are the primary users? ").strip()
            value = input("  What value does it provide? ").strip()

            mission = f"{system_name} {purpose} for {users}, providing {value}."

        mission_file = self.system_root / "docs" / "mission_statement.md"
        with open(mission_file, 'w') as f:
            f.write(f"# {system_name} - Mission Statement\n\n")
            f.write(f"**Created:** {datetime.now().strftime('%Y-%m-%d')}\n\n")
            f.write(f"{mission}\n")

        print(f"\n✓ Mission statement saved to: {mission_file}")

        # User scenarios
        print("\n" + "-" * 70)
        print("Creating User Scenarios")
        print("-" * 70)

        scenarios = []
        while True:
            scenario = input("\nEnter a user scenario (or press Enter to finish): ").strip()
            if not scenario:
                break
            scenarios.append(scenario)

        scenarios_file = self.system_root / "docs" / "user_scenarios.md"
        with open(scenarios_file, 'w') as f:
            f.write(f"# {system_name} - User Scenarios\n\n")
            f.write(f"**Created:** {datetime.now().strftime('%Y-%m-%d')}\n\n")
            for i, scenario in enumerate(scenarios, 1):
                f.write(f"## Scenario {i}\n\n{scenario}\n\n")

        print(f"✓ User scenarios saved to: {scenarios_file}")

        # Success criteria
        print("\n" + "-" * 70)
        print("Creating Success Criteria")
        print("-" * 70)

        criteria = []
        while True:
            criterion = input("\nEnter a success criterion (or press Enter to finish): ").strip()
            if not criterion:
                break
            criteria.append(criterion)

        criteria_file = self.system_root / "docs" / "success_criteria.md"
        with open(criteria_file, 'w') as f:
            f.write(f"# {system_name} - Success Criteria\n\n")
            f.write(f"**Created:** {datetime.now().strftime('%Y-%m-%d')}\n\n")
            for i, criterion in enumerate(criteria, 1):
                f.write(f"{i}. {criterion}\n")

        print(f"✓ Success criteria saved to: {criteria_file}")

        # Update working memory
        self._save_working_memory()
        print("\n✓ Foundational documents created")

    def run(self):
        """Run the complete setup workflow interactively"""
        print("\n" + "="*70)
        print(f"Chain Reflow - {self.workflow_data['workflow_metadata']['name']}")
        print("="*70)
        print(f"\n{self.workflow_data['workflow_metadata']['description']}\n")
        print(f"Version: {self.workflow_data['workflow_metadata']['version']}")
        print(f"System Root: {self.system_root}\n")

        input("Press Enter to begin...")

        # Execute steps
        self.run_step_s01_path_configuration()
        self.run_step_s01a_framework_selection()
        self.run_step_s02_directory_structure()
        self.run_step_s03_foundational_documents()

        print("\n" + "="*70)
        print("Setup Workflow Complete!")
        print("="*70)
        print(f"\nSystem: {self.working_memory.get('system_name', 'N/A')}")
        print(f"Framework: {self.working_memory['framework_configuration'].get('framework_name', 'N/A')}")
        print(f"Root: {self.system_root}")
        print("\nNext steps:")
        print("  1. Review generated documents in docs/")
        print("  2. Run architecture development workflows")
        print("  3. Begin system design\n")


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Interactive Chain Reflow Workflow Executor')
    parser.add_argument('workflow', help='Path to workflow JSON file')
    parser.add_argument('--system-root', help='Root directory for the system', default='.')

    args = parser.parse_args()

    executor = InteractiveExecutor(args.workflow, args.system_root)
    executor.run()


if __name__ == '__main__':
    main()
