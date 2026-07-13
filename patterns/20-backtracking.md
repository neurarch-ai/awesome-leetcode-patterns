# 20 - Backtracking

> **Problem shape:** "Return all subsets." "Generate every permutation." "Find all
> combinations that sum to a target." "Place N queens so none attack." "Solve the
> sudoku." Anything asking you to enumerate or search all valid arrangements of
> choices, where each partial arrangement is built one decision at a time and
> abandoned the moment it cannot lead to a solution.

Backtracking is depth-first search over a decision tree. You build a candidate
incrementally, and whenever a partial candidate is doomed you undo the last choice
and try the next one. It is the pattern for "enumerate everything" and for
constraint satisfaction, and its cost is exponential by nature, which is exactly
why the input sizes are tiny.

## The signal

Reach for backtracking when you see:

- **"All", "every", "enumerate", "generate", "list all"** combined with subsets,
  permutations, combinations, partitions, or arrangements. The answer is a
  collection of collections, not a single number.
- **A small input bound.** `n <= 15`, `n <= 20`, board sizes like `9 x 9`. An
  exponential or factorial blowup is only tractable when n is small, so a tight
  n is the loudest tell that brute-force search with pruning is intended.
- **Constraint satisfaction**: place items subject to rules (N-Queens, sudoku),
  or trace a path through a grid under adjacency rules (word search). You need to
  try a placement, recurse, and retract if it violates a constraint.
- **A decision at each step** with a small branching set, where choices compose
  into a full solution and a partial solution can be validated as you go.

If instead the problem asks for the *count* of arrangements or the *best* one, and
n is large, that is usually [DP](21-dp-linear-knapsack.md), not raw backtracking.

## The idea

Every backtracking problem is a walk over an implicit **decision tree**. Each node
is a partial candidate; each edge is one choice; each leaf is a complete candidate
you either record or reject. The recursion does three things at every node, the
choose / explore / unchoose loop:

1. **Choose** a candidate for the current position (append it to the path).
2. **Explore** by recursing to decide the next position.
3. **Unchoose** by removing what you just added, restoring state so the next
   sibling branch starts clean.

The unchoose step is what makes it "backtracking": one mutable `path` is shared
across the whole tree, pushed on the way down and popped on the way up, so you
never pay to copy state except when you record a finished leaf.

**Pruning** is the other half. If a partial candidate already violates a
constraint (sum exceeds target, a queen attacks another), you return before
recursing, cutting off an entire subtree. Good pruning is the difference between a
solution that finishes and one that times out, even though the worst-case
complexity is unchanged.

Complexity is inherently exponential: subsets are `O(2^n)` nodes, permutations are
`O(n!)`, and each leaf costs `O(n)` to copy, so a typical bound is `O(n * 2^n)` or
`O(n * n!)`. There is no polynomial escape; the game is to prune hard and keep the
constant factor low.

## The template

**The universal choose / explore / unchoose skeleton (subsets):**

```python
# Time: O(n * 2^n), Space: O(n) (recursion depth plus path, output aside)
def subsets(nums):
    res = []
    path = []

    def backtrack(start):
        res.append(path[:])                # every node is a valid subset
        for i in range(start, len(nums)):
            path.append(nums[i])           # choose
            backtrack(i + 1)               # explore (i + 1: no reuse, no reorder)
            path.pop()                     # unchoose

    backtrack(0)
    return res
```

The `start` index is the key to combinations and subsets: it forbids going
backward, so `[1,2]` and `[2,1]` are not both generated. Permutations drop `start`
and instead track which elements are already used.

**Permutations (order matters, so use a `used` set instead of `start`):**

```python
# Time: O(n * n!), Space: O(n) (recursion depth plus path and used, output aside)
def permute(nums):
    res = []
    path = []
    used = [False] * len(nums)

    def backtrack():
        if len(path) == len(nums):
            res.append(path[:])
            return
        for i in range(len(nums)):
            if used[i]:
                continue
            used[i] = True
            path.append(nums[i])
            backtrack()
            path.pop()
            used[i] = False

    backtrack()
    return res
```

**Combination sum (unbounded reuse, prune when the running sum overshoots):**

```python
# Time: O(exponential in target/min candidate), Space: O(target / min candidate) recursion depth
def combination_sum(candidates, target):
    candidates.sort()                      # enables the early break prune
    res = []
    path = []

    def backtrack(start, remaining):
        if remaining == 0:
            res.append(path[:])
            return
        for i in range(start, len(candidates)):
            if candidates[i] > remaining:  # sorted: all later are bigger too
                break                      # prune the rest of this level
            path.append(candidates[i])
            backtrack(i, remaining - candidates[i])   # i, not i + 1: reuse allowed
            path.pop()

    backtrack(0, target)
    return res
```

