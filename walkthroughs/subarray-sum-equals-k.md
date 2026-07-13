# Walkthrough: Subarray Sum Equals K (LC 560)

A worked example that runs the six-step framework on one problem end to end.
The goal is to show the process, not just the answer.

## The problem

**LeetCode 560, Medium.** Given an integer array `nums` and an integer `k`,
return the total number of contiguous subarrays whose elements sum to exactly
`k`. Subarrays are defined by a start and end index, so `[1, 2]` and `[2, 1]`
coming from different positions count separately.

Example: `nums = [1, 1, 1]`, `k = 2` returns `2` (the subarray `[1, 1]` at
indices `0..1` and the one at indices `1..2`).

## 1. Clarify and restate

Before touching code, the questions I would ask out loud:

- **Input types.** `nums` is a list of integers. Can the values be negative or
  zero? This matters a lot. If everything were positive, a sliding window would
  work because the running sum is monotonic. The problem allows negatives and
  zeros, which kills the window idea and forces a different tool. Assume negatives
  are allowed unless told otherwise.
- **What do I return?** A count of subarrays, not the subarrays themselves and
  not their indices. Just an integer.
- **Constraints.** Typical limits are `n` up to `2 * 10^4` and values in
  `[-1000, 1000]`, with `k` in the full int range. Reading `n`: `2 * 10^4` means
  an O(n^2) solution is roughly `4 * 10^8` operations, which is borderline too
  slow. The setter is signalling that the intended answer is O(n).
- **Edge cases.** Empty array (answer `0`), a single element equal to `k`
  (answer `1`), `k = 0` with zeros in the array (each zero is its own valid
  subarray), and negatives that let a longer prefix loop back to the same sum.

Restated: count contiguous slices that sum to `k`, over an array that can contain
negatives, in O(n) if possible.

## 2. Work an example by hand

Take `nums = [3, 4, 7, 2, -3, 1, 4, 2]`, `k = 7`.

By eye, the subarrays summing to 7 are:
- `[3, 4]` at indices `0..1`
- `[7]` at index `2`
- `[7, 2, -3, 1]` at indices `2..5`
- `[1, 4, 2]` at indices `5..7`

That is four subarrays. Notice the third one only exists because the `-3` pulls
a longer run back down to 7. This is exactly the case a positive-only sliding
window would miss, and it is why I need a technique that handles negatives.

## 3. Brute force

The obvious solution: fix every start index, extend the end index, keep a running
sum, and count each time it hits `k`.

```python
def subarray_sum_brute(nums, k):
    count = 0
    n = len(nums)
    for start in range(n):
        running = 0
        for end in range(start, n):
            running += nums[end]      # sum of nums[start..end]
            if running == k:
                count += 1
    return count
```

Two nested loops, so **O(n^2) time** and **O(1) space**. Correct, and a fine
fallback, but at `n = 2 * 10^4` it risks timing out.

## 4. Find the bottleneck and pick the pattern

Look at what the brute force repeats. For each new `start` it rebuilds the running
sum from scratch, re-walking territory it already summed for earlier starts. The
work being repeated is **range sums over a moving window**, and the structure I am
not using is that a range sum can be written as a difference of two prefix sums.

Define `prefix[i]` as the sum of `nums[0..i-1]` (so `prefix[0] = 0`). The sum of
the subarray `nums[j..i-1]` is `prefix[i] - prefix[j]`. I want that difference to
equal `k`:

```
prefix[i] - prefix[j] == k   ->   prefix[j] == prefix[i] - k
```

So while scanning left to right and maintaining the current prefix sum, the number
of subarrays ending at position `i` that sum to `k` is exactly the number of
earlier prefix sums equal to `prefix[i] - k`. That is a **repeated lookup**
("how many times have I seen this prefix value"), which points straight at a
**hash map** counting how often each prefix sum has occurred. Prefix sum removes
the inner loop; hashing makes the lookup O(1).

The one subtlety: seed the map with `{0: 1}` before the scan, representing the
empty prefix. That is what lets a subarray starting at index 0 be counted (its
`prefix[j]` is the empty prefix, value 0).

## 5. Code it

```python
from collections import defaultdict

def subarray_sum(nums, k):
    count = 0
    prefix = 0
    # seen[s] = how many prefixes so far have summed to s.
    # Seed with {0: 1} for the empty prefix, so subarrays that start at
    # index 0 are counted.
    seen = defaultdict(int)
    seen[0] = 1

    for x in nums:
        prefix += x                    # prefix sum of everything up to here
        # a subarray ending here sums to k when some earlier prefix == prefix - k
        count += seen[prefix - k]
        seen[prefix] += 1              # record this prefix for future ends

    return count
```

One pass, one dictionary. Note the order inside the loop: I add to `count` using
the map *before* recording the current prefix. This prevents a zero-length
subarray from being counted when `k = 0`, because the current prefix is not yet
in the map when I query it.

## 6. Test, trace, and analyze

Trace the hand example `nums = [3, 4, 7, 2, -3, 1, 4, 2]`, `k = 7`. Start with
`seen = {0: 1}`, `prefix = 0`, `count = 0`.

| x | prefix | prefix - k | seen[prefix - k] | count | seen after |
|---|--------|-----------|------------------|-------|------------|
| 3 | 3 | -4 | 0 | 0 | {0:1, 3:1} |
| 4 | 7 | 0 | 1 | 1 | {0:1, 3:1, 7:1} |
| 7 | 14 | 7 | 1 | 2 | {..., 14:1} |
| 2 | 16 | 9 | 0 | 2 | {..., 16:1} |
| -3 | 13 | 6 | 0 | 2 | {..., 13:1} |
| 1 | 14 | 7 | 1 | 3 | {..., 14:2} |
| 4 | 18 | 11 | 0 | 3 | {..., 18:1} |
| 2 | 20 | 13 | 1 | 4 | {..., 20:1} |

Final `count = 4`, matching the four subarrays I found by hand. The `-3` case is
handled: at `x = 1` the prefix returns to 14, which was seen once before, so the
subarray `[7, 2, -3, 1]` is counted.

Edge cases:
- **Empty array**: the loop never runs, returns `0`. Correct.
- **Single element equal to k**, `nums = [7], k = 7`: prefix becomes 7,
  `seen[0]` is 1, count is 1. Correct.
- **Zeros with k = 0**, `nums = [0, 0, 0], k = 0`: each step queries `seen[prefix]`
  which already holds the count of earlier zero-prefixes, giving `1, 2, 3` added
  cumulatively for a total of 6. The six subarrays are all contiguous slices of
  three zeros. Correct.

**Complexity: O(n) time** (one pass, O(1) map operations) and **O(n) space** for
the map in the worst case where every prefix is distinct. This meets the target
the constraint pointed at, and beats the O(n^2) brute force.

With more time I would note that if the array were guaranteed non-negative, a
sliding window would drop the space to O(1); the hash map is the price of
supporting negatives.

## What the interviewer is really testing

Whether you recognize that "count subarrays with a given sum over possibly
negative values" is a prefix-sum-plus-hashing problem, not a sliding window. The
trap is reaching for a window because it is the reflex for subarray problems; the
negatives break its monotonicity. The seed `{0: 1}` and the query-before-insert
ordering are the two details that separate a candidate who has internalized the
pattern from one who has only memorized its name.

> Pattern: [03 prefix sum](../patterns/03-prefix-sum.md), [04 hashing](../patterns/04-hashing.md)
