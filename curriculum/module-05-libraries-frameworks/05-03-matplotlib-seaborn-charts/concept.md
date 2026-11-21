## Concept: Headless Chart Generation (`Agg`, Matplotlib & Seaborn)

In backend services, cron jobs, and CI pipelines there is **no display server** (no X11/Wayland). Calling `plt.show()` crashes or hangs unless you configure a non-interactive raster backend like `"Agg"`.

### Headless Best Practices
1. Set `matplotlib.use("Agg")` **before** importing `matplotlib.pyplot` or `seaborn`.
2. Use the object-oriented `fig, ax = plt.subplots(...)` API rather than global `plt.bar(...)` state.
3. Always call `plt.close(fig)` inside a `finally:` block so repeated report runs don't leak memory!

```python
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

def save_rainfall_chart(months: list[str], mm: list[float], out_path: Path) -> Path:
    fig, ax = plt.subplots(figsize=(6, 4))
    try:
        sns.barplot(x=months, y=mm, ax=ax)
        ax.set_title("Monthly Rainfall")
        fig.tight_layout()
        out_path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(out_path, dpi=120)
        return out_path
    finally:
        plt.close(fig)
```

### Challenge
Implement `render_latency_chart(services, p95_ms, output_path, title=...)` in `chart_builder.py` using the `Agg` backend, Seaborn `barplot`, labeled axes/title, and guaranteed `plt.close(fig)` cleanup.
