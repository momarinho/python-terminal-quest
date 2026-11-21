from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from pyquest.domain.models import (
    ChecklistItemSpec,
    LessonKind,
    LessonMode,
    LessonRuntime,
    LessonSpec,
    LinkedinAngle,
    ModuleInsight,
    ModuleMeta,
    PortfolioProject,
    ProjectProgress,
    SprintSpec,
)


def _read_tree(directory: Path) -> dict[str, str]:
    """Read all files in a directory preserving relative POSIX paths."""
    if not directory.exists() or not directory.is_dir():
        return {}
    files: dict[str, str] = {}
    for path in sorted(directory.rglob("*")):
        if not path.is_file():
            continue
        if "__pycache__" in path.parts or path.suffix == ".pyc":
            continue
        rel = path.relative_to(directory).as_posix()
        files[rel] = path.read_text(encoding="utf-8")
    return files


@dataclass(frozen=True)
class ProjectTemplate:
    id: str
    order: int
    title: str
    milestone_label: str
    required_modules_completed: int
    prerequisite_module_ids: list[str]
    tech_stack: list[str]
    business_context: str
    package_layout: str
    sprints: list[SprintSpec]
    review_criteria: list[str]
    showcase_tips: list[str]
    ai_review_prompts: list[str]

    def materialize(
        self,
        completed_module_ids: set[str],
        progress: ProjectProgress,
    ) -> PortfolioProject:
        completed_prereqs = sum(
            1 for mod_id in self.prerequisite_module_ids if mod_id in completed_module_ids
        )
        unlocked = completed_prereqs >= self.required_modules_completed
        return PortfolioProject(
            id=self.id,
            order=self.order,
            title=self.title,
            milestone_label=self.milestone_label,
            required_modules_completed=self.required_modules_completed,
            prerequisite_module_ids=list(self.prerequisite_module_ids),
            completed_prerequisite_modules=completed_prereqs,
            milestone_unlocked=unlocked,
            tech_stack=list(self.tech_stack),
            business_context=self.business_context,
            package_layout=self.package_layout,
            sprints=self.sprints,
            review_criteria=list(self.review_criteria),
            showcase_tips=list(self.showcase_tips),
            ai_review_prompts=list(self.ai_review_prompts),
            progress=progress,
        )


@dataclass
class LoadedCurriculum:
    modules: list[ModuleMeta]
    lessons: list[LessonSpec]
    lessons_by_id: dict[str, LessonSpec]
    insights_by_module: dict[str, ModuleInsight]
    projects: list[ProjectTemplate]


