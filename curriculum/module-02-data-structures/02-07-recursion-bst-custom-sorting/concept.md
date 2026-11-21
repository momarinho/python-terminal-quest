## Concept: Recursion, Binary Search Trees & Multi-Key Sorting

Tree-shaped structures—such as nested service dependencies, JSON ASTs, and ordered search indexes—map naturally to recursion.

### Recursive Traversal & Binary Search Trees (BST)
In a **Binary Search Tree**, every node's left subtree holds strictly smaller keys, and its right subtree holds strictly larger keys:
* **Insert:** Recurse left if `key < node.key`, right if `key > node.key`, or update/skip if equal.
* **In-order traversal (`left -> node -> right`):** Yields all keys in **sorted ascending order**.

```python
def sum_directory_bytes(node: dict[str, object]) -> int:
    total = int(node.get("bytes", 0))
    for child in node.get("children", []):
        total += sum_directory_bytes(child)
    return total
```

### Multi-Key Custom Sorting
Sort complex objects cleanly by returning a tuple from `key=`, e.g., `key=lambda item: (-item["priority"], item["name"])`.

### Challenge
Implement `collect_transitive_deps`, `MetricBST` (`insert`, `contains`, `inorder`), and `sort_services` in `tree_and_sort.py`.
