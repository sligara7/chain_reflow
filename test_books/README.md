# Test Books for Word Frequency DAG

This directory contains example text files for testing word frequency DAG generation and merging.

## Available Books

### 1. `technical_ml.txt` - Machine Learning Fundamentals
- **Genre:** Technical / Educational
- **Domain:** Computer Science / Machine Learning
- **Word count:** ~251 tokens
- **Unique words:** ~133
- **Style:** Formal, technical, explanatory
- **Key concepts:** Neural networks, training, optimization, deep learning

### 2. `poetry_nature.txt` - Whispers of the Forest
- **Genre:** Poetry / Creative Writing
- **Domain:** Nature / Philosophy
- **Word count:** ~235 tokens
- **Unique words:** ~167
- **Style:** Lyrical, descriptive, metaphorical
- **Key concepts:** Forest, seasons, trees, transformation, memory

## Orthogonality

These two books are intentionally **orthogonal** (very different domains):

- **Word overlap:** Only 6.4% (18 common words out of 282 total unique words)
- **Transition overlap:** Only 5 common word pairs out of 443 total transitions
- **Common words:** Mostly grammatical connectors (the, in, of, to, is, and, a, each)

This makes them perfect for demonstrating chain_reflow's creative linking capabilities - finding commonality in seemingly unrelated texts.

## Usage

### Generate Word DAGs

```bash
# Technical ML book
python3 src/word_frequency_dag.py test_books/technical_ml.txt \
  --title "Machine Learning Fundamentals" \
  --output output/ml_book_dag.json

# Poetry book
python3 src/word_frequency_dag.py test_books/poetry_nature.txt \
  --title "Whispers of the Forest" \
  --output output/poetry_book_dag.json
```

### Merge DAGs

```bash
python3 src/merge_word_dags.py \
  output/ml_book_dag.json \
  output/poetry_book_dag.json \
  --output output/merged_word_dag.json
```

## Adding Your Own Books

To analyze your own books:

1. Create a `.txt` file with your book's text
2. Place it in this directory
3. Run `word_frequency_dag.py` on it
4. Merge with other books to compare

**Tips:**
- Plain text works best (no special formatting)
- Longer books give better results (500+ words recommended)
- Try comparing books from very different genres!
