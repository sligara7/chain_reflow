# Word Frequency DAG - Natural Language Analysis with Chain Reflow

## Overview

This feature extends chain_reflow to analyze and merge **word frequency directed acyclic graphs (DAGs)** from books and text documents. It demonstrates how chain_reflow's architecture linking concepts apply to natural language processing.

## Concept

Each book becomes a **network graph** where:
- **Nodes** = Unique words (tokens)
- **Edges** = Transitions from one word to the next
- **Edge weights** = Normalized frequency of transitions (Markov chain style)

This creates a "linguistic fingerprint" of a book that can be:
1. Analyzed independently
2. Compared with other books
3. Merged to find commonalities between orthogonal texts

## Quick Start

### 1. Build Word DAG from a Book

```bash
# Create word frequency DAG from a text file
python3 src/word_frequency_dag.py test_books/technical_ml.txt \
  --title "Machine Learning Fundamentals" \
  --output output/ml_book_dag.json
```

**Output:**
```
✓ Word DAG saved to output/ml_book_dag.json
  Total tokens: 251
  Unique words: 133
  Total transitions: 222
```

### 2. Build DAG for Another Book

```bash
python3 src/word_frequency_dag.py test_books/poetry_nature.txt \
  --title "Whispers of the Forest" \
  --output output/poetry_book_dag.json
```

### 3. Merge the Two DAGs

```bash
python3 src/merge_word_dags.py \
  output/ml_book_dag.json \
  output/poetry_book_dag.json \
  --output output/merged_word_dag.json
```

**Output shows:**
- Word overlap analysis
- Common transitions
- Merged graph statistics

## Example Results: Orthogonal Books

When merging a **technical ML book** with a **poetry book about nature**, we see fascinating results:

### Word Overlap: Only 6.4%!

```
Common words: 18
Unique to 'ML Book': 115
Unique to 'Poetry Book': 149
Overlap percentage: 6.4%
```

### Top Common Words (Function Words)

| Rank | Word     | ML Count | Poetry Count | Total |
|------|----------|----------|--------------|-------|
| 1    | the      | 14       | 20           | 34    |
| 2    | in       | 4        | 10           | 14    |
| 3    | of       | 8        | 4            | 12    |
| 4    | to       | 6        | 3            | 9     |
| 5    | is       | 8        | 1            | 9     |

**Key Insight:** Common words are mostly grammatical connectors (the, in, of, to, is, and), not domain-specific content. The books share linguistic structure but not semantic content - true orthogonality!

### Common Transitions: Only 5 out of 438!

```
1. 'through' → 'the': ML=1, Poetry=2, Total=3
2. 'from' → 'the': ML=1, Poetry=1, Total=2
3. 'on' → 'the': ML=1, Poetry=1, Total=2
4. 'of' → 'the': ML=1, Poetry=1, Total=2
5. 'in' → 'an': ML=1, Poetry=1, Total=2
```

Even the common transitions are grammatical patterns, not semantic pathways.

## Output Format

Word DAGs are exported in `system_of_systems_graph.json` format (compatible with chain_reflow):

```json
{
  "graph_metadata": {
    "graph_id": "word_dag_machine_learning_fundamentals",
    "total_tokens": 251,
    "unique_tokens": 133,
    "total_transitions": 222
  },
  "framework_configuration": {
    "framework_id": "word_frequency",
    "framework_name": "Word Frequency Network Framework"
  },
  "nodes": [
    {
      "node_id": "machine",
      "node_type": "word_token",
      "label": "machine",
      "metadata": {
        "frequency_count": 6,
        "probability": 0.0239,
        "outgoing_transitions": 1
      }
    }
  ],
  "edges": [
    {
      "edge_id": "edge_1",
      "source_node_id": "machine",
      "target_node_id": "learning",
      "edge_type": "word_transition",
      "weight": 1.0,
      "metadata": {
        "raw_count": 6,
        "normalized_weight": 1.0
      }
    }
  ]
}
```

## Use Cases

### 1. Comparative Literature Analysis

Compare writing styles across authors, genres, or time periods:
```bash
# Build DAGs for different authors
python3 src/word_frequency_dag.py hemingway.txt --title "Hemingway" -o output/hemingway_dag.json
python3 src/word_frequency_dag.py joyce.txt --title "Joyce" -o output/joyce_dag.json

# Compare
python3 src/merge_word_dags.py output/hemingway_dag.json output/joyce_dag.json -o output/style_comparison.json
```

### 2. Detecting Plagiarism or Influence

High transition overlap between two books might indicate:
- Plagiarism (very high overlap: >50%)
- Strong influence (moderate overlap: 20-50%)
- Same genre/style (low overlap: 5-20%)
- Orthogonal content (very low overlap: <5%)

### 3. Genre Classification

