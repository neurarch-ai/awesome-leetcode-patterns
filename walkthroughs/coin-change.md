# Walkthrough: Coin Change (LC 322)

A worked example that narrates the six-step solving framework on one problem, so
you can see the process in motion rather than just the finished code. This one
walks the full DP arc: brute-force recursion to memoization to tabulation.

## The problem

**LeetCode 322, Coin Change, Medium.** You are given an integer array `coins`
representing coin denominations and an integer `amount`. Return the fewest number
of coins needed to make up that amount. If the amount cannot be made from any
combination of the coins, return `-1`. You have an unlimited supply of each coin.

Example: `coins = [1, 2, 5]`, `amount = 11` returns `3` (11 = 5 + 5 + 1).

![Dynamic programming over a 1D choice](../assets/dp-linear.svg)

*Dynamic programming over a 1D choice. See the full pattern in the linked file below.*

## 1. Clarify and restate

Questions I would ask before touching code:

- **Unlimited supply of each coin?** Yes. That makes this the **unbounded
  knapsack** shape (each item reusable), not 0/1 knapsack. If supply were limited I
  would need a different state.
- **What do I return?** The minimum coin count, not the set of coins. And crucially
  `-1` when the amount is unreachable, so I need a sentinel for "impossible" that
  survives the min operation.
- **Can amount be 0?** Yes, and the answer is `0` coins. That is the base case, not
  an edge to special-case later.
- **Can coins be empty, or larger than amount?** Coins can be larger than amount
  (they just never apply). If `coins` is empty and `amount > 0`, the answer is
  `-1`.
- **How big is n?** Constraints: `1 <= coins.length <= 12`,
  `1 <= coins[i] <= 2^31 - 1`, `0 <= amount <= 10^4`. The key number is
  `amount <= 10^4`, and there are at most 12 coins. So an `O(amount * len(coins))`
  table (about 120,000 cells) is trivially fast. That constraint is the hint: it
  points straight at a DP over amounts, not at enumerating combinations (which
  would be exponential).
- **Edge cases.** `amount = 0` returns 0. Unreachable amount, e.g.
  `coins = [2], amount = 3`, returns -1. A coin equal to the amount returns 1.

Restated: find the minimum-cardinality multiset of coins summing to `amount`, or
report that no such multiset exists.

## 2. Work an example by hand

`coins = [1, 2, 5]`, `amount = 11`. I will think in terms of "best for each
sub-amount", building up:

- Best for 0: 0 coins.
- Best for 1: 1 (use a 1).
- Best for 2: 1 (use a 2).
- Best for 3: 2 (2 + 1).
- Best for 4: 2 (2 + 2).
- Best for 5: 1 (use a 5).
- Best for 6: 2 (5 + 1).
- ...
- Best for 10: 2 (5 + 5).
- Best for 11: best of (1 + best[10]), (1 + best[9]), (1 + best[6]) across coins
  1, 2, 5 = 1 + best[10] = 1 + 2 = 3, or 1 + best[6] = 1 + 2 = 3. So 3.

Notice what happened: to solve 11, I only needed the answers to 10, 9, and 6, the
amounts I reach by removing one coin. Each of those I already solved. That reuse of
smaller answers is the DP structure surfacing on its own.

## 3. Brute force

The obvious recursion: to make `amount`, try each coin as the "last" coin used,
recurse on the remainder, and take the minimum. Base case: making 0 costs 0 coins;
a negative remainder is invalid.

```python
def coin_change_brute(coins, amount):
    def dfs(remaining):
        if remaining == 0:
            return 0
        if remaining < 0:
            return float("inf")          # invalid path
        best = float("inf")
        for coin in coins:
            best = min(best, 1 + dfs(remaining - coin))
        return best

    result = dfs(amount)
    return result if result != float("inf") else -1
```

Complexity: each call branches into `len(coins)` children and the recursion depth
is up to `amount` (using all 1-coins), so this is `O(len(coins) ^ amount)` time,
exponential. For `amount = 10^4` it never finishes. It is correct, and it returns
`-1` properly via the `inf` sentinel, but it is unusable at the given constraints.

## 4. Find the bottleneck and pick the pattern

Look at the recursion tree. `dfs(6)` gets computed on the way to 11 via coin 5,
and again via other paths, and every one of those recomputes `dfs(5)`, `dfs(4)`,
and so on. The **same sub-amounts are solved over and over**. That is the exact
signal for **dynamic programming**: overlapping subproblems plus optimal
substructure (the best way to make 11 is built from the best way to make some
smaller amount).

