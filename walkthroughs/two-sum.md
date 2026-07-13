# Walkthrough: Two Sum (LC 1)

A worked example that runs the six-step framework on one problem end to end.
The goal is to show the process, not just the answer.

## The problem

**LeetCode 1, Easy.** Given an array of integers `nums` and an integer `target`,
return the indices of the two numbers that add up to `target`. Each input has
exactly one solution, and you may not use the same element twice. Return the two
indices in any order.

Example: `nums = [2, 7, 11, 15]`, `target = 9` returns `[0, 1]` because
`nums[0] + nums[1] = 2 + 7 = 9`.

## 1. Clarify and restate

The questions I would ask:

- **Input types.** `nums` is a list of integers, `target` is an integer. Can the
  values be negative? Yes, so I cannot assume anything about ordering or sign. Is
  the array sorted? No, and that matters: a sorted array would open up a two
  pointer solution, but here the input is arbitrary order.
- **What do I return?** The two **indices**, not the values themselves. This is a
  common trip-up: if I sort the array I destroy the original indices, so any sort
  based approach needs to carry the original positions along.
- **Uniqueness.** The problem guarantees exactly one solution, so I do not have to
  handle "no answer" or "multiple answers". I also may not reuse the same element,
  so index `i` cannot pair with itself.
- **Constraints.** `nums` length is between 2 and `10^4`. That is small enough that
  O(n^2) would technically pass, but the interesting answer is O(n), and the size
  is a hint that a single pass is the intended target.
- **Edge cases.** Exactly two elements (the minimum); duplicate values that form
  the pair (like `[3, 3]`, target `6`); negatives that sum to zero (like
  `[-3, 4, 3, 90]`, target `0`).

Restated: find the one pair of distinct positions whose values sum to `target`,
and return those positions.

## 2. Work an example by hand

`nums = [2, 7, 11, 15]`, `target = 9`.

I walk left to right and, for each number, ask "what value would I need to have
already seen to complete the pair?" That needed value is `target - current`.

- Index 0, value `2`. Complement is `9 - 2 = 7`. Have I seen a 7 yet? No. Remember
  that value 2 lives at index 0.
- Index 1, value `7`. Complement is `9 - 7 = 2`. Have I seen a 2 yet? Yes, at index
  0. Answer is `[0, 1]`.

Notice what made this fast: at index 1 I did not re-scan the earlier elements, I
just asked a single "have I seen 2?" question and got an instant yes. That
"have I seen this value" question is the whole problem.

## 3. Brute force

Check every pair of indices and return the first that sums to `target`.

```python
def two_sum_brute(nums, target):
    n = len(nums)
    for i in range(n):
        for j in range(i + 1, n):
            if nums[i] + nums[j] == target:
                return [i, j]
    return []
```

The outer loop runs n times, the inner loop runs up to n times, so this is
**O(n^2)** time and **O(1)** space. Correct and easy to reason about, but every
inner loop re-scans values I have already walked past once. That re-scanning is
the waste.

## 4. Find the bottleneck and pick the pattern

The brute force asks, for each `i`, "does any later `j` complete the pair?" and
answers it by scanning the rest of the array. But the question is really a lookup:
"is the complement `target - nums[i]` somewhere in the array?" A linear scan
answers a membership question in O(n); a **hash map** answers the same question in
O(1).

This is the textbook signal for **hashing**: I am repeating a "have I seen this
value" lookup, and a hash map (dictionary) collapses each lookup to constant time.
The extra insight is that I do not even need two passes. As I walk the array once,
I can check whether the complement is already in the map (from an earlier index)
and, if not, record the current value and index. Anything that pairs with a later
element will find its partner when that later element is the one being examined.

So I store `value -> index` as I go, and for each new value I look up its
complement before inserting. The map only ever contains elements strictly to the
left of the current one, which automatically enforces the "two distinct indices"
rule.

## 5. Code it

```python
def two_sum(nums, target):
    seen = {}                      # value -> index, for elements to the left
    for i, x in enumerate(nums):
        need = target - x          # the value that would complete the pair
        if need in seen:
            return [seen[need], i] # earlier index first, then current
        seen[x] = i                # record x only after checking, avoids self-pair
    return []                      # unreachable given the one-solution guarantee
```

Two details that read as careful. First, I check `need in seen` **before**
inserting `x`, so a value can never pair with itself: at the moment I test index
`i`, the map holds only indices `0..i-1`. Second, I return `[seen[need], i]` with
the earlier index first, which is tidy even though the problem accepts any order.

The loop invariant: after processing index `i`, `seen` maps every value in
`nums[0..i]` to its index, and no valid pair exists among those first `i + 1`
elements (or I would have already returned).

## 6. Test, trace, and analyze

Trace `nums = [3, 2, 4]`, `target = 6`.

| i | x | need = 6 - x | need in seen? | seen after step |
|---|---|--------------|---------------|-----------------|
| 0 | 3 | 3 | no | {3: 0} |
| 1 | 2 | 4 | no | {3: 0, 2: 1} |
| 2 | 4 | 2 | yes, at index 1 | return [1, 2] |

Returns `[1, 2]`, correct: `nums[1] + nums[2] = 2 + 4 = 6`. Note that at index 0
the complement of 3 is also 3, but the map was still empty, so it did not falsely
pair 3 with itself.

Edge cases:
- **Two elements**, `nums = [3, 3], target = 6`: index 0 records `{3: 0}`, index 1
  looks up complement `3`, finds it at index 0, returns `[0, 1]`. The duplicate
  value is handled correctly because we keyed on value and checked before
  inserting.
- **Negatives summing to zero**, `nums = [-3, 4, 3, 90], target = 0`: index 0
  records `{-3: 0}`, index 2 (value 3) looks up complement `-3`, finds it, returns
  `[0, 2]`. Correct.
- **Minimum size**, any two-element array that sums to target: the pair is found on
  the second iteration.

**Complexity: O(n) time**, one pass with an O(1) hash lookup and insert per
element, and **O(n) extra space** for the map in the worst case (no pair until the
very end). This trades space for time versus the O(n^2), O(1) brute force, which is
the classic hashing bargain.

With more time I would mention the follow-up: if the array were already **sorted**,
I could drop the hash map and use two pointers from both ends for O(n) time and
O(1) space. The pattern choice hinges entirely on whether the input is sorted, and
here it is not.

## What the interviewer is really testing

Whether you recognize a "have I seen this value" question hiding inside a pairwise
scan, and whether you reach for a hash map to make that lookup O(1). The deeper
signal is the single-pass insight: that you do not need to build the whole map
first and then search it, because each element that needs an earlier partner will
find it exactly when it is examined. Candidates who jump straight to O(n) without
first naming the O(n^2) brute force lose the process credit; the strong move is to
state the brute force, point at the repeated lookup as the bottleneck, and name
hashing as the tool that removes it.

> Pattern: [04 hashing](../patterns/04-hashing.md)
