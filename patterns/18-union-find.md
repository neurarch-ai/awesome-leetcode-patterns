# 18 - Union-find (DSU)

> **Problem shape:** "How many provinces / friend circles are there?" "Does adding
> this edge create a cycle in an undirected graph?" "Merge accounts that share an
> email." "Which edge is redundant?" Anything about grouping items into disjoint
> sets and answering "are these two in the same set" as edges arrive, especially
> when the connections come one at a time.

Union-find, also called a disjoint-set union (DSU), maintains a partition of items
into groups and supports two operations in near-constant amortized time: `find`
(which group is this in) and `union` (merge two groups). With path compression and
union by rank or size, a sequence of `m` operations runs in O(m x alpha(n)) where
alpha is the inverse Ackermann function, effectively a small constant. It is the
right tool whenever connectivity is built up incrementally, where relaunching a
traversal per query would be wasteful.

## The signal

Reach for union-find when you see:

- **Grouping / clustering by connection:** "connected components", "provinces",
  "friend circles", "number of islands" when the edges are given as a list rather
  than a grid to flood.
- **"Are these two connected?" asked many times** as edges are added. DSU answers
  each in near O(1); a fresh BFS or DFS per query would be O(V + E) each.
- **Cycle detection in an *undirected* graph.** If an edge connects two nodes that
  already share a root, that edge closes a cycle.
- **Incremental merging:** accounts that share an email, boxes that touch, stones on
  the same row or column. You keep unioning and ask about the resulting groups.
- **Kruskal's minimum spanning tree.** Sort edges by weight, add each edge unless it
  would form a cycle (a DSU query), stop at `V - 1` edges.

The tell is disjoint sets that only ever *merge*, never split, and you care about
membership rather than the actual path between nodes. If you needed the path itself
or distances, that is [graph traversal](16-graph-traversal.md) or
[shortest path](19-shortest-path.md).

## The idea

Represent each group as a tree; the root is the group's identity. `find(x)` walks
parent pointers to the root. `union(x, y)` points one root at the other, merging two
trees into one.

Two optimizations make it near-constant:

- **Path compression.** During `find`, re-point every node on the path directly to
  the root, so later lookups on those nodes are O(1). The tree flattens as you use
  it.
- **Union by rank or size.** Always attach the smaller (or shorter) tree under the
  larger root, so trees stay shallow. Without this, a chain of unions can build a
  degenerate linked list of depth n.

Together they give the inverse-Ackermann bound. Counting components is free: start
the count at `n` and decrement it every time a `union` actually merges two distinct
groups.

## The template

**Reusable DSU class with path compression and union by size:**

```python
class DSU:
    def __init__(self, n):
        self.parent = list(range(n))         # each node is its own root
        self.size = [1] * n                  # size of the tree at each root
        self.count = n                       # number of disjoint components

    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]   # path halving
            x = self.parent[x]
        return x

    def union(self, x, y):
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return False                     # already together: this edge is redundant
        if self.size[rx] < self.size[ry]:   # attach smaller under larger
            rx, ry = ry, rx
        self.parent[ry] = rx
        self.size[rx] += self.size[ry]
        self.count -= 1                      # two groups became one
        return True

    def connected(self, x, y):
        return self.find(x) == self.find(y)
```

**Counting connected components / provinces:**

```python
def count_provinces(is_connected):           # n x n adjacency matrix
    n = len(is_connected)
    dsu = DSU(n)
    for i in range(n):
        for j in range(i + 1, n):
            if is_connected[i][j]:
                dsu.union(i, j)
    return dsu.count
```

**Detecting a cycle in an undirected graph / finding the redundant edge:**

```python
def find_redundant(edges):                   # nodes labeled 1..n
    dsu = DSU(len(edges) + 1)
    for u, v in edges:
        if not dsu.union(u, v):             # both ends already share a root
            return [u, v]                    # this edge closes a cycle
    return []
```

