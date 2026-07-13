# 03 - Prefix sum and difference arrays

> **Problem shape:** "How many subarrays sum to k?" "Answer many range-sum
> queries fast." "Sum over a rectangle of a matrix." "Apply hundreds of range
> updates, then read the array." Anything that asks about the total over a
> range, repeatedly, or that batches range updates, over an array or a grid.

Prefix sum precomputes cumulative totals so any range sum becomes one
subtraction instead of a loop. It trades O(n) setup for O(1) per query, and its
inverse, the difference array, does the same for batched range updates. Both are
about moving work out of the query and into a one-time pass.

## The signal

Reach for prefix sum when you see:

- **Repeated range-sum queries** on a static array. If you will ask "sum of
  `a[i..j]`" more than once, precompute prefixes and answer each in O(1).
- **"Count subarrays whose sum equals / is divisible by k".** The subarray sum
  `a[i..j]` equals `prefix[j+1] - prefix[i]`, so a target sum becomes a lookup on
  seen prefix values (this is where a hash map enters).
- **A 2D grid with rectangle-sum questions** (the integral image). Precompute a
  running sum over the matrix, then any submatrix is four array reads.
- **Many range updates, one final read** ("add v to every index in `[l, r]`",
  repeated). That is the difference array: record the change at the two
  boundaries, integrate once at the end.
- **Prefix XOR** when the question is about XOR over a range instead of a sum. XOR
  is its own inverse, so the same subtraction trick works with `^`.

The tell is that the naive solution recomputes overlapping sums, and the overlap
is exactly what a cumulative array lets you reuse.

## The idea

Define `prefix[k] = a[0] + a[1] + ... + a[k-1]`, with `prefix[0] = 0`. Then the
sum of `a[i..j]` inclusive is `prefix[j+1] - prefix[i]`. The two shared endpoints
cancel, which is why one subtraction replaces a loop. Building the array is one
O(n) pass; every range query afterward is O(1).

The subarray-sum-equals-k trick reads the same identity backward. You want pairs
`(i, j)` with `prefix[j+1] - prefix[i] == k`. Walk the array keeping the running
prefix `s`; at each step the number of valid starts is the number of earlier
prefixes equal to `s - k`. A hash map of "how many times each prefix value has
occurred" answers that in O(1), so the whole count is a single O(n) pass.

The difference array is the dual. If you want to add `v` to every element in
`[l, r]`, record `diff[l] += v` and `diff[r+1] -= v`. After all updates, a prefix
sum of `diff` reconstructs the final array: each element accumulates every update
whose range started at or before it and had not yet ended. N updates cost O(1)
each, and one final O(n) integration materializes the result.

## The template

**1D prefix sum for range queries:**

```python
# Time: O(n), Space: O(n)
def build_prefix(a):
    prefix = [0] * (len(a) + 1)
    for i, x in enumerate(a):
        prefix[i + 1] = prefix[i] + x
    return prefix

# Time: O(1), Space: O(1)
def range_sum(prefix, i, j):        # sum of a[i..j] inclusive
    return prefix[j + 1] - prefix[i]
```

**Subarray sum equals k (hash map of prefix counts):**

```python
# Time: O(n), Space: O(n)
def subarray_sum(nums, k):
    from collections import defaultdict
    seen = defaultdict(int)
    seen[0] = 1                     # empty prefix, enables subarrays from index 0
    s = 0
    count = 0
    for x in nums:
        s += x
        count += seen[s - k]        # earlier prefixes that make the window sum to k
        seen[s] += 1
    return count
```

**2D prefix sum (integral image), rectangle sum in O(1):**

```python
# Time: O(mn), Space: O(mn)
def build_2d(mat):
    rows, cols = len(mat), len(mat[0])
    p = [[0] * (cols + 1) for _ in range(rows + 1)]
    for r in range(rows):
        for c in range(cols):
            p[r + 1][c + 1] = mat[r][c] + p[r][c + 1] + p[r + 1][c] - p[r][c]
    return p

# Time: O(1), Space: O(1)
def region_sum(p, r1, c1, r2, c2):  # inclusive corners
    return p[r2 + 1][c2 + 1] - p[r1][c2 + 1] - p[r2 + 1][c1] + p[r1][c1]
```

**Difference array for batched range updates:**

