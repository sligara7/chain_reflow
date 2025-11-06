# Framework Adapters Guide
**Chain Reflow v1.3.0+**

This guide explains how Chain Reflow handles multiple architecture framework types and provides examples for working with different schemas.

---

## Overview

Chain Reflow's analysis engines (matrix_gap_detection, causality_analysis, matryoshka_analysis, creative_linking) now support automatic format detection, allowing them to work seamlessly with architectures from different frameworks and tools.

### Supported Formats

1. **Ecosystem Format** (original Chain Reflow format)
2. **System of Systems Graph Format** (Reflow compatible)
3. **Direct/Simple Format** (minimal schema)

---

## Framework Types

### 1. Decision Flow Framework

**Used By**: Chain Reflow system architecture
**Component Term**: component
**Connection Term**: interface

**Schema**:
```json
{
  "system_of_systems_graph": {
    "metadata": {
      "system_name": "...",
      "framework": "decision_flow"
    },
    "nodes": [
      {
        "node_id": "component_id",
        "node_name": "Component Name",
        "node_type": "component",
        "tier": "orchestration|infrastructure|analysis",
        "capabilities": ["C01", "C02"],
        "interfaces_provided": ["IInterface"],
        "interfaces_required": ["IOtherInterface"],
        "status": "production_ready|planned"
      }
    ],
    "edges": [
      {
        "edge_id": "E01",
        "source": "component_a",
        "target": "component_b",
        "edge_type": "invocation|data_flow|configuration",
        "weight": 1.0,
        "status": "current|future"
      }
    ]
  }
}
```

**Characteristics**:
- Models systems as decision-making components
- Emphasizes component types and tiers
- Interface-based connections
- Status tracking (production vs planned)

---

### 2. Functional Flow Framework

**Used By**: Reflow functional architecture, Chain Reflow functional specs
**Component Term**: function
**Connection Term**: function_call_or_data_flow

**Schema**:
```json
{
  "framework_id": "functional_flow",
  "flows": [
    {
      "flow_id": "FLOW-001",
      "flow_name": "...",
      "functions": ["F-001", "F-002"]
    }
  ],
  "functions": [
    {
      "function_id": "F-001",
      "function_name": "...",
      "inputs": [...],
      "outputs": [...],
      "context_tokens": 5000
    }
  ]
}
```

**Characteristics**:
- Models systems as data/control flows
- Emphasizes function decomposition
- Context-aware (tracks token consumption)
- Flow-centric organization

---

### 3. UAF 1.2 (Unified Architecture Framework)

**Used By**: Reflow service architectures
**Component Term**: service
**Connection Term**: interface

**Schema**:
```json
{
  "service_id": "service_name",
  "service_name": "...",
  "version": "1.0.0",
  "framework": "uaf",
  "functions": [
    {
      "function_id": "F-001",
      "function_name": "..."
    }
  ],
  "interfaces": {
    "provided": [...],
    "required": [...]
  },
  "dependencies": ["other_service"]
}
```

**Characteristics**:
- Service-oriented architecture
- Interface contracts (provided/required)
- Dependency management
- Version tracking

---

### 4. Ecosystem Format (Chain Reflow Original)

**Used By**: Chain Reflow test examples (wolf/deer ecosystem)
**Component Term**: population/system
**Connection Term**: interaction

**Schema**:
```json
{
  "metadata": {
    "system_name": "...",
    "framework": "systems_biology"
  },
  "graph": {
    "nodes": [
      {
        "id": "node_id",
        "name": "...",
        "type": "population",
        "status": "STRESSED|BALANCED|OVERPOPULATED"
      }
    ],
    "links": [
      {
        "source": "node_a",
        "target": "node_b",
        "type": "inhibition|activation",
        "strength": 0.9
      }
    ]
  }
}
```

**Characteristics**:
- Biological/ecological system modeling
- Interaction types (inhibition, activation, predation)
- Population dynamics
- System health status

---