The whole pattern rides on `union` returning `False` when the two endpoints were
already in the same set. That single boolean is your cycle detector, your redundant
edge finder, and your Kruskal skip test.

## Variations

- **Union by rank vs by size.** Rank tracks tree height, size tracks node count.
  Either keeps trees shallow; size is handy when you also want the size of a group
  (largest component, or "size of the island containing x").
- **String or arbitrary keys.** Map each label to an integer index first, or back
  the DSU with a `parent = {}` dict where `find` self-initializes unseen keys.
  Accounts-merge unions email strings this way.
- **Two-dimensional grid to 1D.** Flatten cell `(r, c)` to `r * cols + c` and union
  adjacent land cells, an alternative to flood-fill counting of islands.
- **Kruskal's MST.** Sort edges ascending by weight; for each, `union` the
  endpoints and keep the edge only if the union succeeded (did not form a cycle);
  stop after `V - 1` edges. The DSU is what makes the greedy cheap.
- **Union-find with rollback / weighted DSU.** Advanced variants track a relative
  offset to each parent (for "equations satisfiable" or bipartite constraints).
- **Number of operations to connect a network.** Extra cables equal
  `edges - (V - 1 - redundant)`; feasible only if you have at least
  `components - 1` spare cables. A direct DSU component count.

## Canonical problems

| # | Problem | Difficulty | What it drills |
|---|---------|-----------|----------------|
| 547 | Number of Provinces | Medium | Component count from an adjacency matrix |
| 684 | Redundant Connection | Medium | Undirected cycle detection via union |
| 721 | Accounts Merge | Medium | Union by shared key, then group by root |
| 1319 | Number of Operations to Make Network Connected | Medium | Component count vs spare edges |
| 200 | Number of Islands | Medium | Grid flattened to DSU indices |
| 323 | Number of Connected Components in an Undirected Graph | Medium | The plain component-count drill |
| 990 | Satisfiability of Equality Equations | Medium | Union equals, then check not-equals |
| 128 | Longest Consecutive Sequence | Medium | Union consecutive values (or a hash-set alt) |
| 1584 | Min Cost to Connect All Points | Medium | Kruskal's MST with a DSU |

## Pitfalls

- **Skipping both optimizations.** Path compression *or* union by rank/size alone is
  okay; neither means `find` can degrade to O(n) and the whole thing crawls on large
  inputs. Include both to be safe.
- **Off-by-one on node labels.** Many problems label nodes `1..n`, not `0..n-1`.
  Size the DSU to `n + 1` or you index out of range.
- **Comparing raw parents instead of roots.** `connected` must compare
  `find(x) == find(y)`, not `parent[x] == parent[y]`; parents may point mid-tree.
- **Decrementing the component count on a no-op union.** Only decrement when the two
  roots actually differed. The template does this by returning early on `rx == ry`.
- **Forgetting DSU only detects cycles in *undirected* graphs.** A directed cycle
  needs topo sort or DFS coloring, see
  [topological sort](17-topological-sort.md); unioning directed edges gives wrong
  answers.
- **Rebuilding the DSU per query.** The point is to build once and answer many
  `connected` queries against the same structure.

## Follow-ups and related patterns

- "I need the actual path or the distance between two nodes, not just whether they
  connect" pushes to [graph traversal](16-graph-traversal.md) or
  [shortest path](19-shortest-path.md).
- "The graph is directed, detect that cycle" pushes to
  [topological sort](17-topological-sort.md), where DSU does not apply.
- "Minimum spanning tree" pairs this with greedy edge selection (Kruskal) or with a
  [heap](24-heap.md) (Prim), see [greedy](25-greedy.md) for the exchange argument.
- Counting components can also be done with repeated BFS or DFS from
  [graph traversal](16-graph-traversal.md); DSU wins when edges arrive incrementally
  or connectivity is queried many times.
