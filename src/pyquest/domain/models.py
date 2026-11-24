from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


class CamelModel(BaseModel):
    """Base Pydantic v2 model serializing snake_case attributes as camelCase JSON."""

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )


LessonStatus = Literal["NOT_STARTED", "IN_PROGRESS", "COMPLETED"]
LessonMode = Literal["PYTHON_CORE", "PYTEST_TDD", "BUG_FIX", "FASTAPI", "AI_SYSTEMS"]
LessonKind = Literal["STANDARD", "BOSS"]
LessonRuntime = Literal["STANDARD", "WEB_INTEGRATION"]
GradeStage = Literal["SYNTAX", "EXECUTION", "TEST", "PASSED"]
ProjectStatus = Literal["NOT_STARTED", "IN_PROGRESS", "COMPLETED"]


class LinkedinAngle(CamelModel):
    hook: str
    python_insight: str
    code_comparison: str


class ModuleInsight(CamelModel):
    module_id: str
    linkedin_angle: LinkedinAngle
    boss_linkedin_angle: LinkedinAngle | None = None
    reflection_prompts: list[str] = Field(default_factory=list)


class ModuleMeta(CamelModel):
    id: str
    order: int
    title: str
    phase: int = 1
    subtitle: str = ""
    insight: ModuleInsight | None = None


class LessonSpec(CamelModel):
    id: str
    module_id: str
    module_title: str
    title: str
    objective: str
    mode: LessonMode = "PYTEST_TDD"
    kind: LessonKind = "STANDARD"
    runtime: LessonRuntime = "STANDARD"
    xp: int = 100
    tags: list[str] = Field(default_factory=list)
    entry_file: str
    concept_markdown: str
    hints: list[str] = Field(default_factory=list)
    starter_files: dict[str, str] = Field(default_factory=dict)
    solution_files: dict[str, str] = Field(default_factory=dict)
    test_files: dict[str, str] = Field(default_factory=dict)
    timeout_seconds: int | None = None


class LessonProgress(CamelModel):
    lesson_id: str
    status: LessonStatus = "NOT_STARTED"
    attempts: int = 0
    hints_revealed: int = 0
    last_diagnostics: str = ""
    notes: str = ""
    flagged: bool = False
    solution_revealed: bool = False
    completed_at: str = ""
    needs_review: bool = False
    updated_at: str = ""


class LessonSummary(CamelModel):
    id: str
    module_id: str
    module_title: str
    title: str
    objective: str
    mode: LessonMode
    kind: LessonKind
    runtime: LessonRuntime
    xp: int
    tags: list[str]
    entry_file: str
    status: LessonStatus
    attempts: int
    hints_revealed: int
    total_hints: int
    flagged: bool
    has_notes: bool
    solution_revealed: bool = False
    needs_review: bool = False


class LessonDetail(CamelModel):
    id: str
    module_id: str
    module_title: str
    title: str
    objective: str
    mode: LessonMode
    kind: LessonKind
    runtime: LessonRuntime
    xp: int
    tags: list[str]
    entry_file: str
    concept_markdown: str
    files: dict[str, str]
    test_files: dict[str, str] = Field(default_factory=dict)
    unlocked_hints: list[str]
    total_hints: int
    progress: LessonProgress
    prev_lesson_id: str | None = None
    next_lesson_id: str | None = None


class Diagnostic(CamelModel):
    file: str
    line: int
    column: int | None = None
    severity: str = "error"
    message: str


class TestCaseResult(CamelModel):
    name: str
    passed: bool
    message: str = ""


class GradeResult(CamelModel):
    passed: bool
    stage: GradeStage
    exit_code: int
    stdout: str = ""
    stderr: str = ""
    test_cases: list[TestCaseResult] = Field(default_factory=list)
    diagnostics: list[Diagnostic] = Field(default_factory=list)
    summary: str = ""


class StreakStats(CamelModel):
    current_streak_days: int = 0
    longest_streak_days: int = 0
    active_today: bool = False
    active_days_total: int = 0


class HeroStatus(CamelModel):
    tier: int = 1
    title: str = "Apprentice"
    subtitle: str = "Wood Sword & Morning Coffee"
    completed_modules: int = 0
    completed_lessons: int = 0
    earned_xp: int = 0
    next_tier: int | None = 2
    next_tier_title: str | None = "Explorer"
    modules_for_next_tier: int = 1


