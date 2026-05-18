"""Command-line entry point for Hermes Deep Research."""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

from .pipeline import run_pipeline


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="deepresearch",
        description="Run an autonomous research pipeline over a query.",
    )
    parser.add_argument("query", help="Research question to investigate")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("examples/research-report.md"),
        help="Path to write the markdown report",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Print per-stage progress",
    )
    args = parser.parse_args(argv)

    def progress(stage: str, message: str) -> None:
        if args.verbose:
            print(f"[{stage}] {message}", flush=True)

    started = time.perf_counter()
    run = run_pipeline(args.query, on_progress=progress)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(run.report, encoding="utf-8")

    elapsed_ms = (time.perf_counter() - started) * 1000
    output_size = args.output.stat().st_size
    print(f"Report written: {args.output} ({output_size} bytes)")
    print(f"Sub-questions: {len(run.plan.sub_questions)}")
    print(f"Sources collected: {len(run.results)}")
    print(f"Evidence units: {len(run.evidence)}")
    if args.verbose:
        if elapsed_ms < 1000:
            print(f"Elapsed: {elapsed_ms:.1f} ms (offline corpus, no LLM call)")
        else:
            print(f"Elapsed: {elapsed_ms / 1000:.2f} s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
