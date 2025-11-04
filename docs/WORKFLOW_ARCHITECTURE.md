# Chain Reflow Workflow Architecture

**Created**: 2025-11-04
**Pattern**: Based on reflow workflow methodology
**Purpose**: Link multiple system_of_systems_graph.json files at any hierarchical level

---

## Overview

Chain Reflow provides a complete workflow suite for linking independently developed system architectures, following the reflow framework's modular, staged approach.

### Core Principle

> "Take individual system_of_systems_graph.json files created by reflow and figure out how to link them, no matter how divergent or seemingly orthogonal they are."

---

## Workflow Suite Design

Following reflow's methodology, chain_reflow implements a **5-phase workflow architecture**:

### Phase 0: Setup & Configuration

**Workflow**: `chain-00-setup.json` ✅ **IMPLEMENTED**

**Purpose**: Initialize the chain_reflow system

**Steps**:
- CH00-01: Path Configuration - Verify directory structure
- CH00-02: Input Graph Discovery - Load system_of_systems_graph.json files
- CH00-03: Working Memory Initialization - Create session state
- CH00-04: Environment Validation - Check Python, dependencies, engines
- CH00-05: Setup Completion - Generate summary, mark ready

**Outputs**:
- `context/working_memory.json` - Session state
- `context/graph_inventory.json` - List of graphs to link
- `docs/setup_summary_{timestamp}.md`

**Quality Gates**:
- Minimum 2 valid graphs
- Valid JSON structure
- Python 3.8+ required

---

### Phase 1: Multi-Graph Analysis

#### Workflow 1A: `chain-01-analyze-multi-graphs.json`

**Purpose**: Analyze ALL graphs before linking

**Steps**:

**CH01-01: Domain & Framework Analysis**
- Extract domain from each graph (software, biological, mechanical, social, etc.)
- Extract framework (UAF, Decision Flow, Systems Biology, etc.)
- Classify architectural patterns
- Create domain compatibility matrix

**CH01-02: Pair-wise Orthogonality Assessment**
- For each graph pair (N choose 2 pairs for N graphs)
- Use CreativeLinkingEngine.assess_orthogonality()
- Classify as: ALIGNED, RELATED, DIVERGENT, ORTHOGONAL
- Store in orthogonality matrix

**CH01-03: Hierarchical Level Inference**
- For each graph, infer hierarchy level using Matryoshka analysis
- Classify as: component, subsystem, system, system-of-systems, enterprise
- Create hierarchy level map
- Identify level gaps (e.g., component and system-of-systems with no intermediate)

**CH01-04: Network Topology Analysis** (if N > 2)
- Analyze relationships between all N graphs
- Identify:
  - Hub graphs (central to many connections)
  - Peripheral graphs (few connections)
  - Clusters (groups of related graphs)
  - Bridges (graphs connecting clusters)

**CH01-05: Correlation Detection** (optional)
- If user provides observations about relationships
- Run causality analysis on each pair
- Generate correlation matrix
- Flag potential causal relationships

**Outputs**:
- `context/multi_graph_analysis.json`
- `context/orthogonality_matrix.json`
- `context/hierarchy_map.json`
- `context/network_topology.json`
- `docs/multi_graph_analysis_report_{timestamp}.md`

**Quality Gates**:
- All graphs successfully analyzed
- Orthogonality assessed for all pairs
- Hierarchy levels inferred

---

#### Workflow 1B: `chain-01a-determine-strategy.json`

**Purpose**: Decide HOW to link the graphs based on analysis

**Steps**:

**CH01A-01: Strategy Decision Matrix**

Based on multi-graph analysis, determine linking strategy:

**Case 1: All graphs at SAME hierarchy level**
→ Strategy: **Peer-to-peer mesh linking**
→ Workflow: chain-02b-link-network.json

**Case 2: Clear parent-child relationships**
→ Strategy: **Hierarchical linking**
→ Workflow: chain-02a-link-hierarchical.json

