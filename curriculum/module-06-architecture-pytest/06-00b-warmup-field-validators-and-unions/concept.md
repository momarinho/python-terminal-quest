## Beginner Warm-Up 2: Field Validators & Tagged Models

Normalize fields automatically on validation using `@field_validator`:

```python
from pydantic import BaseModel, field_validator

class TagInput(BaseModel):
    tag: str

    @field_validator("tag")
    @classmethod
    def clean_tag(cls, v: str) -> str:
        cleaned = v.strip().lower()
        if not cleaned:
            raise ValueError("tag cannot be blank")
        return cleaned
```

### Challenge
Complete `TagInput.clean_tag` and `format_action` in `warmup.py`.
