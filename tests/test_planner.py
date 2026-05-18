from deepresearch.planner import build_plan


def test_empty_query_returns_inert_plan():
    plan = build_plan("   ")
    assert not plan.is_actionable()
    assert plan.sub_questions == []


def test_plan_caps_questions():
    plan = build_plan("mixture of experts language models", max_questions=4)
    assert plan.is_actionable()
    assert len(plan.sub_questions) == 4
    assert all(plan.query in angle for angle in plan.angles)


def test_plan_questions_are_unique():
    plan = build_plan("vector search at scale")
    assert len(plan.sub_questions) == len(set(plan.sub_questions))
