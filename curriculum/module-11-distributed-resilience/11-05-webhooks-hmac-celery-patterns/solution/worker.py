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
        if not self.broker_queue:
            return None

        task_id = self.broker_queue[0] if self._acks_late else self.broker_queue.popleft()
        record = self.results_backend[task_id]

        try:
            output = self._handler(record.payload)
        except BaseException as exc:
            if self._acks_late and self.broker_queue and self.broker_queue[0] == task_id:
                self.broker_queue.popleft()
            record.attempts += 1
            record.last_error = str(exc)
            if isinstance(exc, Exception) and record.attempts <= self._max_retries:
                delay = float(min(self._max_delay, self._base_delay * (2 ** (record.attempts - 1))))
                record.state = "RETRY"
                record.retry_delays.append(delay)
                self.broker_queue.append(task_id)
            else:
                record.state = "FAILURE"
            return record

        if self._acks_late and self.broker_queue and self.broker_queue[0] == task_id:
            self.broker_queue.popleft()
        record.attempts += 1
        record.state = "SUCCESS"
        record.result = output
        record.last_error = ""
        return record
