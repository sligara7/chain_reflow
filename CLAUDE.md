# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Chain Reflow extends the reflow systems engineering workflows (https://github.com/sligara7/reflow) by linking multiple system-of-systems architectures together. It integrates system_of_systems_graph.json files produced by reflow to enable:

- **Functional architecture chaining** (PRIMARY USE CASE) - Link multiple functional flow architectures from different teams/repos
- Independent development of system components with intelligent linking
- Hierarchical composition analysis (Matryoshka nesting)
- Framework-aware linking strategies (UAF-to-UAF, functional-to-functional, etc.)
- Correlation vs. causation analysis to distinguish observed patterns from proven relationships
- Multi-level validation and integration

**CRITICAL**: Chain_reflow builds on top of reflow. Reflow creates individual architectures → Chain_reflow links them together.

## Prerequisites and Dependencies

### Python Requirements
- **Python 3.8+** (tested with Python 3.13.5)
- **No external Python dependencies** for core functionality
- Optional: `pytest` for running integration tests (`pip3 install pytest`)

### Related Repositories
- **Reflow** (parent framework): `/home/ajs7/project/reflow`
  - Chain_reflow extends reflow's workflows
  - Reflow tools can analyze chain_reflow's output
  - Used for meta-analysis validation

### File System Requirements
- Workflows expect paths relative to repository root
- Context files stored in `context/` directory
- Analysis tools read/write to `specs/`, `docs/`, `output/` directories

## Framework Compatibility

### ⚠️ CRITICAL: Framework-Aware Linking

**Chain_reflow inherits reflow's framework-based architecture**. Just as reflow supports multiple frameworks (UAF, Systems Biology, Decision Flow, Functional Flow, etc.), chain_reflow must respect framework boundaries when linking.

**PRIMARY USE CASE (v1.0)**: Link architectures of the SAME framework type
- ✅ Functional Flow → Functional Flow (chaining function compositions)
- ✅ UAF Service-Oriented → UAF Service-Oriented (linking microservice systems)
- ✅ Systems Biology → Systems Biology (linking pathway models)
- ✅ Decision Flow → Decision Flow (linking workflow systems)

**ADVANCED/FUTURE**: Cross-framework linking (different framework types)
- ⚠️ Functional Flow + UAF Service-Oriented = Very difficult
- ⚠️ Requires "overlay architecture" techniques
- ⚠️ Different semantic models (functions vs services, transformations vs interfaces)
- ⚠️ Not supported in v1.0 - future research goal

### Why Framework Compatibility Matters

Different frameworks have different semantics:
- **Functional Flow**: Nodes = functions/transformations, Edges = data flow, Composition = function chaining
- **UAF**: Nodes = services/components, Edges = interfaces/APIs, Composition = service orchestration
- **Systems Biology**: Nodes = genes/proteins, Edges = activation/inhibition, Composition = pathway integration
- **Decision Flow**: Nodes = states/decisions, Edges = transitions, Composition = workflow merging

**Linking across frameworks** means bridging fundamentally different semantic models - this requires sophisticated "overlay" techniques that align disparate architecture types.

### Framework Detection

Chain_reflow automatically detects framework type from each `system_of_systems_graph.json`:
```json
{
  "framework_configuration": {
    "framework_id": "functional_flow",
    "framework_name": "Functional Flow Framework"
  }
}
```

**Quality Gates**:
- **BLOCKING**: Warn user if attempting to link different framework types
- **INTERACTIVE**: Require explicit consent for cross-framework linking
- **EXPLORATORY**: Mark all cross-framework links as experimental

## Word Frequency DAG Framework (NEW)

**NEW**: Chain_reflow now supports **Word Frequency Directed Acyclic Graphs** for natural language analysis. This demonstrates how chain_reflow's architecture linking concepts extend beyond traditional systems engineering to linguistic analysis.

### What is Word Frequency DAG?

A **Word Frequency DAG** transforms books/text into network graphs where:
- **Nodes** = Unique words (tokens)
- **Edges** = Transitions from one word to the next
- **Edge weights** = Normalized frequency (Markov chain style)
- **Framework ID**: `word_frequency`

