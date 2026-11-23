from __future__ import annotations

import json
import sqlite3
from collections.abc import Iterator
from contextlib import contextmanager, suppress
from datetime import UTC, date, datetime, timedelta
from pathlib import Path

from pyquest.domain.models import (
    HeroStatus,
    LessonProgress,
    LessonSpec,
    LessonStatus,
    ProgressBackupPayload,
    ProgressState,
    ProjectProgress,
    ProjectStatus,
    StreakStats,
)

HERO_TIERS: list[tuple[int, int, str, str]] = [
    (1, 0, "Apprentice", "Wood Sword & Morning Coffee"),
    (2, 3, "Explorer", "Hooded Cloak & Cyan Rune"),
    (3, 6, "Async Knight", "Visor Helm & Concurrency Sparks"),
    (4, 9, "Backend Architect", "Gilded Mantle & Rune Tome"),
    (5, 12, "AI Grandmaster", "Emerald-Gold Crown & Aura"),
]


def _utc_now_iso() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds")


def compute_hero_status(
    completed_modules: int,
    completed_lessons: int,
    earned_xp: int,
) -> HeroStatus:
    """Compute the 5-tier RPG Hero Companion status from completed modules."""
    current = HERO_TIERS[0]
    next_spec: tuple[int, int, str, str] | None = HERO_TIERS[1]
    for idx, tier_spec in enumerate(HERO_TIERS):
        if completed_modules >= tier_spec[1]:
            current = tier_spec
            next_spec = HERO_TIERS[idx + 1] if idx + 1 < len(HERO_TIERS) else None

    return HeroStatus(
        tier=current[0],
        title=current[2],
        subtitle=current[3],
        completed_modules=completed_modules,
        completed_lessons=completed_lessons,
        earned_xp=earned_xp,
        next_tier=next_spec[0] if next_spec else None,
        next_tier_title=next_spec[2] if next_spec else None,
        modules_for_next_tier=next_spec[1] if next_spec else current[1],
    )


