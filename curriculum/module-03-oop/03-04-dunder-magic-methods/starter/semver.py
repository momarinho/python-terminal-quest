from collections.abc import Iterator
from functools import total_ordering


@total_ordering
class SemVer:
    def __init__(self, major: int, minor: int, patch: int) -> None:
        if major < 0 or minor < 0 or patch < 0:
            raise ValueError("SemVer components must be non-negative")
        self.major = major
        self.minor = minor
        self.patch = patch

    @classmethod
    def parse(cls, raw: str) -> "SemVer":
        """Parse 'v1.2.3' or '1.2.3' into SemVer; raise ValueError on malformed versions."""
        raise NotImplementedError

    def bump(self, part: str) -> "SemVer":
        """Return a new SemVer bumping 'major', 'minor', or 'patch'; raise ValueError otherwise."""
        raise NotImplementedError

    def __repr__(self) -> str:
        return ""

    def __str__(self) -> str:
        return ""

    def __eq__(self, other: object) -> bool:
        return False

    def __lt__(self, other: object) -> bool:
        return False

    def __hash__(self) -> int:
        return 0


class ReleaseQueue:
    """Iterable collection yielding unique SemVer releases in ascending order."""

    def __init__(self) -> None:
        self._versions: set[SemVer] = set()

    def add(self, version: SemVer) -> None:
        self._versions.add(version)

    def __len__(self) -> int:
        return 0

    def __contains__(self, item: object) -> bool:
        return False

    def __iter__(self) -> Iterator[SemVer]:
        return iter(())
