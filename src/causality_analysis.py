#!/usr/bin/env python3
"""
Causality Analysis Module for Chain Reflow

Handles the distinction between correlation and causation when linking architectures.
Users may observe that two systems seem related (correlation) without understanding
whether one actually affects the other (causation).

Key Principles:
1. Correlation ≠ Causation (just because systems seem related doesn't mean one causes the other)
2. Worth exploring: Correlations are valid starting points for scientific investigation
3. Requires validation: Causal claims must be tested and validated
4. Clear disclaimers: All correlational links must be marked as such

IMPORTANT: This module generates HYPOTHESES about causal relationships.
These are exploratory and require validation through testing, observation, or analysis.
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
from datetime import datetime


class RelationshipType(Enum):
    """Types of relationships between architectures"""
    CORRELATION = "correlation"  # Observed pattern, causation unknown
    CAUSAL_HYPOTHESIS = "causal_hypothesis"  # Proposed causal link, needs validation
    VALIDATED_CAUSAL = "validated_causal"  # Tested and confirmed causal link
    SPURIOUS = "spurious"  # False correlation, no actual relationship
    BIDIRECTIONAL = "bidirectional"  # Both systems affect each other
    CONFOUNDED = "confounded"  # Related through a third factor


class CausalDirection(Enum):
    """Direction of potential causal relationship"""
    A_CAUSES_B = "a_causes_b"  # Architecture A affects Architecture B
    B_CAUSES_A = "b_causes_a"  # Architecture B affects Architecture A
    BIDIRECTIONAL = "bidirectional"  # Both affect each other
    UNKNOWN = "unknown"  # Correlation observed, direction unknown
    NO_CAUSATION = "no_causation"  # Correlation but no causal mechanism


class ValidationMethod(Enum):
    """Methods for validating causal hypotheses"""
    OBSERVATIONAL = "observational"  # Watch systems in operation
    EXPERIMENTAL = "experimental"  # Deliberately change one system, observe effect
    COUNTERFACTUAL = "counterfactual"  # "What if A didn't exist? Would B still behave this way?"
    MECHANISM_ANALYSIS = "mechanism_analysis"  # Identify the causal mechanism
    TEMPORAL_ANALYSIS = "temporal_analysis"  # Check if cause precedes effect
    INTERVENTION = "intervention"  # Modify the proposed cause, check if effect changes


@dataclass
class CorrelationPattern:
    """Represents an observed correlation between architectures"""
    id: str
    source_architecture: str
    target_architecture: str
    pattern_description: str
    evidence: List[str]
    correlation_strength: float  # 0.0 to 1.0
    observed_by: str  # "user" or "system"
    timestamp: str

    def to_dict(self):
        return asdict(self)


@dataclass
class CausalHypothesis:
    """Represents a hypothesis about causal relationship"""
    id: str
    correlation_id: str  # Links back to observed correlation
    source_architecture: str
    target_architecture: str
    causal_direction: str
    hypothesis: str  # "If X happens in source, then Y happens in target"
    proposed_mechanism: str  # How the causation works
    confidence: float  # 0.0 to 1.0 - how confident we are
    alternative_explanations: List[str]  # Competing hypotheses
    validation_methods: List[str]  # How to test this
    validation_status: str  # "untested", "testing", "validated", "refuted"
    exploratory: bool = True

    def to_dict(self):
        return asdict(self)


@dataclass
class SpuriousCorrelation:
    """Represents a false correlation with no causal link"""
    id: str
    correlation_id: str
    source_architecture: str
    target_architecture: str
    why_spurious: str
    confounding_factor: Optional[str] = None

    def to_dict(self):
        return asdict(self)


class CausalityAnalyzer:
    """
    Analyzes relationships between architectures to distinguish:
    - Correlation (observed pattern)
    - Causation (proven mechanism)
    - Spurious correlation (coincidental)
    """

    def __init__(self):
        self.correlations: List[CorrelationPattern] = []
        self.hypotheses: List[CausalHypothesis] = []
        self.spurious: List[SpuriousCorrelation] = []

    def detect_correlation(
        self,
        arch1: Dict[str, Any],
        arch2: Dict[str, Any],
        user_observation: Optional[str] = None
    ) -> List[CorrelationPattern]:
        """
        Detect correlational patterns between architectures

        Note: This detects CORRELATION, not CAUSATION
        """
        correlations = []

        # User-reported correlation
        if user_observation:
            corr = CorrelationPattern(
                id=f"corr_user_{arch1['name']}_{arch2['name']}",
                source_architecture=arch1['name'],
                target_architecture=arch2['name'],
                pattern_description=user_observation,
                evidence=["User observation"],
                correlation_strength=0.7,  # Higher for user observations
                observed_by="user",
                timestamp=datetime.now().isoformat()
            )
            correlations.append(corr)

        # System-detected correlations
        # Look for temporal patterns
        temporal_corr = self._detect_temporal_correlation(arch1, arch2)
        if temporal_corr:
            correlations.append(temporal_corr)

        # Look for structural similarities
        structural_corr = self._detect_structural_correlation(arch1, arch2)
        if structural_corr:
            correlations.append(structural_corr)

        # Look for behavioral patterns
        behavioral_corr = self._detect_behavioral_correlation(arch1, arch2)
        if behavioral_corr:
            correlations.append(behavioral_corr)

        self.correlations.extend(correlations)
        return correlations

    def _detect_temporal_correlation(
        self,
        arch1: Dict[str, Any],
        arch2: Dict[str, Any]
    ) -> Optional[CorrelationPattern]:
        """
        Detect temporal patterns: "When X happens in arch1, Y tends to happen in arch2"

        Note: Temporal correlation (A before B) is NECESSARY but NOT SUFFICIENT for causation
        """
        # In a real implementation, this would analyze execution traces, logs, metrics
        # For now, we'll look for structural hints

        # Check if arch1 has "trigger" or "emit" components and arch2 has "listen" or "respond"
        arch1_triggers = any(
            'trigger' in comp.get('name', '').lower() or
            'emit' in comp.get('name', '').lower() or
            'generate' in comp.get('name', '').lower()
            for comp in arch1.get('components', [])
        )

        arch2_responds = any(
            'listen' in comp.get('name', '').lower() or
            'respond' in comp.get('name', '').lower() or
            'handle' in comp.get('name', '').lower()
            for comp in arch2.get('components', [])
        )

        if arch1_triggers and arch2_responds:
            return CorrelationPattern(
                id=f"corr_temporal_{arch1['name']}_{arch2['name']}",
                source_architecture=arch1['name'],
                target_architecture=arch2['name'],
                pattern_description=f"{arch1['name']} has trigger/emit components, {arch2['name']} has listen/respond components - suggesting temporal correlation",
                evidence=[
                    "Source architecture has trigger/emit components",
                    "Target architecture has listen/respond components"
                ],
                correlation_strength=0.5,
                observed_by="system",
                timestamp=datetime.now().isoformat()
            )

        return None

    def _detect_structural_correlation(
        self,
        arch1: Dict[str, Any],
        arch2: Dict[str, Any]
    ) -> Optional[CorrelationPattern]:
        """Detect structural similarities that might indicate relationship"""
        # Check if both architectures have similar component counts or structures
        comp_count1 = len(arch1.get('components', []))
        comp_count2 = len(arch2.get('components', []))

        # If component counts are very similar, might be correlation
        if comp_count1 > 0 and comp_count2 > 0:
            ratio = min(comp_count1, comp_count2) / max(comp_count1, comp_count2)
            if ratio > 0.8:  # Very similar sizes
                return CorrelationPattern(
                    id=f"corr_structural_{arch1['name']}_{arch2['name']}",
                    source_architecture=arch1['name'],
                    target_architecture=arch2['name'],
                    pattern_description=f"Similar architectural complexity (both have ~{comp_count1} components)",
                    evidence=[
                        f"{arch1['name']}: {comp_count1} components",
                        f"{arch2['name']}: {comp_count2} components",
                        "Similar complexity might indicate related systems"
                    ],
                    correlation_strength=0.4,
                    observed_by="system",
                    timestamp=datetime.now().isoformat()
                )

        return None

    def _detect_behavioral_correlation(
        self,
        arch1: Dict[str, Any],
        arch2: Dict[str, Any]
    ) -> Optional[CorrelationPattern]:
        """Detect behavioral patterns that might indicate relationship"""
        # Check if both architectures have similar behavioral patterns
        # (in real implementation, would analyze metrics, traces, etc.)

        # For now, check if both have similar framework types
        framework1 = arch1.get('framework', '')
        framework2 = arch2.get('framework', '')

        if framework1 == framework2:
            return CorrelationPattern(
                id=f"corr_behavioral_{arch1['name']}_{arch2['name']}",
                source_architecture=arch1['name'],
                target_architecture=arch2['name'],
                pattern_description=f"Both use {framework1} framework - may indicate similar behavioral patterns",
                evidence=[
                    f"Both use {framework1} framework",
                    "Similar frameworks often indicate related behaviors"
                ],
                correlation_strength=0.6,
                observed_by="system",
                timestamp=datetime.now().isoformat()
            )

        return None

    def generate_causal_hypotheses(
        self,
        correlation: CorrelationPattern,
        user_causal_claim: Optional[str] = None
    ) -> List[CausalHypothesis]:
        """
        Generate hypotheses about potential causal relationships

        IMPORTANT: These are HYPOTHESES, not facts
        They must be validated before accepting as true causal links
        """
        hypotheses = []

        # Generate hypothesis for A → B
        hyp_a_to_b = self._generate_directional_hypothesis(
            correlation,
            CausalDirection.A_CAUSES_B,
            user_causal_claim
        )
        hypotheses.append(hyp_a_to_b)

        # Generate hypothesis for B → A (reverse direction)
        hyp_b_to_a = self._generate_directional_hypothesis(
            correlation,
            CausalDirection.B_CAUSES_A,
            user_causal_claim
        )
        hypotheses.append(hyp_b_to_a)

        # Generate bidirectional hypothesis
        hyp_bidirectional = self._generate_bidirectional_hypothesis(
            correlation,
            user_causal_claim
        )
        hypotheses.append(hyp_bidirectional)

        # Generate spurious hypothesis (correlation but no causation)
        hyp_spurious = self._generate_spurious_hypothesis(correlation)
        hypotheses.append(hyp_spurious)

        self.hypotheses.extend(hypotheses)
        return hypotheses

    def _generate_directional_hypothesis(
        self,
        correlation: CorrelationPattern,
        direction: CausalDirection,
        user_claim: Optional[str]
    ) -> CausalHypothesis:
        """Generate hypothesis for directional causation"""

        if direction == CausalDirection.A_CAUSES_B:
            source = correlation.source_architecture
            target = correlation.target_architecture
            hypothesis_template = f"Changes in {source} cause corresponding changes in {target}"
            mechanism_template = f"{source} produces outputs/events that {target} consumes/responds to"
        else:  # B_CAUSES_A
            source = correlation.target_architecture
            target = correlation.source_architecture
            hypothesis_template = f"Changes in {source} cause corresponding changes in {target}"
            mechanism_template = f"{source} produces outputs/events that {target} consumes/responds to"

        # Higher confidence if user suggested this direction
        confidence = 0.6 if user_claim else 0.4

        return CausalHypothesis(
            id=f"hyp_{direction.value}_{correlation.id}",
            correlation_id=correlation.id,
            source_architecture=source,
            target_architecture=target,
            causal_direction=direction.value,
            hypothesis=hypothesis_template,
            proposed_mechanism=mechanism_template,
            confidence=confidence,
            alternative_explanations=[
                "Reverse causation (other direction)",
                "Bidirectional causation (both affect each other)",
                "Confounding variable (both affected by third factor)",
                "Spurious correlation (coincidental)"
            ],
            validation_methods=[
                ValidationMethod.OBSERVATIONAL.value,
                ValidationMethod.TEMPORAL_ANALYSIS.value,
                ValidationMethod.INTERVENTION.value,
                ValidationMethod.MECHANISM_ANALYSIS.value
            ],
            validation_status="untested",
            exploratory=True
        )

    def _generate_bidirectional_hypothesis(
        self,
        correlation: CorrelationPattern,
        user_claim: Optional[str]
    ) -> CausalHypothesis:
        """Generate hypothesis for bidirectional causation (feedback loop)"""
        return CausalHypothesis(
            id=f"hyp_bidirectional_{correlation.id}",
            correlation_id=correlation.id,
            source_architecture=correlation.source_architecture,
            target_architecture=correlation.target_architecture,
            causal_direction=CausalDirection.BIDIRECTIONAL.value,
            hypothesis=f"{correlation.source_architecture} and {correlation.target_architecture} form a feedback loop where each affects the other",
            proposed_mechanism="Bidirectional coupling with feedback: changes in either system propagate to the other",
            confidence=0.3,  # Lower confidence - feedback loops are complex
            alternative_explanations=[
                "Unidirectional causation (only one direction)",
                "Independent systems with shared confounding factor",
                "Spurious correlation"
            ],
            validation_methods=[
                ValidationMethod.OBSERVATIONAL.value,
                ValidationMethod.EXPERIMENTAL.value,
                ValidationMethod.MECHANISM_ANALYSIS.value
            ],
            validation_status="untested",
            exploratory=True
        )

    def _generate_spurious_hypothesis(
        self,
        correlation: CorrelationPattern
    ) -> CausalHypothesis:
        """Generate hypothesis that correlation is spurious (no causation)"""
        return CausalHypothesis(
            id=f"hyp_spurious_{correlation.id}",
            correlation_id=correlation.id,
            source_architecture=correlation.source_architecture,
            target_architecture=correlation.target_architecture,
            causal_direction=CausalDirection.NO_CAUSATION.value,
            hypothesis=f"Correlation between {correlation.source_architecture} and {correlation.target_architecture} is spurious - no causal mechanism",
            proposed_mechanism="No causal mechanism. Systems may be correlated due to: shared external factor, coincidental timing, or selection bias",
            confidence=0.3,
            alternative_explanations=[
                "Hidden causal mechanism not yet discovered",
                "Indirect causation through intermediate system",
                "Confounding variable causing both"
            ],
            validation_methods=[
                ValidationMethod.MECHANISM_ANALYSIS.value,
                ValidationMethod.COUNTERFACTUAL.value
            ],
            validation_status="untested",
            exploratory=True
        )

    def design_validation_experiment(
        self,
        hypothesis: CausalHypothesis
    ) -> Dict[str, Any]:
        """
        Design an experiment/analysis to test a causal hypothesis

        Returns a validation plan that can be executed to test the hypothesis
        """
        validation_plan = {
            "hypothesis_id": hypothesis.id,
            "hypothesis": hypothesis.hypothesis,
            "objective": f"Determine if causal relationship exists: {hypothesis.causal_direction}",
            "validation_methods": [],
            "success_criteria": {},
            "expected_timeline": "TBD",
            "resources_needed": []
        }

        # Add validation methods based on hypothesis
        for method in hypothesis.validation_methods:
            if method == ValidationMethod.OBSERVATIONAL.value:
                validation_plan["validation_methods"].append({
                    "method": "Observational Study",
                    "description": "Monitor both systems in production and collect correlation metrics",
                    "steps": [
                        f"Instrument {hypothesis.source_architecture} to collect state/event data",
                        f"Instrument {hypothesis.target_architecture} to collect state/event data",
                        "Collect time-series data for both systems",
                        "Perform correlation analysis with time lag analysis",
                        "Check if source changes precede target changes"
                    ],
                    "success_criteria": "Strong temporal correlation with source preceding target by consistent time lag"
                })

            elif method == ValidationMethod.EXPERIMENTAL.value:
                validation_plan["validation_methods"].append({
                    "method": "Controlled Experiment",
                    "description": "Deliberately modify source system and observe effect on target",
                    "steps": [
                        f"Establish baseline behavior of both {hypothesis.source_architecture} and {hypothesis.target_architecture}",
                        f"Introduce controlled change to {hypothesis.source_architecture}",
                        f"Monitor {hypothesis.target_architecture} for corresponding changes",
                        "Repeat with different modifications to establish pattern",
                        "Compare with control period (no modifications)"
                    ],
                    "success_criteria": "Target system changes consistently following source modifications",
                    "warning": "⚠️ May disrupt production systems - use test environment"
                })

            elif method == ValidationMethod.INTERVENTION.value:
                validation_plan["validation_methods"].append({
                    "method": "Intervention Test",
                    "description": "Block or modify the proposed causal pathway and check if effect disappears",
                    "steps": [
                        "Identify the proposed causal mechanism (interface, event, data flow)",
                        "Create test environment where causal pathway can be controlled",
                        f"Block/modify pathway from {hypothesis.source_architecture} to {hypothesis.target_architecture}",
                        "Observe if correlation disappears",
                        "Restore pathway and observe if correlation returns"
                    ],
                    "success_criteria": "Correlation disappears when pathway is blocked, returns when restored"
                })

            elif method == ValidationMethod.MECHANISM_ANALYSIS.value:
                validation_plan["validation_methods"].append({
                    "method": "Mechanism Analysis",
                    "description": "Identify and trace the causal mechanism",
                    "steps": [
                        f"Map all connections from {hypothesis.source_architecture} to {hypothesis.target_architecture}",
                        "Identify interfaces, events, shared resources",
                        "Trace data/control flow through the connection",
                        "Document the mechanism by which changes propagate",
                        "Verify mechanism with code review and architecture diagrams"
                    ],
                    "success_criteria": "Clear causal pathway identified with documented mechanism"
                })

            elif method == ValidationMethod.TEMPORAL_ANALYSIS.value:
                validation_plan["validation_methods"].append({
                    "method": "Temporal Analysis",
                    "description": "Verify that cause precedes effect (necessary for causation)",
                    "steps": [
                        "Collect timestamped events from both systems",
                        "Analyze temporal ordering of changes",
                        "Check if source changes consistently precede target changes",
                        "Measure time lag between cause and effect",
                        "Rule out reverse causation"
                    ],
                    "success_criteria": "Source changes consistently precede target changes by measureable time lag"
                })

            elif method == ValidationMethod.COUNTERFACTUAL.value:
                validation_plan["validation_methods"].append({
                    "method": "Counterfactual Analysis",
                    "description": "Ask: 'What if the source didn't exist? Would target still behave this way?'",
                    "steps": [
                        f"Create scenario where {hypothesis.source_architecture} is removed/disabled",
                        f"Observe {hypothesis.target_architecture} behavior",
                        "Compare with normal behavior when source is present",
                        "If behavior changes significantly, supports causation",
                        "If behavior unchanged, suggests spurious correlation"
                    ],
                    "success_criteria": "Target behavior significantly different when source is absent"
                })

        return validation_plan

    def generate_disclaimer(
        self,
        relationship_type: RelationshipType
    ) -> str:
        """Generate appropriate disclaimer for relationship type"""

        if relationship_type == RelationshipType.CORRELATION:
            return """
