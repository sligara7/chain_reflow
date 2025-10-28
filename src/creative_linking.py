#!/usr/bin/env python3
"""
Creative Linking Module for Chain Reflow

This module handles the discovery of connections between seemingly orthogonal architectures
using synesthetic mapping, cross-sensory metaphors, and neural plasticity-inspired approaches.

IMPORTANT: Creative links are EXPLORATORY in nature and should be marked as such.
They represent potential connections that may require validation or refinement.
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum


class LinkType(Enum):
    """Types of links between architectures"""
    DIRECT = "direct"  # Clear technical interface
    ANALOGICAL = "analogical"  # Same pattern, different domain
    SYNESTHETIC = "synesthetic"  # Cross-domain metaphorical mapping
    EMERGENT = "emergent"  # Connection only makes sense at system-of-systems level
    EXPLORATORY = "exploratory"  # Speculative connection requiring validation


class OrthogonalityLevel(Enum):
    """How orthogonal/unrelated two architectures appear"""
    ALIGNED = "aligned"  # Same domain, clear connections
    RELATED = "related"  # Different domains, some overlap
    DIVERGENT = "divergent"  # Different domains, minimal overlap
    ORTHOGONAL = "orthogonal"  # Completely different domains, no apparent connection


@dataclass
class CreativeTouchpoint:
    """Represents a creative/exploratory link between architectures"""
    id: str
    source_architecture: str
    target_architecture: str
    source_component: str
    target_component: str
    link_type: str
    metaphor: str
    reasoning: str
    confidence: float  # 0.0 to 1.0
    exploratory: bool
    validation_needed: bool
    proposed_interface: Optional[Dict[str, Any]] = None

    def to_dict(self):
        return asdict(self)


@dataclass
class SynestheticMapping:
    """
    Represents a cross-domain mapping similar to synesthesia
    Maps concepts/properties from one domain to another
    """
    source_domain: str
    target_domain: str
    source_property: str
    target_property: str
    metaphor: str
    examples: List[str]

    def to_dict(self):
        return asdict(self)


class CreativeLinkingEngine:
    """
    Engine for discovering creative links between orthogonal architectures

    Inspired by:
    - Synesthesia: Cross-sensory/domain mappings
    - Neural plasticity: Growing new connections
    - Metaphorical reasoning: Finding deep structural similarities
    """

    def __init__(self):
        self.synesthetic_mappings = self._init_synesthetic_mappings()
        self.domain_metaphors = self._init_domain_metaphors()

    def _init_synesthetic_mappings(self) -> List[SynestheticMapping]:
        """Initialize common cross-domain mappings"""
        return [
            SynestheticMapping(
                source_domain="biological",
                target_domain="software",
                source_property="signal_transduction",
                target_property="event_propagation",
                metaphor="Biological signals are like software events - both carry information and trigger responses",
                examples=[
                    "Hormone receptor → Event listener",
                    "Signal cascade → Event chain",
                    "Cellular response → Event handler"
                ]
            ),
            SynestheticMapping(
                source_domain="biological",
                target_domain="software",
                source_property="metabolism",
                target_property="resource_processing",
                metaphor="Metabolism is like data processing - both transform inputs to outputs with energy/compute cost",
                examples=[
                    "Enzyme → Function/method",
                    "Metabolic pathway → Processing pipeline",
                    "ATP → Computational resource"
                ]
            ),
            SynestheticMapping(
                source_domain="mechanical",
                target_domain="software",
                source_property="force_transmission",
                target_property="data_flow",
                metaphor="Force transmission is like data flow - both transfer 'something' from source to sink",
                examples=[
                    "Axle torque → Data throughput",
                    "Gear ratio → Data transformation",
                    "Bearing → Connection point"
                ]
            ),
            SynestheticMapping(
                source_domain="social",
                target_domain="software",
                source_property="communication",
                target_property="messaging",
                metaphor="Social communication is like message passing - both involve information exchange between entities",
                examples=[
                    "Conversation → RPC call",
                    "Broadcast → Pub/sub event",
                    "Whisper network → Gossip protocol"
                ]
            ),
            SynestheticMapping(
                source_domain="ecological",
                target_domain="software",
                source_property="resource_flow",
                target_property="data_pipeline",
                metaphor="Ecological resource flow is like data pipelines - both move resources through a network",
                examples=[
                    "Energy flow → Data stream",
                    "Nutrient cycle → Data lifecycle",
                    "Food web → Dependency graph"
                ]
            ),
            SynestheticMapping(
                source_domain="mechanical",
                target_domain="biological",
                source_property="structural_connection",
                target_property="tissue_interface",
                metaphor="Mechanical joints are like tissue interfaces - both connect different components while allowing specific interactions",
                examples=[
                    "Bolt pattern → Receptor binding site",
                    "Bearing surface → Cell membrane interface",
                    "Torque transfer → Force transduction"
                ]
            )
        ]

    def _init_domain_metaphors(self) -> Dict[str, Dict[str, str]]:
        """Initialize high-level domain metaphors"""
        return {
            "software": {
                "essence": "information processing and transformation",
                "units": "data, functions, services",
                "connections": "APIs, events, messages",
                "dynamics": "execution, state changes, data flow"
            },
            "biological": {
                "essence": "chemical processing and regulation",
                "units": "molecules, cells, organisms",
                "connections": "binding, signaling, physical contact",
                "dynamics": "reactions, growth, adaptation"
            },
            "mechanical": {
                "essence": "force transmission and motion",
                "units": "parts, assemblies, machines",
                "connections": "joints, bearings, interfaces",
                "dynamics": "rotation, translation, deformation"
            },
            "social": {
                "essence": "information exchange and coordination",
                "units": "agents, groups, organizations",
                "connections": "relationships, communication, influence",
                "dynamics": "interaction, emergence, evolution"
            },
            "ecological": {
                "essence": "energy and matter flow",
                "units": "species, populations, ecosystems",
                "connections": "predation, competition, symbiosis",
                "dynamics": "flow, cycles, succession"
            }
        }

    def assess_orthogonality(
        self,
        arch1: Dict[str, Any],
        arch2: Dict[str, Any]
    ) -> Tuple[OrthogonalityLevel, str]:
        """
        Assess how orthogonal/unrelated two architectures are

        Returns:
            Tuple of (OrthogonalityLevel, reasoning)
        """
        # Extract domain information
        domain1 = arch1.get('domain', 'unknown')
        domain2 = arch2.get('domain', 'unknown')

        framework1 = arch1.get('framework', 'unknown')
        framework2 = arch2.get('framework', 'unknown')

        # Check for obvious alignment
        if domain1 == domain2 and framework1 == framework2:
            return (
                OrthogonalityLevel.ALIGNED,
                f"Same domain ({domain1}) and framework ({framework1})"
            )

        # Check for same framework, different domains
        if framework1 == framework2 and domain1 != domain2:
            return (
                OrthogonalityLevel.RELATED,
                f"Same framework ({framework1}) but different domains ({domain1} vs {domain2})"
            )

        # Check for completely different frameworks and domains
        if framework1 != framework2 and domain1 != domain2:
            # Check if domains have known mappings
            has_mapping = any(
                (m.source_domain == domain1 and m.target_domain == domain2) or
                (m.source_domain == domain2 and m.target_domain == domain1)
                for m in self.synesthetic_mappings
            )

            if has_mapping:
                return (
                    OrthogonalityLevel.DIVERGENT,
                    f"Different frameworks ({framework1} vs {framework2}) and domains ({domain1} vs {domain2}), but synesthetic mappings exist"
                )
            else:
                return (
                    OrthogonalityLevel.ORTHOGONAL,
                    f"Completely orthogonal: different frameworks ({framework1} vs {framework2}) and domains ({domain1} vs {domain2}) with no known mappings"
                )

        # Default to divergent
        return (
            OrthogonalityLevel.DIVERGENT,
            f"Architectures are divergent: frameworks ({framework1} vs {framework2}), domains ({domain1} vs {domain2})"
        )

    def find_creative_touchpoints(
        self,
        arch1: Dict[str, Any],
        arch2: Dict[str, Any],
        user_consent: bool = False,
        user_context: Optional[str] = None
    ) -> List[CreativeTouchpoint]:
        """
        Find creative/exploratory touchpoints between architectures

        Args:
            arch1: First architecture
            arch2: Second architecture
            user_consent: User has consented to creative linking
            user_context: User's description of how they think systems relate

        Returns:
            List of creative touchpoints
        """
        if not user_consent:
            raise ValueError(
                "Creative linking requires explicit user consent. "
                "This is an exploratory technique that generates speculative connections."
            )

        touchpoints = []

        # Assess orthogonality
        orthogonality, reasoning = self.assess_orthogonality(arch1, arch2)

        # Only proceed with creative linking if divergent or orthogonal
        if orthogonality in [OrthogonalityLevel.ALIGNED, OrthogonalityLevel.RELATED]:
            return []  # Use standard linking for these cases

        # Extract components
        components1 = arch1.get('components', [])
        components2 = arch2.get('components', [])

        domain1 = arch1.get('domain', 'unknown')
        domain2 = arch2.get('domain', 'unknown')

        # Find applicable synesthetic mappings
        applicable_mappings = [
            m for m in self.synesthetic_mappings
            if (m.source_domain == domain1 and m.target_domain == domain2) or
               (m.source_domain == domain2 and m.target_domain == domain1)
        ]

        # Generate creative touchpoints using synesthetic mappings
        for mapping in applicable_mappings:
            for comp1 in components1:
                for comp2 in components2:
                    # Check if component properties align with mapping
                    if self._components_match_mapping(comp1, comp2, mapping):
                        touchpoint = self._create_synesthetic_touchpoint(
                            arch1['name'], arch2['name'],
                            comp1, comp2, mapping,
                            orthogonality
                        )
                        touchpoints.append(touchpoint)

        # If user provided context, try to find touchpoints based on that
        if user_context:
            user_touchpoints = self._extract_user_suggested_links(
                arch1, arch2, user_context, orthogonality
            )
            touchpoints.extend(user_touchpoints)

        # Apply neural plasticity-inspired discovery
        # (look for structural similarities even without domain mapping)
        structural_touchpoints = self._find_structural_analogies(
            arch1, arch2, orthogonality
        )
        touchpoints.extend(structural_touchpoints)

        return touchpoints

    def _components_match_mapping(
        self,
        comp1: Dict[str, Any],
        comp2: Dict[str, Any],
        mapping: SynestheticMapping
    ) -> bool:
        """Check if two components match a synesthetic mapping"""
        # Simple heuristic: check if component descriptions or types
        # contain keywords from the mapping
        comp1_text = (
            comp1.get('name', '') + ' ' +
            comp1.get('description', '') + ' ' +
            comp1.get('type', '')
        ).lower()

        comp2_text = (
            comp2.get('name', '') + ' ' +
            comp2.get('description', '') + ' ' +
            comp2.get('type', '')
        ).lower()

        # Check for property keywords
        source_keywords = mapping.source_property.replace('_', ' ').split()
        target_keywords = mapping.target_property.replace('_', ' ').split()

        source_match = any(kw in comp1_text for kw in source_keywords)
        target_match = any(kw in comp2_text for kw in target_keywords)

        return source_match and target_match

    def _create_synesthetic_touchpoint(
        self,
        arch1_name: str,
        arch2_name: str,
        comp1: Dict[str, Any],
        comp2: Dict[str, Any],
        mapping: SynestheticMapping,
        orthogonality: OrthogonalityLevel
    ) -> CreativeTouchpoint:
        """Create a synesthetic touchpoint"""
        touchpoint_id = f"creative_{arch1_name}_{comp1['name']}_{arch2_name}_{comp2['name']}"

        # Confidence decreases with orthogonality
        confidence = {
            OrthogonalityLevel.DIVERGENT: 0.6,
            OrthogonalityLevel.ORTHOGONAL: 0.3
        }.get(orthogonality, 0.4)

        return CreativeTouchpoint(
            id=touchpoint_id.replace(' ', '_').replace('/', '_'),
            source_architecture=arch1_name,
            target_architecture=arch2_name,
            source_component=comp1['name'],
            target_component=comp2['name'],
            link_type=LinkType.SYNESTHETIC.value,
            metaphor=mapping.metaphor,
            reasoning=f"Cross-domain mapping: {mapping.source_property} → {mapping.target_property}. "
                     f"Components share structural similarity via synesthetic mapping.",
            confidence=confidence,
            exploratory=True,
            validation_needed=True,
            proposed_interface={
                "type": "synesthetic_mapping",
                "source_property": mapping.source_property,
                "target_property": mapping.target_property,
                "mapping_examples": mapping.examples
            }
        )

    def _extract_user_suggested_links(
        self,
        arch1: Dict[str, Any],
        arch2: Dict[str, Any],
        user_context: str,
        orthogonality: OrthogonalityLevel
    ) -> List[CreativeTouchpoint]:
        """
        Extract potential links based on user's description
        This is a simplified version - in practice, would use NLP/LLM
        """
        touchpoints = []

        # Look for explicit component mentions in user context
        components1 = arch1.get('components', [])
        components2 = arch2.get('components', [])

        user_context_lower = user_context.lower()

        for comp1 in components1:
            comp1_name_lower = comp1['name'].lower()
            if comp1_name_lower in user_context_lower:
                # User mentioned this component, look for related components in arch2
                for comp2 in components2:
                    comp2_name_lower = comp2['name'].lower()
                    if comp2_name_lower in user_context_lower:
                        # Both components mentioned by user
                        touchpoint_id = f"user_suggested_{arch1['name']}_{comp1['name']}_{arch2['name']}_{comp2['name']}"

                        touchpoints.append(CreativeTouchpoint(
                            id=touchpoint_id.replace(' ', '_').replace('/', '_'),
                            source_architecture=arch1['name'],
                            target_architecture=arch2['name'],
                            source_component=comp1['name'],
                            target_component=comp2['name'],
                            link_type=LinkType.EXPLORATORY.value,
                            metaphor="User-suggested connection",
                            reasoning=f"User indicated these components may be related: '{user_context}'",
                            confidence=0.7,  # Higher confidence since user suggested
                            exploratory=True,
                            validation_needed=True,
                            proposed_interface={
                                "type": "user_suggested",
                                "user_context": user_context
                            }
                        ))

        return touchpoints

    def _find_structural_analogies(
        self,
        arch1: Dict[str, Any],
        arch2: Dict[str, Any],
        orthogonality: OrthogonalityLevel
    ) -> List[CreativeTouchpoint]:
        """
        Find structural analogies between components
        Similar to neural plasticity - growing connections based on structural similarity
        """
        touchpoints = []

        components1 = arch1.get('components', [])
        components2 = arch2.get('components', [])

        # Look for structural patterns:
        # - Both have inputs and outputs
        # - Both transform something
        # - Both serve as intermediaries
        # - Both are endpoints

        for comp1 in components1:
            for comp2 in components2:
                structural_similarity = self._compute_structural_similarity(comp1, comp2)

                if structural_similarity > 0.5:  # Threshold for considering a connection
                    touchpoint_id = f"structural_{arch1['name']}_{comp1['name']}_{arch2['name']}_{comp2['name']}"

                    touchpoints.append(CreativeTouchpoint(
                        id=touchpoint_id.replace(' ', '_').replace('/', '_'),
                        source_architecture=arch1['name'],
                        target_architecture=arch2['name'],
                        source_component=comp1['name'],
                        target_component=comp2['name'],
                        link_type=LinkType.ANALOGICAL.value,
                        metaphor="Structural analogy - components play similar roles in their respective systems",
                        reasoning=f"Components share structural similarity (score: {structural_similarity:.2f}). "
                                f"Both appear to serve analogous functions in their architectures.",
                        confidence=structural_similarity * 0.6,  # Scale down for exploratory nature
                        exploratory=True,
                        validation_needed=True,
                        proposed_interface={
                            "type": "structural_analogy",
                            "similarity_score": structural_similarity
                        }
                    ))

        return touchpoints

    def _compute_structural_similarity(
        self,
        comp1: Dict[str, Any],
        comp2: Dict[str, Any]
    ) -> float:
        """
        Compute structural similarity between components
        Returns score from 0.0 to 1.0
        """
        score = 0.0

        # Check if both have inputs
        has_inputs_1 = 'inputs' in comp1 or 'input' in comp1.get('name', '').lower()
        has_inputs_2 = 'inputs' in comp2 or 'input' in comp2.get('name', '').lower()
        if has_inputs_1 and has_inputs_2:
            score += 0.2

        # Check if both have outputs
        has_outputs_1 = 'outputs' in comp1 or 'output' in comp1.get('name', '').lower()
        has_outputs_2 = 'outputs' in comp2 or 'output' in comp2.get('name', '').lower()
        if has_outputs_1 and has_outputs_2:
            score += 0.2

        # Check if both are transformers (have both inputs and outputs)
        if (has_inputs_1 and has_outputs_1) and (has_inputs_2 and has_outputs_2):
            score += 0.3

        # Check for similar position in architecture (e.g., both are central/hub-like)
        # This would require graph analysis in a full implementation
        # For now, just a placeholder

        # Check for semantic similarity in descriptions
        desc1 = comp1.get('description', '').lower()
        desc2 = comp2.get('description', '').lower()

        # Simple keyword overlap
        if desc1 and desc2:
            words1 = set(desc1.split())
            words2 = set(desc2.split())
            overlap = len(words1 & words2) / max(len(words1), len(words2), 1)
            score += overlap * 0.3

        return min(score, 1.0)

    def generate_linking_report(
        self,
        touchpoints: List[CreativeTouchpoint],
        arch1_name: str,
        arch2_name: str,
        orthogonality: OrthogonalityLevel
    ) -> str:
        """Generate a human-readable report of creative links"""
        report = []
        report.append("="*70)
        report.append("CREATIVE LINKING REPORT")
        report.append("="*70)
        report.append("")
        report.append(f"Architecture 1: {arch1_name}")
        report.append(f"Architecture 2: {arch2_name}")
        report.append(f"Orthogonality Level: {orthogonality.value}")
        report.append("")
        report.append("⚠️  IMPORTANT DISCLAIMER ⚠️")
        report.append("-"*70)
        report.append("The connections below are EXPLORATORY and SPECULATIVE in nature.")
        report.append("They represent potential metaphorical or analogical links between")
        report.append("architectures that appear orthogonal (unrelated). These connections")
        report.append("require validation and may not represent actual technical interfaces.")
        report.append("")
        report.append("Think of these as hypotheses or creative insights rather than")
        report.append("established facts. They may help spark ideas for how to bridge")
        report.append("seemingly unrelated systems.")
        report.append("="*70)
        report.append("")

        if not touchpoints:
            report.append("No creative touchpoints discovered.")
            report.append("The architectures may be too orthogonal for automatic discovery.")
            report.append("Consider providing more context about how you envision them connecting.")
            return "\n".join(report)

        report.append(f"Discovered {len(touchpoints)} creative touchpoint(s):")
        report.append("")

        for i, tp in enumerate(touchpoints, 1):
            report.append(f"{i}. {tp.source_component} ↔ {tp.target_component}")
            report.append(f"   Link Type: {tp.link_type}")
            report.append(f"   Confidence: {tp.confidence:.0%}")
            report.append(f"   Metaphor: {tp.metaphor}")
            report.append(f"   Reasoning: {tp.reasoning}")
            if tp.proposed_interface:
                report.append(f"   Proposed Interface: {tp.proposed_interface.get('type', 'N/A')}")
            report.append("")

        report.append("="*70)
        report.append("NEXT STEPS")
        report.append("="*70)
        report.append("1. Review each touchpoint and assess validity")
        report.append("2. Refine metaphors based on domain expertise")
        report.append("3. Design concrete interfaces for validated connections")
        report.append("4. Mark accepted connections in system_of_systems_graph.json")
        report.append("5. Document the creative linking rationale for future reference")
        report.append("")

        return "\n".join(report)


def main():
    """Demo of creative linking"""
    # Example: Linking a mechanical system with a software system
    arch1 = {
        "name": "Axle System",
        "domain": "mechanical",
        "framework": "mechanical_engineering",
        "components": [
            {"name": "Drive Shaft", "type": "power_transmission", "description": "Transmits torque from drivetrain"},
            {"name": "Bearing Assembly", "type": "support", "description": "Supports rotating shaft"},
            {"name": "Wheel Mount", "type": "connection", "description": "Connects to wheel hub"}
        ]
    }

    arch2 = {
        "name": "Event Processing System",
        "domain": "software",
        "framework": "microservices",
        "components": [
            {"name": "Event Bus", "type": "messaging", "description": "Distributes events to subscribers"},
            {"name": "Event Handler", "type": "processor", "description": "Processes incoming events"},
            {"name": "Event Store", "type": "storage", "description": "Persists event history"}
        ]
    }

    engine = CreativeLinkingEngine()

    # Assess orthogonality
    orthogonality, reasoning = engine.assess_orthogonality(arch1, arch2)
    print(f"Orthogonality: {orthogonality.value}")
    print(f"Reasoning: {reasoning}\n")

    # Find creative touchpoints (with user consent)
    touchpoints = engine.find_creative_touchpoints(
        arch1, arch2,
        user_consent=True,
        user_context="The drive shaft distributes power like the event bus distributes events"
    )

    # Generate report
    report = engine.generate_linking_report(
        touchpoints, arch1['name'], arch2['name'], orthogonality
    )
    print(report)


if __name__ == '__main__':
    main()
