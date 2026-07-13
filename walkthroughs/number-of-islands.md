# Walkthrough: Number of Islands (LC 200)

A worked example that runs the six-step framework on one problem end to end.
The goal is to show the process, not just the answer.

## The problem

**LeetCode 200, Medium.** Given a 2D grid of `'1'` (land) and `'0'` (water),
count the number of islands. An island is a group of `'1'` cells connected
horizontally or vertically (not diagonally), and the grid edges count as water.

Example: the grid
```
1 1 0 0 0
1 1 0 0 0
0 0 1 0 0
0 0 0 1 1
```
has `3` islands.

## 1. Clarify and restate

Questions before coding:

- **Input types.** A list of lists of single-character strings `'1'` or `'0'`
  (LeetCode uses string cells, not ints, so I will compare against `'1'`). Is the
  grid rectangular (every row the same width)? Yes, assume so. Can it be empty or
  have empty rows? Handle the empty case.
- **Connectivity.** Four-directional only (up, down, left, right). Diagonals do
  **not** connect. Confirm this, because eight-directional would change the answer.
- **What do I return?** A single integer, the count of connected land components.
- **Am I allowed to mutate the grid?** If yes, I can mark visited cells in place
  and save the O(m*n) visited set. Ask; if not, I keep a separate visited
  structure. I will assume mutation is allowed and mention the alternative.
- **Constraints.** Grid up to a few hundred by a few hundred, so up to ~`10^5`
  cells. Reading that: I need to touch each cell O(1) times, target O(m*n).
- **Edge cases.** Empty grid (`0`), all water (`0`), all land (`1`), a single
  cell, islands touching the border, a one-wide snake of land.

Restated: count connected components of `'1'` cells under 4-directional adjacency,
visiting each cell a constant number of times.

## 2. Work an example by hand

Scan the example grid row by row, left to right, looking for an unvisited `'1'`
that has not been absorbed into an earlier island.

- Row 0, col 0 is `'1'` and unseen. This is a new island (count -> 1). Flood it:
  it connects to (0,1), (1,0), (1,1). Mark all four as water/visited.
- Continue scanning. The next unvisited `'1'` is at (2,2). New island (count -> 2).
  It has no unvisited land neighbors, so the flood covers just that one cell.
- Continue. Next unvisited `'1'` is at (3,3), connecting to (3,4). New island
  (count -> 3). Flood both.
- No more unvisited land. Answer `3`.

The key move: each time the outer scan finds land that has not been swallowed by a
previous flood, that is one fresh island, and I immediately flood its entire
connected blob so the scan never counts any of its cells again.

## 3. Brute force

There is not really a meaningfully slower "brute force" here; the natural correct
solution is already the flood-fill. A genuinely naive alternative would be
union-find over every cell plus a pass to count distinct roots, which is more
machinery for the same O(m*n) result. So I will state the direct idea and its cost
rather than an artificially bad version.

```python
# Idea: scan every cell. When an unvisited land cell is found, it starts a new
# island; flood its whole connected region so its cells are not recounted.
# Without the flood (counting every land cell) you would massively overcount,
# so the flood is not an optimization, it is the correctness mechanism.
```

Counting land cells alone is O(m*n) but wrong (it returns cell count, not island
count). The flood-fill fixes correctness at the same asymptotic cost.

## 4. Find the bottleneck and pick the pattern

The real question is not "how do I go faster" but "what structure am I counting".
Islands are exactly the **connected components** of a graph whose nodes are land
cells and whose edges join 4-adjacent land cells. Counting connected components in
a graph is a textbook **grid DFS/BFS**: run one traversal per component, and the
number of traversals you launch is the number of components.

Why this is O(m*n) and not worse: the outer double loop visits every cell once to
*find* component starts, and the flood traversals collectively visit every land
cell exactly once (each cell is marked the moment it is reached, so no cell is
entered twice). Marking visited (by overwriting `'1'` with `'0'`, or a visited
set) is what guarantees each cell is processed a constant number of times. The
pattern is: **outer scan launches a traversal only from unvisited land; each
traversal sinks its whole island so the scan skips it thereafter.**