```python
# Time: O(n + q), Space: O(n)  (q = number of updates)
def range_updates(n, updates):      # updates: list of (l, r, v), r inclusive
    diff = [0] * (n + 1)
    for l, r, v in updates:
        diff[l] += v
        diff[r + 1] -= v
    out = [0] * n
    running = 0
    for i in range(n):
        running += diff[i]
        out[i] = running
    return out
```

The 2D read uses inclusion-exclusion: add the big rectangle, subtract the two
overhanging strips, add back the corner you subtracted twice.

## Variations

- **Subarray sum divisible by k.** Bucket prefixes by `s % k` instead of by exact
  value. Two prefixes in the same residue class bound a range whose sum is a
  multiple of k. Watch negative mods: use `s % k` then normalize into `[0, k)`.
- **Longest subarray with sum k, or with equal 0s and 1s.** Store the first index
  where each prefix value appeared, then the answer at each step is `i - first[s - k]`.
  For equal 0s and 1s, map 0 to -1 and look for a prefix that repeats.
- **Prefix XOR.** Replace `+` with `^` and subtraction with `^` (XOR is its own
  inverse). "Count subarrays with XOR equal to k" is the hash-map trick with
  `seen[s ^ k]`.
- **Prefix product** (for "product of array except self" style problems), though
  division by zero forces the two-pass left-product / right-product form instead.
- **2D difference array.** The grid analogue of range updates: mark the four
  corners of each rectangle, then take a 2D prefix sum once to apply them all.
- **Running prefix without an array.** When you only pass through once (the
  subarray-count problems), keep a single accumulator instead of a full prefix
  list. The array form is for random-access queries.

## Canonical problems

| # | Problem | Difficulty | What it drills |
|---|---------|-----------|----------------|
| 303 | Range Sum Query - Immutable | Easy | The base 1D prefix build and query |
| 724 | Find Pivot Index | Easy | Left sum vs right sum from one prefix pass |
| 560 | Subarray Sum Equals K | Medium | Prefix count in a hash map |
| 974 | Subarray Sums Divisible by K | Medium | Bucket prefixes by residue mod k |
| 523 | Continuous Subarray Sum | Medium | First-seen residue index, length constraint |
| 525 | Contiguous Array | Medium | Map 0 to -1, find repeating prefix |
| 304 | Range Sum Query 2D - Immutable | Medium | Integral image, inclusion-exclusion |
| 1248 | Count Number of Nice Subarrays | Medium | Prefix count on parity, exactly-k framing |
| 1094 | Car Pooling | Medium | Difference array over pickup and dropoff |
| 370 | Range Addition | Medium | The base difference-array template |
| 1738 | Find Kth Largest XOR Coordinate Value | Medium | 2D prefix XOR |

## Pitfalls

- **Off-by-one between value indices and prefix indices.** `prefix` has length
  `n + 1` and `prefix[0] = 0`. The sum of `a[i..j]` is `prefix[j+1] - prefix[i]`,
  not `prefix[j] - prefix[i]`. Write it once, trust it.
- **Forgetting `seen[0] = 1`** in subarray-sum-equals-k. Without the empty-prefix
  seed you miss every subarray that starts at index 0.
- **Negative modulo** in the divisible-by-k variant. In Python `%` already returns
  a non-negative result, but if you port to a language where it does not, normalize
  or you will miss matches.
- **Off-by-one on the difference array boundary.** The decrement goes at `r + 1`,
  so size the diff array as `n + 1` to hold that last marker without an index error.
- **2D inclusion-exclusion signs.** The double-subtracted corner must be added
  back. Getting one sign wrong passes small tests and fails large ones; derive it
  from the picture, do not memorize blindly.
- **Overflow** in languages with fixed-width ints (not Python). Cumulative sums
  grow; size the accumulator accordingly.

## Follow-ups and related patterns

- "The subarray must be contiguous and you want the best window, not a count"
  often flips back to [sliding window](02-sliding-window.md), which is prefix sum
  with a moving left edge when all values are non-negative.
- "The values can be negative, so the window trick breaks" is exactly why prefix
  sum plus a [hashing](04-hashing.md) map (or a monotonic deque in
  [stacks](11-stacks.md)) takes over.
- "Now the array changes between queries" pushes past a static prefix to a Fenwick
  or segment tree; see [design](28-design.md) for point-update, range-query
  structures.
- The prefix-plus-hashmap counting move is pure [hashing](04-hashing.md); this
  pattern is that lookup applied to cumulative sums.
