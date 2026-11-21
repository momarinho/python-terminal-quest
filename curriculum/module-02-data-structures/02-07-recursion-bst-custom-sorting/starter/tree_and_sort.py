from dataclasses import dataclass


def collect_transitive_deps(graph: dict[str, list[str]], root: str) -> list[str]:
    """Recursively collect all reachable dependencies of `root` (excluding `root`), sorted."""
    # TODO: recursive DFS with cycle-safe visited set
    return []


@dataclass
class BSTNode:
    key: int
    left: "BSTNode | None" = None
    right: "BSTNode | None" = None


class MetricBST:
    """Binary Search Tree storing unique integer latency buckets."""

    def __init__(self) -> None:
        self.root: BSTNode | None = None

    def insert(self, key: int) -> None:
        # TODO: insert key maintaining BST invariant
        pass

    def contains(self, key: int) -> bool:
        # TODO: search BST for key
        return False

    def inorder(self) -> list[int]:
        # TODO: return sorted keys via left -> root -> right traversal
        return []


def sort_services(services: list[dict[str, object]]) -> list[dict[str, object]]:
    """Sort services by tier desc, latency_ms asc, and name asc."""
    # TODO: sorted(..., key=...)
    return []