## Format Auto-Detection

All Chain Reflow analysis engines automatically detect format:

### Detection Algorithm

```python
def detect_format(data: dict) -> str:
    """Detect architecture format"""
    if 'system_of_systems_graph' in data:
        return "system_of_systems_graph"  # Format 2 (Reflow)
    elif 'graph' in data and isinstance(data['graph'], dict):
        return "ecosystem"  # Format 1 (Chain Reflow original)
    elif 'nodes' in data:
        return "direct"  # Format 3 (Simple)
    else:
        return "unknown"
```

### Field Normalization

Chain Reflow automatically normalizes field names:

| Ecosystem | System of Systems | Normalized |
|-----------|-------------------|------------|
| `id` | `node_id` | `id` |
| `name` | `node_name` | `name` |
| `links` | `edges` | `edges` |
| `strength` | `weight` | `weight` |

---

## Usage Examples

### Example 1: Analyzing Reflow System Graph

```bash
python3 src/matrix_gap_detection.py \
  /path/to/reflow/system_of_systems_graph.json \
  /path/to/other/system_graph.json \
  --format text
```

**Auto-detected**: `system_of_systems_graph` format

### Example 2: Analyzing Ecosystem Graph

```bash
python3 src/causality_analysis.py \
  test_ecosystems/with_wolves/ecosystem_graph.json \
  --format json
```

**Auto-detected**: `ecosystem` format

### Example 3: Mixed Format Analysis

```bash
python3 src/matryoshka_analysis.py \
  /path/to/reflow_graph.json  # system_of_systems_graph format
  # Tool auto-detects and handles correctly
```

### Example 4: Creative Linking Across Frameworks

```bash
python3 src/creative_linking.py \
  chain_reflow_graph.json \  # decision_flow framework
  reflow_graph.json          # UAF framework
  --format text
```

**Auto-detected**: Both formats recognized, frameworks noted in output

---

## Converting Between Formats

### Ecosystem → System of Systems Graph

```python
import json

def ecosystem_to_sos_graph(ecosystem_file: str, output_file: str):
    """Convert ecosystem format to system_of_systems_graph format"""
    with open(ecosystem_file, 'r') as f:
        data = json.load(f)

    # Extract ecosystem graph
    eco_graph = data.get('graph', {})
    metadata = data.get('metadata', {})

    # Build system_of_systems_graph
    sos_graph = {
        "system_of_systems_graph": {
            "metadata": {
                "system_name": metadata.get('system_name', 'Unknown'),
                "framework": metadata.get('framework', 'unknown'),
                "version": "1.0.0"
            },
            "nodes": [],
            "edges": []
        }
    }

    # Convert nodes (id → node_id, name → node_name)
    for node in eco_graph.get('nodes', []):
        sos_node = {
            "node_id": node.get('id'),
            "node_name": node.get('name'),
            "node_type": node.get('type', 'component'),
            "status": node.get('status', 'operational')
        }
        sos_graph['system_of_systems_graph']['nodes'].append(sos_node)

    # Convert edges (links → edges, strength → weight)
    for link in eco_graph.get('links', []):
        sos_edge = {
            "edge_id": f"E{len(sos_graph['system_of_systems_graph']['edges']) + 1:02d}",
            "source": link.get('source'),
            "target": link.get('target'),
            "edge_type": link.get('type', 'interaction'),
            "weight": link.get('strength', 1.0)
        }
        sos_graph['system_of_systems_graph']['edges'].append(sos_edge)

    # Write output
    with open(output_file, 'w') as f:
        json.dumps(sos_graph, f, indent=2)

    print(f"✓ Converted {ecosystem_file} → {output_file}")
```

### System of Systems Graph → Direct Format