DFS or BFS both work. DFS is a few lines recursively but can hit Python's
recursion limit on a large single island (a snake filling a 200x200 grid is 40000
deep). BFS with an explicit queue avoids that, so I will write BFS and note DFS as
the shorter alternative.

## 5. Code it

```python
from collections import deque

def num_islands(grid):
    if not grid or not grid[0]:
        return 0

    rows, cols = len(grid), len(grid[0])
    count = 0

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1':          # an unvisited land cell = a new island
                count += 1
                grid[r][c] = '0'           # mark before enqueue so it is not re-added
                queue = deque([(r, c)])
                while queue:
                    cr, cc = queue.popleft()
                    for nr, nc in ((cr - 1, cc), (cr + 1, cc),
                                   (cr, cc - 1), (cr, cc + 1)):
                        if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == '1':
                            grid[nr][nc] = '0'   # sink it on discovery
                            queue.append((nr, nc))

    return count
```

The invariant: any cell that has been discovered is set to `'0'` at the moment it
is discovered (before it goes into the queue), so it can never be enqueued twice
and the outer scan will never treat it as a new island. Marking on *discovery*,
not on *dequeue*, is the detail that prevents a cell from being pushed by two
neighbors.

A recursive DFS is shorter if recursion depth is acceptable:

```python
def num_islands_dfs(grid):
    if not grid or not grid[0]:
        return 0
    rows, cols = len(grid), len(grid[0])

    def sink(r, c):
        if r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] != '1':
            return
        grid[r][c] = '0'
        sink(r - 1, c); sink(r + 1, c); sink(r, c - 1); sink(r, c + 1)

    count = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1':
                count += 1
                sink(r, c)
    return count
```

## 6. Test, trace, and analyze

Trace the BFS on the example grid. The outer scan walks row-major.

- (0,0) is `'1'`: count -> 1. BFS from (0,0) sinks (0,0), then discovers (0,1) and
  (1,0), then (1,1). Queue drains. The whole top-left 2x2 block is now `'0'`.
- Scan continues through the rest of rows 0 and 1: all `'0'` now, nothing fires.
- (2,2) is `'1'`: count -> 2. BFS finds no land neighbors, sinks just (2,2).
- (3,3) is `'1'`: count -> 3. BFS sinks (3,3) and discovers (3,4). Queue drains.
- Scan finishes. Return `3`. Matches the hand count.

Edge cases:
- **Empty grid** `[]` or `[[]]`: the guard returns `0`. Correct.
- **All water**: the outer scan never finds a `'1'`, returns `0`. Correct.
- **All land** (single rectangle): the first land cell launches one BFS that sinks
  the entire grid, returns `1`. Correct.
- **Single cell** `[['1']]`: count -> 1, BFS sinks it, returns `1`. `[['0']]`
  returns `0`. Correct.
- **Border-touching island**: the bounds check `0 <= nr < rows` stops the
  traversal from stepping off the grid, so edge islands are counted normally.

**Complexity: O(m*n) time**, since every cell is examined by the outer loop once
and enqueued/dequeued at most once across all BFS runs, and **O(m*n) space** in
the worst case (a grid that is all land makes the BFS queue hold up to O(m*n)
cells; recursive DFS has the same worst-case stack depth). If mutating the grid is
disallowed, add a `visited` set of the same O(m*n) size and check it instead of
overwriting.

With more time I would mention that **union-find** solves the same problem and is
the better tool when islands are formed incrementally (LC 305, "Number of Islands
II", where cells turn to land one at a time and you want the count after each
addition); for a static grid, DFS/BFS is simpler and equally fast.

## What the interviewer is really testing

Whether you recognize a grid as an implicit graph and counting islands as counting
connected components, then run exactly one traversal per component while marking
visited so nothing is double-counted. The subtle correctness point to voice is
*when* you mark a cell visited (on discovery, before enqueue), which is what keeps
the traversal linear and prevents a cell from being processed twice. Getting the
four-directional neighbor generation and bounds checks clean, without off-grid
indexing, is the execution signal.

> Pattern: [16 graph traversal](../patterns/16-graph-traversal.md)