⚠️  CORRELATION DISCLAIMER ⚠️

The relationship described below is an OBSERVED CORRELATION.
Correlation DOES NOT imply causation.

Possible explanations:
• One system causes changes in the other (directional causation)
• Both systems affect each other (bidirectional causation)
• Both are affected by a third factor (confounding variable)
• The correlation is coincidental (spurious correlation)

This correlation is worth exploring, but requires validation to establish
whether a causal relationship exists.
"""

        elif relationship_type == RelationshipType.CAUSAL_HYPOTHESIS:
            return """
⚠️  CAUSAL HYPOTHESIS DISCLAIMER ⚠️

The relationship described below is a HYPOTHESIS about causation.
This is a PROPOSED causal link that has NOT been validated.

This hypothesis:
• Is based on observed correlation
• Proposes a mechanism for how causation might work
• Requires testing and validation
• May be refuted by evidence
• Should be treated as exploratory until validated

Do NOT assume this is a proven causal relationship.
"""

        elif relationship_type == RelationshipType.VALIDATED_CAUSAL:
            return """
✓ VALIDATED CAUSAL RELATIONSHIP

The relationship described below is a VALIDATED causal link.
Evidence supports that changes in the source system cause
corresponding changes in the target system.

Validation includes:
• Demonstrated causal mechanism
• Temporal ordering verified (cause precedes effect)
• Experimental validation (where applicable)
• Alternative explanations ruled out

