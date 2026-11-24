from __future__ import annotations

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from pyquest.config import Settings
from pyquest.curriculum.loader import CurriculumLoader, LoadedCurriculum
from pyquest.domain.models import (
    ChecklistUpdateRequest,
    CurriculumResponse,
    FilesRequest,
    FlagRequest,
    HintResponse,
    LessonDetail,
    LessonProgress,
    LessonSpec,
    LessonSummary,
    ModuleGroup,
    NotesRequest,
    OracleRequest,
    OracleResponse,
    PortfolioProject,
    ProgressBackupPayload,
    ProjectsResponse,
    RagEvalReport,
    RepoUpdateRequest,
    RunResponse,
)
from pyquest.persistence.store import ProgressStore
from pyquest.rag.evaluator import evaluate_rag_oracle
from pyquest.rag.interfaces import RagPipeline
from pyquest.rag.pipeline import AgenticRagOracle, build_rag_oracle
from pyquest.runner.grader import PytestGrader


def _build_lesson_summary(
    lesson: LessonSpec,
    progress: LessonProgress,
) -> LessonSummary:
    return LessonSummary(
        id=lesson.id,
        module_id=lesson.module_id,
        module_title=lesson.module_title,
        title=lesson.title,
        objective=lesson.objective,
        mode=lesson.mode,
        kind=lesson.kind,
        runtime=lesson.runtime,
        xp=lesson.xp,
        tags=lesson.tags,
        entry_file=lesson.entry_file,
        status=progress.status,
        attempts=progress.attempts,
        hints_revealed=progress.hints_revealed,
        total_hints=len(lesson.hints),
        flagged=progress.flagged,
        has_notes=bool(progress.notes.strip()),
        solution_revealed=progress.solution_revealed,
        needs_review=progress.needs_review,
    )


def _build_module_groups(
    curriculum: LoadedCurriculum,
    progress_map: dict[str, LessonProgress],
) -> list[ModuleGroup]:
    lessons_by_mod: dict[str, list[LessonSpec]] = {}
    for lesson in curriculum.lessons:
        lessons_by_mod.setdefault(lesson.module_id, []).append(lesson)

    groups: list[ModuleGroup] = []
    for mod in curriculum.modules:
        mod_lessons = lessons_by_mod.get(mod.id, [])
        summaries: list[LessonSummary] = []
        completed = 0
        total_xp = 0
        earned_xp = 0
        for lesson in mod_lessons:
            prog = progress_map.get(lesson.id, LessonProgress(lesson_id=lesson.id))
            summaries.append(_build_lesson_summary(lesson, prog))
            total_xp += lesson.xp
            if prog.status == "COMPLETED":
                completed += 1
                earned_xp += lesson.xp

        groups.append(
            ModuleGroup(
                id=mod.id,
                order=mod.order,
                phase=mod.phase,
                subtitle=mod.subtitle,
                title=mod.title,
                total_lessons=len(mod_lessons),
                completed_lessons=completed,
                total_xp=total_xp,
                earned_xp=earned_xp,
                lessons=summaries,
                insight=mod.insight,
            )
        )
    return groups


