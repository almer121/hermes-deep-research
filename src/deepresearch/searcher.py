"""Search abstraction.

The searcher is intentionally provider-agnostic. The default is a
deterministic offline corpus so the pipeline can be tested without network
access. A production deployment swaps the corpus for a real search API
(SerpAPI, Brave, Tavily, or a self-hosted index) by implementing
``SearchProvider``.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Protocol


@dataclass
class SearchResult:
    title: str
    url: str
    snippet: str
    source: str = "offline"


class SearchProvider(Protocol):
    def search(self, query: str, limit: int = 5) -> List[SearchResult]: ...


class OfflineCorpusSearcher:
    """A small in-memory corpus, used for tests and the demo run."""

    def __init__(self, corpus: Iterable[SearchResult]):
        self._corpus = list(corpus)

    def search(self, query: str, limit: int = 5) -> List[SearchResult]:
        if not query:
            return []
        terms = [t.lower() for t in query.split() if len(t) > 2]
        scored: List[tuple[int, SearchResult]] = []
        for item in self._corpus:
            haystack = f"{item.title} {item.snippet}".lower()
            score = sum(haystack.count(term) for term in terms)
            if score:
                scored.append((score, item))
        scored.sort(key=lambda pair: pair[0], reverse=True)
        return [item for _, item in scored[:limit]]


def default_corpus() -> List[SearchResult]:
    """Demo corpus covering the sample query used in the CLI walkthrough."""

    return [
        SearchResult(
            title="Mixture of Experts: A Practical Overview",
            url="https://example.org/papers/moe-overview",
            snippet=(
                "Mixture of Experts models route each token through a small "
                "subset of expert subnetworks, scaling parameter count "
                "without proportional compute cost."
            ),
        ),
        SearchResult(
            title="Switch Transformers benchmark report",
            url="https://example.org/benchmarks/switch-transformer",
            snippet=(
                "Switch Transformer demonstrates that sparse routing can "
                "match dense baselines at a fraction of the FLOPs while "
                "introducing routing instability challenges."
            ),
        ),
        SearchResult(
            title="DeepSeek MoE engineering blog",
            url="https://example.org/blog/deepseek-moe",
            snippet=(
                "DeepSeek MoE introduces fine-grained expert segmentation "
                "and shared experts to reduce redundancy and improve "
                "specialization across language and code domains."
            ),
        ),
        SearchResult(
            title="Routing collapse and load balancing in MoE",
            url="https://example.org/papers/routing-collapse",
            snippet=(
                "A common failure mode in mixture-of-experts training is "
                "routing collapse, where most tokens are routed to the same "
                "expert. Auxiliary load-balancing losses mitigate this."
            ),
        ),
        SearchResult(
            title="Open-source MoE tooling: Megablocks and Tutel",
            url="https://example.org/tools/moe-tooling",
            snippet=(
                "Megablocks and Tutel provide block-sparse kernels and "
                "communication primitives that make distributed MoE "
                "training tractable on modern GPU clusters."
            ),
        ),
        SearchResult(
            title="Practical adoption of MoE in production LLMs",
            url="https://example.org/reports/moe-production",
            snippet=(
                "Recent open-weight releases — including Mixtral and "
                "Qwen-MoE — show that mixture-of-experts has moved from "
                "research curiosity to standard production architecture."
            ),
        ),
    ]