**Case 3: Mixed (2-3 graphs, mixed relationships)**
→ Strategy: **Iterative pairwise linking**
→ Workflow: chain-02-link-pairwise.json

**Case 4: Complex network (>5 graphs, various relationships)**
→ Strategy: **Phased linking** (clusters first, then inter-cluster)
→ Workflow: chain-02c-link-phased.json

**CH01A-02: Linking Order Determination**

For sequential linking (pairwise or phased):
- Determine optimal order based on:
  - Orthogonality (link ALIGNED pairs first)
  - Hierarchy (link adjacent levels first)
  - User priority (if specified)
  - Dependency analysis (if available)

**CH01A-03: Present Strategy to User**

Show user the recommended strategy with rationale:
```
📊 LINKING STRATEGY

Graphs to link: {N} graphs
Strategy: {strategy_name}
Rationale: {explanation}

Linking order:
1. {graph1} ↔ {graph2} ({orthogonality}, {hierarchy_relation})
2. {graph3} ↔ {graph4} ({orthogonality}, {hierarchy_relation})
...

Estimated touchpoints: {estimate}
Estimated time: {estimate}

Proceed? [Y/N]
Alternative strategy? [number]
```

**Outputs**:
- `context/linking_strategy.json`
- `context/linking_order.json`

---

### Phase 2: Linking Execution

#### Workflow 2A: `chain-02-link-pairwise.json`

**Purpose**: Link graphs two-at-a-time (iterative)

**Pattern**: Uses existing `chain-01-link-architectures.json` logic in a loop

**Steps**:

**CH02-01: Pair Selection**
- Select next pair from linking_order.json
- Load both graphs

**CH02-02: Execute Pairwise Linking**
- Run chain-01-link-architectures.json for this pair:
  - CH02-02-A01: Load & analyze (C-01)
  - CH02-02-A02: Correlation/causation analysis (C-01A)
  - CH02-02-A03: Matryoshka analysis (C-01B)
  - CH02-02-A04: Select linking strategy (C-02)
  - CH02-02-A05: Touchpoint discovery (C-03 or C-03A)
  - CH02-02-A06: Touchpoint refinement (C-04)
  - CH02-02-A07: Generate partial integrated graph (C-05)

**CH02-03: Merge Partial Result**
- Merge this pair's integrated graph with cumulative result
- Update touchpoint catalog
- Update validation status

**CH02-04: Check if More Pairs**
- If more pairs in linking_order.json:
  - Loop back to CH02-01
- Else:
  - Proceed to CH02-05

**CH02-05: Generate Pairwise Summary**
- Document all pairwise links created
- Show touchpoint statistics
- Mark any exploratory/creative links

**Outputs**:
- `output/pairwise_results/pair_{i}_integrated_graph.json` (for each pair)
- `output/cumulative_integrated_graph.json` (final)
- `docs/pairwise_linking_report_{timestamp}.md`

---

#### Workflow 2B: `chain-02a-link-hierarchical.json`

**Purpose**: Link graphs with clear parent-child relationships

**Key Difference**: Respects hierarchical containment (subsystems inside systems)

**Steps**:

**CH02A-01: Build Hierarchy Tree**
- From hierarchy_map.json, construct tree
- Root: Highest level graph (e.g., enterprise or system-of-systems)
- Leaves: Lowest level graphs (e.g., components)

**CH02A-02: Link Parent-Child Pairs**
- For each parent-child relationship:
  - Identify containment touchpoints
  - Generate containment interfaces
  - Document hierarchical dependencies

**CH02A-03: Link Siblings** (graphs at same level under same parent)
- For each sibling pair:
  - Run standard pairwise linking (chain-01 logic)
  - Mark as peer-to-peer connection

**CH02A-04: Generate Hierarchical Graph**
- Create system_of_systems_graph.json with:
  - Nested structure (parent contains children nodes)
  - Hierarchical metadata on edges
  - Clear tier assignments