This can be used for system design and integration decisions.
"""

        elif relationship_type == RelationshipType.SPURIOUS:
            return """
❌ SPURIOUS CORRELATION

The relationship described below is a SPURIOUS correlation.
The systems appear correlated but investigation shows NO causal connection.

This is documented to:
• Prevent false assumptions
• Record negative findings
• Guide future analysis
• Help others avoid the same mistake

Do NOT link these systems based on this correlation.
"""

        return "Unknown relationship type"

    def generate_causality_report(
        self,
        correlations: List[CorrelationPattern],
        hypotheses: List[CausalHypothesis]
    ) -> str:
        """Generate comprehensive report on correlation vs causation analysis"""

        report = []
        report.append("="*70)
        report.append("CORRELATION VS. CAUSATION ANALYSIS REPORT")
        report.append("="*70)
        report.append("")
        report.append("⚠️  FUNDAMENTAL PRINCIPLE ⚠️")
        report.append("-"*70)
        report.append("CORRELATION ≠ CAUSATION")
        report.append("")
        report.append("Just because two systems appear related does NOT mean:")
        report.append("• One causes the other")
        report.append("• They should be linked in the architecture")
        report.append("• Changes in one will affect the other")
        report.append("")
        report.append("However, observed correlations ARE worth exploring scientifically")
        report.append("to determine if actual causal relationships exist.")
        report.append("="*70)
        report.append("")

        # Report correlations
        report.append(f"OBSERVED CORRELATIONS: {len(correlations)}")
        report.append("-"*70)
        for i, corr in enumerate(correlations, 1):
            report.append(f"\n{i}. {corr.source_architecture} ↔ {corr.target_architecture}")
            report.append(f"   Pattern: {corr.pattern_description}")
            report.append(f"   Strength: {corr.correlation_strength:.0%}")
            report.append(f"   Observed by: {corr.observed_by}")
            report.append(f"   Evidence:")
            for evidence in corr.evidence:
                report.append(f"     • {evidence}")
        report.append("")

        # Report hypotheses
        report.append(f"\nCAUSAL HYPOTHESES: {len(hypotheses)}")
        report.append("-"*70)
        report.append("These are PROPOSED causal relationships that require validation.")
        report.append("")

        for i, hyp in enumerate(hypotheses, 1):
            report.append(f"\n{i}. Hypothesis: {hyp.causal_direction}")
            report.append(f"   {hyp.hypothesis}")
            report.append(f"   Confidence: {hyp.confidence:.0%}")
            report.append(f"   Proposed Mechanism: {hyp.proposed_mechanism}")
            report.append(f"   Validation Status: {hyp.validation_status}")
            report.append(f"   Alternative Explanations:")
            for alt in hyp.alternative_explanations:
                report.append(f"     • {alt}")
        report.append("")

        # Next steps
        report.append("\n" + "="*70)
        report.append("RECOMMENDED NEXT STEPS")
        report.append("="*70)
        report.append("1. Review all correlations and hypotheses")
        report.append("2. Select hypotheses to test based on:")
        report.append("   • Importance to system integration")
        report.append("   • Ease of validation")
        report.append("   • User confidence in the relationship")
        report.append("3. Design validation experiments (see validation plans)")
        report.append("4. Execute validation studies")
        report.append("5. Update relationship status based on evidence")
        report.append("6. Only link architectures based on VALIDATED causal relationships")
        report.append("")
        report.append("⚠️  CRITICAL: Do not assume causation from correlation alone!")
        report.append("")

        return "\n".join(report)


def main():
    """Demo of causality analysis"""

    # Example architectures
    arch1 = {
        "name": "User Authentication System",
        "domain": "software",
        "framework": "microservices",
        "components": [
            {"name": "Login Service", "type": "service"},
            {"name": "Token Generator", "type": "service"},
            {"name": "Session Manager", "type": "service"}
        ]
    }

    arch2 = {
        "name": "Logging System",
        "domain": "software",
        "framework": "microservices",
        "components": [
            {"name": "Log Collector", "type": "service"},
            {"name": "Log Processor", "type": "service"},
            {"name": "Log Storage", "type": "service"}
        ]
    }

    analyzer = CausalityAnalyzer()

    # User observes correlation
    print("Scenario: User observes that logging system activity increases when")
    print("authentication system has more traffic.\n")

    # Detect correlation
    correlations = analyzer.detect_correlation(
        arch1,
        arch2,
        user_observation="Logging system activity increases when authentication system has high traffic"
    )

    print(f"Detected {len(correlations)} correlation(s)\n")

    # Generate causal hypotheses
    for corr in correlations:
        hypotheses = analyzer.generate_causal_hypotheses(
            corr,
            user_causal_claim="Authentication events cause logging activity"
        )

        print(f"Generated {len(hypotheses)} hypotheses for this correlation\n")

        # Generate validation plan for most likely hypothesis
        best_hypothesis = max(hypotheses, key=lambda h: h.confidence)
        validation_plan = analyzer.design_validation_experiment(best_hypothesis)

        print("Validation Plan for Most Likely Hypothesis:")
        print(json.dumps(validation_plan, indent=2))
        print()

    # Generate report
    report = analyzer.generate_causality_report(
        analyzer.correlations,
        analyzer.hypotheses
    )
    print("\n" + report)


if __name__ == '__main__':
    main()
