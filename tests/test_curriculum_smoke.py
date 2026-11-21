from pathlib import Path

import pytest

from pyquest.curriculum.loader import CurriculumLoader
from pyquest.persistence.store import HERO_TIERS, compute_hero_status
from pyquest.runner.grader import PytestGrader

REPO_ROOT = Path(__file__).resolve().parents[1]
CURRICULUM_DIR = REPO_ROOT / "curriculum"


def test_curriculum_loads_all_12_modules_75_lessons_and_3_gates() -> None:
    loaded = CurriculumLoader(CURRICULUM_DIR).load()
    assert len(loaded.modules) == 12
    assert len(loaded.lessons) == 75

    boss_lessons = [lesson for lesson in loaded.lessons if lesson.kind == "BOSS"]
    assert [b.id for b in boss_lessons] == [
        "01-09",
        "02-08",
        "03-06",
        "04-07",
        "05-08",
        "06-05",
        "07-05",
        "08-05",
        "09-05",
        "10-06",
        "11-06",
        "12-05",
    ]
    assert all(b.xp == 250 for b in boss_lessons)

    assert len(loaded.projects) == 3
    assert [p.id for p in loaded.projects] == [
        "proj-01-cli-ledger-reconciler",
        "proj-02-inventory-audit-service",
        "proj-03-mini-sidekiq-ai-triage",
    ]
    assert [p.required_modules_completed for p in loaded.projects] == [5, 9, 12]

    # Pedagogical hygiene: all modules carry Dual-Angle LinkedIn Insights
    for mod in loaded.modules:
        assert mod.insight is not None, f"{mod.id} missing insight metadata"
        assert mod.insight.linkedin_angle.hook.strip(), f"{mod.id} missing linkedinAngle.hook"
        assert mod.insight.linkedin_angle.python_insight.strip()
        assert mod.insight.boss_linkedin_angle is not None, f"{mod.id} missing bossLinkedinAngle"
        assert len(mod.insight.reflection_prompts) >= 1, f"{mod.id} missing reflectionPrompts"

    # Hero tier thresholds align cleanly across 0 -> 12 modules
    assert [threshold for _, threshold, _, _ in HERO_TIERS] == [0, 3, 6, 9, 12]
    assert compute_hero_status(12, 72, 9000).title == "AI Grandmaster"

    # Pedagogical hygiene: concept depth, hints, and valid file sets
    for lesson in loaded.lessons:
        assert len(lesson.hints) == 3, f"{lesson.id} must have exactly 3 hints"
        assert all(h.strip() for h in lesson.hints), f"{lesson.id} contains blank hint"
        assert len(set(lesson.hints)) == 3, f"{lesson.id} hints must be distinct"
        assert len(lesson.concept_markdown.strip()) >= 400, (
            f"{lesson.id} concept.md too short ({len(lesson.concept_markdown.strip())} chars)"
        )
        assert lesson.entry_file in lesson.starter_files
        assert lesson.entry_file in lesson.solution_files


@pytest.mark.parametrize(
    "lesson_id",
    [lesson.id for lesson in CurriculumLoader(CURRICULUM_DIR).load().lessons],
)
def test_starter_fails_and_solution_passes(lesson_id: str) -> None:
    loaded = CurriculumLoader(CURRICULUM_DIR).load()
    lesson = loaded.lessons_by_id[lesson_id]
    grader = PytestGrader()

    starter_res = grader.grade(lesson, lesson.starter_files)
    assert starter_res.passed is False, f"{lesson_id} starter unexpectedly passed"
    assert starter_res.stage != "SYNTAX", f"{lesson_id} starter has syntax errors: {starter_res.diagnostics}"

    solution_res = grader.grade(lesson, lesson.solution_files)
    assert solution_res.passed is True, (
        f"{lesson_id} solution failed: {solution_res.summary} | {solution_res.test_cases}"
    )
    assert solution_res.stage == "PASSED"
    assert len(solution_res.test_cases) >= 2
