# 23 - DP III: grids, intervals, bitmask

> **Problem shape:** "How many paths from the top-left to the bottom-right?"
> "Minimum sum path through a grid." "Largest all-ones square." "Max coins from
> bursting all the balloons." "Cheapest way to merge these stones into one pile."
> "Shortest route visiting every node." Anything where the state is a 2D cell, an
> interval `[i, j]`, or a subset encoded as a bitmask, and the answer composes from
> smaller cells, shorter intervals, or smaller subsets.

This file collects the three DP shapes that show up once the state stops being a
single index: grid DP (state is a cell), interval DP (state is a range you build
from the inside out), and bitmask DP (state is a set of used elements). Each has a
signature evaluation order that is the whole trick.

## The signal

Reach for these when you see:

- **A 2D grid with movement rules** (right/down, or four directions) and "count the
  paths", "min/max cost path", or "largest square/rectangle". The state is
  naturally `dp[r][c]`.
- **An interval you resolve by choosing a split or a last operation.** "Burst
  balloons", "merge stones", "matrix chain multiplication", "minimum cost to merge"
  all pick a pivot inside `[i, j]` and combine two subranges. The tell is that the
  cost of an element depends on its neighbors *at the time it is processed*, so
  order matters.
- **A small `n` (n <= ~20) plus "visit all / assign all / cover all".** TSP,
  assignment, "shortest path visiting every node". The state that remembers "which
  ones are done" is a bitmask, and `2^20` states is tractable while `20!` is not.

The `n <= 20` bound specifically screams bitmask, just as `n <= 15` screams
[backtracking](20-backtracking.md); the extra room comes from caching the `2^n`
subset states instead of re-exploring permutations.

## The idea

**Grid DP.** Each cell's answer is built from the cells you can arrive from,
usually the one above and the one to the left. Fill row by row so those neighbors
are ready. The recurrence is a `sum` (counting paths) or a `min`/`max` (cheapest
path), and it is `O(rows * cols)` time.

**Interval DP.** The state is `dp[i][j]` over the subarray `[i, j]`, and you build
it from *shorter* intervals. The powerful framing is "consider the last element to
be removed (or the last split point) inside `[i, j]`": fix which index `k` is
resolved last, so the two sides `[i, k-1]` and `[k+1, j]` are already fully solved
and independent. Iterate by increasing interval length so shorter ranges are
computed first. Cost is typically `O(n^3)`: `O(n^2)` intervals times `O(n)` split
choices.

**Bitmask DP.** The state is `dp[mask]` or `dp[mask][i]`, where `mask` is the set
of elements already used and `i` is where you currently are. You transition by
adding one more element to the set. Since a subset only transitions to supersets,
iterating masks in increasing numeric order respects the dependency. There are
`2^n` masks (times `n` for the position), so `O(2^n * n^2)` for TSP: exponential,
but the only thing that beats brute-force `O(n!)`.

The unifying theme across all three: identify the state, then find the evaluation
order in which every value a transition reads is already filled. Grids go row by
row, intervals go short to long, bitmasks go by increasing set.

## The template

**Grid path count, unique paths (only right and down moves):**

```python
def unique_paths(m, n):
    dp = [1] * n                           # first row: exactly one way to each cell
    for _ in range(1, m):
        for c in range(1, n):
            dp[c] += dp[c - 1]             # from above (old dp[c]) + from left
    return dp[-1]
```

**Min path sum (each cell adds its cost to the cheaper predecessor):**

```python
def min_path_sum(grid):
    m, n = len(grid), len(grid[0])
    dp = [[0] * n for _ in range(m)]
    dp[0][0] = grid[0][0]
    for r in range(m):
        for c in range(n):
            if r == 0 and c == 0:
                continue
            up   = dp[r - 1][c] if r > 0 else float('inf')
            left = dp[r][c - 1] if c > 0 else float('inf')
            dp[r][c] = grid[r][c] + min(up, left)
    return dp[m - 1][n - 1]
```

**Maximal square (side of the largest all-ones square ending at each cell):**

```python
def maximal_square(matrix):
    m, n = len(matrix), len(matrix[0])
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    best = 0
    for r in range(1, m + 1):
        for c in range(1, n + 1):
            if matrix[r - 1][c - 1] == '1':
                # a square here is bounded by its three neighbors
                dp[r][c] = 1 + min(dp[r - 1][c], dp[r][c - 1], dp[r - 1][c - 1])
                best = max(best, dp[r][c])
    return best * best                     # area is side squared
```

**Interval DP, burst balloons ("which balloon in (i, j) do I burst last?"):**

```python
def max_coins(nums):
    a = [1] + nums + [1]                   # pad with virtual 1s at both ends
    n = len(a)
    dp = [[0] * n for _ in range(n)]       # dp[i][j] = coins from open range (i, j)
    for length in range(2, n):             # shorter ranges first
        for i in range(0, n - length):
            j = i + length
            for k in range(i + 1, j):      # k is burst LAST in (i, j)
                # when k bursts last, its neighbors are the fixed walls a[i], a[j]
                dp[i][j] = max(dp[i][j],
                               dp[i][k] + a[i] * a[k] * a[j] + dp[k][j])
    return dp[0][n - 1]
```

