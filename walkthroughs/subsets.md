# Walkthrough: Subsets (LC 78)

A worked example that narrates the six-step solving framework on one problem, so
you can see the process in motion rather than just the finished code.

## The problem

**LeetCode 78, Subsets, Medium.** Given an integer array `nums` of unique
elements, return all possible subsets (the power set). The solution set must not
contain duplicate subsets, and you may return the subsets in any order.

Example: `nums = [1, 2, 3]` returns
`[[], [1], [2], [3], [1,2], [1,3], [2,3], [1,2,3]]` (any order).

## 1. Clarify and restate

Questions I would ask before touching code:

- **Are the elements unique?** The prompt says yes. That matters: if there were
  duplicates I would need the LC 90 "Subsets II" dedup logic (sort, then skip
  equal siblings). Unique elements mean every subset I generate is automatically
  distinct, so no dedup step.
- **What is the output type?** A list of lists of ints. Order of subsets does not
  matter, and order within a subset does not matter, but I will keep elements in
  input order for readability.
- **How big is n?** The constraint is `1 <= nums.length <= 10`. That is the single
  most important number in the room. There are `2^n` subsets, so for n = 10 the
  answer itself has 1024 subsets. n <= 10 is the classic "backtracking is fine,
  exponential output is expected" signal. I am not going to beat `2^n`, because the
  output is that big.
- **Edge cases.** Empty array (the problem says length >= 1, but a robust solution
  should still return `[[]]`). Single element returns `[[], [x]]`. Negatives and
  zero are allowed values but do not change the logic, the values are opaque tokens
  here.

Restated: build the power set. Every element is either in a subset or out of it,
so there are exactly `2^n` subsets, and I need to enumerate all of them.

## 2. Work an example by hand

Take `nums = [1, 2, 3]`. I will build subsets by walking left to right and, at
each element, deciding "include it" or "skip it". That is a binary decision per
element, so the choices form a depth-3 decision tree:

```
                          start []
                 include 1 /        \ skip 1
                    [1]                []
          inc 2 /      \ skip 2   inc 2 /   \ skip 2
        [1,2]          [1]         [2]        []
       i3/  \s3       i3/ \s3     i3/ \s3    i3/ \s3
  [1,2,3] [1,2]   [1,3] [1]   [2,3] [2]  [3]   []
```

Reading off the leaves gives all 8 subsets. The structure is clean: at depth `i`
I decide element `i`, and each root-to-leaf path is one subset. Eight leaves,
`2^3 = 8` subsets. The tree is the algorithm.

## 3. Brute force

The "obvious" enumeration is the bitmask trick: every subset corresponds to an
n-bit number from `0` to `2^n - 1`, where bit `j` set means "include `nums[j]`".
This is genuinely a valid solution, not just a strawman, but I call it the brute
force because it is the mechanical enumeration before I reach for the pattern.

```python
def subsets_bitmask(nums):
    n = len(nums)
    result = []
    for mask in range(1 << n):           # 0 .. 2^n - 1
        subset = []
        for j in range(n):
            if mask & (1 << j):          # is bit j set?
                subset.append(nums[j])
        result.append(subset)
    return result
```

Complexity: the outer loop runs `2^n` times, the inner loop runs `n` times, so
`O(n * 2^n)` time and `O(n * 2^n)` space for the output. That is optimal for the
time, since the output is that large. The reason I do not stop here in an
interview is that the interviewer usually wants the recursive decision tree, which
generalizes to "Subsets II", "Combinations", "Permutations", and every other
enumeration problem.

## 4. Find the bottleneck and pick the pattern

There is no repeated-work bottleneck to remove here, `O(n * 2^n)` is the floor
because the answer has that many entries. The thing the bitmask version does not
show is the **structure of the decision**, and that structure is what the
interviewer is testing and what transfers to harder problems.

The signal is textbook: "return all possible subsets", "every combination". That
is the **backtracking** signal. Backtracking is a depth-first walk of the decision
tree where you make a choice, recurse, then undo the choice (choose / explore /
unchoose). It builds one shared `path` list and mutates it in place, which is why
it is memory-lean compared to copying at every node.

The decision at each node: for element `i`, either include it in the current path
or not. I record a subset at every node of the tree, not just the leaves, because
every prefix of choices is itself a valid subset (this is the difference from
"combinations of size k", where you only record at the leaves).

## 5. Code it

```python
from typing import List

class Solution:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        result = []
        path = []

        def backtrack(start: int) -> None:
            # Every node is a valid subset: record a copy of the current path.
            result.append(path[:])
            # Try adding each remaining element as the next choice.
            for i in range(start, len(nums)):
                path.append(nums[i])        # choose
                backtrack(i + 1)            # explore with i consumed
                path.pop()                  # unchoose (backtrack)

        backtrack(0)
        return result
```

The invariant: when `backtrack(start)` is called, `path` holds a valid subset
built from elements before `start`, and the loop extends it using only elements at
index `start` or later. Passing `i + 1` (not `start + 1`) is what prevents
revisiting earlier elements and so prevents duplicate subsets like `[2,1]` and
`[1,2]`. The `path[:]` copy is essential: `path` is mutated throughout, so I must
snapshot it, not store a reference.

## 6. Test, trace, and analyze

Trace `nums = [1, 2, 3]`:

- `backtrack(0)` records `[]`. Loop i=0: push 1, recurse.
  - `backtrack(1)` records `[1]`. Loop i=1: push 2, recurse.
    - `backtrack(2)` records `[1,2]`. Loop i=2: push 3, recurse.
      - `backtrack(3)` records `[1,2,3]`, loop empty, return. Pop 3.
    - Pop 2. Loop i=2: push 3, recurse.
      - `backtrack(3)` records `[1,3]`, return. Pop 3.
    - Return. Pop 1.
  - Loop i=1: push 2, recurse.
    - `backtrack(2)` records `[2]`. Loop i=2: push 3, recurse.
      - records `[2,3]`, return. Pop 3.
    - Return. Pop 2.
  - Loop i=2: push 3, recurse.
    - records `[3]`, return. Pop 3.

Collected: `[], [1], [1,2], [1,2,3], [1,3], [2], [2,3], [3]`. That is all 8
subsets, matching the hand trace. Correct.

Edge cases:

- `nums = []`: `backtrack(0)` records `[]`, loop does not run, returns `[[]]`. The
  power set of the empty set is the set containing the empty set. Correct.
- `nums = [0]`: records `[]`, then pushes 0 and records `[0]`, returns
  `[[], [0]]`. Correct, and note zero is handled like any value.
- Negatives, e.g. `nums = [-1, 5]`: values are opaque, returns
  `[[], [-1], [-1, 5], [5]]`. Correct.

Complexity: **O(n * 2^n) time** (there are `2^n` subsets and copying each into the
result costs up to `O(n)`), which is optimal because the output is that size.
**Space: O(n * 2^n)** for the output, or **O(n)** auxiliary if you exclude the
output (the recursion depth and the `path` list are both bounded by n). With more
time I would mention the bitmask version as an iterative alternative that avoids
recursion depth, and the "Subsets II" dedup follow-up for non-unique input.

## What the interviewer is really testing

Whether you can model a problem as a decision tree and translate that tree into
clean choose / explore / unchoose recursion without leaking state between
branches. Subsets is the simplest member of a large family (combinations,
permutations, partitions, N-Queens), so getting the `path[:]` snapshot and the
`i + 1` recursion boundary right here signals you will get the harder members
right too.

> Pattern: [20 backtracking](../patterns/20-backtracking.md)
