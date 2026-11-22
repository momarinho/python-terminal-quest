def merge_tenant_flags(
    defaults: dict[str, bool],
    overrides: dict[str, bool],
) -> dict[str, bool]:
    """Return a new dict merging defaults with tenant overrides without mutating inputs."""
    return defaults | overrides


def enabled_flags_for_env(
    flags: dict[str, dict[str, object]],
    env: str,
) -> dict[str, bool]:
    """Return {flag_name: True} for flags enabled and targeting `env`."""
    return {
        name: True
        for name, cfg in flags.items()
        if bool(cfg.get("enabled", False)) and env in (cfg.get("envs") or ())
    }


def invert_unique_aliases(aliases: dict[str, str]) -> dict[str, str]:
    """Invert alias -> service_id into service_id -> alias; raise ValueError on duplicate target."""
    inverted: dict[str, str] = {}
    for alias, service_id in aliases.items():
        if service_id in inverted:
            raise ValueError(f"Duplicate target service_id: {service_id}")
        inverted[service_id] = alias
    return inverted


def diff_flag_snapshots(
    before: dict[str, bool],
    after: dict[str, bool],
) -> dict[str, tuple[bool | None, bool | None]]:
    """Return {flag: (old_val, new_val)} sorted by flag name for keys that were added, removed, or changed."""
    return {
        key: (before.get(key), after.get(key))
        for key in sorted(before.keys() | after.keys())
        if before.get(key) != after.get(key)
    }
