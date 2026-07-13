# Dynamic programming: the full sub-pattern map

Dynamic programming is not one pattern, it is a family, and "I know DP" usually
means "I know three or four of its shapes". This page is the map: every DP
sub-pattern worth recognizing, the state and transition that define it, and where
in this repo it is taught in depth. Candidates struggle with DP because they treat
each problem as new; in reality there are about a dozen recurring shapes, and
naming the shape gives you the recurrence.

The three core files carry the templates: [DP I: linear and knapsack](21-dp-linear-knapsack.md),
[DP II: subsequences and strings](22-dp-strings.md), and
[DP III: grids, intervals, bitmask](23-dp-grids-intervals.md). The
[state-machine DP](30-state-machine-dp.md) file covers the stock family. This page
sits above them as the recognition index.

## The universal recipe

Every DP, regardless of shape, is four decisions. If you can fill these in, you can
code it:

1. **State.** What does `dp[...]` mean, as a precise English sentence? "The min
   coins to make amount c." A fuzzy state is the root of every stuck DP.
2. **Transition.** How is a state built from smaller states? This is the
   recurrence.
3. **Base case.** The smallest states, filled in directly.
4. **Order.** The sequence to evaluate states so every dependency is ready. For
   memoization the recursion handles it; for tabulation you choose the loop order.

The sub-patterns below are just recurring answers to "what is the state, and what
is the transition".

## The sub-patterns

### 1. Linear DP (one sequence, one dimension)

- **State:** `dp[i]` = the answer considering the first `i` elements (or ending at
  `i`).
- **Transition:** from `dp[i-1]` and maybe `dp[i-2]`.
- **Examples:** climbing stairs, house robber, maximum subarray (Kadane), decode
  ways, longest increasing subsequence in O(n^2).
- **Taught in:** [DP I](21-dp-linear-knapsack.md).

### 2. Knapsack (items against a budget)

- **State:** `dp[i][c]` = best value using the first `i` items with capacity `c`.
- **Transition:** take item `i` (`dp[i-1][c - w_i] + v_i`) or skip it
  (`dp[i-1][c]`).
- **Variants:** 0/1 knapsack (each item once), unbounded knapsack (reuse allowed,
  coin change), bounded knapsack, subset sum, partition equal subset, target sum.
- **The tell:** "take or skip each item against a shared limit."
- **Taught in:** [DP I](21-dp-linear-knapsack.md).

### 3. Two-sequence DP (align two strings or arrays)

- **State:** `dp[i][j]` = the answer for the first `i` of one sequence and first
  `j` of the other.
- **Transition:** match (`dp[i-1][j-1]`) or skip from one side (`dp[i-1][j]`,
  `dp[i][j-1]`).
- **Examples:** longest common subsequence, edit distance, distinct subsequences,
  interleaving string, regular-expression and wildcard matching.
- **The tell:** two strings, and the answer for prefixes builds the answer for the
  whole.
- **Taught in:** [DP II](22-dp-strings.md).

### 4. Subsequence DP on one sequence

- **State:** `dp[i]` ending at `i`, often with a secondary scan or a binary-search
  speedup.
- **Examples:** longest increasing subsequence (O(n log n) with patience sorting),
  longest arithmetic subsequence, number of longest increasing subsequences.
- **Taught in:** [DP II](22-dp-strings.md).

### 5. Grid DP (paths and areas on a 2D board)

- **State:** `dp[i][j]` = the answer to reach or end at cell `(i, j)`.
- **Transition:** from the neighbors you are allowed to come from (usually up and
  left).
- **Examples:** unique paths, minimum path sum, maximal square, dungeon game,
  cherry pickup (two-agent grid DP).
- **Taught in:** [DP III](23-dp-grids-intervals.md).

### 6. Interval DP (solve a range by its split point)

- **State:** `dp[i][j]` = the answer for the subarray or substring `[i, j]`.
- **Transition:** choose the last thing to process in the range, or a split point
  `k` between `i` and `j`; combine the two sub-intervals. Evaluate by increasing
  interval length.
- **Examples:** burst balloons, matrix-chain multiplication, minimum cost to merge
  stones, longest palindromic subsequence, remove boxes.
- **The tell:** the answer for a range depends on splitting it, and n is small
  (O(n^3) is acceptable).
- **Taught in:** [DP III](23-dp-grids-intervals.md).

### 7. Bitmask / state-compression DP (subset as an integer)

- **State:** `dp[mask]` where `mask` is a subset of up to ~20 items encoded in bits.
- **Transition:** add or remove one element (one bit) from the subset.
- **Examples:** travelling salesman, shortest path visiting all nodes, partition to
  k equal subsets, minimum incompatibility, assignment problems.
- **The tell:** n <= ~20 and the natural state is "which items have I used".
- **Taught in:** [DP III](23-dp-grids-intervals.md).

### 8. State-machine DP (a few modes with transitions)

- **State:** `dp[i][mode]` where `mode` is one of a small fixed set (holding,
  cash, cooldown).
- **Examples:** the entire stock buy-and-sell family, paint house, delete and
  earn.
- **Taught in:** [State-machine DP](30-state-machine-dp.md).

### 9. DP on trees (aggregate over a rooted tree)

- **State:** `dp[node][...]` computed from the children's DP values, usually with a
  post-order DFS.
- **Transition:** combine children, often with two cases per node (include the node
  or not).
- **Examples:** house robber III, binary tree cameras, diameter of a tree,
  maximum path sum, counting subtrees.
- **The tell:** the input is a tree and each node's answer needs its children's
  answers. This is the [tree DFS](12-tree-dfs.md) "return a value up from children"
  idea, seen as DP.

### 10. Digit DP (count numbers with a digit property)

- **State:** position in the number, a `tight` flag (are we still bounded by the
  limit), and any carried property (sum of digits so far, last digit).
- **Examples:** count numbers <= N with no repeated digits, numbers with a digit
  sum divisible by k, count of integers in a range with some property.
- **The tell:** "how many integers in `[0, N]` (with N up to 10^18) satisfy a
  digit condition." You cannot enumerate, so you build the number digit by digit.
- **Note:** advanced; rare in standard interviews, common in competitive rounds.

### 11. Probability and expectation DP

- **State:** a configuration plus the probability or expected value of reaching it.
- **Transition:** weight each move by its probability.
- **Examples:** knight probability on a chessboard, soup servings, new 21 game,
  dice roll simulation.
- **The tell:** the problem asks for a probability or an expected value over random
  moves.

## How to use this map

When a problem smells like DP (a "max/min/count/is-it-possible" over choices with
overlapping subproblems), do not start coding. Match it to a shape above:

- One sequence, one running answer: **linear**.
- Take-or-skip against a budget: **knapsack**.
- Two strings: **two-sequence**.
- A 2D board: **grid**.
- A range split by a midpoint: **interval**.
- n <= 20 and "which subset": **bitmask**.
- A few modes: **state-machine**.
- A tree: **tree DP**.

Then write the state sentence, the transition, and the base case. The shape hands
you all three. When two shapes seem to fit, code the one whose state you can state
most precisely; a state you can say in one clear sentence is a state you can
implement.

> Depth lives in the core files: [DP I](21-dp-linear-knapsack.md),
> [DP II](22-dp-strings.md), [DP III](23-dp-grids-intervals.md),
> [state-machine DP](30-state-machine-dp.md). This page is the index that points
> you to the right one.