class CurriculumLoader:
    """Loads and validates YAML-driven curriculum modules, lessons, and projects."""

    def __init__(self, curriculum_dir: Path) -> None:
        self.curriculum_dir = curriculum_dir

    def load(self) -> LoadedCurriculum:
        if not self.curriculum_dir.exists():
            raise FileNotFoundError(f"Curriculum directory not found: {self.curriculum_dir}")

        insights_by_module, modules_from_meta = self._load_modules_meta()
        lessons = self._load_lessons()
        lessons_by_id: dict[str, LessonSpec] = {}
        for lesson in lessons:
            if lesson.id in lessons_by_id:
                raise ValueError(f"Duplicate lesson id: {lesson.id}")
            lessons_by_id[lesson.id] = lesson

        # Ensure every module referenced by lessons has ModuleMeta
        meta_by_id = {m.id: m for m in modules_from_meta}
        ordered_modules: list[ModuleMeta] = []
        seen_mod_ids: set[str] = set()
        for lesson in lessons:
            if lesson.module_id in seen_mod_ids:
                continue
            seen_mod_ids.add(lesson.module_id)
            meta = meta_by_id.get(lesson.module_id)
            if meta is None:
                order = self._extract_order(lesson.module_id)
                meta = ModuleMeta(
                    id=lesson.module_id,
                    order=order,
                    title=lesson.module_title,
                    phase=1,
                    insight=insights_by_module.get(lesson.module_id),
                )
            elif meta.insight is None:
                meta = meta.model_copy(update={"insight": insights_by_module.get(lesson.module_id)})
            ordered_modules.append(meta)

        ordered_modules.sort(key=lambda m: (m.order, m.id))
        projects = self._load_projects()

        return LoadedCurriculum(
            modules=ordered_modules,
            lessons=lessons,
            lessons_by_id=lessons_by_id,
            insights_by_module=insights_by_module,
            projects=projects,
        )

    def _extract_order(self, module_id: str) -> int:
        digits = "".join(ch for ch in module_id if ch.isdigit())
        return int(digits) if digits else 0

    def _load_modules_meta(self) -> tuple[dict[str, ModuleInsight], list[ModuleMeta]]:
        meta_path = self.curriculum_dir / "modules-meta.yaml"
        if not meta_path.exists():
            return {}, []

        raw: dict[str, Any] = yaml.safe_load(meta_path.read_text(encoding="utf-8")) or {}
        insights: dict[str, ModuleInsight] = {}
        modules: list[ModuleMeta] = []

        for idx, entry in enumerate(raw.get("modules", []), start=1):
            module_id = str(entry["moduleId"])
            angle_raw = entry["linkedinAngle"]
            linkedin_angle = LinkedinAngle(
                hook=str(angle_raw["hook"]).strip(),
                python_insight=str(
                    angle_raw.get("pythonInsight") or angle_raw.get("insight") or ""
                ).strip(),
                code_comparison=str(angle_raw["codeComparison"]),
            )
            boss_raw = entry.get("bossLinkedinAngle")
            boss_angle = None
            if boss_raw:
                boss_angle = LinkedinAngle(
                    hook=str(boss_raw["hook"]).strip(),
                    python_insight=str(
                        boss_raw.get("pythonInsight") or boss_raw.get("insight") or ""
                    ).strip(),
                    code_comparison=str(boss_raw["codeComparison"]),
                )
            insight = ModuleInsight(
                module_id=module_id,
                linkedin_angle=linkedin_angle,
                boss_linkedin_angle=boss_angle,
                reflection_prompts=[str(p).strip() for p in entry.get("reflectionPrompts", [])],
            )
            insights[module_id] = insight
            if "title" in entry:
                modules.append(
                    ModuleMeta(
                        id=module_id,
                        order=int(entry.get("order", idx)),
                        title=str(entry["title"]),
                        phase=int(entry.get("phase", 1)),
                        subtitle=str(entry.get("subtitle", "")),
                        insight=insight,
                    )
                )

        return insights, modules

    def _load_lessons(self) -> list[LessonSpec]:
        lessons: list[LessonSpec] = []
        module_dirs = sorted(
            p
            for p in self.curriculum_dir.iterdir()
            if p.is_dir() and p.name.startswith("module-")
        )
        for mod_dir in module_dirs:
            lesson_dirs = sorted(p for p in mod_dir.iterdir() if p.is_dir())
            for lesson_dir in lesson_dirs:
                yaml_path = lesson_dir / "lesson.yaml"
                if not yaml_path.exists():
                    continue
                lessons.append(self._load_single_lesson(lesson_dir, yaml_path))
        return lessons

    def _load_single_lesson(self, lesson_dir: Path, yaml_path: Path) -> LessonSpec:
        data: dict[str, Any] = yaml.safe_load(yaml_path.read_text(encoding="utf-8")) or {}
        lesson_id = str(data["id"])
        kind: LessonKind = data.get("kind") or ("BOSS" if "boss" in lesson_dir.name.lower() else "STANDARD")
        mode: LessonMode = data.get("mode", "PYTEST_TDD")
        runtime: LessonRuntime = data.get("runtime", "STANDARD")
        default_xp = 250 if kind == "BOSS" else 100
        xp = int(data.get("xp", default_xp))

        concept_path = lesson_dir / "concept.md"
        if not concept_path.exists():
            raise FileNotFoundError(f"Missing concept.md for lesson {lesson_id}")
        concept_markdown = concept_path.read_text(encoding="utf-8")

        hints_path = lesson_dir / "hints.yaml"
        if not hints_path.exists():
            raise FileNotFoundError(f"Missing hints.yaml for lesson {lesson_id}")
        hints_raw = yaml.safe_load(hints_path.read_text(encoding="utf-8")) or {}
        hints = [str(h).strip() for h in hints_raw.get("hints", []) if str(h).strip()]

        starter_files = _read_tree(lesson_dir / "starter")
        solution_files = _read_tree(lesson_dir / "solution")
        test_files = _read_tree(lesson_dir / "tests")

        if not starter_files:
            raise ValueError(f"Lesson {lesson_id} has empty starter/ directory")
        if not solution_files:
            raise ValueError(f"Lesson {lesson_id} has empty solution/ directory")
        if not test_files:
            raise ValueError(f"Lesson {lesson_id} has empty tests/ directory")

        entry_file = str(data.get("entryFile") or next(iter(starter_files)))
        if entry_file not in starter_files:
            raise ValueError(f"Lesson {lesson_id}: entryFile '{entry_file}' not found in starter/")
        if entry_file not in solution_files:
            raise ValueError(f"Lesson {lesson_id}: entryFile '{entry_file}' not found in solution/")

        tags = [str(t) for t in data.get("tags", [])]

        return LessonSpec(
            id=lesson_id,
            module_id=str(data["moduleId"]),
            module_title=str(data["moduleTitle"]),
            title=str(data["title"]),
            objective=str(data["objective"]),
            mode=mode,
            kind=kind,
            runtime=runtime,
            xp=xp,
            tags=tags,
            entry_file=entry_file,
            concept_markdown=concept_markdown,
            hints=hints,
            starter_files=starter_files,
            solution_files=solution_files,
            test_files=test_files,
            timeout_seconds=data.get("timeoutSeconds"),
        )

    def _load_projects(self) -> list[ProjectTemplate]:
        projects_path = self.curriculum_dir / "projects.yaml"
        if not projects_path.exists():
            return []

        raw: dict[str, Any] = yaml.safe_load(projects_path.read_text(encoding="utf-8")) or {}
        templates: list[ProjectTemplate] = []
        for entry in raw.get("projects", []):
            sprints = [
                SprintSpec(
                    id=str(sp["id"]),
                    title=str(sp["title"]),
                    items=[
                        ChecklistItemSpec(id=str(item["id"]), text=str(item["text"]))
                        for item in sp.get("items", [])
                    ],
                )
                for sp in entry.get("sprints", [])
            ]
            templates.append(
                ProjectTemplate(
                    id=str(entry["id"]),
                    order=int(entry["order"]),
                    title=str(entry["title"]),
                    milestone_label=str(entry["milestoneLabel"]),
                    required_modules_completed=int(entry["requiredModulesCompleted"]),
                    prerequisite_module_ids=[str(m) for m in entry.get("prerequisiteModuleIds", [])],
                    tech_stack=[str(t) for t in entry.get("techStack", [])],
                    business_context=str(entry.get("businessContext", "")).strip(),
                    package_layout=str(entry.get("packageLayout", "")).rstrip(),
                    sprints=sprints,
                    review_criteria=[str(c) for c in entry.get("reviewCriteria", [])],
                    showcase_tips=[str(t) for t in entry.get("showcaseTips", [])],
                    ai_review_prompts=[str(p) for p in entry.get("aiReviewPrompts", [])],
                )
            )
        templates.sort(key=lambda p: p.order)
        return templates
