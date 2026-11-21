from __future__ import annotations

import ast
import os
import re
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

from pyquest.domain.models import Diagnostic, GradeResult, LessonSpec, TestCaseResult

SYNTAX_TRACE_RE = re.compile(
    r'File "([^"]+)", line (\d+).*?\n(?:\s*[^\n]*\n)?(?:\s*\^+\n)?((?:SyntaxError|IndentationError|TabError):\s*[^\n]+)',
    re.DOTALL,
)

ROOT_CAUSE_EXC_RE = re.compile(
    r"(?:^|\n)(?:E\s+)?((?:pydantic\.)?(?:ValidationError|AssertionError|ImportError|ModuleNotFoundError|TypeError|ValueError|KeyError|AttributeError|NameError|ZeroDivisionError|IndexError|RuntimeError|[A-Z][A-Za-z]+Error)):\s*(.+)"
)


def _safe_rel_path(raw_path: str) -> Path:
    candidate = Path(raw_path)
    if candidate.is_absolute() or ".." in candidate.parts:
        raise ValueError(f"Invalid relative file path: {raw_path}")
    return candidate


def check_python_syntax(files: dict[str, str]) -> list[Diagnostic]:
    """Run fast AST syntax validation across all Python files before invoking pytest."""
    diagnostics: list[Diagnostic] = []
    for rel_path, content in sorted(files.items()):
        if not rel_path.endswith(".py"):
            continue
        try:
            ast.parse(content, filename=rel_path)
        except (SyntaxError, IndentationError) as exc:
            err_name = type(exc).__name__
            msg = exc.msg or "invalid syntax"
            diagnostics.append(
                Diagnostic(
                    file=rel_path,
                    line=max(1, exc.lineno or 1),
                    column=max(1, exc.offset or 1),
                    severity="error",
                    message=f"{err_name}: {msg}",
                )
            )
    return diagnostics


def summarize_failure_text(raw_message: str, raw_body: str = "") -> str:
    """Turn a raw pytest failure/JUnit body into a crisp, actionable root-cause summary."""
    combined = "\n".join(part for part in (raw_message.strip(), raw_body.strip()) if part)
    if not combined:
        return "Test assertion failed."

    lines = [line.rstrip() for line in combined.splitlines() if line.strip()]
    # Prefer pytest's `E   ...` diagnostic lines when available
    e_lines = [line[2:].strip() for line in lines if line.startswith("E ")]

    exc_match = ROOT_CAUSE_EXC_RE.search(combined)
    if exc_match:
        exc_type, exc_detail = exc_match.group(1), exc_match.group(2).strip()
        if exc_type == "AssertionError" and e_lines:
            # Keep assertion comparison lines (usually 1-3 crisp lines)
            concise = [ln for ln in e_lines if not ln.startswith("assert ") or len(e_lines) <= 2]
            detail_block = "\n".join((concise or e_lines)[:4])
            return f"AssertionError: {detail_block}"
        return f"{exc_type}: {exc_detail}"

    if e_lines:
        return "\n".join(e_lines[:4])

    # Fallback: take last 3 informative non-traceback-header lines
    filtered = [
        ln
        for ln in lines
        if not ln.startswith(("Traceback ", "___", "---", "During handling"))
    ]
    return "\n".join(filtered[-3:] if filtered else lines[-3:])


def parse_syntax_diagnostics_from_output(text: str, known_files: set[str]) -> list[Diagnostic]:
    """Extract SyntaxError/IndentationError locations from raw pytest stderr/stdout."""
    diagnostics: list[Diagnostic] = []
    for match in SYNTAX_TRACE_RE.finditer(text):
        raw_file, line_str, msg = match.group(1), match.group(2), match.group(3).strip()
        file_name = Path(raw_file).name
        resolved = raw_file if raw_file in known_files else next(
            (f for f in known_files if f.endswith(file_name)), file_name
        )
        diagnostics.append(
            Diagnostic(
                file=resolved,
                line=max(1, int(line_str)),
                column=1,
                severity="error",
                message=msg,
            )
        )
    return diagnostics


def parse_junit_xml(junit_path: Path) -> list[TestCaseResult]:
    """Parse JUnit XML produced by pytest into crisp TestCaseResult items."""
    if not junit_path.exists():
        return []
    tree = ET.parse(junit_path)
    root = tree.getroot()
    results: list[TestCaseResult] = []

    for tc in root.findall(".//testcase"):
        name = tc.attrib.get("name") or "unnamed_test"
        failure = tc.find("failure")
        error = tc.find("error")
        skipped = tc.find("skipped")
        if skipped is not None:
            continue
        node = failure if failure is not None else error
        if node is None:
            results.append(TestCaseResult(name=name, passed=True, message=""))
        else:
            raw_msg = node.attrib.get("message", "")
            raw_body = node.text or ""
            results.append(
                TestCaseResult(
                    name=name,
                    passed=False,
                    message=summarize_failure_text(raw_msg, raw_body),
                )
            )
    return results