class ProgressState(CamelModel):
    completed_lessons: list[str] = Field(default_factory=list)
    earned_xp: int = 0
    streak: StreakStats = Field(default_factory=StreakStats)
    hero: HeroStatus = Field(default_factory=HeroStatus)
    lessons: dict[str, LessonProgress] = Field(default_factory=dict)


class ModuleGroup(CamelModel):
    id: str
    order: int = 0
    phase: int = 1
    subtitle: str = ""
    title: str
    total_lessons: int
    completed_lessons: int
    total_xp: int
    earned_xp: int
    lessons: list[LessonSummary]
    insight: ModuleInsight | None = None


class CurriculumResponse(CamelModel):
    total_lessons: int
    completed_lessons: int
    in_progress_lessons: int
    not_started_lessons: int
    total_xp: int
    earned_xp: int
    streak: StreakStats
    hero: HeroStatus
    modules: list[ModuleGroup]


class ChecklistItemSpec(CamelModel):
    id: str
    text: str


class SprintSpec(CamelModel):
    id: str
    title: str
    items: list[ChecklistItemSpec]


class ProjectProgress(CamelModel):
    project_id: str
    status: ProjectStatus = "NOT_STARTED"
    completed_checklist_ids: list[str] = Field(default_factory=list)
    repo_url: str = ""
    updated_at: str = ""


class PortfolioProject(CamelModel):
    id: str
    order: int
    title: str
    milestone_label: str
    required_modules_completed: int
    prerequisite_module_ids: list[str]
    completed_prerequisite_modules: int
    milestone_unlocked: bool
    tech_stack: list[str]
    business_context: str
    package_layout: str
    sprints: list[SprintSpec]
    review_criteria: list[str]
    showcase_tips: list[str]
    ai_review_prompts: list[str]
    progress: ProjectProgress


class ProjectsResponse(CamelModel):
    total_projects: int
    completed_projects: int
    unlocked_projects: int
    projects: list[PortfolioProject]


class RunResponse(CamelModel):
    result: GradeResult
    progress: LessonProgress
    hero: HeroStatus


class HintResponse(CamelModel):
    lesson_id: str
    unlocked_hints: list[str]
    total_hints: int
    progress: LessonProgress


class FilesRequest(CamelModel):
    files: dict[str, str]


class NotesRequest(CamelModel):
    notes: str


class FlagRequest(CamelModel):
    flagged: bool


class OracleTurn(CamelModel):
    role: Literal["user", "oracle"]
    text: str


class OracleRequest(CamelModel):
    lesson_id: str
    question: str
    files: dict[str, str] = Field(default_factory=dict)
    last_diagnostics: str = ""
    history: list[OracleTurn] = Field(default_factory=list)


class OracleCitation(CamelModel):
    lesson_id: str
    title: str
    snippet: str
    score: float


class OracleResponse(CamelModel):
    answer: str
    provider: str
    mode: Literal["stub", "offline-rag", "live-llm"] = "stub"
    citations: list[OracleCitation] = Field(default_factory=list)
    cited_sources: list[str] = Field(default_factory=list)
    reasoning_steps: list[str] = Field(default_factory=list)
    guardrail_triggered: bool = False
    latency_ms: int = 0


class RagEvalReport(CamelModel):
    total_queries: int
    recall_at_k: float
    mrr_at_k: float
    zero_leak_verified: bool
    guardrail_block_rate: float
    p50_latency_ms: float
    p95_latency_ms: float


class ChecklistUpdateRequest(CamelModel):
    item_id: str
    checked: bool


class RepoUpdateRequest(CamelModel):
    repo_url: str = ""
    completed: bool | None = None


class ProgressBackupPayload(CamelModel):
    version: str = "1.0"
    exported_at: str = ""
    lessons: list[LessonProgress] = Field(default_factory=list)
    drafts: dict[str, dict[str, str]] = Field(default_factory=dict)
    activity_days: list[str] = Field(default_factory=list)
    projects: list[ProjectProgress] = Field(default_factory=list)
