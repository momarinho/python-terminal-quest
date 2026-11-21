from __future__ import annotations

from collections import deque
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Literal

TaskState = Literal["PENDING", "RETRY", "SUCCESS", "FAILURE"]


@dataclass
class TaskRecord:
    task_id: str
    payload: dict[str, object]
    state: TaskState = "PENDING"
    attempts: int = 0
    result: object | None = None
    last_error: str = ""
    retry_delays: list[float] = field(default_factory=list)


class TaskQueueWorker:
    """In-memory Celery-like worker separating broker queue from result backend state."""

    def __init__(
        self,
        handler: Callable[[dict[str, object]], object],
        *,
        max_retries: int = 2,
        acks_late: bool = True,
        base_delay: float = 0.5,
        max_delay: float = 8.0,
    ) -> None:
        self._handler = handler
        self._max_retries = max_retries
        self._acks_late = acks_late
        self._base_delay = base_delay
        self._max_delay = max_delay
        self.broker_queue: deque[str] = deque()
        self.results_backend: dict[str, TaskRecord] = {}

    def enqueue(self, task_id: str, payload: dict[str, object]) -> TaskRecord:
        record = TaskRecord(task_id=task_id, payload=dict(payload), state="PENDING")
        self.results_backend[task_id] = record
        self.broker_queue.append(task_id)
        return record

    def run_next(self) -> TaskRecord | None:
        """Consume one queued task honoring acks_late, exponential backoff retries, and result states."""
        # TODO:
        # 1. Inspect / pop next task_id from broker_queue (keep queued until acked if acks_late=True)
        # 2. Run handler(record.payload); on success -> state='SUCCESS', record.result=res, ack
        # 3. On exception -> increment attempts; if attempts <= max_retries mark 'RETRY', append backoff
        #    min(max_delay, base_delay * (2 ** (attempts - 1))) and requeue; else mark 'FAILURE'
        raise NotImplementedError("TODO: TaskQueueWorker.run_next")
