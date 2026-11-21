def merge_tenant_flags(
    defaults: dict[str, bool],
    overrides: dict[str, bool],
) -> dict[str, bool]:
    """Return a new dict merging defaults with tenant overrides without mutating inputs."""
    # TODO: use dict union |
    return {}


def enabled_flags_for_env(
    flags: dict[str, dict[str, object]],
    env: str,
) -> dict[str, bool]:
    """Return {flag_name: True} for flags enabled and targeting `env`."""
    # TODO: use a dict comprehension with safe .get() lookups
    return {}


def invert_unique_aliases(aliases: dict[str, str]) -> dict[str, str]:
    """Invert alias -> service_id into service_id -> alias; raise ValueError on duplicate target."""
    # TODO: detect collisions and raise ValueError
    return {}
