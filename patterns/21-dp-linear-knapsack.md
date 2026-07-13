# 21 - DP I: linear and knapsack

> **Problem shape:** "How many ways to climb n stairs?" "Max money you can rob
> without hitting two adjacent houses." "Largest sum of a contiguous subarray."
> "Fewest coins to make an amount." "Can this array be split into two equal-sum
> halves?" Anything where an optimal or counted answer over a sequence or a set of
> items decomposes into the same question on a smaller prefix or a smaller
> capacity.

Dynamic programming solves a problem by solving overlapping subproblems once and
reusing the answers. This first DP file covers the two foundational shapes: 1D
linear DP over a sequence, and knapsack DP over items with a capacity budget. Get
the recipe here and the string and grid DP in the next files become variations.

## The signal

Reach for DP when you see:

- **"Maximum", "minimum", "how many ways", "is it possible"** over a sequence or a
  set, where a greedy choice is not obviously safe and brute force is exponential.
- **Optimal substructure**: the best answer for `n` is built from the best answers
  for smaller inputs (`n-1`, `n-2`, or a smaller capacity). If you can write the
  answer as a recurrence on smaller instances, DP applies.
- **Overlapping subproblems**: the naive recursion recomputes the same call many
  times. Fibonacci-style branching, `f(n) = f(n-1) + f(n-2)`, is the giveaway.
- **A choice per element** ("take it or skip it") with a shared budget (a target
  sum, a weight capacity). That "take or skip against a budget" is exactly
  knapsack.

If choices are independent and a local optimum is provably global, it is
[greedy](25-greedy.md), not DP. DP is what you use when a locally worse choice can
lead to a globally better answer.

## The idea

Every DP is four decisions. Nail these and the code writes itself:

1. **State**: what does `dp[i]` (or `dp[i][c]`) *mean*? Pin it to a precise English
   sentence, for example "the max money robbable from the first `i` houses" or
   "the min coins to make amount `c`". A fuzzy state definition is the root of most
   DP bugs.
2. **Transition**: how is one state built from smaller ones? This is the
   recurrence, and it usually encodes a choice: `dp[i] = max(skip, take)`.
3. **Base case**: the smallest states you can fill directly, `dp[0]`, `dp[1]`, or
   `dp[...][0]`. Getting these wrong shifts every later value.
4. **Evaluation order**: fill states so that every value a transition reads is
   already computed. For linear DP that is left to right; for knapsack the order
   also decides 0-1 vs unbounded (see below).

The payoff: a naive recursion that branches into `O(2^n)` calls collapses to
`O(n)` or `O(n * capacity)` once each state is computed once and cached. You are
trading exponential recomputation for a polynomial-size table.

## The template

**1D linear DP, house robber (skip vs take):**

```python
def rob(nums):
    prev2, prev1 = 0, 0                    # best up to i-2, i-1
    for x in nums:
        # state: best money considering houses so far
        # transition: skip this house (prev1) or take it (prev2 + x)
        prev2, prev1 = prev1, max(prev1, prev2 + x)
    return prev1
```

**Kadane, max subarray (the running-best must either extend or restart):**

```python
def max_subarray(nums):
    best = cur = nums[0]
    for x in nums[1:]:
        cur = max(x, cur + x)              # extend the run, or start fresh at x
        best = max(best, cur)
    return best
```

**0-1 knapsack / subset sum (each item used at most once):**

```python
def can_partition_to(nums, target):
    # dp[c] = True if some subset sums to exactly c
    dp = [False] * (target + 1)
    dp[0] = True
    for x in nums:                         # outer loop: items
        for c in range(target, x - 1, -1): # inner loop DOWNWARD: 0-1, no reuse
            dp[c] = dp[c] or dp[c - x]
    return dp[target]
```

**Unbounded knapsack, coin change (each coin reusable, count the min):**

```python
def coin_change(coins, amount):
    INF = float('inf')
    dp = [0] + [INF] * amount              # dp[c] = min coins to make c
    for c in range(1, amount + 1):
        for coin in coins:
            if coin <= c:
                dp[c] = min(dp[c], dp[c - coin] + 1)
    return dp[amount] if dp[amount] != INF else -1
```

The single most important knapsack detail: **iterate capacity downward for 0-1**
(so each item is used at most once) and **upward for unbounded** (so an item can be
picked again within the same pass).

## Variations

- **Climbing stairs / distinct ways.** Same recurrence as Fibonacci,
  `dp[i] = dp[i-1] + dp[i-2]`. The base cases and what "a way" means are the only
  content; space collapses to two rolling variables.