This creates a "linguistic fingerprint" that can be analyzed, compared, and merged using chain_reflow's tools.

### Quick Start

```bash
# 1. Build word DAG from a book
python3 src/word_frequency_dag.py book.txt --title "Book Title" --output output/book_dag.json

# 2. Build DAG for another book
python3 src/word_frequency_dag.py book2.txt --title "Book 2" --output output/book2_dag.json

# 3. Merge the two DAGs
python3 src/merge_word_dags.py output/book_dag.json output/book2_dag.json --output output/merged_dag.json
```

### Use Cases

1. **Comparative Literature**: Compare writing styles across authors/genres
2. **Plagiarism Detection**: High overlap indicates potential plagiarism
3. **Genre Classification**: Build DAGs as training data
4. **Translation Quality**: Compare original vs translated texts
5. **Finding Semantic Bridges**: Discover universal linguistic patterns in orthogonal texts

### Example: Orthogonal Books

Merging a **technical ML book** with a **poetry book** reveals:
- **Only 6.4% word overlap** (18 common words: mostly grammatical connectors like "the", "in", "of")
- **Only 5 common transitions** out of 438 total
- **Common words are function words**, not domain-specific content
- True orthogonality demonstrated quantitatively!

See detailed documentation: `docs/WORD_FREQUENCY_DAG_USAGE.md`

### Integration with Chain Reflow

Word DAGs use the standard `system_of_systems_graph.json` format with:
- `framework_id: "word_frequency"`
- Compatible with chain_reflow's matryoshka, causality, and creative linking tools
- Future: Multi-level hierarchical DAGs (word → sentence → paragraph → chapter → book)

### Test Examples

See `test_books/` directory:
- `technical_ml.txt` - Technical machine learning text
- `poetry_nature.txt` - Poetry about nature
- Perfect for demonstrating orthogonal text merging!

## Self-Sharpening Meta-Analysis

**NEW**: Chain_reflow can analyze itself using reflow's meta-analysis methodology + its own specialized tools.

### Meta-Analysis Workflows

**98-chain_feature_update.json** (Use for ALL feature updates)
- Workflow: `workflows/98-chain_feature_update.json`
- When: After every feature implementation
- How: Claude Code reads workflow and executes steps

**99-chain_meta_analysis.json** (Run quarterly or before major releases)
- Workflow: `workflows/99-chain_meta_analysis.json`
- When: Quarterly health checks, before major releases
- How: Claude Code reads workflow and executes steps

### What Meta-Analysis Does

1. **Standard Analysis** (from reflow):
   - Defines functional requirements and architecture
   - Detects context bottlenecks (>160k tokens)
   - Finds orphaned/unreachable functions
   - Identifies circular dependencies

2. **Chain_reflow Enhancements**:
   - **CHAIN-META-04A**: Matryoshka analysis → Detects missing hierarchy levels
   - **CHAIN-META-04B**: Causality analysis → Validates chain_reflow → reflow dependency
   - **CHAIN-META-04C**: Links chain_reflow + reflow functional architectures
   - **CHAIN-META-04D**: Reclassifies gaps (code vs system vs hierarchy issues)

