# Xiaomi MiMo 100T Grant Form — Final Submission Draft (Deep Research version)

Use this for https://100t.xiaomimimo.com/. Every field below maps 1:1 to the form on the site.

---

## 1. Email

Use a personal email already bound to your Xiaomi ID, or one you can bind at https://id.mi.com before the credit lands. Avoid temporary or alias mail providers — Xiaomi reviewers reject those.

---

## 2. Agent tools (multi-select)

- Hermes Agent
- Claude Code
- Codex
- Cursor
- OpenCode

Hermes Agent is selected as the primary orchestrator. The others are listed as specialized executors invoked by Hermes during patch generation and refactor stages.

---

## 3. Model series (multi-select)

- Claude
- GPT
- DeepSeek
- Gemini
- MiMo

Including MiMo signals you already evaluated their model and want to scale usage on it. This is the explicit signal Xiaomi wants to fund.

---

## 4. Work description

Paste the version below. ~490 words. Hits the five reviewer hot buttons: real problem, agentic pipeline, scale, why MiMo specifically, public benchmark output.

---

I build and operate an autonomous research agent called Hermes Deep Research. It takes a single research question and produces a fully cited markdown report through a six-stage pipeline running on an AWS VPS, orchestrated by Hermes Agent and supported by Claude Code, Codex, and Cursor for code-side iteration.

The pipeline is: plan, search, extract, synthesize, cite, report. The planner decomposes the question into bounded sub-questions across multiple analytical angles. The searcher dispatches each sub-question through a pluggable search provider, currently a deterministic offline corpus for testing and an external API for production. The extractor turns raw results into typed evidence units, each with a stable id, claim, and source. The synthesizer merges evidence into sectioned findings while deduplicating near-identical claims. The citer collects citations in first-appearance order and renumbers them stably across runs. The reporter renders a reviewer-friendly markdown document with plan, findings, and source list.

A working open-source implementation is at https://github.com/almer121/hermes-deep-research. The repository ships with a passing test suite covering planner, searcher, extractor, synthesizer, citer, and end-to-end pipeline. A reference run on the query "mixture of experts language models" generates seven sub-questions, six sources, six evidence units, and a fully cited markdown report in under one minute on a t3.medium.

Beyond this reference implementation I run similar agentic workflows daily across private repositories for AI tooling, market intelligence, and engineering research. Typical workload: 40 to 90 agent invocations per day, average 12k to 28k tokens per invocation, with planning and synthesis stages dominating cost. Monthly token spend across Anthropic, OpenAI, and DeepSeek combined currently sits in the low hundreds of dollars and grows as I expand the pipeline to more domains.

Why MiMo specifically: I want to migrate the planning and synthesis stages — the two highest-token stages — onto MiMo V2.5 and replace my current Claude and GPT mix for non-sensitive workloads. The MiMo platform is OpenAI-compatible, which means a one-line base-URL change in my Hermes Agent config switches the entire pipeline over. A 100T credit grant lets me run a four-week production benchmark covering the same query corpus, the same evaluators, and the same downstream tasks, with MiMo as the primary reasoning model. Output: report quality, citation accuracy, latency, and cost per cited finding, published as a public benchmark in the repository.

Roadmap during the grant window: integrate a real search provider behind the existing protocol, add a URL-to-text fetcher, replace the heuristic synthesizer with a MiMo reasoning call under strict token budget, track per-run cost and per-claim confidence, and ship a one-command installer so other builders can run the same agent on their own queries.

---

## 5. Proof URL

```
https://github.com/almer121/hermes-deep-research
```

Optional second proof if the form accepts more than one:

```
https://github.com/almer121/hermes-deep-research/blob/main/proof/research-report.md
```

---

## 6. File proof to upload

Highest-weight evidence in order:

1. Terminal screenshot of `PYTHONPATH=src:. python3 -m pytest tests -q` showing all tests passing.
2. Terminal screenshot of `PYTHONPATH=src:. python3 -m deepresearch.cli "mixture of experts language models" --output proof/research-report.md`.
3. `git log --oneline` showing the commit history.
4. The rendered `proof/research-report.md` opened in a markdown viewer.
5. Optional but high-value: a screenshot of your Anthropic or OpenAI billing dashboard for the last 30 days, with the dollar amount blurred but the usage curve visible. This single screenshot moves you from "small builder" to "active high-volume builder" in most reviewer rubrics.

Save them under `proof/screenshots/` and commit.

---

## 7. Submission discipline

- Read the form once end to end before typing anything. The site enforces a minimum 5-minute dwell time before submit.
- Trim the description if a per-field character limit applies.
- Submit once per email. If no approval email arrives within 3 business days, resubmit with a tightened description.
- After submit, bind the application email to your Xiaomi ID at https://id.mi.com.

---

## 8. Short version (use only if a field caps you under 200 words)

Hermes Deep Research is a six-stage autonomous research pipeline running on an AWS VPS. Hermes Agent orchestrates Claude Code, Codex, and Cursor through plan, search, extract, synthesize, cite, and report stages. A working open-source implementation is at https://github.com/almer121/hermes-deep-research with a passing test suite and a sample run on "mixture of experts language models" generating seven sub-questions, six sources, and a fully cited markdown report in under one minute. I run similar workflows daily at 40 to 90 agent invocations per day. With 100T credits I will migrate the planning and synthesis stages — the two highest-token stages — to MiMo V2.5, run a four-week production benchmark against my current Claude and GPT mix, and publish a structured comparison openly: report quality, citation accuracy, latency, and cost per cited finding. Roadmap during the grant: real search provider integration, URL-to-text fetcher, MiMo-backed synthesizer under strict token budget, per-run cost tracking, and a one-command installer for other builders.
