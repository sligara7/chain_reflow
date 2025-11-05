# Chain Reflow Meta-Analysis Plan

**Created**: 2025-11-04
**Purpose**: Adapt reflow's self-sharpening meta-analysis workflow (99-meta_analysis.json) for chain_reflow
**Innovation**: Use chain_reflow's own tools during meta-analysis to discover missing systems and link with reflow's architecture

---

## Overview

Chain_reflow will perform self-analysis using reflow's meta-analysis methodology, with key enhancements:

1. **Use chain_reflow's own analysis engines** during gap detection
2. **Link chain_reflow + reflow functional architectures** using chain_reflow's linking workflows
3. **Detect missing intermediate systems** using matryoshka hierarchical analysis
4. **Apply causality analysis** to understand dependencies between chain_reflow and reflow

---

## Adaptation Strategy

### Base Workflow: reflow/99-meta_analysis.json

The reflow meta-analysis workflow has 8 steps:
- META-01: Setup
- META-02: Functional Requirements
- META-03: Functional Architecture with Context Tracking
- META-04: Analyze for Bottlenecks/Gaps
- META-05: Refine Architecture
- **META-05B: Fix Implementation** (self-sharpening)
- META-06: Visualizations (optional)
- META-07: Documentation
- META-08: Operational Testing (optional)

### Chain_reflow Enhancements

#### Enhancement 1: Use Chain_reflow's Analysis Tools in META-04

**Standard META-04**: Run `analyze_functional_architecture.py` to detect:
- Context bottlenecks
- Orphaned functions
- Unreachable functions
- Circular dependencies

**Chain_reflow META-04+**: Additionally run chain_reflow's specialized tools:

**A. Matryoshka Hierarchical Analysis** (`src/matryoshka_analysis.py`)
```python
# After standard gap analysis, run:
python3 src/matryoshka_analysis.py --analyze specs/functional/functional_architecture.json

# Detects:
# - Missing hierarchy levels (component → subsystem → system → system-of-systems)
# - Cross-level linking issues (e.g., component directly linked to system-of-systems)
# - Parent-child vs peer relationships
```

**Example Output**:
```json
{
  "hierarchy_analysis": {
    "detected_levels": {
      "component": ["workflow_runner.py", "creative_linking.py"],
      "system": ["chain_reflow_system"],
      "missing_levels": ["subsystem"]
    },
    "hierarchy_gaps": [
      {
        "gap_id": "HGAP-001",
        "type": "missing_intermediate",
        "description": "Component 'workflow_runner.py' links directly to system 'chain_reflow_system'",
        "missing_level": "subsystem",
        "recommendation": "Create subsystem grouping for workflow execution components"
      }
    ]
  }
}
```

**B. Causality Analysis** (`src/causality_analysis.py`)
```python
# Analyze dependencies between chain_reflow and reflow
python3 src/causality_analysis.py \
  --system-a specs/functional/functional_architecture.json \
  --system-b /home/ajs7/project/reflow/specs/functional/functional_architecture.json \
  --analyze-correlation

# Detects:
# - Correlation vs causation in dependencies
# - A→B: Chain_reflow depends on reflow
# - B→A: Reflow depends on chain_reflow (shouldn't exist!)
# - Spurious correlations
```

**Example Output**:
```json
{
  "causality_analysis": {
    "relationship_type": "A→B",
    "confidence": 0.95,
    "evidence": [
      "Chain_reflow imports reflow workflows",
      "Chain_reflow uses reflow tools (system_of_systems_graph_v2.py)",
      "Chain_reflow extends reflow's framework methodology"
    ],
    "validation_experiments": [
      "Block reflow access → chain_reflow fails (confirms causation)",
      "Remove chain_reflow → reflow continues (confirms one-way dependency)"
    ]
  }
}
```

**C. Creative Linking** (`src/creative_linking.py`)
```python
# Assess orthogonality between chain_reflow and reflow
python3 src/creative_linking.py \
  --assess-orthogonality \
  --system-a specs/functional/functional_architecture.json \
  --system-b /home/ajs7/project/reflow/specs/functional/functional_architecture.json

# Determines:
# - ALIGNED: Both use functional flow methodology
# - RELATED: Chain_reflow extends reflow
# - DIVERGENT: Would indicate architectural mismatch
# - ORTHOGONAL: Would indicate serious design issue
```