class ProgressStore:
    """SQLite persistence for lesson progress, multi-file drafts, notes, flags, streaks, and projects."""

    def __init__(self, db_path: Path) -> None:
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_schema()

    @contextmanager
    def _connect(self) -> Iterator[sqlite3.Connection]:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        finally:
            conn.close()

    def _init_schema(self) -> None:
        with self._connect() as conn:
            conn.execute("PRAGMA journal_mode=WAL")
            conn.executescript(
                """
                CREATE TABLE IF NOT EXISTS lesson_progress (
                    lesson_id TEXT PRIMARY KEY,
                    status TEXT NOT NULL DEFAULT 'NOT_STARTED',
                    attempts INTEGER NOT NULL DEFAULT 0,
                    hints_revealed INTEGER NOT NULL DEFAULT 0,
                    last_diagnostics TEXT NOT NULL DEFAULT '',
                    notes TEXT NOT NULL DEFAULT '',
                    flagged INTEGER NOT NULL DEFAULT 0,
                    solution_revealed INTEGER NOT NULL DEFAULT 0,
                    completed_at TEXT NOT NULL DEFAULT '',
                    updated_at TEXT NOT NULL DEFAULT ''
                );

                CREATE TABLE IF NOT EXISTS lesson_drafts (
                    lesson_id TEXT PRIMARY KEY,
                    files_json TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS activity_days (
                    day_iso TEXT PRIMARY KEY
                );

                CREATE TABLE IF NOT EXISTS project_progress (
                    project_id TEXT PRIMARY KEY,
                    status TEXT NOT NULL DEFAULT 'NOT_STARTED',
                    completed_checklist_json TEXT NOT NULL DEFAULT '[]',
                    repo_url TEXT NOT NULL DEFAULT '',
                    updated_at TEXT NOT NULL DEFAULT ''
                );
                """
            )
            for ddl in (
                "ALTER TABLE lesson_progress ADD COLUMN solution_revealed INTEGER NOT NULL DEFAULT 0",
                "ALTER TABLE lesson_progress ADD COLUMN completed_at TEXT NOT NULL DEFAULT ''",
            ):
                with suppress(sqlite3.OperationalError):
                    conn.execute(ddl)

    def get_lesson_progress(self, lesson_id: str) -> LessonProgress:
        with self._connect() as conn:
            row = conn.execute(
                "SELECT * FROM lesson_progress WHERE lesson_id = ?",
                (lesson_id,),
            ).fetchone()
        if row is None:
            return LessonProgress(lesson_id=lesson_id)
        return self._row_to_lesson_progress(row)

    def list_lesson_progress(self) -> dict[str, LessonProgress]:
        with self._connect() as conn:
            rows = conn.execute("SELECT * FROM lesson_progress").fetchall()
        return {row["lesson_id"]: self._row_to_lesson_progress(row) for row in rows}

    def get_draft_files(self, lesson_id: str) -> dict[str, str] | None:
        with self._connect() as conn:
            row = conn.execute(
                "SELECT files_json FROM lesson_drafts WHERE lesson_id = ?",
                (lesson_id,),
            ).fetchone()
        if row is None:
            return None
        loaded = json.loads(row["files_json"])
        if not isinstance(loaded, dict):
            return None
        return {str(k): str(v) for k, v in loaded.items()}

    def save_draft_files(self, lesson_id: str, files: dict[str, str]) -> None:
        now = _utc_now_iso()
        payload = json.dumps(files)
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO lesson_drafts (lesson_id, files_json, updated_at)
                VALUES (?, ?, ?)
                ON CONFLICT(lesson_id) DO UPDATE SET
                    files_json = excluded.files_json,
                    updated_at = excluded.updated_at
                """,
                (lesson_id, payload, now),
            )
            conn.execute(
                """
                INSERT INTO lesson_progress (lesson_id, status, updated_at)
                VALUES (?, 'IN_PROGRESS', ?)
                ON CONFLICT(lesson_id) DO UPDATE SET
                    status = CASE
                        WHEN lesson_progress.status = 'NOT_STARTED' THEN 'IN_PROGRESS'
                        ELSE lesson_progress.status
                    END,
                    updated_at = excluded.updated_at
                """,
                (lesson_id, now),
            )

    def reset_draft_files(self, lesson_id: str, starter_files: dict[str, str]) -> dict[str, str]:
        now = _utc_now_iso()
        payload = json.dumps(starter_files)
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO lesson_drafts (lesson_id, files_json, updated_at)
                VALUES (?, ?, ?)
                ON CONFLICT(lesson_id) DO UPDATE SET
                    files_json = excluded.files_json,
                    updated_at = excluded.updated_at
                """,
                (lesson_id, payload, now),
            )
            conn.execute(
                """
                UPDATE lesson_progress
                SET hints_revealed = 0,
                    solution_revealed = 0,
                    updated_at = ?
                WHERE lesson_id = ?
                """,
                (now, lesson_id),
            )
        return dict(starter_files)

    def mark_solution_revealed(self, lesson_id: str) -> LessonProgress:
        now = _utc_now_iso()
        with self._connect() as conn:
            existing = conn.execute(
                "SELECT status FROM lesson_progress WHERE lesson_id = ?",
                (lesson_id,),
            ).fetchone()
            if existing is None:
                conn.execute(
                    """
                    INSERT INTO lesson_progress (lesson_id, status, solution_revealed, updated_at)
                    VALUES (?, 'IN_PROGRESS', 1, ?)
                    """,
                    (lesson_id, now),
                )
            elif existing["status"] != "COMPLETED":
                conn.execute(
                    """
                    UPDATE lesson_progress
                    SET solution_revealed = 1,
                        updated_at = ?
                    WHERE lesson_id = ?
                    """,
                    (now, lesson_id),
                )
            row = conn.execute(
                "SELECT * FROM lesson_progress WHERE lesson_id = ?",
                (lesson_id,),
            ).fetchone()
        assert row is not None
        return self._row_to_lesson_progress(row)

    def record_run_attempt(
        self,
        lesson_id: str,
        passed: bool,
        diagnostics_summary: str,
    ) -> LessonProgress:
        now = _utc_now_iso()
        today_iso = date.today().isoformat()
        with self._connect() as conn:
            existing = conn.execute(
                "SELECT * FROM lesson_progress WHERE lesson_id = ?",
                (lesson_id,),
            ).fetchone()
            attempts = (int(existing["attempts"]) if existing else 0) + 1
            prev_status: LessonStatus = existing["status"] if existing else "NOT_STARTED"
            next_status: LessonStatus = (
                "COMPLETED" if (passed or prev_status == "COMPLETED") else "IN_PROGRESS"
            )
            existing_completed_at = str(existing["completed_at"]) if existing else ""
            completed_at = now if passed else existing_completed_at
            conn.execute(
                """
                INSERT INTO lesson_progress (
                    lesson_id, status, attempts, last_diagnostics, completed_at, updated_at
                )
                VALUES (?, ?, ?, ?, ?, ?)
                ON CONFLICT(lesson_id) DO UPDATE SET
                    status = excluded.status,
                    attempts = excluded.attempts,
                    last_diagnostics = excluded.last_diagnostics,
                    completed_at = excluded.completed_at,
                    updated_at = excluded.updated_at
                """,
                (lesson_id, next_status, attempts, diagnostics_summary, completed_at, now),
            )
            if passed:
                conn.execute(
                    "INSERT OR IGNORE INTO activity_days (day_iso) VALUES (?)",
                    (today_iso,),
                )
            row = conn.execute(
                "SELECT * FROM lesson_progress WHERE lesson_id = ?",
                (lesson_id,),
            ).fetchone()
        assert row is not None
        return self._row_to_lesson_progress(row)

    def reveal_next_hint(self, lesson_id: str, total_hints: int) -> LessonProgress:
        now = _utc_now_iso()
        with self._connect() as conn:
            existing = conn.execute(
                "SELECT hints_revealed FROM lesson_progress WHERE lesson_id = ?",
                (lesson_id,),
            ).fetchone()
            current = int(existing["hints_revealed"]) if existing else 0
            next_count = min(total_hints, current + 1)
            conn.execute(
                """
                INSERT INTO lesson_progress (lesson_id, hints_revealed, updated_at)
                VALUES (?, ?, ?)
                ON CONFLICT(lesson_id) DO UPDATE SET
                    hints_revealed = excluded.hints_revealed,
                    updated_at = excluded.updated_at
                """,
                (lesson_id, next_count, now),
            )
            row = conn.execute(
                "SELECT * FROM lesson_progress WHERE lesson_id = ?",
                (lesson_id,),
            ).fetchone()
        assert row is not None
        return self._row_to_lesson_progress(row)

    def save_notes(self, lesson_id: str, notes: str) -> LessonProgress:
        now = _utc_now_iso()
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO lesson_progress (lesson_id, notes, updated_at)
                VALUES (?, ?, ?)
                ON CONFLICT(lesson_id) DO UPDATE SET
                    notes = excluded.notes,
                    updated_at = excluded.updated_at
                """,
                (lesson_id, notes, now),
            )
            row = conn.execute(
                "SELECT * FROM lesson_progress WHERE lesson_id = ?",
                (lesson_id,),
            ).fetchone()
        assert row is not None
        return self._row_to_lesson_progress(row)

    def set_flagged(self, lesson_id: str, flagged: bool) -> LessonProgress:
        now = _utc_now_iso()
        flag_int = 1 if flagged else 0
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO lesson_progress (lesson_id, flagged, updated_at)
                VALUES (?, ?, ?)
                ON CONFLICT(lesson_id) DO UPDATE SET
                    flagged = excluded.flagged,
                    updated_at = excluded.updated_at
                """,
                (lesson_id, flag_int, now),
            )
            row = conn.execute(
                "SELECT * FROM lesson_progress WHERE lesson_id = ?",
                (lesson_id,),
            ).fetchone()
        assert row is not None
        return self._row_to_lesson_progress(row)

    def get_streak(self, today: date | None = None) -> StreakStats:
        today_date = today or date.today()
        with self._connect() as conn:
            rows = conn.execute("SELECT day_iso FROM activity_days ORDER BY day_iso ASC").fetchall()
        days = sorted({date.fromisoformat(row["day_iso"]) for row in rows})
        if not days:
            return StreakStats()

        day_set = set(days)
        active_today = today_date in day_set

        # Current streak counts backwards from today if active today, else yesterday
        cursor = today_date if active_today else (today_date - timedelta(days=1))
        current_streak = 0
        while cursor in day_set:
            current_streak += 1
            cursor -= timedelta(days=1)

        # Longest streak across all recorded days
        longest = 1
        run = 1
        for prev_day, curr_day in zip(days, days[1:], strict=False):
            if (curr_day - prev_day).days == 1:
                run += 1
                longest = max(longest, run)
            else:
                run = 1

        return StreakStats(
            current_streak_days=current_streak,
            longest_streak_days=longest,
            active_today=active_today,
            active_days_total=len(days),
        )

    def get_progress_state(self, lessons: list[LessonSpec]) -> ProgressState:
        progress_map = self.list_lesson_progress()
        completed_ids: list[str] = []
        earned_xp = 0
        lessons_by_mod: dict[str, list[LessonSpec]] = {}

        for lesson in lessons:
            lessons_by_mod.setdefault(lesson.module_id, []).append(lesson)
            prog = progress_map.get(lesson.id)
            if prog and prog.status == "COMPLETED":
                completed_ids.append(lesson.id)
                earned_xp += lesson.xp

        completed_modules = 0
        for mod_lessons in lessons_by_mod.values():
            if mod_lessons and all(
                (p := progress_map.get(item.id)) is not None and p.status == "COMPLETED"
                for item in mod_lessons
            ):
                completed_modules += 1

        streak = self.get_streak()
        hero = compute_hero_status(
            completed_modules=completed_modules,
            completed_lessons=len(completed_ids),
            earned_xp=earned_xp,
        )
        return ProgressState(
            completed_lessons=completed_ids,
            earned_xp=earned_xp,
            streak=streak,
            hero=hero,
            lessons=progress_map,
        )

    def get_project_progress(self, project_id: str) -> ProjectProgress:
        with self._connect() as conn:
            row = conn.execute(
                "SELECT * FROM project_progress WHERE project_id = ?",
                (project_id,),
            ).fetchone()
        if row is None:
            return ProjectProgress(project_id=project_id)
        return self._row_to_project_progress(row)

    def update_project_checklist(
        self,
        project_id: str,
        item_id: str,
        checked: bool,
        total_items: int,
    ) -> ProjectProgress:
        current = self.get_project_progress(project_id)
        items = set(current.completed_checklist_ids)
        if checked:
            items.add(item_id)
        else:
            items.discard(item_id)

        sorted_items = sorted(items)
        status: ProjectStatus = current.status
        if status != "COMPLETED":
            status = "IN_PROGRESS" if sorted_items else "NOT_STARTED"
        if total_items > 0 and len(sorted_items) >= total_items and current.repo_url.strip():
            status = "COMPLETED"

        now = _utc_now_iso()
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO project_progress (project_id, status, completed_checklist_json, repo_url, updated_at)
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(project_id) DO UPDATE SET
                    status = excluded.status,
                    completed_checklist_json = excluded.completed_checklist_json,
                    updated_at = excluded.updated_at
                """,
                (project_id, status, json.dumps(sorted_items), current.repo_url, now),
            )
            row = conn.execute(
                "SELECT * FROM project_progress WHERE project_id = ?",
                (project_id,),
            ).fetchone()
        assert row is not None
        return self._row_to_project_progress(row)

    def update_project_repo(
        self,
        project_id: str,
        repo_url: str,
        completed: bool | None = None,
    ) -> ProjectProgress:
        current = self.get_project_progress(project_id)
        cleaned_url = repo_url.strip()
        status: ProjectStatus = current.status
        if completed is True:
            status = "COMPLETED"
        elif completed is False:
            status = "IN_PROGRESS" if (current.completed_checklist_ids or cleaned_url) else "NOT_STARTED"
        elif cleaned_url and status == "NOT_STARTED":
            status = "IN_PROGRESS"

        now = _utc_now_iso()
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO project_progress (project_id, status, completed_checklist_json, repo_url, updated_at)
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(project_id) DO UPDATE SET
                    status = excluded.status,
                    repo_url = excluded.repo_url,
                    updated_at = excluded.updated_at
                """,
                (
                    project_id,
                    status,
                    json.dumps(current.completed_checklist_ids),
                    cleaned_url,
                    now,
                ),
            )
            row = conn.execute(
                "SELECT * FROM project_progress WHERE project_id = ?",
                (project_id,),
            ).fetchone()
        assert row is not None
        return self._row_to_project_progress(row)

    def export_backup(self) -> ProgressBackupPayload:
        with self._connect() as conn:
            lesson_rows = conn.execute("SELECT * FROM lesson_progress ORDER BY lesson_id").fetchall()
            draft_rows = conn.execute("SELECT lesson_id, files_json FROM lesson_drafts ORDER BY lesson_id").fetchall()
            day_rows = conn.execute("SELECT day_iso FROM activity_days ORDER BY day_iso").fetchall()
            project_rows = conn.execute("SELECT * FROM project_progress ORDER BY project_id").fetchall()

        drafts: dict[str, dict[str, str]] = {}
        for row in draft_rows:
            loaded = json.loads(row["files_json"] or "{}")
            if isinstance(loaded, dict):
                drafts[str(row["lesson_id"])] = {str(k): str(v) for k, v in loaded.items()}

        return ProgressBackupPayload(
            exported_at=_utc_now_iso(),
            lessons=[self._row_to_lesson_progress(r) for r in lesson_rows],
            drafts=drafts,
            activity_days=[str(r["day_iso"]) for r in day_rows],
            projects=[self._row_to_project_progress(r) for r in project_rows],
        )

    def import_backup(self, payload: ProgressBackupPayload) -> None:
        now = _utc_now_iso()
        with self._connect() as conn:
            for lp in payload.lessons:
                conn.execute(
                    """
                    INSERT INTO lesson_progress (
                        lesson_id, status, attempts, hints_revealed, last_diagnostics,
                        notes, flagged, solution_revealed, completed_at, updated_at
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ON CONFLICT(lesson_id) DO UPDATE SET
                        status = excluded.status,
                        attempts = excluded.attempts,
                        hints_revealed = excluded.hints_revealed,
                        last_diagnostics = excluded.last_diagnostics,
                        notes = excluded.notes,
                        flagged = excluded.flagged,
                        solution_revealed = excluded.solution_revealed,
                        completed_at = excluded.completed_at,
                        updated_at = excluded.updated_at
                    """,
                    (
                        lp.lesson_id,
                        lp.status,
                        lp.attempts,
                        lp.hints_revealed,
                        lp.last_diagnostics,
                        lp.notes,
                        1 if lp.flagged else 0,
                        1 if lp.solution_revealed else 0,
                        lp.completed_at,
                        lp.updated_at or now,
                    ),
                )
            for lesson_id, files in payload.drafts.items():
                conn.execute(
                    """
                    INSERT INTO lesson_drafts (lesson_id, files_json, updated_at)
                    VALUES (?, ?, ?)
                    ON CONFLICT(lesson_id) DO UPDATE SET
                        files_json = excluded.files_json,
                        updated_at = excluded.updated_at
                    """,
                    (lesson_id, json.dumps(files), now),
                )
            for day_iso in payload.activity_days:
                conn.execute("INSERT OR IGNORE INTO activity_days (day_iso) VALUES (?)", (day_iso,))
            for proj in payload.projects:
                conn.execute(
                    """
                    INSERT INTO project_progress (
                        project_id, status, completed_checklist_json, repo_url, updated_at
                    )
                    VALUES (?, ?, ?, ?, ?)
                    ON CONFLICT(project_id) DO UPDATE SET
                        status = excluded.status,
                        completed_checklist_json = excluded.completed_checklist_json,
                        repo_url = excluded.repo_url,
                        updated_at = excluded.updated_at
                    """,
                    (
                        proj.project_id,
                        proj.status,
                        json.dumps(proj.completed_checklist_ids),
                        proj.repo_url,
                        proj.updated_at or now,
                    ),
                )

    def reset_all_progress(self) -> None:
        with self._connect() as conn:
            conn.execute("DELETE FROM lesson_progress")
            conn.execute("DELETE FROM lesson_drafts")
            conn.execute("DELETE FROM activity_days")
            conn.execute("DELETE FROM project_progress")

    def _row_to_lesson_progress(self, row: sqlite3.Row) -> LessonProgress:
        hints_revealed = int(row["hints_revealed"])
        solution_revealed = bool(row["solution_revealed"])
        flagged = bool(row["flagged"])
        status: LessonStatus = row["status"]
        needs_review = status == "COMPLETED" and (hints_revealed > 0 or solution_revealed or flagged)
        return LessonProgress(
            lesson_id=str(row["lesson_id"]),
            status=status,
            attempts=int(row["attempts"]),
            hints_revealed=hints_revealed,
            last_diagnostics=str(row["last_diagnostics"]),
            notes=str(row["notes"]),
            flagged=flagged,
            solution_revealed=solution_revealed,
            completed_at=str(row["completed_at"]),
            needs_review=needs_review,
            updated_at=str(row["updated_at"]),
        )

    def _row_to_project_progress(self, row: sqlite3.Row) -> ProjectProgress:
        checklist = json.loads(row["completed_checklist_json"] or "[]")
        return ProjectProgress(
            project_id=str(row["project_id"]),
            status=row["status"],
            completed_checklist_ids=[str(x) for x in checklist],
            repo_url=str(row["repo_url"]),
            updated_at=str(row["updated_at"]),
        )
