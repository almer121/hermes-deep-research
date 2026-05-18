# Hermes Deep Research

Autonomous multi-stage research agent. Decompose a question into sub-questions, search across sources, extract typed evidence, synthesize findings, attach citations, render a markdown report. Built as a reference workflow for agentic research pipelines.

This repository is a working proof for an AI builder grant application. It demonstrates a real coding-agent workflow that turns one user question into a cited markdown research report, end to end, in under one minute on commodity hardware.

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
pip install pytest
PYTHONPATH=src:. python3 -m pytest tests -q
PYTHONPATH=src:. python3 -m deepresearch.cli \
  "mixture of experts language models" \
  --output proof/research-report.md
```

Expected output:

```text
Report written: proof/research-report.md
Sub-questions: 7
Sources collected: 6
Evidence units: 6
```

A sample report is committed at `proof/research-report.md`.

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
proof/                            generated proof artifacts
```

## Grant application positioning

This project is the proof artifact for the Xiaomi MiMo 100T Token Grant application. The grant funds a four-week production benchmark in which the reasoning and synthesis stages of this pipeline are migrated from a Claude/GPT mix to MiMo V2.5, with patch correctness, latency, and cost-per-resolved-question measured on a fixed query corpus. Results will be published openly in this repository.

- Agent tools: Hermes Agent (orchestrator), Claude Code, Codex, Cursor
- Model series: Claude, GPT, DeepSeek, Gemini, MiMo
- Proof: passing test suite, generated report, repository link, terminal screenshots

## Roadmap

- Plug a real search provider (Brave or Tavily) behind the existing `SearchProvider` protocol.
- Add a fetcher stage that resolves URLs to full text and chunks them.
- Replace the heuristic synthesizer with a reasoning model under a strict token budget.
- Track per-run cost and per-claim confidence in the report.
- Add a one-command installer for other builders to run the same pipeline on their own queries.
