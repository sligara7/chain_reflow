#!/usr/bin/env python3
"""
Merge Word Frequency DAGs

Demonstrates how to merge word frequency DAGs from different books.
This shows how chain_reflow's concepts apply to natural language networks.
"""

import json
import argparse
from pathlib import Path
from collections import defaultdict


def load_word_dag(filepath):
    """Load word DAG from JSON file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def merge_word_dags(dag1, dag2, merge_strategy='union'):
    """
    Merge two word frequency DAGs

    Merge strategies:
    - union: Combine all nodes and edges (add weights for common edges)
    - intersection: Only keep shared nodes and edges
    - weighted_average: Average weights for common edges
    """

    # Extract metadata
    graph1_name = dag1['graph_metadata']['graph_name']
    graph2_name = dag2['graph_metadata']['graph_name']

    print(f"\n{'='*70}")
    print(f"MERGING WORD DAGS")
    print(f"{'='*70}")
    print(f"Graph 1: {graph1_name}")
    print(f"  Total tokens: {dag1['graph_metadata']['total_tokens']}")
    print(f"  Unique words: {dag1['graph_metadata']['unique_tokens']}")
    print(f"\nGraph 2: {graph2_name}")
    print(f"  Total tokens: {dag2['graph_metadata']['total_tokens']}")
    print(f"  Unique words: {dag2['graph_metadata']['unique_tokens']}")
    print(f"{'='*70}\n")

    # Build node sets
    nodes1 = {node['node_id']: node for node in dag1['nodes']}
    nodes2 = {node['node_id']: node for node in dag2['nodes']}

    # Find common and unique words
    common_words = set(nodes1.keys()) & set(nodes2.keys())
    unique_to_dag1 = set(nodes1.keys()) - set(nodes2.keys())
    unique_to_dag2 = set(nodes2.keys()) - set(nodes1.keys())

    print(f"WORD OVERLAP ANALYSIS:")
    print(f"-" * 70)
    print(f"Common words: {len(common_words)}")
    print(f"Unique to '{graph1_name}': {len(unique_to_dag1)}")
    print(f"Unique to '{graph2_name}': {len(unique_to_dag2)}")
    print(f"Overlap percentage: {len(common_words) / len(set(nodes1.keys()) | set(nodes2.keys())) * 100:.1f}%")
    print(f"\nTop 20 common words (sorted by combined frequency):")

    # Calculate combined frequencies for common words
    common_word_freqs = []
    for word in common_words:
        freq1 = nodes1[word]['metadata']['frequency_count']
        freq2 = nodes2[word]['metadata']['frequency_count']
        combined = freq1 + freq2
        common_word_freqs.append((word, freq1, freq2, combined))

    common_word_freqs.sort(key=lambda x: x[3], reverse=True)

    for i, (word, freq1, freq2, combined) in enumerate(common_word_freqs[:20], 1):
        print(f"  {i:2}. {word:15s} (ML: {freq1:3d}, Poetry: {freq2:3d}, Total: {combined:3d})")

    # Analyze edges
    edges1 = {(e['source_node_id'], e['target_node_id']): e for e in dag1['edges']}
    edges2 = {(e['source_node_id'], e['target_node_id']): e for e in dag2['edges']}

    common_transitions = set(edges1.keys()) & set(edges2.keys())

    print(f"\n\nTRANSITION OVERLAP ANALYSIS:")
    print(f"-" * 70)
    print(f"Total transitions in '{graph1_name}': {len(edges1)}")
    print(f"Total transitions in '{graph2_name}': {len(edges2)}")
    print(f"Common transitions: {len(common_transitions)}")

    if common_transitions:
        print(f"\nTop 10 common transitions:")
        common_trans_data = []
        for trans in common_transitions:
            e1 = edges1[trans]
            e2 = edges2[trans]
            combined_count = e1['metadata']['raw_count'] + e2['metadata']['raw_count']
            common_trans_data.append((trans, e1['metadata']['raw_count'], e2['metadata']['raw_count'], combined_count))

        common_trans_data.sort(key=lambda x: x[3], reverse=True)

        for i, ((src, tgt), count1, count2, combined) in enumerate(common_trans_data[:10], 1):
            print(f"  {i:2}. '{src}' → '{tgt}': ML={count1}, Poetry={count2}, Total={combined}")

    # Create merged graph based on strategy
    merged_nodes = []
    merged_edges = []

    if merge_strategy == 'union':
        # Add all nodes from both graphs
        all_node_ids = set(nodes1.keys()) | set(nodes2.keys())

        for node_id in all_node_ids:
            if node_id in nodes1 and node_id in nodes2:
                # Node exists in both - combine metadata
                freq1 = nodes1[node_id]['metadata']['frequency_count']
                freq2 = nodes2[node_id]['metadata']['frequency_count']
                merged_nodes.append({
                    "node_id": node_id,
                    "node_type": "word_token",
                    "label": node_id,
                    "metadata": {
                        "frequency_count_graph1": freq1,
                        "frequency_count_graph2": freq2,
                        "combined_frequency": freq1 + freq2,
                        "source": "both"
                    }
                })
            elif node_id in nodes1:
                # Only in graph 1
                node = nodes1[node_id].copy()
                node['metadata']['source'] = 'graph1'
                merged_nodes.append(node)
            else:
                # Only in graph 2
                node = nodes2[node_id].copy()
                node['metadata']['source'] = 'graph2'
                merged_nodes.append(node)

        # Add all edges
        all_edge_keys = set(edges1.keys()) | set(edges2.keys())
        edge_id = 1

        for edge_key in all_edge_keys:
            src, tgt = edge_key
            if edge_key in edges1 and edge_key in edges2:
                # Edge exists in both - average weights
                w1 = edges1[edge_key]['weight']
                w2 = edges2[edge_key]['weight']
                merged_edges.append({
                    "edge_id": f"merged_edge_{edge_id}",
                    "source_node_id": src,
                    "target_node_id": tgt,
                    "edge_type": "word_transition",
                    "weight": (w1 + w2) / 2,
                    "metadata": {
                        "weight_graph1": w1,
                        "weight_graph2": w2,
                        "source": "both"
                    }
                })
            elif edge_key in edges1:
                edge = edges1[edge_key].copy()
                edge['edge_id'] = f"merged_edge_{edge_id}"
                edge['metadata']['source'] = 'graph1'
                merged_edges.append(edge)
            else:
                edge = edges2[edge_key].copy()
                edge['edge_id'] = f"merged_edge_{edge_id}"
                edge['metadata']['source'] = 'graph2'
                merged_edges.append(edge)

            edge_id += 1

    # Create merged graph JSON
    merged_graph = {
        "graph_metadata": {
            "graph_id": "merged_word_dag",
            "graph_name": f"Merged: {graph1_name} + {graph2_name}",
            "version": "1.0.0",
            "description": f"Merged word frequency DAG using {merge_strategy} strategy",
            "source_graphs": [
                dag1['graph_metadata']['graph_id'],
                dag2['graph_metadata']['graph_id']
            ],
            "merge_strategy": merge_strategy,
            "total_nodes": len(merged_nodes),
            "total_edges": len(merged_edges),
            "common_nodes": len(common_words),
            "common_edges": len(common_transitions)
        },
        "framework_configuration": {
            "framework_id": "word_frequency",
            "framework_name": "Word Frequency Network Framework",
            "framework_version": "1.0.0",
            "description": "Merged natural language processing framework"
        },
        "nodes": merged_nodes,
        "edges": merged_edges
    }

    print(f"\n\nMERGED GRAPH STATISTICS:")
    print(f"-" * 70)
    print(f"Total nodes: {len(merged_nodes)}")
    print(f"Total edges: {len(merged_edges)}")
    print(f"Nodes from both graphs: {len(common_words)}")
    print(f"Edges from both graphs: {len(common_transitions)}")
    print(f"{'='*70}\n")

    return merged_graph


def main():
    parser = argparse.ArgumentParser(
        description="Merge word frequency DAGs from different books",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Merge two word DAGs
  python3 src/merge_word_dags.py output/ml_book_dag.json output/poetry_book_dag.json --output output/merged_dag.json

  # Use different merge strategy
  python3 src/merge_word_dags.py dag1.json dag2.json --strategy intersection
        """
    )

    parser.add_argument('dag1', help='First word DAG JSON file')
    parser.add_argument('dag2', help='Second word DAG JSON file')
    parser.add_argument('--output', '-o', help='Output merged DAG file', required=True)
    parser.add_argument('--strategy', choices=['union', 'intersection', 'weighted_average'],
                        default='union', help='Merge strategy (default: union)')

    args = parser.parse_args()

    # Load DAGs
    dag1 = load_word_dag(args.dag1)
    dag2 = load_word_dag(args.dag2)

    # Merge
    merged = merge_word_dags(dag1, dag2, args.strategy)

    # Save
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(merged, f, indent=2, ensure_ascii=False)

    print(f"✓ Merged DAG saved to {output_path}")


if __name__ == '__main__':
    main()
