"""Command-line entry point for Hermes Deep Research."""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

from .pipeline import run_pipeline


def _log(verbose: bool, message: str) -> None:
    if verbose:
        print(message, flush=True)


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

    started = time.perf_counter()
    _log(args.verbose, f"[plan] decomposing query: {args.query}")

    run = run_pipeline(args.query)

    _log(args.verbose, f"[plan] {len(run.plan.sub_questions)} sub-questions")
    _log(args.verbose, f"[search] {len(run.results)} sources collected")
    _log(args.verbose, f"[extract] {len(run.evidence)} evidence units")
    _log(args.verbose, f"[synthesize] {len(run.synthesis.sections)} sections")
    _log(args.verbose, "[report] rendering markdown")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(run.report, encoding="utf-8")

    elapsed = time.perf_counter() - started
    print(f"Report written: {args.output}")
    print(f"Sub-questions: {len(run.plan.sub_questions)}")
    print(f"Sources collected: {len(run.results)}")
    print(f"Evidence units: {len(run.evidence)}")
    if args.verbose:
        print(f"Elapsed: {elapsed * 1000:.1f} ms")
    return 0


if __name__ == "__main__":
    sys.exit(main())
