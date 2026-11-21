from pathlib import Path

import pytest

from pyquest.curriculum.loader import CurriculumLoader
from pyquest.runner.grader import PytestGrader

REPO_ROOT = Path(__file__).resolve().parents[1]
CURRICULUM_DIR = REPO_ROOT / "curriculum"


def test_curriculum_loads_modules_1_and_2_with_17_lessons() -> None:
    loaded = CurriculumLoader(CURRICULUM_DIR).load()
    assert len(loaded.modules) == 2
    assert len(loaded.lessons) == 17

    boss_lessons = [lesson for lesson in loaded.lessons if lesson.kind == "BOSS"]
    assert [b.id for b in boss_lessons] == ["01-09", "02-08"]
    assert all(b.xp == 250 for b in boss_lessons)

    for lesson in loaded.lessons:
        assert len(lesson.hints) == 3, f"{lesson.id} must have exactly 3 hints"
        assert len(set(lesson.hints)) == 3, f"{lesson.id} hints must be distinct"
        assert lesson.concept_markdown.strip()
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
