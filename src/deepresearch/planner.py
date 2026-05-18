"""Query decomposition planner.

The planner takes a single research question and breaks it into a small set
of focused sub-questions that can be researched independently and recombined.
This mirrors the planning stage used by OpenAI Deep Research and similar
agentic systems.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List


@dataclass
class ResearchPlan:
    """A structured research plan derived from a user query."""

    query: str
    angles: List[str] = field(default_factory=list)
    sub_questions: List[str] = field(default_factory=list)
    expected_sources: List[str] = field(default_factory=list)

    def is_actionable(self) -> bool:
        return bool(self.sub_questions)


def _expand_angles(query: str) -> List[str]:
    """Generate analytical angles for a query.

    A real deployment would call a reasoning model. The deterministic
    fallback below produces stable, testable output for offline runs.
    """

    base_angles = [
        "definition and scope",
        "current state of the art",
        "leading approaches and trade-offs",
        "open challenges and recent advances",
        "practical adoption and tooling",
    ]
    q = query.strip()
    if not q:
        return []
    return [f"{q}: {angle}" for angle in base_angles]


def _angle_to_questions(angle: str) -> List[str]:
    seed = angle.lower()
    if "definition" in seed:
        return [f"What exactly is meant by '{angle}'?"]
    if "state of the art" in seed:
        return [f"What is the current state of the art for {angle}?"]
    if "approaches" in seed:
        return [
            f"What are the leading approaches for {angle}?",
            f"What are the main trade-offs between those approaches?",
        ]
    if "challenges" in seed:
        return [f"What are the open challenges and most recent advances for {angle}?"]
    if "adoption" in seed:
        return [
            f"Which tools, libraries, or platforms support {angle} today?",
            f"How are practitioners actually using {angle} in production?",
        ]
    return [f"What should a researcher know about {angle}?"]


def build_plan(query: str, max_questions: int = 8) -> ResearchPlan:
    """Decompose ``query`` into a bounded research plan.

    The plan caps total sub-questions at ``max_questions`` to keep token
    budget predictable. Empty or whitespace queries return an inert plan.
    """

    if not query or not query.strip():
        return ResearchPlan(query=query)

    angles = _expand_angles(query)
    questions: List[str] = []
    for angle in angles:
        for q in _angle_to_questions(angle):
            if q not in questions:
                questions.append(q)
            if len(questions) >= max_questions:
                break
        if len(questions) >= max_questions:
            break

    return ResearchPlan(
        query=query,
        angles=angles,
        sub_questions=questions,
        expected_sources=[
            "academic papers",
            "official documentation",
            "engineering blog posts",
            "benchmark reports",
        ],
    )
