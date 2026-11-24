## Beginner Warm-Up 2: Dictionaries & Sets

`dict` gives you O(1) key-value lookups, and `set` removes duplicates and computes overlaps cleanly:

```python
def safe_lookup(scores: dict[str, int], player: str) -> int:
    return scores.get(player, 0)

def unique_sorted_tags(tags: list[str]) -> list[str]:
    return sorted(set(tags))
```

### Challenge
Complete `safe_lookup` and `unique_sorted_tags` in `warmup.py`.
