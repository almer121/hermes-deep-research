"""Command-line entry point for Hermes Deep Research."""

from __future__ import annotations

import argparse
import sys
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
    args = parser.parse_args(argv)

    run = run_pipeline(args.query)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(run.report, encoding="utf-8")

    print(f"Report written: {args.output}")
    print(f"Sub-questions: {len(run.plan.sub_questions)}")
    print(f"Sources collected: {len(run.results)}")
    print(f"Evidence units: {len(run.evidence)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