**Expected Result**: ALIGNED or RELATED (both use functional flow, chain_reflow extends reflow)

#### Enhancement 2: Link Chain_reflow + Reflow Architectures

**New Step: META-04C - Link Functional Architectures**

After running gap analysis, use chain_reflow's linking workflow to integrate:

```bash
# Step 1: Create input graph list
cat > /tmp/graph_list.json <<EOF
{
  "graphs": [
    {
      "graph_id": "chain_reflow_functional",
      "path": "/home/ajs7/project/chain_reflow/specs/functional/functional_architecture.json",
      "system_name": "Chain Reflow",
      "framework_id": "functional_flow"
    },
    {
      "graph_id": "reflow_functional",
      "path": "/home/ajs7/project/reflow/specs/functional/functional_architecture.json",
      "system_name": "Reflow",
      "framework_id": "functional_flow"
    }
  ]
}
EOF

# Step 2: Run chain_reflow's linking workflow
python3 src/workflow_runner.py workflows/chain-01-link-architectures.json \
  --input-graphs /tmp/graph_list.json

# Outputs:
# - output/integrated_functional_architecture.json
# - docs/touchpoint_catalog_{timestamp}.md (chain_reflow → reflow touchpoints)
# - context/linking_analysis.json (relationship type: extension/dependency)
```

**What This Reveals**:
- **Touchpoints**: Where chain_reflow calls reflow tools
- **Dependencies**: Which reflow functions chain_reflow requires
- **Hierarchy**: Chain_reflow is a "subsystem" or "extension" of reflow ecosystem
- **Gaps**: Missing interfaces or undocumented dependencies

#### Enhancement 3: Detect Missing Systems with Matryoshka

**Problem**: BU-03 (Integration Gap Analysis) found 15 gaps in chain_reflow. Some gaps may be **missing intermediate systems**, not missing code.

**Example from "Carburetor-to-Body Problem" (README.md)**:
- User thinks: "Need to link Carburetor to Body"
- Reality: Missing the **Engine System** that contains Carburetor
- Solution: Document missing Engine System, don't link Carburetor directly to Body

**Apply to Chain_reflow**:
```python
# Run matryoshka analysis on chain_reflow gaps
python3 src/matryoshka_analysis.py \
  --analyze-gaps specs/machine/integration_gaps.json \
  --component-inventory specs/machine/component_inventory.json

# For each gap, determine:
# 1. Is this a missing component? (write code to fill gap)
# 2. Is this a missing intermediate system? (document the missing system)
# 3. Is this a hierarchy level mismatch? (reclassify components)
```

**Example Analysis**:
```json
{
  "gap_reclassification": {
    "GAP-008": {
      "original": "Missing workflow validation in workflow_runner.py",
      "analysis": "Component-level gap - requires code implementation",
      "action": "Implement validation logic in workflow_runner.py"
    },
    "GAP-010": {
      "original": "No integration between creative_linking and causality_analysis",
      "analysis": "Missing subsystem - 'Combined Analysis Engine'",
      "hierarchy_issue": "These are peer components, need parent subsystem to coordinate",
      "action": "Create AnalysisOrchestrator subsystem that coordinates both engines",
      "missing_level": "subsystem"
    },
    "GAP-013": {
      "original": "No user consent mechanism for creative linking",
      "analysis": "Component-level gap - requires code implementation",
      "action": "Add consent checks in interactive_executor.py"
    }
  }
}
```

**Key Insight**: Some "gaps" are actually **missing architectural levels**, not missing code!

---

## Workflows to Create

### 1. 99-chain_meta_analysis.json (Comprehensive Meta-Analysis)

**Purpose**: Full self-analysis of chain_reflow, run quarterly or before major releases

**Based on**: reflow/99-meta_analysis.json

**When to use**:
- Quarterly health checks
- Before major version releases
- After multiple feature updates
- When architectural review needed

### 2. 98-chain_feature_update.json (Auto-Sharpening Feature Updates)

**Purpose**: Feature update workflow that AUTO-TRIGGERS meta-analysis

**Based on**: reflow/98-reflow_feature_update.json