Build word DAGs for books in different genres and use them as training data for genre classification.

### 4. Translation Quality Analysis

Compare original text with translations - good translations should preserve:
- Similar word frequency distributions
- Similar transition patterns
- Same "shape" of the network

### 5. Finding Semantic Bridges

When merging orthogonal books, the few common transitions reveal universal linguistic patterns that transcend domain boundaries.

## Advanced: Using Chain Reflow Workflows

The word DAGs can be analyzed using chain_reflow's existing workflows:

### Matryoshka Analysis (Hierarchical Nesting)

Word networks have natural hierarchy levels:
- **Token** (word level) - what we built
- **Sentence** (sentence-level DAG)
- **Paragraph** (paragraph-level DAG)
- **Chapter** (chapter-level DAG)
- **Book** (book-level DAG)

Future work could build multi-level hierarchical word DAGs.

### Creative Linking

For truly orthogonal books (like our ML + Poetry example), creative linking could find:
- **Metaphorical connections**: "deep learning" (ML) ↔ "deep roots" (nature)
- **Synesthetic mappings**: "neural network layers" ↔ "forest canopy layers"
- **Cross-domain analogies**: "information flow" ↔ "water flow"

### Causality Analysis

When two books share unusual transitions, ask:
- **Correlation**: Both books happen to use similar phrases
- **Causation**: One author influenced the other
- **Spurious**: Coincidental similarity
- **Common source**: Both influenced by a third source

## Normalization Strategy

Word transitions are normalized **per-node** (Markov chain style):
- Each word's outgoing edges sum to 1.0
- Example: "learning" appears 10 times in the text
  - "learning" → "is": 3 times (weight: 0.3)
  - "learning" → "uses": 1 time (weight: 0.1)
  - etc. (sum of all outgoing weights = 1.0)

This makes the network interpretable as a **language model**:
- Node probability = P(word appears in text)
- Edge weight = P(next_word | current_word)

## Tokenization Details

Current implementation:
- **Case-insensitive**: "Machine" → "machine"
- **Punctuation removed**: "learning." → "learning"
- **Apostrophes preserved**: "it's" (kept), but trailing apostrophes removed
- **Stop words kept**: "the", "a", "is" are important for structure

Future enhancements could add:
- Lemmatization: "running" → "run"
- N-gram support: bigrams, trigrams
- Part-of-speech tagging
- Named entity recognition

## File Structure

```
chain_reflow/
├── src/
│   ├── word_frequency_dag.py      # Build word DAG from text
│   ├── merge_word_dags.py         # Merge multiple word DAGs
│   └── [existing tools...]
├── test_books/
│   ├── technical_ml.txt           # Example: ML technical text
│   └── poetry_nature.txt          # Example: Nature poetry
├── output/
│   ├── ml_book_dag.json           # Generated word DAG (ML)
│   ├── poetry_book_dag.json       # Generated word DAG (poetry)
│   └── merged_word_dag.json       # Merged result
└── docs/
    └── WORD_FREQUENCY_DAG_USAGE.md  # This file
```

## Future Enhancements

### 1. Sentence-Level DAGs
Build hierarchical DAGs where nodes are sentences (not words) and edges are sentence-to-sentence transitions.

### 2. Topic Modeling Integration
Integrate with LDA or other topic modeling to add semantic layers to word networks.

### 3. Temporal Analysis
For books with timestamps (e.g., social media, news articles), add temporal dimension to edges.

### 4. Weighted by Semantic Distance
Instead of just frequency, weight edges by semantic similarity (using word embeddings).

### 5. Interactive Visualization
Build web UI to explore word networks interactively.

## References

This work is inspired by:
- **Markov chains** in language modeling
- **Network analysis** in computational linguistics
- **Chain_reflow's** systems engineering methodology applied to natural language

## Example: Finding Commonality in Orthogonal Texts

The beauty of this approach is seeing how **orthogonal books find commonality**:

**ML Book (Technical):**
```
"Neural networks are fundamental architecture in machine learning..."
```

**Poetry Book (Creative):**
```
"Trees stand tall, their roots deep in the earth..."
```

**Merged Analysis Reveals:**
- Both use "deep" (ML: "deep learning", Poetry: "deep in earth")
- Both use "through" (ML: "through the network", Poetry: "through the undergrowth")
- Both describe **flow and transformation** (information flow vs water flow)

These connections emerge from the data - not imposed by the analyst!

## Conclusion

Word frequency DAGs transform books into analyzable network structures. By applying chain_reflow's methodology to natural language, we can:

1. **Quantify** stylistic differences between texts
2. **Discover** unexpected connections between orthogonal domains
3. **Validate** theories about literary influence
4. **Build** linguistic models from first principles

This is systems engineering for language - treating books as architectures to be linked, merged, and analyzed!