class PytestGrader:
    """Isolated temporary-directory subprocess pytest grader."""

    def __init__(
        self,
        standard_timeout_seconds: int = 15,
        web_timeout_seconds: int = 25,
    ) -> None:
        self.standard_timeout_seconds = standard_timeout_seconds
        self.web_timeout_seconds = web_timeout_seconds

    def grade(self, lesson: LessonSpec, submitted_files: dict[str, str]) -> GradeResult:
        # 1. Fast AST syntax pre-check on learner files
        syntax_diags = check_python_syntax(submitted_files)
        if syntax_diags:
            first = syntax_diags[0]
            return GradeResult(
                passed=False,
                stage="SYNTAX",
                exit_code=2,
                diagnostics=syntax_diags,
                summary=f"Syntax check failed at {first.file}:{first.line} — {first.message}",
            )

        timeout = lesson.timeout_seconds or (
            self.web_timeout_seconds
            if lesson.runtime == "WEB_INTEGRATION"
            else self.standard_timeout_seconds
        )

        with tempfile.TemporaryDirectory(prefix="pyquest_run_") as tmp:
            workdir = Path(tmp)
            self._materialize_workspace(workdir, lesson, submitted_files)
            junit_path = workdir / ".junit-report.xml"

            env = self._isolated_env(workdir)
            cmd = [
                sys.executable,
                "-m",
                "pytest",
                f"--junitxml={junit_path}",
                "-q",
                "--tb=short",
                "tests",
            ]

            try:
                proc = subprocess.run(
                    cmd,
                    cwd=workdir,
                    env=env,
                    capture_output=True,
                    text=True,
                    timeout=timeout,
                )
            except subprocess.TimeoutExpired as exc:
                stdout = (exc.stdout or "") if isinstance(exc.stdout, str) else ""
                stderr = (exc.stderr or "") if isinstance(exc.stderr, str) else ""
                return GradeResult(
                    passed=False,
                    stage="EXECUTION",
                    exit_code=124,
                    stdout=stdout,
                    stderr=stderr or f"Execution timed out after {timeout}s (check for infinite loops).",
                    summary=f"Execution timed out after {timeout}s.",
                )

            test_cases = parse_junit_xml(junit_path)
            combined_output = "\n".join(p for p in (proc.stdout, proc.stderr) if p).strip()

            if proc.returncode == 0 and test_cases and all(tc.passed for tc in test_cases):
                return GradeResult(
                    passed=True,
                    stage="PASSED",
                    exit_code=0,
                    stdout=proc.stdout.strip(),
                    stderr="",
                    test_cases=test_cases,
                    summary=f"All {len(test_cases)}/{len(test_cases)} tests passed.",
                )

            # Check if a SyntaxError leaked through test import/collection
            extra_diags = parse_syntax_diagnostics_from_output(
                combined_output, set(submitted_files.keys())
            )
            if extra_diags:
                first = extra_diags[0]
                return GradeResult(
                    passed=False,
                    stage="SYNTAX",
                    exit_code=proc.returncode,
                    stdout=proc.stdout.strip(),
                    stderr=proc.stderr.strip(),
                    test_cases=test_cases,
                    diagnostics=extra_diags,
                    summary=f"Syntax check failed at {first.file}:{first.line} — {first.message}",
                )

            if test_cases:
                failed = [tc for tc in test_cases if not tc.passed]
                passed_count = len(test_cases) - len(failed)
                first_reason = failed[0].message.splitlines()[0] if failed else "Test failure"
                stage = "EXECUTION" if any(
                    tag in first_reason for tag in ("ImportError", "ModuleNotFoundError")
                ) else "TEST"
                return GradeResult(
                    passed=False,
                    stage=stage,
                    exit_code=proc.returncode,
                    stdout=proc.stdout.strip(),
                    stderr=proc.stderr.strip(),
                    test_cases=test_cases,
                    summary=(
                        f"{passed_count}/{len(test_cases)} passed · "
                        f"{len(failed)} failed ({first_reason[:110]})"
                    ),
                )

            # Collection or runtime failure before individual tests ran
            summary_msg = summarize_failure_text(combined_output)
            return GradeResult(
                passed=False,
                stage="EXECUTION",
                exit_code=proc.returncode,
                stdout=proc.stdout.strip(),
                stderr=summary_msg,
                summary=summary_msg.splitlines()[0][:140],
            )

    def _materialize_workspace(
        self,
        workdir: Path,
        lesson: LessonSpec,
        submitted_files: dict[str, str],
    ) -> None:
        # Base starter files + learner edits (learner edits overwrite starter paths)
        merged_files = dict(lesson.starter_files)
        merged_files.update(submitted_files)

        for rel_path, content in merged_files.items():
            target = workdir / _safe_rel_path(rel_path)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8")

        tests_dir = workdir / "tests"
        tests_dir.mkdir(parents=True, exist_ok=True)
        for rel_path, content in lesson.test_files.items():
            target = tests_dir / _safe_rel_path(rel_path)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8")

    def _isolated_env(self, workdir: Path) -> dict[str, str]:
        return {
            "PATH": os.environ.get("PATH", "/usr/local/bin:/usr/bin:/bin"),
            "HOME": str(workdir),
            "TMPDIR": str(workdir),
            "PYTHONPATH": str(workdir),
            "PYTHONDONTWRITEBYTECODE": "1",
            "PYTHONNOUSERSITE": "1",
            "LC_ALL": "C.UTF-8",
            "LANG": "C.UTF-8",
        }