**When to use**:
- Every time you add/update a chain_reflow feature
- Updating workflows/*.json
- Updating tools/*.py (src/)
- Adding new analysis engines

**Key Innovation**: Automatically runs meta-analysis after every feature to catch issues immediately

**Workflow Structure**:
```
CFU-01: Setup Feature Update
  ↓
CFU-02: Execute Standard Feature Update (FU-01 through FU-05)
  ↓
CFU-03: AUTO-TRIGGER Analysis (META-04 + CHAIN-META-04A/B/C/D)
  ↓
CFU-04: AUTO-TRIGGER Refinement (META-05 + META-05B if issues found)
  ↓
CFU-05: AUTO-TRIGGER Self-Sharpening (optimization pass)
  ↓
CFU-06: Commit & Document (feature + fixes)
```

**Benefit**: Prevents technical debt accumulation - every feature is immediately validated

---

## Workflow: 99-chain_meta_analysis.json

### Adapted Steps

All steps from reflow's 99-meta_analysis.json, plus:

**CHAIN-META-04A: Apply Matryoshka Analysis**
- Run matryoshka hierarchical analysis on functional architecture
- Detect missing intermediate systems/subsystems
- Reclassify components by hierarchy level
- Output: `specs/functional/hierarchy_analysis.json`

**CHAIN-META-04B: Apply Causality Analysis**
- Analyze chain_reflow → reflow dependency relationship
- Validate causation (not just correlation)
- Document dependency touchpoints
- Output: `specs/functional/causality_analysis.json`

**CHAIN-META-04C: Link with Reflow Functional Architecture**
- Use chain-01-link-architectures.json to link chain_reflow + reflow
- Discover touchpoints and integration patterns
- Generate integrated functional architecture
- Output: `output/integrated_functional_architecture.json`

**CHAIN-META-04D: Reclassify Gaps**
- Review integration_gaps.json (15 gaps from BU-03)
- For each gap, determine:
  - Component gap (missing code) → Add to deltas
  - System gap (missing intermediate) → Document missing system
  - Hierarchy mismatch → Reclassify components
- Output: `specs/functional/reclassified_gaps.json`

**CHAIN-META-05B: Fix Implementation** (Self-Sharpening)
- Fix workflows/*.json based on analysis
- Fix tools/*.py to address bottlenecks
- **NEW**: Implement missing subsystems identified by matryoshka analysis
- **NEW**: Add integration points discovered by linking analysis
- Validate all changes

---

## Expected Outputs

### 1. Functional Architecture Documents
- `specs/functional/functional_requirements.json` - What chain_reflow must do
- `specs/functional/functional_architecture.json` - How chain_reflow works
- `specs/functional/functional_architecture_analysis.json` - Gaps and bottlenecks

### 2. Chain_reflow-Specific Analyses
- `specs/functional/hierarchy_analysis.json` - Matryoshka results
- `specs/functional/causality_analysis.json` - Chain_reflow → reflow dependencies
- `specs/functional/reclassified_gaps.json` - Gap categorization (code vs system vs hierarchy)

### 3. Integrated Architecture
- `output/integrated_functional_architecture.json` - Chain_reflow + reflow linked
- `docs/touchpoint_catalog_{timestamp}.md` - All touchpoints documented
- `docs/integration_report_{timestamp}.md` - Full integration analysis

### 4. Implementation Fixes
- Updated `workflows/*.json` - Context refresh points, missing steps
- Updated `src/*.py` - Bottleneck fixes, missing subsystems
- New subsystems (if matryoshka analysis identifies missing levels)

### 5. Documentation
- `docs/CHAIN_META_ANALYSIS_REPORT_{date}.md` - Full report
- `docs/HIERARCHY_ANALYSIS_SUMMARY.md` - Matryoshka findings
- `docs/CHAIN_REFLOW_POSITION_IN_ECOSYSTEM.md` - Relationship to reflow

---

## Benefits of This Approach

### 1. Self-Improvement
Like reflow, chain_reflow will "sharpen itself" by:
- Detecting its own gaps and bottlenecks
- Fixing implementation issues proactively
- Continuously improving architecture quality

### 2. Dogfooding
Chain_reflow uses **its own tools** during meta-analysis:
- Matryoshka analysis detects missing hierarchy levels
- Causality analysis validates dependencies
- Creative linking assesses orthogonality
- Proves that chain_reflow's tools work on real systems (itself!)

### 3. Ecosystem Integration
By linking chain_reflow + reflow functional architectures:
- Understand exact relationship (extension, dependency)
- Document all touchpoints (tool calls, workflow reuse)
- Validate architectural coherence
- Detect accidental coupling or missing abstractions

### 4. Gap Reclassification
Not all gaps are missing code:
- Some are missing **intermediate systems** (matryoshka reveals)
- Some are **hierarchy mismatches** (components at wrong level)
- Some are **architectural issues** (not implementation issues)
- Proper classification prevents wasted implementation effort

---

## Execution Plan

### Phase 1: Setup (1 hour)
1. Create `workflows/99-chain_meta_analysis.json` (adapt from reflow)
2. Update `context/working_memory.json` for meta-analysis mode
3. Create `specs/functional/` directories

### Phase 2: Requirements & Architecture (3-4 hours)
4. Define functional requirements (META-02)
5. Create functional architecture with context tracking (META-03)

### Phase 3: Analysis with Chain_reflow Tools (2-3 hours)
6. Run standard functional architecture analysis (META-04)
7. Run matryoshka hierarchical analysis (CHAIN-META-04A)
8. Run causality analysis on chain_reflow → reflow (CHAIN-META-04B)
9. Link chain_reflow + reflow architectures (CHAIN-META-04C)
10. Reclassify integration gaps (CHAIN-META-04D)

### Phase 4: Refinement (2-4 hours)
11. Refine functional architecture (META-05)
12. Fix implementation (META-05B)
13. Implement missing subsystems if matryoshka identified any
14. Re-run analyses to validate fixes

### Phase 5: Documentation (1-2 hours)
15. Generate visualizations (META-06)
16. Write meta-analysis report (META-07)
17. Update CLAUDE.md and README.md with findings

**Total Estimated Time**: 9-14 hours

---

## Success Criteria

1. ✅ Functional architecture created with context tracking
2. ✅ All context paths < 160k tokens (Claude Sonnet limit)
3. ✅ No critical gaps or unreachable functions
4. ✅ **Matryoshka analysis identifies hierarchy structure**
5. ✅ **Causality analysis validates chain_reflow → reflow dependency**
6. ✅ **Integrated architecture links chain_reflow + reflow**
7. ✅ **Gaps reclassified (code vs system vs hierarchy)**
8. ✅ Implementation fixes applied and validated
9. ✅ Meta-analysis report documents findings and improvements
10. ✅ Chain_reflow has successfully "sharpened itself"

---

## Implementation Priority

### High Priority (Do First)

1. **Create 98-chain_feature_update.json**
   - Most immediately useful
   - Validates every feature update automatically
   - Prevents technical debt accumulation
   - Use for ALL future chain_reflow development

2. **Run initial meta-analysis** (using adapted 99-chain_meta_analysis.json)
   - Establish baseline functional architecture
   - Identify current gaps and issues
   - Validate existing implementation
   - Document chain_reflow's position in ecosystem

### Medium Priority (Do After Initial Meta-Analysis)

3. **Reclassify the 15 integration gaps** from BU-03
   - Use matryoshka analysis to categorize gaps
   - Determine which are missing code vs missing systems
   - Update implementation roadmap accordingly

4. **Link chain_reflow + reflow architectures**
   - Document all touchpoints
   - Validate dependency relationship (should be A→B only)
   - Generate integrated architecture view

### Low Priority (Ongoing)

5. **Use 98-chain_feature_update.json for all future features**
   - Every new analysis engine → run meta-analysis
   - Every new workflow → validate integration
   - Every tool enhancement → check context consumption

6. **Run 99-chain_meta_analysis.json quarterly**
   - Comprehensive health check
   - Compare with previous analyses
   - Track architectural evolution

---

## Next Steps

1. **Immediate**: Create 98-chain_feature_update.json (adapt from reflow's 98-reflow_feature_update.json)
2. **Next**: Create 99-chain_meta_analysis.json (adapt from reflow's 99-meta_analysis.json)
3. **Then**: Run META-01/02/03 to establish baseline functional architecture
4. **Then**: Run CHAIN-META-04A/B/C/D to apply chain_reflow's specialized tools
5. **Then**: Run META-05B to fix any critical issues found
6. **Finally**: Document findings and update CLAUDE.md/README.md

---

**Status**: Planning complete, ready for execution
**Owner**: Chain_reflow development team
**Dependencies**: Reflow v3.12.0 functional architecture analysis tools