**Bitmask DP, TSP-style shortest route visiting all nodes:**

```python
def shortest_tour(dist):
    n = len(dist)
    FULL = (1 << n) - 1
    INF = float('inf')
    # dp[mask][i] = shortest path that has visited exactly `mask`, now at node i
    dp = [[INF] * n for _ in range(1 << n)]
    for i in range(n):
        dp[1 << i][i] = 0                  # start at each node
    for mask in range(1 << n):             # increasing masks: supersets come later
        for i in range(n):
            if dp[mask][i] == INF:
                continue
            for j in range(n):
                if not (mask & (1 << j)):  # j not yet visited
                    nmask = mask | (1 << j)
                    dp[nmask][j] = min(dp[nmask][j], dp[mask][i] + dist[i][j])
    return min(dp[FULL][i] for i in range(n))
```

## Variations

- **Grid with obstacles.** Same recurrence, but force `dp = 0` on blocked cells so
  no path routes through them. "Unique Paths II" is the drill.
- **Triangle / falling path.** Grid DP where the reachable predecessors are the two
  or three cells diagonally above; only the neighbor set changes.
- **Maximal rectangle.** A grid problem that reduces to a histogram per row, solved
  with a monotonic stack rather than a plain 2D recurrence: worth knowing that not
  every grid problem stays a clean grid DP.
- **Matrix chain multiplication / minimum cost to merge stones.** Pure interval DP:
  the split point `k` decides where you cut `[i, j]`, and you add the cost of
  combining the two halves. "Consider the last split" is the same lens as "burst
  last".
- **Palindrome partitioning II (min cuts).** Interval feasibility (is `[i, j]` a
  palindrome) feeds a linear DP over cut positions: interval DP as a subroutine.
- **Assignment problem / "shortest superstring".** Bitmask over which tasks/strings
  are used; `dp[mask]` or `dp[mask][last]` tracks the best assignment covering that
  set.
- **Bitmask over "which are placed this row".** Broken-profile DP for tiling and
  board-covering counts the ways to fill a grid column by column, the mask being
  the occupied cells of the frontier.

## Canonical problems

| # | Problem | Difficulty | What it drills |
|---|---------|-----------|----------------|
| 62 | Unique Paths | Medium | Grid path counting, `dp[c] += dp[c-1]` |
| 64 | Minimum Path Sum | Medium | Min-cost grid path from cheaper predecessor |
| 221 | Maximal Square | Medium | Square side from three-neighbor min |
| 63 | Unique Paths II | Medium | Grid DP with obstacle cells |
| 120 | Triangle | Medium | Grid DP with a shifting neighbor set |
| 312 | Burst Balloons | Hard | Interval DP, "burst last" framing |
| 1000 | Minimum Cost to Merge Stones | Hard | Interval DP with a k-way merge constraint |
| 847 | Shortest Path Visiting All Nodes | Hard | Bitmask DP over the visited set |

## Pitfalls

- **Wrong evaluation order in interval DP.** `dp[i][j]` needs shorter intervals, so
  the outer loop must be interval length (or `i` descending, `j` ascending). Looping
  `i` then `j` both ascending reads cells that are still zero.
- **The "last" trick applied as "first".** In burst balloons, choosing `k` to burst
  *first* leaves its neighbors changing as the subranges resolve, so the subproblems
  are not independent. Choosing `k` *last* fixes the walls `a[i]` and `a[j]`. Getting
  this backward gives a subtly wrong recurrence.
- **Missing the sentinel padding.** Burst balloons and similar need virtual `1`s at
  both ends so edge balloons have defined neighbors; without them the boundary cases
  are wrong.
- **Bitmask iteration order.** Masks must be visited so subsets precede supersets;
  ascending numeric order works because adding a bit only increases the value.
  Iterating any other way reads unfinished states.
- **`2^n` blows up past n = 20.** Bitmask DP is only for tiny n. If n is larger, the
  intended solution is polynomial (greedy, flow, or a different DP), not a mask.
- **Off-by-one on grid boundaries.** First row and first column have a single
  predecessor; guard them (or pad with an infinity/zero border) so you do not read
  `dp[-1]` and wrap around.
- **Confusing area with side in maximal square.** `dp` stores the side length; the
  answer is `side * side`. Returning the raw `dp` value is a common miss.

## Follow-ups and related patterns

- "It is a single sequence with a capacity budget" steps back to
  [DP I: linear and knapsack](21-dp-linear-knapsack.md).
- "It is two strings or a subsequence" is [DP II: subsequences and
  strings](22-dp-strings.md); the interval DP here generalizes the palindrome
  interval DP there.
- "n is 15 and I must enumerate, not just optimize" pushes to
  [backtracking](20-backtracking.md); bitmask DP is the memoized version of that
  subset search.
- "The grid is really a weighted graph and I want a true shortest path" pushes to
  [graph traversal](16-graph-traversal.md) and Dijkstra; grid DP only works when
  moves are acyclic (one direction), while general movement needs a graph search.
- The subset encoding leans on [bit manipulation](26-bit-manipulation.md):
  `mask & (1 << j)`, `mask | (1 << j)`, and popcount are the primitives.
- When a local rule provably picks the global optimum without a table, it collapses
  to [greedy](25-greedy.md).
