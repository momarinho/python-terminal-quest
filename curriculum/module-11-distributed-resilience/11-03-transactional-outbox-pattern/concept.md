# Transactional Outbox Pattern

Publishing directly to Kafka/RabbitMQ inside an API handler creates the **Dual-Write Problem**:
- Commit DB first, then publish -> if the process crashes or broker times out before publishing, your domain state updated **with no event**.
- Publish first, then commit DB -> if DB rolls back, downstream consumers act on a **phantom event**.

## The Fix: Outbox Table in the Same DB Transaction

1. **Write Phase (`service.py`):** Insert both the domain row (e.g., `shipments`) and an `outbox_events` row (`status = 'PENDING'`) inside the **same database transaction**. If either write fails, both roll back cleanly.
2. **Relay Phase (`relay.py`):** A background worker polls `PENDING` rows, publishes them to the message broker, and marks each delivered row `PUBLISHED`. If the broker fails temporarily, the row stays `PENDING` with an incremented `attempts` count so no event is ever lost.

```python
with conn:
    conn.execute("INSERT INTO shipments (id, tracking) VALUES (?, ?)", (ship_id, code))
    conn.execute(
        "INSERT INTO outbox_events (id, event_type, payload_json) VALUES (?, ?, ?)",
        (f"evt-{ship_id}", "ShipmentDispatched", json.dumps({"shipment_id": ship_id})),
    )
```