This is the **unbounded knapsack** flavor because each coin can be reused, so when
I take a coin I recurse on `remaining - coin` with the *same* coin set still fully
available (I do not consume the coin). The DP recipe:

- **State:** `dp[a]` = the minimum number of coins to make amount `a`.
- **Transition:** `dp[a] = min(dp[a - coin] + 1)` over every `coin <= a`.
- **Base case:** `dp[0] = 0`. Every other `dp[a]` starts at "infinity" (I use
  `amount + 1` as a safe sentinel, since no real answer can exceed `amount` coins).

I will show both the memoized top-down form (which is the brute force plus a cache)
and the bottom-up table, which is what I would hand over.

**Memoized (top-down):**

```python
from functools import lru_cache

def coin_change_memo(coins, amount):
    @lru_cache(maxsize=None)
    def dfs(remaining):
        if remaining == 0:
            return 0
        if remaining < 0:
            return float("inf")
        return min((1 + dfs(remaining - coin)) for coin in coins)

    result = dfs(amount)
    return result if result != float("inf") else -1
```

The cache collapses the exponential tree: each distinct `remaining` from 0 to
`amount` is computed once, so this is `O(amount * len(coins))`.

## 5. Code it

The bottom-up tabulation, which avoids recursion depth entirely:

```python
from typing import List

class Solution:
    def coinChange(self, coins: List[int], amount: int) -> int:
        # dp[a] = fewest coins to make amount a. amount + 1 is an "impossible"
        # sentinel: no reachable amount needs more than `amount` coins.
        dp = [0] + [amount + 1] * amount

        for a in range(1, amount + 1):
            for coin in coins:
                if coin <= a:
                    dp[a] = min(dp[a], dp[a - coin] + 1)

        return dp[amount] if dp[amount] != amount + 1 else -1
```

The invariant: when the outer loop reaches amount `a`, every `dp[a - coin]` for a
smaller amount is already final, so `dp[a]` sees correct subproblem answers. The
sentinel `amount + 1` is chosen so it is strictly larger than any real answer (the
worst real case is `amount` coins of denomination 1), which means it never wins a
`min` and cleanly marks "unreachable" at the end.

## 6. Test, trace, and analyze

Trace `coins = [1, 2, 5]`, `amount = 11`. Table after the fill (each cell is the
min coin count):

```
a    : 0  1  2  3  4  5  6  7  8  9  10 11
dp[a]: 0  1  1  2  2  1  2  3  3  4  2  3
```

Spot-check `dp[11]`: candidates are `dp[10] + 1 = 3`, `dp[9] + 1 = 5`,
`dp[6] + 1 = 3`. Min is 3. Matches the hand computation. Correct.

Edge cases:

- `coins = [2], amount = 3`: `dp[1]` stays at `amount + 1 = 4` (no coin fits),
  `dp[2] = 1`, `dp[3]` tries `dp[1] + 1 = 5` which is the sentinel-plus-one, so
  `dp[3]` remains `4`. Final check `dp[3] == 4` is true, so return `-1`. Correct,
  the unreachable case is handled.
- `amount = 0`: `dp = [0]`, the loop does not run, `dp[0] = 0 != 1`, return `0`.
  Correct.
- `coins = [1], amount = 2`: `dp[1] = 1`, `dp[2] = dp[1] + 1 = 2`, return `2`.
  Correct.
- Coin larger than amount, `coins = [5, 10], amount = 3`: no coin ever fits any
  `a <= 3`, all stay at sentinel, return `-1`. Correct.

Complexity: **O(amount * len(coins)) time**, since each of the `amount` cells does
`len(coins)` work, about 120,000 operations at the max constraints.
**O(amount) space** for the table. This is optimal for the standard formulation.
With more time I would note that the transition can be reordered to iterate coins
outer and amounts inner (same result here since we take a min over all coins), and
that reconstructing the actual coin set, not just the count, needs a parent
pointer array.

## What the interviewer is really testing

Whether you can recognize overlapping subproblems, write down the state /
transition / base-case recipe explicitly, and carry a solution from exponential
recursion through memoization to a clean bottom-up table. The `-1` sentinel
handling is a deliberate trap: candidates who forget it produce wrong answers on
unreachable inputs, and the fix reveals whether you actually reasoned about what
"impossible" means in the recurrence.

> Pattern: [21 DP linear and knapsack](../patterns/21-dp-linear-knapsack.md)
