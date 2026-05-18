"""End-to-end research pipeline orchestration."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, List, Optional

from .extractor import Evidence, extract_evidence
from .planner import ResearchPlan, build_plan
from .reporter import render_report
from .searcher import OfflineCorpusSearcher, SearchProvider, SearchResult, default_corpus
from .synthesizer import Synthesis, synthesize


ProgressCallback = Callable[[str, str], None]


@dataclass
class PipelineRun:
    plan: ResearchPlan
    results: List[SearchResult]
    evidence: List[Evidence]
    synthesis: Synthesis
    report: str


def run_pipeline(
    query: str,
    searcher: SearchProvider | None = None,
    on_progress: Optional[ProgressCallback] = None,
) -> PipelineRun:
    def emit(stage: str, message: str) -> None:
        if on_progress is not None:
            on_progress(stage, message)

    emit("plan", f"decomposing query: {query}")
    plan = build_plan(query)
    emit("plan", f"{len(plan.sub_questions)} sub-questions generated")

    provider: SearchProvider = searcher or OfflineCorpusSearcher(default_corpus())
    mode = "offline corpus" if isinstance(provider, OfflineCorpusSearcher) else "external provider"
    emit("search", f"mode: {mode}")

    aggregated: List[SearchResult] = []
    seen_urls: set[str] = set()
    for question in plan.sub_questions:
        truncated = question if len(question) <= 70 else question[:67] + "..."
        emit("search", f"querying: {truncated}")
        for result in provider.search(question, limit=3):
            if result.url in seen_urls:
                continue
            seen_urls.add(result.url)
            aggregated.append(result)
    emit("search", f"{len(aggregated)} unique sources collected")

    evidence = extract_evidence(aggregated)
    emit("extract", f"{len(evidence)} evidence units")

    emit("synthesize", "grouping evidence by analytical angle")
    synthesis = synthesize(plan, evidence)
    emit("synthesize", f"{len(synthesis.sections)} sections produced")

    report = render_report(plan, synthesis)
    emit("report", "markdown rendered")

    return PipelineRun(
        plan=plan,
        results=aggregated,
        evidence=evidence,
        synthesis=synthesis,
        report=report,
    )
