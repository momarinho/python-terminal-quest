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

    def __repr__(self) -> str:
        # TODO: return 'SemVer(major, minor, patch)'
        return ""

    def __str__(self) -> str:
        # TODO: return 'major.minor.patch'
        return ""

    def __eq__(self, other: object) -> bool:
        # TODO: return NotImplemented for non-SemVer, else tuple equality
        return False

    def __lt__(self, other: object) -> bool:
        # TODO: return NotImplemented for non-SemVer, else tuple comparison
        return False

    def __hash__(self) -> int:
        # TODO: hash the (major, minor, patch) tuple
        return 0


class ReleaseQueue:
    """Iterable collection yielding unique SemVer releases in ascending order."""

    def __init__(self) -> None:
        self._versions: set[SemVer] = set()

    def add(self, version: SemVer) -> None:
        self._versions.add(version)

    def __len__(self) -> int:
        # TODO: return number of queued unique versions
        return 0

    def __iter__(self) -> Iterator[SemVer]:
        # TODO: yield sorted versions
        return iter(())
