"""Synthesis stage.

The synthesizer merges evidence into a coherent narrative organized by
research angle. It deduplicates near-identical claims and tags every
sentence with one or more evidence ids so the citer can resolve them.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List

from .extractor import Evidence
from .planner import ResearchPlan


@dataclass
class SynthesizedSection:
    heading: str
    bullets: List[str] = field(default_factory=list)


@dataclass
class Synthesis:
    sections: List[SynthesizedSection] = field(default_factory=list)
    evidence_index: Dict[str, Evidence] = field(default_factory=dict)


def _match_evidence(angle: str, evidence: List[Evidence]) -> List[Evidence]:
    seed = angle.lower()
    matches: List[Evidence] = []
    for ev in evidence:
        haystack = f"{ev.claim} {ev.source_title}".lower()
        # Heuristic match: angle keyword overlap with evidence text.
        keywords = [w for w in seed.split() if len(w) > 3]
        if any(k in haystack for k in keywords):
            matches.append(ev)
    return matches or evidence[:2]


def synthesize(plan: ResearchPlan, evidence: List[Evidence]) -> Synthesis:
    if not plan.angles or not evidence:
        return Synthesis()

    evidence_index = {ev.id: ev for ev in evidence}
    sections: List[SynthesizedSection] = []
    seen_claims: set[str] = set()

    for angle in plan.angles:
        section = SynthesizedSection(heading=angle.split(":", 1)[-1].strip().title())
        matched = _match_evidence(angle, evidence)
        for ev in matched:
            key = ev.claim.lower()
            if key in seen_claims:
                continue
            seen_claims.add(key)
            section.bullets.append(f"{ev.claim} [{ev.id}]")
        if section.bullets:
            sections.append(section)

    return Synthesis(sections=sections, evidence_index=evidence_index)
