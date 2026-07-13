# 13 - Tree BFS and level-order

> **Problem shape:** "Return the level-order traversal of a binary tree." "Give me
> the right-side view." "What is the minimum depth?" "Zigzag the levels." "Connect
> each node to its next right neighbor." Anything where the answer is organized *by
> level*, or where you want the *shallowest* node that satisfies a condition.

Tree BFS visits nodes in breadth-first order using a queue, one level fully before
the next. It runs in O(n) time and O(w) space where w is the maximum width of the
tree. The single trick that unlocks the whole pattern is snapshotting the queue
length so you process exactly one level per outer iteration.

## The signal

Reach for tree BFS when the problem is phrased in terms of levels or distance from
the root:

- **"Level order", "by level", "each row", "average of levels"**: the output is a
  list per depth. BFS produces levels in order for free.
- **"Right-side view", "left-side view", "largest value in each row"**: you want
  one representative per level, which is trivial once you can iterate a level at a
  time.
- **"Minimum depth", "shortest path to a leaf"**: BFS reaches the closest leaf
  first, so you can return the instant you see one, without exploring deeper
  branches. This is where BFS strictly beats DFS.
- **"Zigzag", "connect next right pointers"**: both are level-structure problems.
  Zigzag alternates the emit direction per level; next-pointers wire siblings
  within a level.

If the problem cares about *which level* a node is on, or wants the *nearest*
qualifying node, BFS is the pattern. If it cares about root-to-leaf branches or
subtree aggregates, use [tree DFS](12-tree-dfs.md) instead.

## The idea

BFS uses a FIFO queue. Seed it with the root, then repeatedly pop a node and push
its children. To recover level boundaries (which a flat queue loses), take a
**snapshot of the current queue length** at the top of each outer loop: that count
is exactly the number of nodes on the current level, so an inner loop of that many
pops drains precisely one level.

```
level_size = len(queue)     # everything now in the queue is one level
for _ in range(level_size): # drain exactly this level, enqueue the next
    ...
```

Because each node is enqueued and dequeued once, the pass is O(n). The queue holds
at most one level at a time, so space is O(w), the tree's maximum width (O(n) in
the worst case of a full bottom level).

For minimum depth, BFS wins because the first leaf it dequeues is the shallowest
possible: you return immediately and never touch the deeper subtrees, whereas DFS
would explore full branches before finding the shortest.

## The template

**Level-order traversal, the snapshot trick (this is the base for all variations):**

```python
from collections import deque

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def level_order(root):
    if not root:
        return []
    result = []
    queue = deque([root])
    while queue:
        level_size = len(queue)        # snapshot: nodes on THIS level
        level = []
        for _ in range(level_size):    # drain exactly one level
            node = queue.popleft()
            level.append(node.val)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        result.append(level)
    return result
```

**Right-side view (last node of each level):**

```python
def right_side_view(root):
    if not root:
        return []
    view = []
    queue = deque([root])
    while queue:
        level_size = len(queue)
        for i in range(level_size):
            node = queue.popleft()
            if i == level_size - 1:    # last node dequeued on this level
                view.append(node.val)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
    return view
```

**Minimum depth, return early on the first leaf:**

```python
def min_depth(root):
    if not root:
        return 0
    queue = deque([(root, 1)])
    while queue:
        node, depth = queue.popleft()
        if not node.left and not node.right:   # first leaf reached is the shallowest
            return depth
        if node.left:
            queue.append((node.left, depth + 1))
        if node.right:
            queue.append((node.right, depth + 1))
```

## Variations

- **Zigzag level order.** Same snapshot loop, but reverse the emit order on
  alternate levels. Build each level left to right as usual, then reverse it (or
  append with a `deque` from the correct end) on odd levels. Toggle a boolean each
  round.
- **Per-level aggregates.** Largest value per row, average per row, level sums:
  compute the aggregate inside the inner loop instead of collecting all values.
- **Bottom-up level order.** Produce levels top-down, then reverse the result list,
  or prepend each level.
- **Populating next right pointers.** Wire each node's `next` to the node dequeued
  after it within the same level; the last node's `next` is `None`. For a *perfect*
  tree you can even do it in O(1) extra space using the already-established `next`
  pointers of the level above instead of a queue.
- **Multi-source BFS on grids.** The same one-level-at-a-time loop, seeded with
  many starting cells, computes distances in grids ("rotting oranges", "01 matrix").
  See [graph traversal](16-graph-traversal.md).

## Canonical problems

| # | Problem | Difficulty | What it drills |
|---|---------|-----------|----------------|
| 102 | Binary Tree Level Order Traversal | Medium | The snapshot-length base template |
| 111 | Minimum Depth of Binary Tree | Easy | BFS returns on the first leaf |
| 199 | Binary Tree Right Side View | Medium | Last node per level |
| 637 | Average of Levels in Binary Tree | Easy | Per-level aggregate |
| 103 | Binary Tree Zigzag Level Order Traversal | Medium | Alternating emit direction |
| 515 | Find Largest Value in Each Tree Row | Medium | Per-level max |
| 116 | Populating Next Right Pointers in Each Node | Medium | Wire siblings within a level |
| 117 | Populating Next Right Pointers II (not perfect) | Medium | Same, tree not full |
| 107 | Binary Tree Level Order Traversal II | Medium | Bottom-up, reverse the levels |

## Pitfalls

- **Not snapshotting the length.** If you read `len(queue)` inside the inner loop
  after pushing children, your level boundary is wrong and levels bleed together.
  Capture `level_size` once, before the inner loop.
- **Pushing `None` children.** Guard `if node.left` / `if node.right` before
  enqueuing, or you dereference `None` when you pop it. (If a problem needs
  explicit nulls, for example serialization, push them deliberately and handle them
  on pop.)
- **Using a list as a queue.** `list.pop(0)` is O(n), making the whole traversal
  O(n^2). Use `collections.deque` and `popleft`.
- **Forgetting the empty-root guard.** An empty tree should return an empty result,
  not crash on `deque([None])`.
- **Reversing per level in zigzag by re-sorting.** Just reverse the built list or
  append from the correct end; do not sort.

## Follow-ups and related patterns

- "Walk branches and aggregate subtrees instead of levels" pushes back to
  [tree DFS](12-tree-dfs.md); depth problems can be solved either way, but
  per-level output is BFS's home turf.
- "Do BFS on a grid or a general graph" is the same queue mechanics with a visited
  set, in [graph traversal](16-graph-traversal.md); level-by-level BFS is how you
  get shortest paths in unweighted graphs.
- "Edges have weights, so the nearest node is not the fewest hops" breaks plain BFS
  and pushes to [shortest path](19-shortest-path.md) (Dijkstra).
- The queue-with-length-snapshot mechanic reappears anywhere you need distance
  layers, including multi-source flood fills.
