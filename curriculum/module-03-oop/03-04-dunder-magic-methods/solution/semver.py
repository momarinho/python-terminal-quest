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

    def _key(self) -> tuple[int, int, int]:
        return (self.major, self.minor, self.patch)

    def __repr__(self) -> str:
        return f"SemVer({self.major}, {self.minor}, {self.patch})"

    def __str__(self) -> str:
        return f"{self.major}.{self.minor}.{self.patch}"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, SemVer):
            return NotImplemented
        return self._key() == other._key()

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, SemVer):
            return NotImplemented
        return self._key() < other._key()

    def __hash__(self) -> int:
        return hash(self._key())


class ReleaseQueue:
    """Iterable collection yielding unique SemVer releases in ascending order."""

    def __init__(self) -> None:
        self._versions: set[SemVer] = set()

    def add(self, version: SemVer) -> None:
        self._versions.add(version)

    def __len__(self) -> int:
        return len(self._versions)

    def __iter__(self) -> Iterator[SemVer]:
        return iter(sorted(self._versions))
