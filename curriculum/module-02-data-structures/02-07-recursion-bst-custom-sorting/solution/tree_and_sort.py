from dataclasses import dataclass


def collect_transitive_deps(graph: dict[str, list[str]], root: str) -> list[str]:
    """Recursively collect all reachable dependencies of `root` (excluding `root`), sorted."""
    visited: set[str] = set()

    def _dfs(node: str) -> None:
        for dep in graph.get(node, ()):
            if dep not in visited:
                visited.add(dep)
                _dfs(dep)

    _dfs(root)
    visited.discard(root)
    return sorted(visited)


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
        def _insert(node: BSTNode | None, val: int) -> BSTNode:
            if node is None:
                return BSTNode(key=val)
            if val < node.key:
                node.left = _insert(node.left, val)
            elif val > node.key:
                node.right = _insert(node.right, val)
            return node

        self.root = _insert(self.root, key)

    def contains(self, key: int) -> bool:
        node = self.root
        while node is not None:
            if key == node.key:
                return True
            node = node.left if key < node.key else node.right
        return False

    def inorder(self) -> list[int]:
        out: list[int] = []

        def _walk(node: BSTNode | None) -> None:
            if node is None:
                return
            _walk(node.left)
            out.append(node.key)
            _walk(node.right)

        _walk(self.root)
        return out


def sort_services(services: list[dict[str, object]]) -> list[dict[str, object]]:
    """Sort services by tier desc, latency_ms asc, and name asc."""
    return sorted(
        services,
        key=lambda s: (-int(s["tier"]), int(s["latency_ms"]), str(s["name"])),
    )