**Outputs**:
- `output/hierarchical_integrated_graph.json`
- `docs/hierarchical_structure_{timestamp}.md`

---

#### Workflow 2C: `chain-02b-link-network.json`

**Purpose**: Link graphs as interconnected mesh/network (all at same level)

**Key Difference**: All graphs are peers, no parent-child relationships

**Steps**:

**CH02B-01: Identify Link Candidates**
- From orthogonality matrix:
  - ALIGNED pairs: Standard technical linking
  - RELATED pairs: Enhanced technical linking
  - DIVERGENT pairs: Hybrid (with user consent)
  - ORTHOGONAL pairs: Creative linking (with user consent)

**CH02B-02: Execute All-to-All Linking** (if N is small, <5)
- Link every pair (N choose 2)
- Run chain-01 logic for each

**CH02B-03: Execute Selective Linking** (if N is large, ≥5)
- Link only pairs with orthogonality ≤ RELATED
- Create hub-spoke topology (hub = central graph)
- Link peripheral graphs through hub

**CH02B-04: Optimize Network Topology**
- Remove redundant links
- Identify shortest paths
- Minimize coupling while ensuring connectivity

**CH02B-05: Generate Network Graph**
- Create flat system_of_systems_graph.json
- All nodes at same tier
- Edge weights represent link strength/confidence

**Outputs**:
- `output/network_integrated_graph.json`
- `docs/network_topology_{timestamp}.md`
- `docs/network_metrics_{timestamp}.json` (centrality, clustering, etc.)

---

### Phase 3: Integration & Merging

#### Workflow 3: `chain-03-merge-graphs.json`

**Purpose**: Create final unified system_of_systems_graph.json

**Steps**:

**CH03-01: Collect All Partial Graphs**
- From Phase 2 outputs (pairwise, hierarchical, or network)
- Validate each partial graph

**CH03-02: Merge Nodes**
- Deduplicate nodes (same node appearing in multiple partial graphs)
- Assign unique node_ids
- Preserve all metadata
- Assign tier/level based on hierarchy

**CH03-03: Merge Edges**
- Consolidate all touchpoints/edges
- Remove duplicate edges
- Assign edge weights (based on confidence, link type)
- Mark creative/exploratory edges

**CH03-04: Add System-level Metadata**
- Create root "system_of_systems_graph" object
- Add metadata:
  - Linked systems (count, names)
  - Total nodes, edges
  - Frameworks involved
  - Domains involved
  - Linking strategies used
  - Timestamp, version

**CH03-05: Validate Merged Graph**
- Check for orphan nodes
- Check for circular dependencies (if not allowed)
- Check tier consistency
- Verify all interfaces are provided

**Outputs**:
- `output/integrated_system_of_systems_graph.json` ✅ **FINAL OUTPUT**
- `context/merge_report.json`

---

#### Workflow 3A: `chain-03a-document-integration.json`

**Purpose**: Generate comprehensive integration documentation

**Steps**:

**CH03A-01: Generate Integration Report**

Contents:
- Executive Summary
  - Systems linked (N graphs)
  - Linking strategies used
  - Total touchpoints created
  - Hierarchical structure (if applicable)
- Per-Graph Analysis
  - Each input graph's role in integration
  - Touchpoints from/to this graph
  - Hierarchy level
- Touchpoint Catalog
  - All touchpoints with details
  - Standard vs creative
  - Validation status
- Known Issues/Gaps
  - Exploratory links requiring validation
  - Missing intermediate levels
  - Unresolved correlations vs causations

**CH03A-02: Generate Visual Documentation**
- If reflow integrated, run system_of_systems_graph_v2.py on final graph
- Generate graph visualization (DOT/GraphViz)
- Generate network metrics report

**CH03A-03: Generate Interface Catalog Document (ICD)**
- Document all interfaces between linked systems
- API specifications
- Data schemas
- Protocols

