## Concept: Polymorphism & Composition Over Deep Inheritance

Inheritance models **"is-a"** specialization when subclasses share a cohesive contract, whereas **composition** ("has-a") lets an orchestrator combine interchangeable components dynamically at runtime.

### Calling `super().__init__` & Polymorphic Dispatch
```python
class VehicleSensor:
    def __init__(self, sensor_id: str) -> None:
        self.sensor_id = sensor_id

    def read_label(self) -> str:
        return f"sensor:{self.sensor_id}"

class ThermalSensor(VehicleSensor):
    def __init__(self, sensor_id: str, unit: str = "C") -> None:
        super().__init__(sensor_id)
        self.unit = unit

    def read_label(self) -> str:
        return f"thermal:{self.sensor_id}({self.unit})"
```

An orchestrator (`TelemetryUnit`) **composes** a list of `VehicleSensor` objects rather than subclassing `ThermalSensor` + `GpsSensor`!

### Challenge
Implement `NotificationChannel`, `EmailChannel`, `SlackChannel`, and `AlertDispatcher` (composing channels and routing by severity) in `notifier.py`.
