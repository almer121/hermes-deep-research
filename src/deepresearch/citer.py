"""Citation rendering.

The citer takes a synthesized output and produces a flat citation list
preserving the order in which evidence ids first appear. This ensures
citation numbering is stable across runs.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Dict, List

from .extractor import Evidence
from .synthesizer import Synthesis


_CITE_PATTERN = re.compile(r"\[(E\d+)\]")


@dataclass
class Citation:
    number: int
    evidence_id: str
    title: str
    url: str


def collect_citations(synthesis: Synthesis) -> List[Citation]:
    order: List[str] = []
    for section in synthesis.sections:
        for bullet in section.bullets:
            for match in _CITE_PATTERN.findall(bullet):
                if match not in order:
                    order.append(match)

    citations: List[Citation] = []
    for index, ev_id in enumerate(order, start=1):
        ev = synthesis.evidence_index.get(ev_id)
        if not ev:
            continue
        citations.append(
            Citation(
                number=index,
                evidence_id=ev_id,
                title=ev.source_title,
                url=ev.source_url,
            )
        )
    return citations


def renumber_bullet(bullet: str, mapping: Dict[str, int]) -> str:
    def replace(match: re.Match[str]) -> str:
        ev_id = match.group(1)
        if ev_id in mapping:
            return f"[{mapping[ev_id]}]"
        return match.group(0)

    return _CITE_PATTERN.sub(replace, bullet)
