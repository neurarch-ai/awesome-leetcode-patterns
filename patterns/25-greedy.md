# 25 - Greedy

> **Problem shape:** "Select the maximum number of non-overlapping intervals."
> "Reach the last index in the fewest jumps." "Can you complete the circuit
> starting from some gas station?" "Burst all balloons with the fewest arrows."
> Problems where a sequence of locally optimal choices, made in the right order,
> provably builds a globally optimal answer, and you never have to reconsider a
> past choice.

Greedy makes the choice that looks best right now and commits to it, never
backtracking. When it is correct, it is the cheapest possible algorithm: usually a
sort plus a single pass, O(n log n) or O(n). The catch, and the entire difficulty
of the pattern, is that "looks best now" is only safe when you can prove the
locally optimal pick never blocks the global optimum. Greedy without that argument
is just a guess that happens to pass some tests.

## The signal

Reach for greedy when you see:

- **"Maximum number of ...", "minimum number of ...", "fewest", "earliest",
  "smallest"** over a set you can order, where each choice is independent enough
  that a local rule decides it.
- **Intervals** to select, merge, or stab: "max non-overlapping", "min arrows to
  burst balloons", "min meeting rooms". Sorting by start or by end unlocks a
  one-pass sweep.
- **Reachability and coverage**: "can you jump to the end", "fewest jumps",
  "minimum number of platforms". You track the furthest you can reach and extend
  it greedily.
- **An exchange feels safe**: you can argue that swapping any optimal solution's
  choice for the greedy choice never makes things worse. That argument is the
  license to be greedy.

The anti-signal: if a choice's payoff depends on choices you have not made yet, or
the same subproblem recurs with overlapping state, greedy will silently return a
wrong answer and you want [DP](21-dp-linear-knapsack.md) instead.

## The idea

Greedy is correct when the problem has the **greedy-choice property**: there exists
a globally optimal solution that agrees with the greedy first choice. You prove it
with an **exchange argument**. Take any optimal solution, and show that
transforming it toward the greedy choice (swapping in the greedy pick for whatever
it did first) keeps it valid and no worse. If every step can be exchanged this
way, the all-greedy solution is optimal.

Concretely, for "max non-overlapping intervals": sort by end time and always take
the interval that finishes earliest among those that still fit. The exchange
argument: any optimal schedule's first interval can be replaced by the
earliest-finishing compatible one without reducing the count, because finishing
earlier only leaves more room for the rest. Repeat, and you have converted the
optimal solution into the greedy one with the same size, so greedy is optimal.

This is the discipline the pattern demands: pick a sort key, state the local rule,
and be able to say why the exchange holds. When you cannot, greedy is unproven and
probably wrong.

**Where greedy fails and DP is needed.** Coin change with arbitrary denominations
is the classic counterexample: greedily taking the largest coin under the target
can overshoot the optimum (coins `[1, 3, 4]`, target `6`, greedy gives `4+1+1 = 3`
coins, optimal is `3+3 = 2`). The choices interact, no exchange argument holds, and
you need DP over subproblems. The 0/1 knapsack is the same story: greedy by
value-per-weight is optimal for the fractional version but not the 0/1 version.

## The template

**Sort, then make the locally optimal pick (max non-overlapping intervals):**

```python
# Time: O(n log n) (dominated by the sort), Space: O(1) auxiliary
def max_non_overlapping(intervals):
    intervals.sort(key=lambda iv: iv[1])   # sort by END time
    count = 0
    current_end = float('-inf')
    for start, end in intervals:
        if start >= current_end:           # fits after the last chosen one
            count += 1
            current_end = end              # commit, never reconsider
    return count
```

**Furthest-reach sweep (jump game I: can you reach the end?):**

```python
# Time: O(n), Space: O(1)
def can_reach_end(nums):
    furthest = 0
    for i, jump in enumerate(nums):
        if i > furthest:                   # a gap we could never bridge
            return False
        furthest = max(furthest, i + jump)
    return True
```

**Level-by-level frontier (jump game II: fewest jumps):**

```python
# Time: O(n), Space: O(1)
def min_jumps(nums):
    jumps = 0
    current_end = 0                        # boundary of the current jump's reach
    furthest = 0                           # best reach seen within this level
    for i in range(len(nums) - 1):
        furthest = max(furthest, i + nums[i])
        if i == current_end:               # must jump now to go further
            jumps += 1
            current_end = furthest
    return jumps
```

**One-pass feasibility with a running deficit (gas station):**

