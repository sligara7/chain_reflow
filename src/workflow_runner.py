#!/usr/bin/env python3
"""
Chain Reflow Workflow Runner
Executes reflow workflows in the context of chaining multiple system architectures
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime


class WorkflowRunner:
    """Main workflow execution engine for chain_reflow"""

    def __init__(self, workflow_file: str, system_root: Optional[str] = None):
        """
        Initialize the workflow runner

        Args:
            workflow_file: Path to the workflow JSON file
            system_root: Root directory for the system being developed
        """
        self.workflow_file = Path(workflow_file)
        self.system_root = Path(system_root) if system_root else Path.cwd()
        self.context_dir = self.system_root / "context"
        self.workflow_data = None
        self.working_memory = {}

        # Load workflow
        self._load_workflow()

        # Initialize context
        self._init_context()

    def _load_workflow(self):
        """Load the workflow JSON file"""
        try:
            with open(self.workflow_file, 'r') as f:
                self.workflow_data = json.load(f)
            print(f"✓ Loaded workflow: {self.workflow_data['workflow_metadata']['name']}")
            print(f"  Version: {self.workflow_data['workflow_metadata']['version']}")
            print(f"  Description: {self.workflow_data['workflow_metadata']['description']}\n")
        except Exception as e:
            print(f"✗ Failed to load workflow: {e}")
            sys.exit(1)

    def _init_context(self):
        """Initialize the context directory and working memory"""
        # Create context directory if it doesn't exist
        self.context_dir.mkdir(parents=True, exist_ok=True)

        # Load or create working memory
        working_memory_file = self.context_dir / "working_memory.json"
        if working_memory_file.exists():
            with open(working_memory_file, 'r') as f:
                self.working_memory = json.load(f)
            print("✓ Loaded existing working memory")
        else:
            self.working_memory = {
                "system_name": None,
                "workflow_id": self.workflow_data['workflow_metadata']['workflow_id'],
                "workflow_version": self.workflow_data['workflow_metadata']['version'],
                "started_at": datetime.now().isoformat(),
                "paths": {
                    "system_root": str(self.system_root.absolute())
                },
                "framework_configuration": {},
                "current_step": None,
                "operations_since_refresh": 0
            }
            print("✓ Initialized new working memory")

    def _save_working_memory(self):
        """Save working memory to disk"""
        working_memory_file = self.context_dir / "working_memory.json"
        with open(working_memory_file, 'w') as f:
            json.dump(self.working_memory, f, indent=2)

    def _update_step_progress(self, step_id: str, status: str, details: Optional[Dict] = None):
        """Update step progress tracker"""
        tracker_file = self.context_dir / "step_progress_tracker.json"

        if tracker_file.exists():
            with open(tracker_file, 'r') as f:
                tracker = json.load(f)
        else:
            tracker = {"steps": {}}

        tracker["steps"][step_id] = {
            "status": status,
            "timestamp": datetime.now().isoformat(),
            "details": details or {}
        }

        with open(tracker_file, 'w') as f:
            json.dump(tracker, f, indent=2)

    def run(self, entry_point: str = "new_system"):
        """
        Run the workflow from a specific entry point

        Args:
            entry_point: The entry point ID to start from
        """
        print(f"\n{'='*60}")
        print(f"Starting Workflow Execution")
        print(f"{'='*60}\n")

        # Get the entry point
        if entry_point not in self.workflow_data.get('entry_points', {}):
            print(f"✗ Unknown entry point: {entry_point}")
            return

        entry = self.workflow_data['entry_points'][entry_point]
        first_step_id = entry['first_step']

        print(f"Entry Point: {entry['description']}")
        print(f"Starting at step: {first_step_id}\n")

        # Execute workflow steps
        current_step_id = first_step_id
        while current_step_id:
            current_step_id = self._execute_step(current_step_id)

        print(f"\n{'='*60}")
        print(f"Workflow Execution Complete")
        print(f"{'='*60}\n")

    def _execute_step(self, step_id: str) -> Optional[str]:
        """
        Execute a single workflow step

        Args:
            step_id: The step ID to execute

        Returns:
            The next step ID, or None if workflow is complete
        """
        # Find the step in the workflow
        step = None
        for s in self.workflow_data.get('workflow_steps', []):
            if s['step_id'] == step_id:
                step = s
                break

        if not step:
            print(f"✗ Step {step_id} not found in workflow")
            return None

        print(f"\n{'─'*60}")
        print(f"Step {step_id}: {step['name']}")
        print(f"{'─'*60}")
        print(f"Description: {step['description']}")
        print(f"Phase: {step.get('phase', 'unknown')}\n")

        # Update working memory
        self.working_memory['current_step'] = step_id
        self._save_working_memory()

        # Update progress tracker
        self._update_step_progress(step_id, "in_progress")

        # Execute actions
        for action in step.get('actions', []):
            self._execute_action(step_id, action)

        # Mark step as complete
        self._update_step_progress(step_id, "completed")

        # Increment operations counter
        self.working_memory['operations_since_refresh'] += 1
        self._save_working_memory()

        # Return next step
        return step.get('next_step')

    def _execute_action(self, step_id: str, action: Dict[str, Any]):
        """
        Execute a single action within a step

        Args:
            step_id: The parent step ID
            action: The action configuration
        """
        action_id = action['action_id']
        description = action['description']

        print(f"  [{action_id}] {description}")

        # Handle different action types
        if 'command_pattern' in action:
            # This is a command execution action
            command = action['command_pattern']
            print(f"    Command: {command}")
            print(f"    (Simulated - would execute: {command})")

        elif 'user_prompt' in action:
            # This is a user interaction action
            prompt = action['user_prompt']
            print(f"    User Prompt Required:")
            print(f"    {prompt.get('message_format', 'N/A')}")

        elif 'llm_instructions' in action:
            # This is an LLM-guided action
            instructions = action['llm_instructions']
            print(f"    LLM Instructions:")
            for i, instr in enumerate(instructions, 1):
                print(f"      {i}. {instr}")

        elif 'purpose' in action:
            # General purpose action
            print(f"    Purpose: {action['purpose']}")

        # Handle storage updates
        if 'store_in' in action:
            store_location = action['store_in']
            print(f"    Storing results in: {store_location}")

            # If this is working_memory.json, update it
            if 'working_memory.json' in store_location:
                if 'updates' in action:
                    self._apply_updates(action['updates'])
                    self._save_working_memory()

        # Handle verification
        if 'verification' in action:
            print(f"    Verification: {action['verification']}")

        print()

    def _apply_updates(self, updates: Dict[str, Any]):
        """Apply updates to working memory"""
        for key, value in updates.items():
            if isinstance(value, dict):
                if key not in self.working_memory:
                    self.working_memory[key] = {}
                self.working_memory[key].update(value)
            else:
                self.working_memory[key] = value

    def get_status(self) -> Dict[str, Any]:
        """Get current workflow execution status"""
        return {
            "workflow_id": self.workflow_data['workflow_metadata']['workflow_id'],
            "workflow_name": self.workflow_data['workflow_metadata']['name'],
            "current_step": self.working_memory.get('current_step'),
            "system_root": str(self.system_root),
            "context_dir": str(self.context_dir),
            "operations_since_refresh": self.working_memory.get('operations_since_refresh', 0)
        }


def main():
    """Main entry point for the workflow runner"""
    import argparse

    parser = argparse.ArgumentParser(description='Chain Reflow Workflow Runner')
    parser.add_argument('workflow', help='Path to workflow JSON file')
    parser.add_argument('--system-root', help='Root directory for the system', default='.')
    parser.add_argument('--entry-point', help='Workflow entry point', default='new_system')
    parser.add_argument('--status', action='store_true', help='Show status only')

    args = parser.parse_args()

    # Create runner
    runner = WorkflowRunner(args.workflow, args.system_root)

    if args.status:
        # Show status
        status = runner.get_status()
        print(json.dumps(status, indent=2))
    else:
        # Run workflow
        runner.run(args.entry_point)


if __name__ == '__main__':
    main()