3. **Implementation Fixes** (self-sharpening):
   - Updates workflows/*.json to fix bottlenecks
   - Updates src/*.py to optimize tools
   - Creates missing subsystems if identified by matryoshka analysis

### Dogfooding: Using Chain_reflow's Tools on Itself

Meta-analysis uses chain_reflow's own specialized tools:
- `src/matryoshka_analysis.py` detects missing hierarchy levels in chain_reflow
- `src/causality_analysis.py` validates dependencies between chain_reflow and reflow
- `workflows/chain-01-link-architectures.json` links chain_reflow + reflow architectures

This proves the tools work on real systems (including itself!).

### Documentation

See detailed plans:
- `docs/CHAIN_META_ANALYSIS_PLAN.md` - Full technical plan
- `docs/META_ANALYSIS_SUMMARY.md` - Executive summary

## Core Commands

### Workflow Execution Model

**Chain_reflow follows reflow's LLM-assisted execution philosophy:**

🤖 **Claude Code (or similar AI agent) IS the workflow executor**
- Workflows are JSON specifications, not executable scripts
- AI reads workflow steps and executes them intelligently
- AI invokes tools directly: `python3 {paths.tools_path}/[tool].py`
- Human-in-the-loop for critical decisions (framework selection, creative linking)

**How to Execute a Workflow:**
1. Tell Claude Code: "Execute workflow `workflows/99-chain_meta_analysis.json`"
2. Claude Code reads the workflow JSON
3. Claude Code executes each step's actions
4. Claude Code updates `context/working_memory.json` to track progress

**There is NO automated workflow runner** - this is intentional! AI agents provide:
- Intelligent error handling and recovery
- Context-aware decision making
- Ability to skip/modify steps based on project state
- Human consultation when needed

### Analysis Tools (CLI)

```bash
# Matryoshka hierarchical analysis
python3 src/matryoshka_analysis.py system_of_systems_graph.json

# Causality analysis (correlation vs causation)
python3 src/causality_analysis.py graph1.json graph2.json

# Creative linking for orthogonal architectures
python3 src/creative_linking.py graph1.json graph2.json

# Matrix-based gap detection (NEW: detect missing intermediate systems)
python3 src/matrix_gap_detection.py system_a.json system_c.json

# Word frequency DAG builder (NEW: natural language analysis)
python3 src/word_frequency_dag.py book.txt --title "Book Title" --output output/book_dag.json

# Merge word frequency DAGs (NEW: compare and merge books)
python3 src/merge_word_dags.py dag1.json dag2.json --output output/merged_dag.json

# All tools support --help, --output, --format flags
python3 src/matryoshka_analysis.py --help
python3 src/matrix_gap_detection.py --help
```

### Development Commands

```bash
# Check Python version (requires 3.8+, tested with 3.13.5)
python3 --version

# View working memory state
cat context/working_memory.json

# View workflow progress
cat context/step_progress_tracker.json

# View current focus
cat context/current_focus.md

# Run integration tests (requires pytest)
pip3 install pytest  # Install pytest if needed
pytest tests/test_integration_end_to_end.py -v

# Run specific test class
pytest tests/test_integration_end_to_end.py::TestMatryoshkaAnalysis -v
pytest tests/test_integration_end_to_end.py::TestCausalityAnalysis -v
pytest tests/test_integration_end_to_end.py::TestCreativeLinking -v

# Validate Python syntax (useful before commits)
python3 -m py_compile src/*.py
```

## Architecture

### Workflow-Driven Design

Chain Reflow follows the reflow methodology with a 5-phase workflow architecture:

1. **Phase 0: Setup** (`chain-00-setup.json`) - Initialize system, discover graphs, validate environment
2. **Phase 1: Analysis** (`chain-01-analyze-multi-graphs.json`, `chain-01a-determine-strategy.json`) - Analyze all graphs, assess orthogonality, infer hierarchy, determine linking strategy
3. **Phase 2: Linking** (`chain-02-execute-linking-strategy.json`) - Execute linking based on strategy (router + executor: pairwise, hierarchical, or network)
4. **Phase 3: Integration** (`chain-03-merge-graphs.json`) - Merge partial results into final integrated graph
5. **Phase 4: Validation** (`chain-04-validate.json`) - Validate using reflow analysis tools

### Key Modules

**`src/creative_linking.py`** - Creative linking for orthogonal architectures
- Implements synesthetic mappings (cross-domain metaphors)
- Assesses orthogonality levels: ALIGNED, RELATED, DIVERGENT, ORTHOGONAL
- Generates exploratory touchpoints with confidence scores
- Domain metaphors for biological ↔ software, mechanical ↔ software, etc.

**`src/matryoshka_analysis.py`** - Hierarchical nesting analysis
- Infers hierarchy levels: component → subsystem → system → system-of-systems → enterprise
- Detects missing intermediate levels (hierarchical gaps)
- Prevents incorrect cross-level linking (e.g., component directly to system-of-systems)

**`src/causality_analysis.py`** - Correlation vs. causation analysis
- Distinguishes observed correlations from causal relationships
- Generates competing hypotheses (A→B, B→A, A↔B, spurious)
- Designs validation experiments

**`src/matrix_gap_detection.py`** - Matrix-based missing system detection
- Mathematically infers missing intermediate systems using linear algebra
- Homography matrix analogy: B = C * A^(-1) solves for transformation matrix
- SVD decomposition detects multi-layer subsystems (neural network analogy)
- Generates hypotheses based on matrix properties (rank, sparsity, eigenvalues)
- Example: Yellowstone wolf system decomposes into B1 (predation) + B2 (landscape of fear) + B3 (cascading effects)
- Workflow: `workflows/chain-05-detect-missing-systems.json`
- **Status**: Integrated into system_of_systems_graph.json v1.1.0 (2025-11-06)
- **Context consumption**: 20k tokens (F-080: Load Systems for Gap Detection)
- **Dogfooding**: Successfully used on chain_reflow itself to detect missing Phase 2 workflows

**`src/interactive_executor.py`** - Interactive workflow execution
- Human-in-the-loop decision points
- User consent for creative linking
- Strategy selection and validation

### Working Memory Pattern

All workflows read/write `context/working_memory.json` which contains:
- Current workflow ID and step ID
- Session state and paths
- Framework configuration
- Operations counter for refresh tracking

This enables:
- Resume capability if workflow interrupted
- Full audit trail of execution
- State inspection for debugging

### Directory Structure

```
chain_reflow/
├── src/                    # Python modules (workflow runner, analysis engines)
├── workflows/              # Workflow JSON files (chain-00-setup.json, etc.)
├── context/                # Working memory and session state
├── docs/                   # Generated documentation and reports
├── specs/                  # Interface specifications and graph schemas
│   ├── functional/         # Functional architecture specs (for meta-analysis)
│   └── machine/            # Machine-readable specs and graphs
├── examples/               # Example code (e.g., carburetor_body_example.py)
├── test_architectures/     # UAF test suite (auth, API gateway, user mgmt)
├── test_ecosystems/        # Ecological examples (Yellowstone wolf reintroduction)
│   ├── with_wolves/        # System state with wolves present
│   ├── without_wolves/     # System state without wolves (degraded)
│   └── demo_matrix_gap/    # Matrix gap detection demo data
├── tests/                  # Integration tests (pytest)
└── output/                 # Generated output files (integrated graphs, reports)
```

### Test Ecosystems

Chain_reflow includes comprehensive test data in `test_ecosystems/`:

**Yellowstone Wolf Reintroduction** - Real-world ecological case study:
- `with_wolves/`: Ecosystem after wolf reintroduction (balanced state)
  - Wolf predation controls deer population
  - Vegetation recovers, beaver populations increase
  - River morphology changes (trophic cascade)
- `without_wolves/`: Ecosystem without wolves (degraded state)
  - Deer overpopulation, vegetation decline
  - Beaver disappearance, river channel changes
- **Purpose**: Demonstrates matrix gap detection finding missing intermediate system (wolves)

**Matrix Gap Detection Demo** - Synthetic examples:
- `system_a_degraded.json`: Initial degraded state
- `system_c_balanced.json`: Final balanced state
- **Purpose**: Mathematical validation of B = C × A^(-1) gap detection

**UAF Service Architecture** - Software system examples:
- Authentication service, API gateway, user management
- **Purpose**: Test matryoshka/causality/creative_linking on software architectures

These test ecosystems are actively used in integration tests and meta-analysis validation.

## Key Concepts

### Hierarchical Levels (Matryoshka)

When linking architectures, never assume they're at the same hierarchical level. The system recognizes five levels:

1. **Component** - Individual parts (axle, API endpoint)
2. **Subsystem** - Groups of components (suspension, auth module)
3. **System** - Complete functional systems (vehicle chassis, microservice)
4. **System-of-Systems** - Multiple integrated systems (vehicle, cloud platform)
5. **Enterprise** - Organization-level (product portfolio, fleet)

**Critical**: Missing intermediate levels often appear as "gaps". Don't link across levels—identify and document the missing intermediates (see README.md "Carburetor-to-Body Problem").

### Orthogonality Assessment

Architectures are classified by how related they are **within the same framework**:

- **ALIGNED**: Same domain, clear technical connections (e.g., two microservice systems in UAF)
- **RELATED**: Different domains, some overlap (e.g., user management + payment processing in UAF)
- **DIVERGENT**: Different domains, minimal overlap (e.g., frontend + backend functional flows)
- **ORTHOGONAL**: Completely different domains (e.g., authentication system + data analytics in UAF)

**Framework mismatch overrides all other classifications**:
- Two architectures with different frameworks are automatically at least DIVERGENT
- Example: Functional Flow + UAF = DIVERGENT (minimum), possibly ORTHOGONAL

Use standard technical linking for ALIGNED/RELATED. Use creative linking (with user consent) for DIVERGENT/ORTHOGONAL.

### Creative Linking

Only use creative linking when:
- Architectures are DIVERGENT or ORTHOGONAL
- User explicitly consents
- Links are marked as EXPLORATORY
- Validation is required

Creative links use synesthetic mappings (cross-domain metaphors) like:
- Biological signal transduction ↔ Software event propagation
- Mechanical force transmission ↔ Software data flow

**Always mark creative links with low confidence scores and exploratory flags.**

### Correlation vs. Causation

When architectures seem related, distinguish:
- **Correlation**: Systems appear related (observed pattern)
- **Causation**: One system actually affects the other (proven mechanism)
- **Spurious**: Coincidental relationship (no real link)

Generate competing hypotheses and design validation experiments before linking.

## Workflow Execution Patterns

### Sequential Execution

Most workflows execute sequentially:
```
chain-00-setup → chain-01-analyze-multi-graphs → chain-01a-determine-strategy →
chain-02-execute-linking-strategy → chain-03-merge-graphs → chain-04-validate
```

### Branching by Strategy

**Phase 2 uses a router + executor pattern** (discovered via matrix gap detection dogfooding):
- **Single workflow**: `chain-02-execute-linking-strategy.json`
- **Layer 1 (Router)**: Reads strategy from Phase 1a, branches to appropriate executor
- **Layer 2 (Executor)**: Executes linking based on strategy:
  - **Pairwise**: 2-3 graphs, mixed relationships (all-to-all pairing)
  - **Hierarchical**: Clear parent-child relationships (tree traversal)
  - **Network**: All graphs at same level (mesh/hub-spoke topology)

**Key Insight**: Matrix gap detection revealed Phase 2 should be a simple rank-2 system (router + executor), not 3 complex workflows.

### Reusing Workflows

The `chain-01-link-architectures.json` workflow is reused as inner loop logic in pairwise, hierarchical, and network linking strategies. Don't duplicate—delegate to existing workflow.

## Important Principles

### Quality Gates

Each workflow has quality gates:
- **Blocking**: Must pass to continue (e.g., minimum 2 valid graphs)
- **Warning**: Issues flagged but workflow continues
- **Interactive**: User decision required (e.g., creative linking consent)

### Human-in-the-Loop

Following reflow v3.8.0 pattern:
- User consent required for creative linking
- User validation of exploratory touchpoints
- User strategy selection when alternatives exist

### Scalability

Approach varies by number of graphs:
- **Small N (2-3)**: All-to-all linking, sequential execution
- **Medium N (4-10)**: Selective linking, hub-spoke topology, phased execution
- **Large N (>10)**: Clustering, hierarchical decomposition

## Integration with Reflow

Chain Reflow extends the reflow workflows (v3.12.0) from /home/ajs7/project/reflow:

**Workflow Progression**:
1. **Reflow Phase**: Teams independently design architectures using reflow workflows
   - Team A: Runs reflow `01c-top_down_design.json` → produces `system_a_graph.json` (Functional Flow)
   - Team B: Runs reflow `01b-bottom_up_integration.json` → produces `system_b_graph.json` (Functional Flow)
   - Team C: Runs reflow `01c-top_down_design.json` → produces `system_c_graph.json` (UAF Service-Oriented)

2. **Chain_reflow Phase**: Link architectures together
   - Discovers touchpoints between Team A and Team B (same framework: Functional Flow)
   - **Warns** about linking Team C (different framework: UAF) with Team A/B
   - Generates integrated graph with framework-aware linking strategies

3. **Reflow Analysis Phase**: Validate integrated graph
   - Run reflow's `system_of_systems_graph_v2.py` on integrated graph
   - Identifies gaps, orphans, inconsistencies at system-of-systems level

**Key Files**:
- Input: Multiple `system_of_systems_graph.json` files (from different reflow projects)
- Output: `output/integrated_system_of_systems_graph.json` (compatible with reflow tools)

**Framework Compatibility**:
- Final integrated graph must have a single coherent framework_id
- When linking same-framework graphs: Preserve framework metadata
- When attempting cross-framework: Generate overlay architecture (future feature)

## File Format Notes

### Workflow JSON Structure

Workflows follow reflow's structure:
```json
{
  "workflow_metadata": {
    "workflow_id": "chain-XX",
    "name": "...",
    "version": "1.0.0",
    "description": "..."
  },
  "entry_points": { "new_system": { "first_step": "..." } },
  "workflow_steps": [ { "step_id": "...", "actions": [...] } ]
}
```

### Graph JSON Structure

System graphs follow the system_of_systems_graph.json schema from reflow with nodes, edges, and metadata.

## Common Pitfalls

1. **Don't link different framework types without explicit consent**: Always check framework_id first
2. **Don't assume peer relationships**: Check hierarchy levels before linking
3. **Don't use creative linking by default**: Only for orthogonal domains with consent
4. **Don't skip validation**: All exploratory links require validation
5. **Don't link directly across hierarchy levels**: Identify missing intermediates
6. **Don't confuse correlation with causation**: Generate and test hypotheses
7. **Don't default to UAF thinking**: Reflow supports 6+ frameworks; chain_reflow must respect framework semantics
8. **Don't assume all gaps are missing code**: Use matryoshka analysis to categorize gaps (code vs system vs hierarchy)
9. **Don't skip meta-analysis after features**: Use 98-chain_feature_update.json for ALL feature development

## Output Files

Primary output: `output/integrated_system_of_systems_graph.json` - Final linked system graph

Supporting outputs:
- `context/working_memory.json` - Session state
- `context/framework_compatibility_matrix.json` - Framework compatibility analysis
- `context/multi_graph_analysis.json` - Analysis results
- `docs/integration_report_{timestamp}.md` - Full documentation
- `docs/touchpoint_catalog_{timestamp}.md` - All touchpoints
- `docs/framework_mismatch_warnings_{timestamp}.md` - Cross-framework linking warnings
- `output/validation_report_{timestamp}.md` - Validation results

## Future Features

### Overlay Architectures (Not Yet Implemented)

**Goal**: Enable linking of different framework types by creating "overlay" mappings

**Challenge**: Different frameworks have fundamentally different semantic models:
- Functional Flow thinks in terms of function composition and data transformations
- UAF Service-Oriented thinks in terms of service interfaces and API contracts
- Systems Biology thinks in terms of molecular interactions and pathways

**Proposed Approach** (future research):
1. Define semantic bridge patterns between framework pairs
2. Create bidirectional translation layers
3. Preserve both framework semantics in overlay graph
4. Enable queries/analysis from either framework's perspective

**Example**: Functional Flow + UAF Service-Oriented
- Functional Flow function → UAF service endpoint (one-to-many mapping)
- Function input/output → Service request/response schema
- Function composition → Service orchestration pattern

**Status**: Research phase - not implemented in v1.0

### Supported Framework Pairs (Future)

Priority order for overlay architecture support:
1. **Functional Flow + Decision Flow**: Similar compositional semantics (HIGH priority)
2. **UAF + Systems Biology**: Both have interface/interaction semantics (MEDIUM)
3. **Decision Flow + UAF**: State transitions + service calls (MEDIUM)
4. **Others**: Lower priority or may not be feasible

**Recommendation**: For v1.0, focus on linking architectures of the SAME framework type.