- **Counting knapsack (coin change II, target sum).** Swap `min`/`max` for a sum:
  `dp[c] += dp[c - coin]`. For "count combinations" put the item loop outside and
  capacity inside; for "count permutations" swap the loop order. This ordering is a
  frequent bug.
- **Subset sum / partition equal subset.** Total must be even; the target is
  `total // 2`; then it is boolean 0-1 knapsack. Target Sum (assign + and -) is the
  same after the algebra `positives = (total + target) / 2`.
- **House robber II (circular).** Run the linear robber twice, once excluding the
  first house and once excluding the last, and take the max. A wrapper trick over
  the base recurrence.
- **Max product subarray.** Kadane with a twist: track both the running max and the
  running min, because a negative number flips them.

## The memoization to tabulation to space progression

Almost every DP can be written three ways, and knowing the progression lets you
start correct and end fast:

1. **Top-down memoization.** Write the recurrence as a recursive function and cache
   results (`@functools.lru_cache` or a dict). Closest to the natural recursion,
   easiest to get right, only computes reachable states.
2. **Bottom-up tabulation.** Turn the recursion into a loop that fills a table in
   dependency order. No recursion depth limits, and the loop order makes the
   evaluation order explicit.
3. **Space optimization.** If `dp[i]` reads only `dp[i-1]` (and `dp[i-2]`), replace
   the array with a couple of rolling variables, dropping `O(n)` space to `O(1)`.
   Knapsack rows collapse to a single 1D array the same way.

Prototype top-down to get the recurrence right, then rewrite bottom-up and shrink
the space if the interviewer asks. Do not start by micro-optimizing space; get a
correct table first.

## Canonical problems

| # | Problem | Difficulty | What it drills |
|---|---------|-----------|----------------|
| 70 | Climbing Stairs | Easy | The Fibonacci recurrence; two rolling vars |
| 198 | House Robber | Medium | Skip-vs-take linear DP, O(1) space |
| 53 | Maximum Subarray | Medium | Kadane: extend the run or restart |
| 322 | Coin Change | Medium | Unbounded knapsack, minimize count |
| 518 | Coin Change II | Medium | Counting knapsack; item loop outside |
| 416 | Partition Equal Subset Sum | Medium | 0-1 subset sum, capacity loop downward |
| 494 | Target Sum | Medium | +/- assignment reduces to subset-count |
| 279 | Perfect Squares | Medium | Unbounded knapsack over square coins |

## Pitfalls

- **A vague state definition.** If you cannot say in one sentence what `dp[i]`
  means, the transition will be wrong. Write the sentence first, then the
  recurrence.
- **0-1 vs unbounded loop direction.** Iterating capacity upward in a 0-1 problem
  reuses items (wrong answer); iterating downward in an unbounded problem forbids
  reuse. This is the number-one knapsack bug.
- **Combinations vs permutations in counting.** Coin Change II counts combinations
  (item loop outside). Swapping the loops counts ordered sequences instead, a
  different number.
- **Wrong or missing base case.** `dp[0]` is usually the empty-input answer
  (`0` coins, `True` for sum zero, `1` way to make nothing). An off base case is
  off by a constant everywhere downstream.
- **Overwriting a value you still need.** In space-optimized linear DP, update
  `prev2, prev1` simultaneously (tuple assignment) so the new `prev1` does not
  clobber the `prev2` the transition still reads.
- **Reaching for DP when greedy suffices.** If a single scan with a local rule is
  provably optimal, DP is overkill; conversely, do not force greedy where a locally
  worse choice can win globally.

## Follow-ups and related patterns

- "Now it is over two sequences" or "it is a subsequence, not contiguous" pushes to
  [DP II: subsequences and strings](22-dp-strings.md), where the state gains a
  second index.
- "It is a grid, or an interval, or a subset-as-bitmask" pushes to
  [DP III: grids, intervals, bitmask](23-dp-grids-intervals.md).
- "Enumerate the actual subsets, not just count or optimize them" pushes back to
  [backtracking](20-backtracking.md); DP is the memoized collapse of that same
  decision tree.
- "A local greedy choice is provably optimal here" pushes to
  [greedy](25-greedy.md), which is DP without the table when exchange arguments
  hold.
- "The recurrence has a monotone structure I can search over" (as in longest
  increasing subsequence) connects to [binary search](07-binary-search.md), which
  turns an `O(n^2)` DP into `O(n log n)`.