**Outputs**:
- `docs/integration_report_{timestamp}.md` ✅ **MAIN DOCUMENTATION**
- `docs/touchpoint_catalog_{timestamp}.md`
- `docs/interface_control_document_{timestamp}.md`
- `output/integrated_graph_visualization.png` (if available)

---

### Phase 4: Validation & Analysis

#### Workflow 4: `chain-04-validate.json`

**Purpose**: Validate the integrated graph using reflow analysis tools

**Steps**:

**CH04-01: Run Reflow Graph Analysis** (if reflow available)
- Execute reflow's system_of_systems_graph_v2.py on integrated graph
- Run all 25+ NetworkX algorithms
- Detect:
  - Knowledge gaps
  - Orphaned interfaces
  - Missing nodes
  - Structural holes
  - Circular dependencies
  - Community clusters

**CH04-02: Analyze Integration Quality**
- Metrics:
  - **Coverage**: % of nodes from original graphs included
  - **Connectivity**: Avg path length between systems
  - **Modularity**: How well systems remain distinct
  - **Cohesion**: How tightly linked each system's nodes are
  - **Coupling**: How many cross-system links exist

**CH04-03: Validate Touchpoints**
- For each touchpoint:
  - Verify source and target nodes exist
  - Verify interfaces are compatible
  - Check if exploratory link requires validation
  - Suggest concrete interface implementation

**CH04-04: Generate Validation Report**

Include:
- ✅ Passes: What's valid and working
- ⚠️  Warnings: Issues that should be reviewed
- ❌ Failures: Critical problems blocking integration
- 🔍 Recommendations: Suggested improvements

**CH04-05: Present Results to User**

Show:
- Overall integration score (0-100)
- Breakdown by category (structure, interfaces, hierarchy)
- Action items for user
- Next steps (if validation fails)

**Outputs**:
- `output/validation_report_{timestamp}.md`
- `output/integration_score.json`
- `output/reflow_analysis_{timestamp}.json` (if reflow used)

**Quality Gates**:
- No orphan nodes
- No circular dependencies (unless intentional)
- All required interfaces have providers
- Minimum integration score (e.g., 70/100)

---

## Workflow Execution Patterns

### Sequential (Chain) Execution

```
chain-00-setup
  ↓
chain-01-analyze-multi-graphs
  ↓
chain-01a-determine-strategy
  ↓
chain-02-{link-pairwise | link-hierarchical | link-network}
  ↓
chain-03-merge-graphs
  ↓
chain-03a-document-integration
  ↓
chain-04-validate
```

### Branching Based on Strategy

```
chain-01a-determine-strategy
  ├─→ Pairwise → chain-02-link-pairwise
  ├─→ Hierarchical → chain-02a-link-hierarchical
  └─→ Network → chain-02b-link-network
     ↓
     (all converge)
     ↓
chain-03-merge-graphs
```

### Loop Pattern (Pairwise)

```
chain-02-link-pairwise
  ├─→ [For each pair in linking_order]
  │     ├─→ Run chain-01 logic
  │     └─→ Merge result
  └─→ [All pairs done] → CH02-05
```

---

## Key Design Principles

### 1. Modular Workflows

Each workflow is self-contained and can be:
- Executed independently (if prerequisites met)
- Tested in isolation
- Extended without affecting others

### 2. Reusability

The existing `chain-01-link-architectures.json` is **reused** in:
- chain-02-link-pairwise (as inner loop logic)
- chain-02a-link-hierarchical (for sibling linking)
- chain-02b-link-network (for each pair)

**Don't Duplicate, Delegate!**

### 3. Working Memory Pattern

All workflows read/write `context/working_memory.json`:
- Current workflow ID
- Current step ID
- Session state
- Cumulative results

Enables:
- **Resume**: If workflow interrupted, resume from last step
- **Audit**: Full trace of what happened
- **Debugging**: Inspect state at any point

### 4. Quality Gates

