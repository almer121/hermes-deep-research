"""End-to-end research pipeline orchestration."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List

from .extractor import Evidence, extract_evidence
from .planner import ResearchPlan, build_plan
from .reporter import render_report
from .searcher import OfflineCorpusSearcher, SearchProvider, SearchResult, default_corpus
from .synthesizer import Synthesis, synthesize


@dataclass
class PipelineRun:
    plan: ResearchPlan
    results: List[SearchResult]
    evidence: List[Evidence]
    synthesis: Synthesis
    report: str


def run_pipeline(query: str, searcher: SearchProvider | None = None) -> PipelineRun:
    plan = build_plan(query)

    provider: SearchProvider = searcher or OfflineCorpusSearcher(default_corpus())

    aggregated: List[SearchResult] = []
    seen_urls: set[str] = set()
    for question in plan.sub_questions:
        for result in provider.search(question, limit=3):
            if result.url in seen_urls:
                continue
            seen_urls.add(result.url)
            aggregated.append(result)

    evidence = extract_evidence(aggregated)
    synthesis = synthesize(plan, evidence)
    report = render_report(plan, synthesis)

    return PipelineRun(
        plan=plan,
        results=aggregated,
        evidence=evidence,
        synthesis=synthesis,
        report=report,
    )
