from deepresearch.pipeline import run_pipeline


def test_pipeline_produces_report():
    run = run_pipeline("mixture of experts language models")
    assert run.plan.is_actionable()
    assert run.results, "expected aggregated search results"
    assert run.evidence, "expected extracted evidence"
    assert run.synthesis.sections, "expected synthesized sections"
    assert "Research Report:" in run.report
    assert "## Sources" in run.report


def test_pipeline_handles_empty_query():
    run = run_pipeline("")
    assert not run.plan.is_actionable()
    assert run.results == []
    assert run.evidence == []