Each workflow has quality gates:
- **Blocking**: Must pass to continue
- **Warning**: Issues flagged but workflow continues
- **Interactive**: User decision required

### 5. Human-in-the-Loop

Following reflow v3.8.0 pattern:
- User consent for creative linking
- User validation of touchpoints
- User strategy selection (if alternatives exist)

### 6. Scalability Considerations

**Small N (2-3 graphs)**:
- Run all-to-all linking
- Simple sequential execution

**Medium N (4-10 graphs)**:
- Selective linking based on orthogonality
- Hub-spoke or clustered topology
- Phased execution

**Large N (>10 graphs)**:
- Clustering first (group related graphs)
- Link within clusters
- Link cluster representatives
- Hierarchical decomposition

---

## Context Files (Working Memory)

### `context/working_memory.json`
```json
{
  "session_id": "timestamp",
  "current_workflow": "chain-XX",
  "current_step": "CHXX-YY",
  "status": "in_progress",
  "graphs": [...],
  "completed_workflows": ["chain-00", "chain-01"],
  "next_workflow": "chain-02",
  "timestamps": {...}
}
```

### `context/graph_inventory.json`
```json
{
  "graphs": [
    {
      "graph_id": "graph1",
      "file_path": "...",
      "system_name": "...",
      "node_count": 10,
      "edge_count": 15
    }
  ],
  "summary": {...}
}
```

### `context/linking_strategy.json`
```json
{
  "strategy": "pairwise" | "hierarchical" | "network",
  "rationale": "...",
  "graph_count": 5,
  "estimated_pairs": 10,
  "selected_workflow": "chain-02-link-pairwise"
}
```

### `context/orthogonality_matrix.json`
```json
{
  "matrix": [
    ["graph1", "graph2", "ALIGNED"],
    ["graph1", "graph3", "ORTHOGONAL"],
    ...
  ]
}
```

### `context/hierarchy_map.json`
```json
{
  "graph1": {
    "level": "system",
    "confidence": 0.9
  },
  "graph2": {
    "level": "component",
    "confidence": 0.85
  }
}
```

---

## Output Files

### Primary Output

**`output/integrated_system_of_systems_graph.json`** ✅
- The final linked system graph
- Compatible with reflow analysis tools
- Can be further refined or validated

### Supporting Outputs

- `output/pairwise_results/` - Intermediate pairwise graphs
- `output/validation_report_{timestamp}.md` - Validation results
- `output/integration_score.json` - Quantitative metrics
- `docs/integration_report_{timestamp}.md` - Full documentation
- `docs/touchpoint_catalog_{timestamp}.md` - All touchpoints
- `docs/interface_control_document_{timestamp}.md` - ICDs

---

## Implementation Status

### ✅ Implemented

- `chain-00-setup.json` - Complete
- `chain-01-link-architectures.json` - Exists (single pair linking)
- Analysis engines (creative_linking, causality_analysis, matryoshka_analysis)

### 📝 Designed (This Document)

- `chain-01-analyze-multi-graphs.json`
- `chain-01a-determine-strategy.json`
- `chain-02-link-pairwise.json`
- `chain-02a-link-hierarchical.json`
- `chain-02b-link-network.json`
- `chain-03-merge-graphs.json`
- `chain-03a-document-integration.json`
- `chain-04-validate.json`

### 🔮 Future Enhancements

- `chain-02c-link-phased.json` - For very large N
- `chain-05-optimize.json` - Refine integration post-validation
- `chain-06-deploy.json` - Generate deployable artifacts

---

## Usage Examples

### Example 1: Link 2 Software Systems

```bash
# Setup
Run workflow: chain-00-setup.json
  Input: system_a.json, system_b.json

# Analysis
Run workflow: chain-01-analyze-multi-graphs.json
  Output: Both are software, ALIGNED orthogonality

# Strategy
Run workflow: chain-01a-determine-strategy.json
  Selected: Pairwise (only 2 graphs)

# Link
Run workflow: chain-02-link-pairwise.json
  Output: 5 technical touchpoints (APIs)

# Merge & Document
Run workflow: chain-03-merge-graphs.json
Run workflow: chain-03a-document-integration.json

# Validate
Run workflow: chain-04-validate.json
  Result: 95/100 score, all checks pass
```

