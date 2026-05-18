"""Markdown report rendering."""

from __future__ import annotations

from typing import List

from .citer import Citation, collect_citations, renumber_bullet
from .planner import ResearchPlan
from .synthesizer import Synthesis


def render_report(plan: ResearchPlan, synthesis: Synthesis) -> str:
    citations = collect_citations(synthesis)
    mapping = {c.evidence_id: c.number for c in citations}

    lines: List[str] = []
    lines.append(f"# Research Report: {plan.query}")
    lines.append("")
    lines.append("## Plan")
    lines.append("")
    for question in plan.sub_questions:
        lines.append(f"- {question}")
    lines.append("")

    if synthesis.sections:
        lines.append("## Findings")
        lines.append("")
        for section in synthesis.sections:
            lines.append(f"### {section.heading}")
            lines.append("")
            for bullet in section.bullets:
                lines.append(f"- {renumber_bullet(bullet, mapping)}")
            lines.append("")
    else:
        lines.append("## Findings")
        lines.append("")
        lines.append("No findings produced. Search returned no usable evidence.")
        lines.append("")

    if citations:
        lines.append("## Sources")
        lines.append("")
        for citation in citations:
            lines.append(f"[{citation.number}] {citation.title} — {citation.url}")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"
