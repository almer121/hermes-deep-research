"""Evidence extraction.

The extractor turns raw search results into typed evidence units that the
synthesizer can reason over. Each evidence unit keeps a stable id, a
source url, and a one-sentence claim derived from the snippet.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import List

from .searcher import SearchResult


@dataclass(frozen=True)
class Evidence:
    id: str
    claim: str
    source_url: str
    source_title: str


_SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+")


def _first_sentence(text: str) -> str:
    text = text.strip()
    if not text:
        return ""
    parts = _SENTENCE_SPLIT.split(text, maxsplit=1)
    return parts[0].strip()


def extract_evidence(results: List[SearchResult]) -> List[Evidence]:
    evidence: List[Evidence] = []
    for index, result in enumerate(results, start=1):
        claim = _first_sentence(result.snippet) or result.title
        evidence.append(
            Evidence(
                id=f"E{index:02d}",
                claim=claim,
                source_url=result.url,
                source_title=result.title,
            )
        )
    return evidence
