# 09 - Union-find (disjoint set)

Union-find answers one question fast: "are these two things in the same group, and
if not, merge their groups." It maintains a partition of elements into disjoint sets
and supports exactly two operations, `find` (which set is x in) and `union` (merge
two sets). With its two standard optimizations it does both in near-constant
amortized time, which makes it the right tool for connectivity that grows as edges
arrive, counting connected components, and detecting a cycle in an undirected graph.

![A disjoint-set forest with two trees and their roots](../assets/union-find.svg)

*A disjoint-set forest: find follows parents to the root; two nodes are connected iff they share a root.*

## What it is

The structure is a **forest of trees**, one tree per set, where each element points
at a parent and the root of a tree is the set's representative (its "name"). Two
elements are in the same set exactly when they climb to the same root. Initially
every element is its own parent, so there are n singleton sets.

`find(x)` walks parent pointers up to the root. `union(x, y)` finds both roots and
points one at the other, merging the two trees into one. That is the whole idea. The
subtlety, and the reason union-find is famous, is that naive versions degrade into
long chains that make `find` O(n). The two optimizations below keep the trees flat.

- **Path compression** (in `find`): after finding the root, repoint every node on the
  path directly at the root, so the next `find` is O(1). Each `find` flattens the
  path it walked.
- **Union by rank or size** (in `union`): always attach the smaller or shorter tree
  under the larger or taller one, so the tree never gets deep needlessly.

## Operations and complexity

n is the number of elements. α(n) is the inverse Ackermann function, which is at most
4 for any n you will ever encounter, so "O(α(n))" is "constant for all practical
purposes."

| Operation | Cost | Note |
|---|---|---|
| `find(x)` | O(α(n)) amortized | Near constant with path compression |
| `union(x, y)` | O(α(n)) amortized | Two finds plus one pointer repoint |
| `connected(x, y)` | O(α(n)) amortized | Just `find(x) == find(y)` |
| Build over m operations | O(m · α(n)) | Effectively O(m), linear in practice |
| Space | O(n) | Two arrays: parent and size (or rank) |

Why the two optimizations together give near-O(1): **union by size** bounds the tree
height at O(log n) on its own, because a tree only gets taller when merged with one
of at least equal size, so its size doubles each time it deepens. **Path compression**
on its own also helps, but the two combined push the amortized cost down to O(α(n)),
a result of Tarjan's. Either optimization alone is O(log n) amortized; you want both.
See the [complexity cheat sheet](../complexity.md) for the array-access costs
underneath.

## Python implementation

A reusable disjoint-set class with path compression and union by size. `union`
returns whether a real merge happened, which is what cycle detection keys on.

```python
class DSU:
    def __init__(self, n):
        self.parent = list(range(n))   # each element is its own root
        self.size = [1] * n            # size of the tree rooted at i
        self.count = n                 # number of disjoint sets

    def find(self, x):
        # path compression: point every node on the path at the root
        root = x
        while self.parent[root] != root:
            root = self.parent[root]
        while self.parent[x] != root:
            self.parent[x], x = root, self.parent[x]
        return root

    def union(self, x, y):
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return False               # already together: no merge
        # union by size: hang the smaller tree under the larger
        if self.size[rx] < self.size[ry]:
            rx, ry = ry, rx
        self.parent[ry] = rx
        self.size[rx] += self.size[ry]
        self.count -= 1
        return True

    def connected(self, x, y):
        return self.find(x) == self.find(y)
```

**Counting connected components** is free: start `count = n` and decrement on every
successful `union`. After processing all edges, `dsu.count` is the number of
components.

```python
def count_components(n, edges):
    dsu = DSU(n)
    for u, v in edges:
        dsu.union(u, v)
    return dsu.count
```

**Cycle detection in an undirected graph** falls out of the same return value: if
`union` reports the two endpoints were already connected, this edge closes a cycle.

```python
def has_cycle(n, edges):
    dsu = DSU(n)
    for u, v in edges:
        if not dsu.union(u, v):   # already in the same set -> cycle
            return True
    return False
```

## When to use it (and when not)

Reach for union-find when:

- You process **edges incrementally** and keep asking "are these connected now",
  especially if edges only get added (union-find does not handle deletion well).
- You need to **count connected components** or group elements into equivalence
  classes: number of provinces, friend circles, accounts merge, redundant
  connection.
- You want **cycle detection in an undirected graph**, or you are building a
  minimum spanning tree with Kruskal's algorithm (sort edges, union the endpoints,
  skip any edge that would close a cycle).

Skip it when:

- The graph is **static and you need actual paths or distances**. Union-find tells
  you *whether* two nodes connect, never *how*; for the route itself use
  [graph traversal](../patterns/16-graph-traversal.md) or
  [shortest path](../patterns/19-shortest-path.md).
- You must **remove edges** or split groups. Union-find merges only; there is no
  cheap un-union. Reversing the problem (processing deletions backward as additions)
  is the usual workaround.
- The connectivity is **directed** and you need reachability respecting direction.
  Union-find treats every edge as undirected; use DFS or a strongly-connected-
  components algorithm instead.

## Tradeoffs and gotchas

- **Both optimizations or you lose the guarantee.** Path compression without union by
  size, or vice versa, is O(log n), not O(α(n)). Skipping both gives O(n) per
  find in the worst case, a chain. Always ship both.
- **`find` before you compare.** `parent[x] == parent[y]` is wrong; two nodes can
  share a set with different immediate parents. Always compare *roots*:
  `find(x) == find(y)`.
- **Map non-integer elements first.** DSU indexes into arrays, so string or
  coordinate elements need a dict from element to an integer id before you can use
  the array-backed version (or back the DSU with a dict instead of lists).
- **Directed edges lie to union-find.** Merging `u` and `v` erases direction. If the
  problem's cycle or connectivity depends on edge direction, union-find is the wrong
  tool.
- **The double while loop in `find` is the compression.** The first loop finds the
  root, the second repoints the path. A one-liner recursive `find` also works but
  risks hitting Python's recursion limit on a deep chain; the iterative form is
  safer for large n.

## Related patterns

- [union-find](../patterns/18-union-find.md) is the pattern this structure powers:
  components, cycle detection, Kruskal's MST, dynamic connectivity.
- [graph traversal](../patterns/16-graph-traversal.md) is the alternative for
  component counting when the graph is fixed and you can BFS or DFS it in one pass.
- [topological sort](../patterns/17-topological-sort.md) handles the directed,
  ordering side of connectivity that union-find cannot express.
- The [complexity cheat sheet](../complexity.md) has the `list` and `dict` costs the
  DSU arrays are built on.
