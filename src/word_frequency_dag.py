#!/usr/bin/env python3
"""
Word Frequency DAG Builder

Converts text (books) into directed acyclic graphs (DAGs) where:
- Nodes = unique words (tokens)
- Edges = transitions from one word to the next
- Edge weights = normalized frequency of transitions

Output format: system_of_systems_graph.json (compatible with chain_reflow)
"""

import json
import re
import argparse
from collections import defaultdict, Counter
from pathlib import Path
from typing import Dict, List, Tuple


class WordFrequencyDAG:
    """Build word frequency directed graph from text"""

    def __init__(self, text_file: str, book_title: str = None):
        self.text_file = Path(text_file)
        self.book_title = book_title or self.text_file.stem
        self.tokens = []
        self.transitions = defaultdict(Counter)  # word -> {next_word: count}
        self.word_counts = Counter()

    def tokenize(self, text: str) -> List[str]:
        """
        Tokenize text into words
        - Lowercase
        - Keep alphanumeric and apostrophes
        - Split on whitespace and punctuation
        """
        # Convert to lowercase
        text = text.lower()

        # Replace punctuation (except apostrophes) with spaces
        text = re.sub(r"[^\w\s']", ' ', text)

        # Split on whitespace and filter empty strings
        tokens = [t.strip("'") for t in text.split() if t.strip("'")]

        return tokens

    def build_transitions(self):
        """Build word transition matrix"""
        # Read text file
        with open(self.text_file, 'r', encoding='utf-8') as f:
            text = f.read()

        # Tokenize
        self.tokens = self.tokenize(text)

        # Count word frequencies
        self.word_counts = Counter(self.tokens)

        # Build transitions (bigrams)
        for i in range(len(self.tokens) - 1):
            current_word = self.tokens[i]
            next_word = self.tokens[i + 1]
            self.transitions[current_word][next_word] += 1

    def normalize_transitions(self) -> Dict[str, Dict[str, float]]:
        """
        Normalize transitions per node
        Each node's outgoing edges sum to 1.0 (Markov chain style)
        """
        normalized = {}

        for word, next_words in self.transitions.items():
            total = sum(next_words.values())
            normalized[word] = {
                next_word: count / total
                for next_word, count in next_words.items()
            }

        return normalized

    def to_system_of_systems_graph(self) -> dict:
        """
        Convert word DAG to system_of_systems_graph.json format

        Nodes: Words (tokens)
        Edges: Transitions with normalized weights
        """
        normalized_transitions = self.normalize_transitions()

        # Build nodes
        nodes = []
        for word, count in self.word_counts.items():
            # Calculate node probability (word frequency in corpus)
            probability = count / len(self.tokens)

            node = {
                "node_id": word,
                "node_type": "word_token",
                "label": word,
                "metadata": {
                    "frequency_count": count,
                    "probability": probability,
                    "outgoing_transitions": len(normalized_transitions.get(word, {}))
                }
            }
            nodes.append(node)

        # Build edges
        edges = []
        edge_id_counter = 1

        for source_word, targets in normalized_transitions.items():
            for target_word, normalized_weight in targets.items():
                raw_count = self.transitions[source_word][target_word]

                edge = {
                    "edge_id": f"edge_{edge_id_counter}",
                    "source_node_id": source_word,
                    "target_node_id": target_word,
                    "edge_type": "word_transition",
                    "weight": normalized_weight,
                    "metadata": {
                        "raw_count": raw_count,
                        "normalized_weight": normalized_weight
                    }
                }
                edges.append(edge)
                edge_id_counter += 1

        # Build graph
        graph = {
            "graph_metadata": {
                "graph_id": f"word_dag_{self.book_title.replace(' ', '_').lower()}",
                "graph_name": f"Word Frequency DAG: {self.book_title}",
                "version": "1.0.0",
                "description": f"Word frequency directed graph for '{self.book_title}'",
                "creation_timestamp": "2025-11-08T00:00:00Z",
                "source_text": str(self.text_file),
                "total_tokens": len(self.tokens),
                "unique_tokens": len(self.word_counts),
                "total_transitions": sum(len(targets) for targets in self.transitions.values())
            },
            "framework_configuration": {
                "framework_id": "word_frequency",
                "framework_name": "Word Frequency Network Framework",
                "framework_version": "1.0.0",
                "description": "Natural language processing framework using word transition networks"
            },
            "nodes": nodes,
            "edges": edges,
            "hierarchy": {
                "levels": ["token", "sentence", "paragraph", "chapter", "book"],
                "current_level": "token",
                "parent_system": None
            }
        }

        return graph

    def save_graph(self, output_file: str):
        """Save graph to JSON file"""
        graph = self.to_system_of_systems_graph()

        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(graph, f, indent=2, ensure_ascii=False)

        print(f"✓ Word DAG saved to {output_path}")
        print(f"  Total tokens: {len(self.tokens)}")
        print(f"  Unique words: {len(self.word_counts)}")
        print(f"  Total transitions: {sum(len(targets) for targets in self.transitions.values())}")

        return output_path


def main():
    parser = argparse.ArgumentParser(
        description="Build word frequency DAG from text file",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Build word DAG from a book
  python3 src/word_frequency_dag.py book1.txt --title "Moby Dick" --output output/moby_dick_dag.json

  # Build DAG from another book
  python3 src/word_frequency_dag.py book2.txt --title "Pride and Prejudice" --output output/pride_dag.json

  # Then use chain_reflow workflows to merge them
  python3 src/workflow_runner.py workflows/chain-00-setup.json
        """
    )

    parser.add_argument('text_file', help='Path to text file (book)')
    parser.add_argument('--title', '-t', help='Book title (default: filename)')
    parser.add_argument('--output', '-o', help='Output JSON file (default: output/<book>_dag.json)')
    parser.add_argument('--format', choices=['json', 'summary'], default='json',
                        help='Output format (default: json)')

    args = parser.parse_args()

    # Build DAG
    dag_builder = WordFrequencyDAG(args.text_file, args.title)
    dag_builder.build_transitions()

    # Determine output file
    if args.output:
        output_file = args.output
    else:
        book_name = args.title or Path(args.text_file).stem
        output_file = f"output/{book_name.replace(' ', '_').lower()}_dag.json"

    # Save
    if args.format == 'json':
        dag_builder.save_graph(output_file)
    else:
        # Summary mode
        print(f"Book: {dag_builder.book_title}")
        print(f"Total tokens: {len(dag_builder.tokens)}")
        print(f"Unique words: {len(dag_builder.word_counts)}")
        print(f"Total transitions: {sum(len(targets) for targets in dag_builder.transitions.values())}")

        # Top 10 most common words
        print("\nTop 10 most common words:")
        for word, count in dag_builder.word_counts.most_common(10):
            print(f"  {word}: {count}")


if __name__ == '__main__':
    main()
