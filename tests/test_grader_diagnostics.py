from pathlib import Path

from pyquest.curriculum.loader import CurriculumLoader
from pyquest.runner.grader import PytestGrader, check_python_syntax, summarize_failure_text

REPO_ROOT = Path(__file__).resolve().parents[1]
CURRICULUM_DIR = REPO_ROOT / "curriculum"


def test_syntax_error_extracts_file_line_and_column() -> None:
    diags = check_python_syntax({"config_parser.py": "def broken(:\n    return 1\n"})
    assert len(diags) == 1
    assert diags[0].file == "config_parser.py"
    assert diags[0].line == 1
    assert diags[0].column is not None and diags[0].column >= 1
    assert "SyntaxError" in diags[0].message


def test_indentation_error_extracts_exact_line() -> None:
    loaded = CurriculumLoader(CURRICULUM_DIR).load()
    lesson = loaded.lessons_by_id["01-01"]
    grader = PytestGrader()

    result = grader.grade(
        lesson,
        {"config_parser.py": "def parse_service_config():\nreturn {}\n"},
    )
    assert result.passed is False
    assert result.stage == "SYNTAX"
    assert len(result.diagnostics) == 1
    assert result.diagnostics[0].file == "config_parser.py"
    assert result.diagnostics[0].line == 2
    assert "IndentationError" in result.diagnostics[0].message


def test_assertion_error_formats_crisp_root_cause() -> None:
    raw_junit_body = """
    def test_total():
>       assert compute_invoice_total("0.10", 3) == Decimal("0.30")
E       AssertionError: assert Decimal('0.31') == Decimal('0.30')
E        +  where Decimal('0.31') = compute_invoice_total('0.10', 3)
    """
    summary = summarize_failure_text("AssertionError", raw_junit_body)
    assert summary.startswith("AssertionError:")
    assert "Decimal('0.31') == Decimal('0.30')" in summary
    assert "def test_total" not in summary


def test_grader_reports_assertion_failure_on_lesson() -> None:
    loaded = CurriculumLoader(CURRICULUM_DIR).load()
    lesson = loaded.lessons_by_id["01-01"]
    grader = PytestGrader()
    res = grader.grade(lesson, lesson.starter_files)
    assert res.passed is False
    assert res.stage == "TEST"
    assert any(not tc.passed for tc in res.test_cases)


def test_grader_rejects_forbidden_submission_paths() -> None:
    loaded = CurriculumLoader(CURRICULUM_DIR).load()
    lesson = loaded.lessons_by_id["01-01"]
    grader = PytestGrader()

    for bad_path in ("conftest.py", "sub/conftest.py", "tests/test_hack.py", "../escape.py"):
        res = grader.grade(lesson, {bad_path: "def nope(): pass\n"})
        assert res.passed is False
        assert res.stage == "SYNTAX"
        assert "Forbidden file path" in res.summary
