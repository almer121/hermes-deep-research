# Hermes Deep Research

[![tests](https://github.com/almer121/hermes-deep-research/actions/workflows/tests.yml/badge.svg)](https://github.com/almer121/hermes-deep-research/actions/workflows/tests.yml)
[![python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![license](https://img.shields.io/badge/license-MIT-green)](LICENSE)

Autonomous multi-stage research agent. Decompose a question into sub-questions, search across sources, extract typed evidence, synthesize findings, attach citations, render a markdown report. Built as a reference workflow for agentic research pipelines.

## Why deep research

Deep research is the most token-heavy and most architecture-heavy use case for modern reasoning models. A single query expands into dozens of sub-questions, each requiring independent search, evidence extraction, and synthesis. OpenAI Deep Research, Perplexity, and Manus all sit in this niche. The architectural pattern is the same: plan, search, extract, synthesize, cite, report. Hermes Deep Research implements that pattern as a small, testable, swappable Python pipeline.

## Pipeline

```text
query
  -> planner            decompose into sub-questions
  -> searcher           run each sub-question through a search provider
  -> extractor          pull typed evidence units from results
  -> synthesizer        merge evidence into sectioned findings
  -> citer              collect citations and renumber stably
  -> reporter           render a final markdown report
```

Each stage is a pure module under `src/deepresearch/`. The provider interface for search is a `Protocol`, so the offline corpus used in tests can be swapped for SerpAPI, Brave, Tavily, or a self-hosted index without touching the rest of the pipeline.

## Run locally

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -e .[dev]
pytest tests -v
deepresearch "mixture of experts language models" \
  --output examples/research-report.md \
  --verbose
```

Expected output (with `--verbose`):

```text
[plan] decomposing query: mixture of experts language models
[plan] 7 sub-questions generated
[search] mode: offline corpus
[search] querying: What exactly is meant by ...
[search] querying: What is the current state of the art for ...
[search] querying: What are the leading approaches for ...
[search] querying: What are the main trade-offs between those approaches?
[search] querying: What are the open challenges and most recent advances for ...
[search] querying: Which tools, libraries, or platforms support ...
[search] querying: How are practitioners actually using ...
[search] 6 unique sources collected
[extract] 6 evidence units
[synthesize] grouping evidence by analytical angle
[synthesize] 2 sections produced
[report] markdown rendered
Report written: examples/research-report.md (2370 bytes)
Sub-questions: 7
Sources collected: 6
Evidence units: 6
Elapsed: 0.9 ms (offline corpus, no LLM call)
```

A sample report is committed at `examples/research-report.md`.

## Project structure

```text
src/deepresearch/planner.py       query decomposition
src/deepresearch/searcher.py      search provider abstraction + offline corpus
src/deepresearch/extractor.py     typed evidence extraction
src/deepresearch/synthesizer.py   sectioned synthesis with evidence ids
src/deepresearch/citer.py         stable citation renumbering
src/deepresearch/reporter.py      markdown report rendering
src/deepresearch/pipeline.py      end-to-end orchestration
src/deepresearch/cli.py           command-line entry point
tests/                            unit and integration tests
examples/                         sample generated reports
```

## Roadmap

- Plug a real search provider (Brave or Tavily) behind the existing `SearchProvider` protocol.
- Add a fetcher stage that resolves URLs to full text and chunks them.
- Replace the heuristic synthesizer with a reasoning model under a strict token budget.
- Track per-run cost and per-claim confidence in the report.
- Add a one-command installer for other builders to run the same pipeline on their own queries.