Note the two knobs that distinguish the whole family: `start` vs `used` controls
order, and `i` vs `i + 1` in the recursive call controls reuse.

## Variations

- **Handling duplicates (sort + skip).** When the input has repeats and you must
  not emit duplicate results, sort first, then at each level skip a value equal to
  its predecessor: `if i > start and nums[i] == nums[i-1]: continue`. This forbids
  two identical branches at the same tree depth. Combination Sum II and Subsets II
  are the drills.
- **Combinations of size k.** Same as subsets but only record when
  `len(path) == k`, and prune when the remaining elements cannot fill k slots.
- **Generate parentheses.** The decision at each step is "add `(`" or "add `)`",
  pruned by two counters: you can open while `open < n`, and close only while
  `close < open`. A clean example of constraint pruning without an explicit input
  array.
- **Constraint satisfaction on a board (N-Queens, sudoku).** Place one unit
  (a queen per row, a digit per empty cell), check it against the constraints,
  recurse, and undo. Keep O(1) constraint sets (columns, two diagonals for queens)
  so validity is a set lookup, not a board scan.
- **Grid path search (word search).** DFS from each cell, mark the cell visited,
  recurse into the four neighbors that match the next character, then unmark on the
  way out. The "unmark" is the unchoose step applied to a grid.
- **Palindrome partitioning / IP-address restoration.** Choose a prefix cut,
  validate it, recurse on the suffix. The choice is where to place the next split.

## Canonical problems

| # | Problem | Difficulty | What it drills |
|---|---------|-----------|----------------|
| 78 | Subsets | Medium | The `start`-index skeleton; every node is an answer |
| 46 | Permutations | Medium | `used` array instead of `start`; order matters |
| 39 | Combination Sum | Medium | Unbounded reuse (recurse on `i`) plus sum pruning |
| 40 | Combination Sum II | Medium | Duplicates via sort + skip; single use per element |
| 22 | Generate Parentheses | Medium | Pruning with open/close counters, no input array |
| 79 | Word Search | Medium | DFS on a grid with visited-mark and unmark |
| 51 | N-Queens | Hard | Constraint sets for columns and diagonals; place per row |
| 37 | Sudoku Solver | Hard | Try-digit / recurse / undo with return-on-success |

## Pitfalls

- **Forgetting to copy at the leaf.** `res.append(path)` stores a reference to the
  one shared list, which later gets popped empty. You must snapshot with
  `path[:]` (or `list(path)`).
- **Forgetting to unchoose.** Skipping `path.pop()` or leaving `used[i] = True`
  leaks state into sibling branches and corrupts every later result. Every choose
  needs its matching undo on all return paths.
- **`i` vs `i + 1` mix-up.** Recursing on `i` allows reusing the current element
  (unbounded knapsack shape); `i + 1` forbids reuse. Picking the wrong one silently
  changes the problem.
- **Duplicate skip at the wrong scope.** `if i > start` skips duplicates *across
  siblings at the same level* (correct). `if i > 0` would also skip the element on
  the path from the parent, dropping valid results. Sort is a prerequisite for
  either.
- **Weak pruning on constraint problems.** Re-scanning the whole board for validity
  turns an already-exponential search into something that times out. Maintain
  incremental O(1) constraint structures.
- **Not stopping early when one solution suffices.** Sudoku and "does a path exist"
  want the first success, so return a boolean up the stack and short-circuit;
  enumerating all solutions is wasted work.

## Follow-ups and related patterns

- "Just count the arrangements, and n is large" pushes to
  [DP](21-dp-linear-knapsack.md): target-sum and subset-sum counting are the same
  decision tree collapsed with memoization, trading enumeration for a table.
- "The grid search repeats subproblems" or "the state is a visited-set bitmask"
  pushes to [bitmask DP](23-dp-grids-intervals.md), where an exponential set of
  states is cached instead of re-explored.
- Backtracking is [DFS](12-tree-dfs.md) over an implicit tree; the recursion shape
  is identical to tree recursion, with an explicit undo.
- Grid backtracking sits next to [graph traversal](16-graph-traversal.md); the
  difference is that backtracking un-visits cells so other paths can reuse them.
- When a greedy choice provably reaches the optimum without exploring the tree,
  the problem collapses to [greedy](25-greedy.md) instead.