```python
# Time: O(n), Space: O(1)
def can_complete_circuit(gas, cost):
    if sum(gas) < sum(cost):
        return -1                          # not enough fuel overall, impossible
    start = 0
    tank = 0
    for i in range(len(gas)):
        tank += gas[i] - cost[i]
        if tank < 0:                       # cannot reach i+1 from current start
            start = i + 1                   # every station up to i is also invalid
            tank = 0
    return start
```

The gas station argument is worth holding onto: if the total gas covers the total
cost, a valid start exists, and it must be the station right after the last point
where the running tank went negative, because no earlier station could have
survived that stretch either.

## Variations

- **Sort by end vs. sort by start.** For "max non-overlapping" and "min arrows",
  sort by end and greedily extend a boundary. For "merge intervals", sort by start.
  Choosing the wrong key is the most common greedy bug.
- **Min arrows to burst balloons.** Sort by end, shoot an arrow at the first
  balloon's end, and skip every balloon that overlaps that x. It is the
  interval-scheduling greedy counting groups instead of picks. Note the arrow can
  sit on a shared endpoint, so use `>` not `>=` when deciding a new arrow.
- **Non-overlapping intervals (min removals).** The complement of max
  non-overlapping: total minus kept. Same sort-by-end sweep.
- **Best time to buy and sell stock II.** Greedily bank every upward step
  (`sum of max(0, price[i] - price[i-1])`). Since unlimited transactions are
  allowed, capturing each rise is equivalent to any optimal grouping of rises.
- **Partition labels.** Record each character's last index, then extend the
  current partition's end to the furthest last-index of any character seen; cut
  when the scan reaches that end. A greedy furthest-reach sweep in disguise.
- **Stay honest: reach for DP when the exchange breaks.** If picking greedily on
  one axis (largest coin, highest value) can be beaten by a combination, the
  problem has interacting choices. That is the [DP](21-dp-linear-knapsack.md)
  signal, not greedy.

## Canonical problems

| # | Problem | Difficulty | What it drills |
|---|---------|-----------|----------------|
| 122 | Best Time to Buy and Sell Stock II | Medium | Bank every upward step |
| 55 | Jump Game | Medium | Furthest-reach feasibility sweep |
| 45 | Jump Game II | Medium | Level-by-level frontier for fewest jumps |
| 134 | Gas Station | Medium | Running deficit picks the start |
| 435 | Non-overlapping Intervals | Medium | Sort by end, count removals |
| 452 | Minimum Number of Arrows to Burst Balloons | Medium | Interval stabbing, shared endpoints |
| 763 | Partition Labels | Medium | Furthest last-index sweep |
| 621 | Task Scheduler | Medium | Greedy placement of the most frequent task |

## Pitfalls

- **Skipping the correctness argument.** The number-one greedy failure is assuming
  the local rule is optimal because it passes the examples. If you cannot sketch an
  exchange argument, treat greedy as unproven and check whether DP is required.
- **Sorting by the wrong key.** By start when you needed by end (or vice versa)
  quietly produces a plausible but wrong answer. For interval selection, sort by
  end; internalize why (earliest finish leaves the most room).
- **Off-by-one on endpoint equality.** "Intervals touching at a point" may or may
  not count as overlapping. Decide whether `>=` or `>` is correct for the specific
  problem (arrows share endpoints; some scheduling problems do not).
- **Greedy on a problem with interacting choices.** Coin change with arbitrary
  denominations, 0/1 knapsack, longest increasing subsequence: greedy gives wrong
  answers. Overlapping subproblems mean DP.
- **Jump Game II loop bounds.** Iterate to `len(nums) - 1`, not the last index,
  otherwise you count one extra jump when the final element itself would trigger a
  boundary advance.
- **Ignoring the global feasibility check.** In gas station, the total-gas vs
  total-cost check is what licenses the single-pass start search; without it the
  greedy start is meaningless.

## Follow-ups and related patterns

- "Greedy gives a wrong answer here" is the standard pivot to
  [DP: linear and knapsack](21-dp-linear-knapsack.md); coin change and 0/1
  knapsack are the canonical greedy-fails-DP-wins examples.
- "These are intervals, sweep them" connects to
  [intervals and sweep line](05-intervals.md); interval-scheduling greedy is a
  sweep with a commit rule.
- "Sort first" makes greedy a companion of
  [sorting and custom comparators](08-sorting.md); the sort key is usually the
  whole insight.
- "Repeatedly pull the current best" turns a greedy choice into a
  [heap](24-heap.md) when the candidate set changes as you go (task scheduler,
  reorganize string).
```