```python
def sos_graph_to_direct(sos_file: str, output_file: str):
    """Simplify system_of_systems_graph to direct format"""
    with open(sos_file, 'r') as f:
        data = json.load(f)

    sos = data['system_of_systems_graph']

    # Simplify to direct format
    direct = {
        "nodes": [
            {
                "id": n['node_id'],
                "name": n['node_name'],
                "type": n.get('node_type', 'unknown')
            }
            for n in sos['nodes']
        ],
        "edges": [
            {
                "source": e['source'],
                "target": e['target'],
                "type": e.get('edge_type', 'unknown')
            }
            for e in sos.get('edges', [])
        ]
    }

    with open(output_file, 'w') as f:
        json.dump(direct, f, indent=2)

    print(f"✓ Simplified {sos_file} → {output_file}")
```

---

## Framework Compatibility Matrix

| Tool | Ecosystem | System of Systems | Direct | UAF | Functional Flow |
|------|-----------|-------------------|--------|-----|-----------------|
| matrix_gap_detection | ✅ | ✅ | ✅ | ✅* | ✅* |
| causality_analysis | ✅ | ✅ | ✅ | ✅* | ✅* |
| matryoshka_analysis | ✅ | ✅ | ✅ | ✅* | ✅* |
| creative_linking | ✅ | ✅ | ✅ | ✅* | ✅* |
| validate_merged_architecture | ✅ | ✅ | ✅ | ✅* | ✅* |

*Auto-detected via wrapper formats (system_of_systems_graph or direct)

---

## Best Practices

### 1. Use Native Format When Possible
- If creating new architectures for Chain Reflow, use `system_of_systems_graph` format
- Consistent with Reflow tooling
- Better metadata support

### 2. Let Auto-Detection Work
- Don't manually convert unless necessary
- Tools handle format detection automatically
- Reduces errors and maintenance

### 3. Document Framework Choice
- Include `framework` field in metadata
- Examples: `"decision_flow"`, `"functional_flow"`, `"uaf"`, `"systems_biology"`
- Helps users understand architecture type

### 4. Validate After Conversion
- Use `validate_merged_architecture.py` after format conversion
- Check for missing fields or broken references

### 5. Maintain Metadata
- Preserve version information
- Track framework type
- Document conversion history

---

## Troubleshooting

### Error: "Unknown graph format"

**Cause**: File doesn't match any recognized schema

**Solution**:
1. Check file has one of: `system_of_systems_graph`, `graph`, or `nodes` key
2. Ensure JSON is valid
3. Add wrapper if needed:
   ```json
   {
     "nodes": [...],
     "edges": [...]
   }
   ```

### Error: "No nodes or components found"

**Cause**: Nodes key missing or empty

**Solution**:
1. Ensure `nodes` array exists
2. Check node format (must have `id` or `node_id`)
3. Verify file is not corrupted

### Warning: "Skipping edge referencing unknown node"

**Cause**: Edge references node_id that doesn't exist in nodes array

**Solution**:
1. Check all edge `source` and `target` values exist in nodes
2. Remove placeholder nodes like "MISSING_SYSTEM"
3. Update edge references to valid nodes

---

## Advanced Topics

### Custom Framework Support

To add support for a new framework:

1. **Update format detection** in each analysis engine
2. **Add field mappings** for framework-specific fields
3. **Update tier mappings** (for matryoshka_analysis)
4. **Test with sample architectures**
5. **Document in this guide**

### Multi-Framework Projects

When working with multiple frameworks:

1. **Tag each architecture** with framework type in metadata
2. **Use creative_linking** to find connections across frameworks
3. **Validate merged results** with validate_merged_architecture.py
4. **Document framework boundaries** in architecture docs

---

## See Also

- [Chain Reflow README](../README.md) - Main documentation
- [Matrix Gap Detection](matrix_gap_detection_guide.md) - Gap analysis guide
- [Causality Analysis](correlation_vs_causation.md) - Causality vs correlation
- [Matryoshka Analysis](matryoshka_hierarchical_nesting.md) - Hierarchy detection

---

**Updated**: 2025-11-05 (v1.3.0)
**Maintainer**: Chain Reflow Development Team
