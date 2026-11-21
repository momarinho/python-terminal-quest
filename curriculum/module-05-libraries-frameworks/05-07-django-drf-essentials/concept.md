# Django & DRF Essentials — Serializers, APIView & Zero-N+1 QuerySets

While Flask gives you minimal routing and FastAPI pairs natively with Pydantic v2 + SQLAlchemy 2.0, **Django + Django REST Framework (DRF)** dominates batteries-included Python monoliths (built-in ORM, migrations, Admin, auth, and Serializers).

## Django/DRF vs. FastAPI + SQLAlchemy 2.0

| Concern | Django + DRF | FastAPI + SQLAlchemy 2.0 |
|---|---|---|
| Validation & Output DTO | `serializers.Serializer` / `ModelSerializer` | Pydantic v2 `BaseModel` |
| Endpoint Handler | `APIView` / `ViewSet` | `@app.get` / `APIRouter` |
| Eager-load ForeignKey (1:1/N:1) | `.select_related("parent")` | `joinedload(Child.parent)` |
| Eager-load Reverse/M2M (1:N) | `.prefetch_related("items")` | `selectinload(Parent.items)` |

## Preventing Silent N+1 Queries in DRF

If a serializer accesses `source="department.title"` on 20 employees without `select_related("department")`, Django fires **21 SQL queries** (`1 + N`). Wrapping the QuerySet with `.select_related("department")` performs a single SQL `JOIN`:

```python
from rest_framework import serializers

class EmployeeSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source="department.name", read_only=True)

    def validate_salary_cents(self, value: int) -> int:
        if value <= 0:
            raise serializers.ValidationError("salary_cents must be positive")
        return value
```

Use `django.test.utils.CaptureQueriesContext(connection)` in tests to enforce a hard SQL query budget!
