#!/usr/bin/env python3
"""
Word DAG Linguistic Analysis

Applies systems engineering analysis to word frequency DAGs to identify:
- Orphaned nodes (words with no connections)
- Bottleneck words (high centrality - everything flows through them)
- Circular patterns (repetitive word loops)
- Structural efficiency metrics

This demonstrates using graph theory to analyze language structure.
"""

import json
import argparse
from pathlib import Path
from collections import defaultdict

try:
    import networkx as nx
except ImportError:
    print("ERROR: NetworkX is required. Install with: pip3 install networkx")
    exit(1)


class WordDAGAnalyzer:
    """Analyze word frequency DAG for linguistic patterns"""

    def __init__(self, dag_file):
        self.dag_file = Path(dag_file)
        self.dag_data = None
        self.graph = None
        self.load_dag()
        self.build_graph()

    def load_dag(self):
        """Load word DAG JSON"""
        with open(self.dag_file, 'r', encoding='utf-8') as f:
            self.dag_data = json.load(f)

    def build_graph(self):
        """Build NetworkX directed graph from word DAG"""
        self.graph = nx.DiGraph()

        # Add nodes
        for node in self.dag_data['nodes']:
            # Handle both regular and merged DAG structures
            metadata = node['metadata']
            if 'frequency_count' in metadata:
                frequency = metadata['frequency_count']
                probability = metadata.get('probability', 0)
            elif 'combined_frequency' in metadata:
                frequency = metadata['combined_frequency']
                probability = 0  # Merged graphs don't have probability
            else:
                frequency = metadata.get('frequency_count_graph1', 0) + metadata.get('frequency_count_graph2', 0)
                probability = 0

            self.graph.add_node(
                node['node_id'],
                label=node['label'],
                frequency=frequency,
                probability=probability
            )

        # Add edges
        for edge in self.dag_data['edges']:
            # Handle both regular and merged DAG structures
            metadata = edge.get('metadata', {})
            raw_count = metadata.get('raw_count', metadata.get('weight_graph1', 0) + metadata.get('weight_graph2', 0))

            self.graph.add_edge(
                edge['source_node_id'],
                edge['target_node_id'],
                weight=edge['weight'],
                raw_count=raw_count
            )

    def analyze_orphaned_nodes(self):
        """
        Find orphaned nodes (words with zero or minimal connections)

        In language:
        - Degree 0: Completely isolated (shouldn't happen in our DAGs)
        - In-degree 0: Words that never follow another word (sentence starters)
        - Out-degree 0: Words that never lead to another word (sentence enders)
        """
        orphans = {
            'isolated': [],  # No connections at all
            'dead_ends': [],  # No outgoing edges (sentence enders)
            'orphan_starts': []  # No incoming edges (sentence starters)
        }

        for node in self.graph.nodes():
            in_degree = self.graph.in_degree(node)
            out_degree = self.graph.out_degree(node)
            total_degree = in_degree + out_degree

            if total_degree == 0:
                orphans['isolated'].append(node)
            elif out_degree == 0:
                orphans['dead_ends'].append(node)
            elif in_degree == 0:
                orphans['orphan_starts'].append(node)

        return orphans

    def analyze_bottlenecks(self):
        """
        Find bottleneck words (high centrality)

        In language, these are connector words like "the", "is", "a"
        that most sentence paths flow through.
        """
        # Betweenness centrality: How often a word appears on paths between other words
        betweenness = nx.betweenness_centrality(self.graph, weight='weight')

        # In-degree: How many different words can lead to this word
        in_degree_centrality = nx.in_degree_centrality(self.graph)

        # Out-degree: How many different words this word can lead to
        out_degree_centrality = nx.out_degree_centrality(self.graph)

        # Combine metrics
        bottlenecks = []
        for node in self.graph.nodes():
            in_deg = self.graph.in_degree(node)
            out_deg = self.graph.out_degree(node)

            # Consider a word a bottleneck if it has high fan-in or fan-out
            if in_deg > 5 or out_deg > 5:
                bottlenecks.append({
                    'word': node,
                    'in_degree': in_deg,
                    'out_degree': out_deg,
                    'betweenness': betweenness[node],
                    'frequency': self.graph.nodes[node]['frequency']
                })

        # Sort by combined metric
        bottlenecks.sort(key=lambda x: x['in_degree'] + x['out_degree'], reverse=True)

        return bottlenecks, betweenness

    def analyze_circular_patterns(self):
        """
        Find circular dependencies (word loops)

        In language, these are repetitive patterns like:
        "the learning is deep learning" (learning → is → deep → learning)
        """
        # Find simple cycles (limit to first 100 to avoid long computation)
        try:
            cycles = []
            for cycle in nx.simple_cycles(self.graph):
                cycles.append(cycle)
                if len(cycles) >= 100:  # Limit to avoid long computation
                    break
        except:
            cycles = []

        # Find strongly connected components (mutually reachable words)
        sccs = list(nx.strongly_connected_components(self.graph))
        strong_sccs = [scc for scc in sccs if len(scc) > 1]

        return cycles, strong_sccs

    def analyze_paths(self):
        """
        Analyze path metrics

        - Average path length: How many word transitions between any two words
        - Diameter: Longest shortest path (linguistic "width")
        """
        try:
            # Only works for connected graphs
            if nx.is_weakly_connected(self.graph):
                avg_path_length = nx.average_shortest_path_length(self.graph)
                diameter = nx.diameter(self.graph)
            else:
                # For disconnected graphs, analyze largest component
                largest_cc = max(nx.weakly_connected_components(self.graph), key=len)
                subgraph = self.graph.subgraph(largest_cc)
                avg_path_length = nx.average_shortest_path_length(subgraph)
                diameter = nx.diameter(subgraph)

            return avg_path_length, diameter
        except:
            return None, None

    def analyze_efficiency(self):
        """
        Calculate language efficiency metrics

        - Density: How connected is the word network?
        - Clustering coefficient: How much do word neighborhoods overlap?
        - Transitivity: Measure of triangular structures
        """
        density = nx.density(self.graph)

        # Clustering (treat as undirected for this metric)
        undirected = self.graph.to_undirected()
        avg_clustering = nx.average_clustering(undirected)
        transitivity = nx.transitivity(undirected)

        return {
            'density': density,
            'average_clustering': avg_clustering,
            'transitivity': transitivity
        }

    def generate_report(self):
        """Generate comprehensive analysis report"""
        metadata = self.dag_data['graph_metadata']
        book_title = metadata['graph_name']
        total_tokens = metadata.get('total_tokens', metadata.get('total_nodes', len(self.dag_data['nodes'])))
        unique_words = metadata.get('unique_tokens', len(self.dag_data['nodes']))

        print(f"\n{'='*70}")
        print(f"WORD DAG LINGUISTIC ANALYSIS")
        print(f"{'='*70}")
        print(f"Book: {book_title}")
        print(f"Total tokens: {total_tokens}")
        print(f"Unique words: {unique_words}")
        print(f"Total transitions: {len(self.dag_data['edges'])}")
        print(f"{'='*70}\n")

        # 1. Orphaned nodes
        print(f"{'='*70}")
        print(f"ORPHANED NODES ANALYSIS")
        print(f"{'='*70}")
        orphans = self.analyze_orphaned_nodes()

        print(f"\n📍 Sentence Starters (no incoming edges):")
        print(f"   These words begin sentences or text blocks")
        print(f"   Count: {len(orphans['orphan_starts'])}")
        if orphans['orphan_starts'][:10]:
            print(f"   Examples: {', '.join(orphans['orphan_starts'][:10])}")

        print(f"\n🛑 Dead Ends (no outgoing edges):")
        print(f"   These words end sentences or text blocks")
        print(f"   Count: {len(orphans['dead_ends'])}")
        if orphans['dead_ends'][:10]:
            print(f"   Examples: {', '.join(orphans['dead_ends'][:10])}")

        if orphans['isolated']:
            print(f"\n⚠️  Completely Isolated: {len(orphans['isolated'])}")
            print(f"   Examples: {orphans['isolated']}")

        # 2. Bottlenecks
        print(f"\n{'='*70}")
        print(f"BOTTLENECK WORDS ANALYSIS")
        print(f"{'='*70}")
        print(f"These are connector words that most paths flow through\n")

        bottlenecks, betweenness = self.analyze_bottlenecks()

        print(f"Top 15 Bottleneck Words (by degree):")
        print(f"-" * 70)
        print(f"{'Rank':<6}{'Word':<15}{'In-Deg':<10}{'Out-Deg':<10}{'Frequency':<12}{'Betweenness':<12}")
        print(f"-" * 70)

        for i, b in enumerate(bottlenecks[:15], 1):
            print(f"{i:<6}{b['word']:<15}{b['in_degree']:<10}{b['out_degree']:<10}{b['frequency']:<12}{b['betweenness']:<12.4f}")

        # 3. Circular patterns
        print(f"\n{'='*70}")
        print(f"CIRCULAR PATTERNS ANALYSIS")
        print(f"{'='*70}")
        cycles, sccs = self.analyze_circular_patterns()

        print(f"\n🔄 Simple Cycles Found: {len(cycles)}")
        if cycles and len(cycles) <= 20:
            print(f"\nCycle patterns:")
            for i, cycle in enumerate(cycles[:20], 1):
                cycle_str = " → ".join(cycle) + f" → {cycle[0]}"
                print(f"   {i}. {cycle_str}")
        elif cycles:
            print(f"   (showing first 20 of {len(cycles)} cycles)")
            for i, cycle in enumerate(cycles[:20], 1):
                cycle_str = " → ".join(cycle) + f" → {cycle[0]}"
                print(f"   {i}. {cycle_str}")

        print(f"\n🔗 Strongly Connected Components: {len(sccs)}")
        if sccs:
            print(f"   These are word groups that form closed loops:")
            for i, scc in enumerate(sccs[:10], 1):
                print(f"   {i}. [{len(scc)} words]: {', '.join(list(scc)[:10])}")

        # 4. Path analysis
        print(f"\n{'='*70}")
        print(f"PATH & DISTANCE ANALYSIS")
        print(f"{'='*70}")
        avg_path, diameter = self.analyze_paths()

        if avg_path:
            print(f"\n📏 Average path length: {avg_path:.2f} word transitions")
            print(f"   (How many words typically separate any two words)")
            print(f"\n📐 Network diameter: {diameter} transitions")
            print(f"   (Maximum shortest path between any two words)")
        else:
            print(f"\n⚠️  Graph is disconnected - path metrics only apply to largest component")

        # 5. Efficiency metrics
        print(f"\n{'='*70}")
        print(f"LANGUAGE EFFICIENCY METRICS")
        print(f"{'='*70}")
        efficiency = self.analyze_efficiency()

        print(f"\n📊 Network Density: {efficiency['density']:.4f}")
        print(f"   (Ratio of actual transitions to all possible transitions)")
        print(f"   High density = more word-to-word variety")

        print(f"\n🕸️  Average Clustering Coefficient: {efficiency['average_clustering']:.4f}")
        print(f"   (How much word neighborhoods overlap)")
        print(f"   High clustering = tightly grouped vocabulary patterns")

        print(f"\n🔺 Transitivity: {efficiency['transitivity']:.4f}")
        print(f"   (Likelihood of triangular word patterns)")
        print(f"   High transitivity = reinforced linguistic paths")

        # 6. Summary insights
        print(f"\n{'='*70}")
        print(f"LINGUISTIC INSIGHTS")
        print(f"{'='*70}\n")

        # Determine if language is efficient
        if efficiency['density'] < 0.1:
            print(f"✓ Sparse network - diverse vocabulary with limited repetition")
        else:
            print(f"✓ Dense network - high word reuse and repetition")

        if len(bottlenecks) > 0:
            top_bottleneck = bottlenecks[0]
            print(f"✓ Primary bottleneck: '{top_bottleneck['word']}' (appears in {top_bottleneck['frequency']} transitions)")

        if len(cycles) > 10:
            print(f"✓ Heavy circular pattern usage ({len(cycles)} cycles) - repetitive phrasing")
        elif len(cycles) > 0:
            print(f"✓ Moderate circular patterns ({len(cycles)} cycles) - some repetition")
        else:
            print(f"✓ No circular patterns - linear prose structure")

        if len(orphans['dead_ends']) > 20:
            print(f"✓ Many sentence-ending words ({len(orphans['dead_ends'])}) - short, choppy sentences")
        else:
            print(f"✓ Few sentence-ending words ({len(orphans['dead_ends'])}) - longer flowing sentences")

        print(f"\n{'='*70}\n")

        # Return structured data
        return {
            'orphans': orphans,
            'bottlenecks': bottlenecks,
            'cycles': cycles,
            'strongly_connected_components': sccs,
            'paths': {'average': avg_path, 'diameter': diameter},
            'efficiency': efficiency
        }


def main():
    parser = argparse.ArgumentParser(
        description="Analyze word frequency DAG for linguistic patterns",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze ML book
  python3 src/analyze_word_dag.py output/ml_book_dag.json

  # Analyze poetry book
  python3 src/analyze_word_dag.py output/poetry_book_dag.json

  # Save analysis to JSON
  python3 src/analyze_word_dag.py output/ml_book_dag.json --output output/ml_analysis.json
        """
    )

    parser.add_argument('dag_file', help='Path to word DAG JSON file')
    parser.add_argument('--output', '-o', help='Save analysis to JSON file')

    args = parser.parse_args()

    # Analyze
    analyzer = WordDAGAnalyzer(args.dag_file)
    results = analyzer.generate_report()

    # Save if requested
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, default=str)

        print(f"✓ Analysis saved to {output_path}")


if __name__ == '__main__':
    main()