def create_app(
    settings: Settings | None = None,
    oracle_service: RagPipeline | None = None,
) -> FastAPI:
    """Build and wire the FastAPI application."""
    cfg = settings or Settings()
    loader = CurriculumLoader(cfg.curriculum_dir)
    curriculum = loader.load()
    store = ProgressStore(cfg.db_path)
    grader = PytestGrader(
        standard_timeout_seconds=cfg.standard_timeout_seconds,
        web_timeout_seconds=cfg.web_timeout_seconds,
    )
    oracle: RagPipeline = oracle_service or build_rag_oracle(curriculum.lessons, cfg)

    app = FastAPI(
        title="Python Terminal Quest API",
        version="0.1.0",
    )

    def _require_lesson(lesson_id: str) -> LessonSpec:
        lesson = curriculum.lessons_by_id.get(lesson_id)
        if lesson is None:
            raise HTTPException(status_code=404, detail=f"Lesson '{lesson_id}' not found")
        return lesson

    @app.get("/api/health")
    def health() -> dict[str, object]:
        return {
            "status": "ok",
            "app": "python-terminal-quest",
            "modules": len(curriculum.modules),
            "lessons": len(curriculum.lessons),
            "demoMode": cfg.demo_mode,
        }

    @app.get("/api/curriculum", response_model=CurriculumResponse)
    def get_curriculum() -> CurriculumResponse:
        state = store.get_progress_state(curriculum.lessons)
        groups = _build_module_groups(curriculum, state.lessons)
        completed_count = 0
        in_progress_count = 0
        not_started_count = 0
        total_xp = 0
        for grp in groups:
            total_xp += grp.total_xp
            for item in grp.lessons:
                if item.status == "COMPLETED":
                    completed_count += 1
                elif item.status == "IN_PROGRESS":
                    in_progress_count += 1
                else:
                    not_started_count += 1

        return CurriculumResponse(
            total_lessons=len(curriculum.lessons),
            completed_lessons=completed_count,
            in_progress_lessons=in_progress_count,
            not_started_lessons=not_started_count,
            total_xp=total_xp,
            earned_xp=state.earned_xp,
            streak=state.streak,
            hero=state.hero,
            modules=groups,
        )

    @app.get("/api/modules/{module_id}", response_model=ModuleGroup)
    def get_module(module_id: str) -> ModuleGroup:
        state = store.get_progress_state(curriculum.lessons)
        for grp in _build_module_groups(curriculum, state.lessons):
            if grp.id == module_id:
                return grp
        raise HTTPException(status_code=404, detail=f"Module '{module_id}' not found")

    @app.get("/api/lessons/{lesson_id}", response_model=LessonDetail)
    def get_lesson(lesson_id: str) -> LessonDetail:
        lesson = _require_lesson(lesson_id)
        progress = store.get_lesson_progress(lesson_id)
        draft = store.get_draft_files(lesson_id)
        files = draft if draft is not None else dict(lesson.starter_files)

        ordered_ids = [item.id for item in curriculum.lessons]
        idx = ordered_ids.index(lesson_id)
        prev_id = ordered_ids[idx - 1] if idx > 0 else None
        next_id = ordered_ids[idx + 1] if idx + 1 < len(ordered_ids) else None

        unlocked = lesson.hints[: progress.hints_revealed]
        return LessonDetail(
            id=lesson.id,
            module_id=lesson.module_id,
            module_title=lesson.module_title,
            title=lesson.title,
            objective=lesson.objective,
            mode=lesson.mode,
            kind=lesson.kind,
            runtime=lesson.runtime,
            xp=lesson.xp,
            tags=lesson.tags,
            entry_file=lesson.entry_file,
            concept_markdown=lesson.concept_markdown,
            files=files,
            test_files=dict(lesson.test_files),
            unlocked_hints=unlocked,
            total_hints=len(lesson.hints),
            progress=progress,
            prev_lesson_id=prev_id,
            next_lesson_id=next_id,
        )

    @app.post("/api/lessons/{lesson_id}/draft")
    def save_draft(lesson_id: str, body: FilesRequest) -> dict[str, object]:
        _require_lesson(lesson_id)
        store.save_draft_files(lesson_id, body.files)
        return {"lessonId": lesson_id, "files": body.files}

    @app.post("/api/lessons/{lesson_id}/run", response_model=RunResponse)
    def run_lesson(lesson_id: str, body: FilesRequest) -> RunResponse:
        lesson = _require_lesson(lesson_id)
        if cfg.demo_mode and body.files != lesson.solution_files:
            raise HTTPException(
                status_code=403,
                detail="Arbitrary code execution is disabled in read-only demo mode.",
            )
        store.save_draft_files(lesson_id, body.files)
        result = grader.grade(lesson, body.files)
        diag_text = result.summary
        if result.diagnostics:
            first = result.diagnostics[0]
            diag_text = f"{first.file}:{first.line} {first.message}"
        progress = store.record_run_attempt(lesson_id, result.passed, diag_text)
        state = store.get_progress_state(curriculum.lessons)
        return RunResponse(result=result, progress=progress, hero=state.hero)

    @app.post("/api/lessons/{lesson_id}/notes", response_model=LessonProgress)
    def save_notes(lesson_id: str, body: NotesRequest) -> LessonProgress:
        _require_lesson(lesson_id)
        return store.save_notes(lesson_id, body.notes)

    @app.post("/api/lessons/{lesson_id}/flag", response_model=LessonProgress)
    def toggle_flag(lesson_id: str, body: FlagRequest) -> LessonProgress:
        _require_lesson(lesson_id)
        return store.set_flagged(lesson_id, body.flagged)

    @app.post("/api/lessons/{lesson_id}/hint", response_model=HintResponse)
    def reveal_hint(lesson_id: str) -> HintResponse:
        lesson = _require_lesson(lesson_id)
        progress = store.reveal_next_hint(lesson_id, len(lesson.hints))
        return HintResponse(
            lesson_id=lesson_id,
            unlocked_hints=lesson.hints[: progress.hints_revealed],
            total_hints=len(lesson.hints),
            progress=progress,
        )

    @app.get("/api/lessons/{lesson_id}/solution")
    def get_solution(lesson_id: str) -> dict[str, object]:
        lesson = _require_lesson(lesson_id)
        store.mark_solution_revealed(lesson_id)
        return {"lessonId": lesson_id, "files": dict(lesson.solution_files)}

    @app.get("/api/progress/export", response_model=ProgressBackupPayload)
    def export_progress() -> ProgressBackupPayload:
        return store.export_backup()

    @app.post("/api/progress/import")
    def import_progress(body: ProgressBackupPayload) -> dict[str, str]:
        if cfg.demo_mode:
            raise HTTPException(
                status_code=403,
                detail="Import is disabled in read-only demo mode.",
            )
        store.import_backup(body)
        return {"status": "restored"}

    @app.post("/api/progress/reset")
    def reset_progress() -> dict[str, str]:
        if cfg.demo_mode:
            raise HTTPException(
                status_code=403,
                detail="Reset is disabled in read-only demo mode.",
            )
        store.reset_all_progress()
        return {"status": "reset"}

    @app.post("/api/lessons/{lesson_id}/reset")
    def reset_lesson(lesson_id: str) -> dict[str, object]:
        lesson = _require_lesson(lesson_id)
        restored = store.reset_draft_files(lesson_id, lesson.starter_files)
        return {"lessonId": lesson_id, "files": restored}

    @app.get("/api/projects", response_model=ProjectsResponse)
    def get_projects() -> ProjectsResponse:
        state = store.get_progress_state(curriculum.lessons)
        groups = _build_module_groups(curriculum, state.lessons)
        completed_mod_ids = {
            g.id for g in groups if g.total_lessons > 0 and g.completed_lessons == g.total_lessons
        }
        materialized: list[PortfolioProject] = []
        for tpl in curriculum.projects:
            prog = store.get_project_progress(tpl.id)
            materialized.append(tpl.materialize(completed_mod_ids, prog))

        return ProjectsResponse(
            total_projects=len(materialized),
            completed_projects=sum(1 for p in materialized if p.progress.status == "COMPLETED"),
            unlocked_projects=sum(1 for p in materialized if p.milestone_unlocked),
            projects=materialized,
        )

    @app.post("/api/projects/{project_id}/checklist", response_model=PortfolioProject)
    def update_project_checklist(project_id: str, body: ChecklistUpdateRequest) -> PortfolioProject:
        tpl = next((p for p in curriculum.projects if p.id == project_id), None)
        if tpl is None:
            raise HTTPException(status_code=404, detail=f"Project '{project_id}' not found")
        total_items = sum(len(sp.items) for sp in tpl.sprints)
        prog = store.update_project_checklist(project_id, body.item_id, body.checked, total_items)
        state = store.get_progress_state(curriculum.lessons)
        groups = _build_module_groups(curriculum, state.lessons)
        completed_mod_ids = {
            g.id for g in groups if g.total_lessons > 0 and g.completed_lessons == g.total_lessons
        }
        return tpl.materialize(completed_mod_ids, prog)

    @app.post("/api/projects/{project_id}/repo", response_model=PortfolioProject)
    def update_project_repo(project_id: str, body: RepoUpdateRequest) -> PortfolioProject:
        tpl = next((p for p in curriculum.projects if p.id == project_id), None)
        if tpl is None:
            raise HTTPException(status_code=404, detail=f"Project '{project_id}' not found")
        prog = store.update_project_repo(project_id, body.repo_url, body.completed)
        state = store.get_progress_state(curriculum.lessons)
        groups = _build_module_groups(curriculum, state.lessons)
        completed_mod_ids = {
            g.id for g in groups if g.total_lessons > 0 and g.completed_lessons == g.total_lessons
        }
        return tpl.materialize(completed_mod_ids, prog)

    @app.post("/api/oracle/ask", response_model=OracleResponse)
    def ask_oracle(body: OracleRequest) -> OracleResponse:
        lesson = _require_lesson(body.lesson_id)
        progress = store.get_lesson_progress(body.lesson_id)
        diag = body.last_diagnostics or progress.last_diagnostics
        if isinstance(oracle, AgenticRagOracle):
            state = store.get_progress_state(curriculum.lessons)
            notes_map = {
                lid: prog.notes for lid, prog in state.lessons.items() if prog.notes.strip()
            }
            return oracle.ask(
                lesson,
                body.question,
                body.files,
                last_diagnostics=diag,
                history=body.history,
                attempts=progress.attempts,
                hints_revealed=progress.hints_revealed,
                learner_notes=notes_map,
            )
        return oracle.ask(lesson, body.question, body.files, last_diagnostics=diag)

    @app.get("/api/oracle/eval", response_model=RagEvalReport)
    def eval_oracle() -> RagEvalReport:
        return evaluate_rag_oracle(curriculum.lessons, oracle)

    # Serve built SPA assets when web/dist exists
    web_dist = cfg.web_dist_dir
    if web_dist.exists() and (web_dist / "index.html").exists():
        assets_dir = web_dist / "assets"
        if assets_dir.exists():
            app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")
        sprites_dir = web_dist / "sprites"
        if sprites_dir.exists():
            app.mount("/sprites", StaticFiles(directory=sprites_dir), name="sprites")

        @app.get("/{full_path:path}", include_in_schema=False)
        def serve_spa(full_path: str) -> FileResponse:
            if full_path.startswith("api/"):
                raise HTTPException(status_code=404, detail="API route not found")
            candidate = (web_dist / full_path).resolve()
            if (
                full_path
                and candidate.is_file()
                and candidate.is_relative_to(web_dist.resolve())
            ):
                return FileResponse(candidate)
            return FileResponse(web_dist / "index.html")

    return app