### Example 2: Link 5 Hierarchical Systems

```bash
# Setup
Run workflow: chain-00-setup.json
  Input: enterprise.json, system1.json, system2.json, subsystem_a.json, component_x.json

# Analysis
Run workflow: chain-01-analyze-multi-graphs.json
  Output: Clear hierarchy detected
    - enterprise (system-of-systems level)
    - system1, system2 (system level)
    - subsystem_a (subsystem level)
    - component_x (component level)

# Strategy
Run workflow: chain-01a-determine-strategy.json
  Selected: Hierarchical

# Link
Run workflow: chain-02a-link-hierarchical.json
  Output: Parent-child containment + sibling links

# Merge & Document
Run workflow: chain-03-merge-graphs.json

# Validate
Run workflow: chain-04-validate.json
  Result: Hierarchical structure validated
```

### Example 3: Link 3 Orthogonal Domains

```bash
# Setup
Run workflow: chain-00-setup.json
  Input: biological_system.json, software_system.json, mechanical_system.json

# Analysis
Run workflow: chain-01-analyze-multi-graphs.json
  Output:
    - bio ↔ software: ORTHOGONAL
    - bio ↔ mechanical: DIVERGENT
    - software ↔ mechanical: DIVERGENT

# Strategy
Run workflow: chain-01a-determine-strategy.json
  Selected: Pairwise with creative linking

# Link (with user consent for creative linking)
Run workflow: chain-02-link-pairwise.json
  Pair 1: bio ↔ mechanical
    - Creative linking: "signal transduction" → "sensor feedback"
    - 3 exploratory touchpoints
  Pair 2: Result from Pair 1 ↔ software
    - Creative linking: "control loop" metaphor
    - 2 exploratory touchpoints

# Merge & Document
Run workflow: chain-03-merge-graphs.json
  Mark all 5 touchpoints as EXPLORATORY

# Validate
Run workflow: chain-04-validate.json
  Result: 60/100 score (all exploratory)
  Action: User must validate and refine touchpoints
```

---

## Comparison to Reflow

| Aspect | Reflow | Chain Reflow |
|--------|--------|--------------|
| **Input** | Requirements/specs | System graphs (JSON) |
| **Output** | system_of_systems_graph.json | Integrated system_of_systems_graph.json |
| **Approach** | Top-down OR bottom-up | Multi-graph linking |
| **Focus** | Design single system | Link multiple existing systems |
| **Workflows** | 00-setup → 01-design → 02-doc → 03-impl → 04-deploy | 00-setup → 01-analyze → 01a-strategy → 02-link → 03-merge → 04-validate |
| **Novelty** | Architecture from scratch | Creative linking for orthogonal systems |

**Chain Reflow complements reflow**: Use reflow to design each system, then use chain_reflow to link them.

---

## Next Steps

1. **Implement remaining workflows** (chain-01 through chain-04)
2. **Test with sample graphs** (2, 3, 5 graphs)
3. **Integrate with reflow tooling** (system_of_systems_graph_v2.py)
4. **Add workflow runner** logic to execute workflows automatically
5. **Create CLI** for easy invocation
6. **Write user guide** with examples

---

## References

- Reflow CLAUDE.md: https://github.com/sligara7/reflow/blob/main/CLAUDE.md
- Chain Reflow existing workflow: workflows/chain-01-link-architectures.json
- Neural architecture linking: docs/neural_architecture_linking_concept.md
- System graph: specs/machine/graphs/system_of_systems_graph.json

---

**Status**: Architecture complete, ready for implementation
**Author**: Claude (AI Assistant)
**Date**: 2025-11-04
