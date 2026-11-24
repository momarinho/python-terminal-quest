from __future__ import annotations

import ast
import re

from pyquest.domain.models import LessonSpec

_CODE_FENCE_RE = re.compile(r"```python\s*\n(.*?)```", re.DOTALL | re.IGNORECASE)
_COMMON_NOISE_CALLS = {
    "len",
    "range",
    "enumerate",
    "zip",
    "str",
    "int",
    "float",
    "bool",
    "list",
    "dict",
    "set",
    "tuple",
    "print",
    "append",
    "get",
    "items",
    "keys",
    "values",
    "strip",
    "lower",
    "split",
    "join",
}


def _collect_ast_symbols(tree: ast.AST) -> set[str]:
    symbols: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Match):
            symbols.add("match/case")
        elif isinstance(node, ast.Try):
            symbols.add("try/except")
        elif isinstance(node, ast.Raise):
            symbols.add("raise")
        elif isinstance(node, (ast.With, ast.AsyncWith)):
            symbols.add("with/context_manager")
        elif isinstance(node, (ast.ListComp, ast.DictComp, ast.SetComp)):
            symbols.add("comprehension")
        elif isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name) and node.func.id not in _COMMON_NOISE_CALLS:
                symbols.add(f"{node.func.id}()")
            elif isinstance(node.func, ast.Attribute) and node.func.attr not in _COMMON_NOISE_CALLS:
                symbols.add(f".{node.func.attr}()")
    return symbols


def _map_function_ast_dumps(tree: ast.AST) -> dict[str, str]:
    fn_dumps: dict[str, str] = {}
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            fn_dumps[node.name] = ast.dump(node, include_attributes=False)
    return fn_dumps


def inspect_learner_code_gaps(lesson: LessonSpec, learner_files: dict[str, str]) -> list[str]:
    """Compare learner AST structure against starter/solution ASTs without revealing solution code."""
    observations: list[str] = []

    for filename, sol_code in lesson.solution_files.items():
        if not filename.endswith(".py"):
            continue
        learner_code = learner_files.get(filename)
        if learner_code is None or not learner_code.strip():
            observations.append(
                f"File `{filename}` is currently empty or missing from your editor submission."
            )
            continue

        try:
            learner_tree = ast.parse(learner_code)
        except SyntaxError as err:
            observations.append(
                f"SyntaxError in `{filename}` at line {err.lineno or 1}: {err.msg}."
            )
            continue

        try:
            sol_tree = ast.parse(sol_code)
        except SyntaxError:
            continue

        starter_code = lesson.starter_files.get(filename, "")
        try:
            starter_tree = ast.parse(starter_code) if starter_code.strip() else None
        except SyntaxError:
            starter_tree = None

        sol_fns = _map_function_ast_dumps(sol_tree)
        learner_fns = _map_function_ast_dumps(learner_tree)
        starter_fns = _map_function_ast_dumps(starter_tree) if starter_tree else {}

        for fn_name, sol_dump in sol_fns.items():
            if fn_name.startswith("_"):
                continue
            learner_dump = learner_fns.get(fn_name)
            starter_dump = starter_fns.get(fn_name)
            if learner_dump is None:
                observations.append(f"In `{filename}`, expected function `{fn_name}()` is missing.")
            elif (
                starter_dump is not None
                and learner_dump == starter_dump
                and learner_dump != sol_dump
            ):
                observations.append(
                    f"In `{filename}`, `{fn_name}()` still has its unmodified starter body—replace the placeholder logic."
                )

        if len(observations) < 3:
            missing_symbols = sorted(
                _collect_ast_symbols(sol_tree) - _collect_ast_symbols(learner_tree)
            )
            for sym in missing_symbols[: 3 - len(observations)]:
                observations.append(
                    f"In `{filename}`, check if you need `{sym}` to satisfy the stage requirements."
                )

        if len(observations) >= 3:
            break

    return observations[:3]


def extract_concept_code_example(concept_markdown: str, max_lines: int = 6) -> str:
    """Extract a short illustrative snippet from concept.md for progressive Socratic hints."""
    match = _CODE_FENCE_RE.search(concept_markdown)
    if not match:
        return ""
    lines = [line for line in match.group(1).splitlines() if line.strip()]
    if not lines:
        return ""
    snippet = "\n".join(lines[:max_lines])
    return f"```python\n{snippet}\n```"
