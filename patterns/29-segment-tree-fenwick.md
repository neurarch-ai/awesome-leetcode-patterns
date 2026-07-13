# 29 - Segment tree and Fenwick (BIT)

> **Problem shape:** "Support range-sum queries **and** point updates, interleaved."
> "Count how many numbers to the right are smaller than each element." "Count
> reverse pairs." When [prefix sum](03-prefix-sum.md) would be perfect except that
> the array keeps changing, so a rebuilt prefix array would cost O(n) per update.

Prefix sums answer range queries in O(1), but only on a **static** array: one
update forces an O(n) rebuild. When queries and updates interleave, you need a
structure that does both in O(log n). Two structures do this: the **Fenwick tree**
(binary indexed tree, BIT), which is compact and perfect for prefix sums, and the
**segment tree**, which is more general (any associative range aggregate: sum,
min, max, gcd). This is the pattern for "dynamic range queries" and for the
counting problems (inversions, count-of-smaller) that reduce to them.

## The signal

Reach for a Fenwick or segment tree when:

- The problem interleaves **range aggregate queries** (sum, min, max on a range)
  with **updates** to individual elements. Prefix sum cannot absorb the updates
  cheaply; you need O(log n) per operation.
- You are **counting inversions** or **count of smaller/greater elements** to one
  side. These reduce to "how many previously-seen values fall below x", which is a
  prefix-count query on a frequency array, updated as you sweep. That is a BIT.
- The value range is large but the number of distinct values is small: combine
  the structure with **coordinate compression** (map values to ranks 1..k first).
- You see constraints like n and number-of-queries both up to 10^5 with mixed
  update and query operations. O(n) per query is 10^10 and times out; O(log n) is
  the intended solution.

If the array never changes after you build it, do not reach here. A static prefix
sum (or a sparse table for min/max) is simpler and faster.

## The idea

Both structures cut a range into O(log n) precomputed pieces so no query walks
more than log n nodes.

- A **Fenwick tree** stores, at index i, the sum of a block of elements whose size
  is the lowest set bit of i. Walking `i -= i & (-i)` peels off one block at a
  time, so a prefix sum touches O(log n) blocks. An update walks
  `i += i & (-i)`, touching the O(log n) blocks that contain i. It is the least
  code for prefix-sum-with-update, and the bit trick `i & (-i)` (isolate the
  lowest set bit) is its whole engine.
- A **segment tree** is a binary tree over the array: each leaf is an element,
  each internal node stores the aggregate of its children's range. A query splits
  the target range into the O(log n) nodes that exactly tile it; an update walks
  the single root-to-leaf path and refixes each ancestor. It generalizes to any
  associative operation, and with **lazy propagation** it also supports range
  updates (deferring a pending update on a node until you need to descend into it).

Rule of thumb: prefix sums with point updates, reach for the **BIT** (less code).
Range min/max, or range updates, reach for the **segment tree**.

## The template

**Fenwick tree (BIT), 1-indexed, prefix sums with point update:**

```python
# Space: O(n)
class BIT:
    # Time: O(n)
    def __init__(self, n):
        self.n = n
        self.tree = [0] * (n + 1)      # 1-indexed

    # Time: O(log n)
    def update(self, i, delta):        # add delta at position i
        while i <= self.n:
            self.tree[i] += delta
            i += i & (-i)              # move to the next block that covers i

    # Time: O(log n)
    def query(self, i):                # prefix sum of [1..i]
        s = 0
        while i > 0:
            s += self.tree[i]
            i -= i & (-i)              # peel off the lowest block
        return s

    # Time: O(log n)
    def range_query(self, l, r):       # sum of [l..r], inclusive
        return self.query(r) - self.query(l - 1)
```

**Iterative segment tree, point update and range-sum query on [l, r):**

```python
# Space: O(n)
class SegTree:
    # Time: O(n)
    def __init__(self, data):
        self.n = len(data)
        self.tree = [0] * (2 * self.n)
        for i in range(self.n):        # leaves live in the second half
            self.tree[self.n + i] = data[i]
        for i in range(self.n - 1, 0, -1):
            self.tree[i] = self.tree[2 * i] + self.tree[2 * i + 1]

    # Time: O(log n)
    def update(self, i, val):          # set position i to val
        i += self.n
        self.tree[i] = val
        i //= 2
        while i >= 1:
            self.tree[i] = self.tree[2 * i] + self.tree[2 * i + 1]
            i //= 2

    # Time: O(log n)
    def query(self, l, r):             # sum on the half-open range [l, r)
        res = 0
        l += self.n
        r += self.n
        while l < r:
            if l & 1:
                res += self.tree[l]
                l += 1
            if r & 1:
                r -= 1
                res += self.tree[r]
            l //= 2
            r //= 2
        return res
```

**Count of smaller numbers after self, BIT plus coordinate compression:**

```python
# Time: O(n log n), Space: O(n)
def count_smaller(nums):
    rank = {v: i + 1 for i, v in enumerate(sorted(set(nums)))}  # 1-indexed ranks
    bit = BIT(len(rank))
    res = []
    for x in reversed(nums):           # sweep right to left
        r = rank[x]
        res.append(bit.query(r - 1))   # count of already-seen values strictly smaller
        bit.update(r, 1)               # record this value
    res.reverse()
    return res
```

## Variations

- **Range sum with point update** (307): the textbook BIT or segment tree use.
- **Count of smaller / greater to the right** (315): BIT over compressed ranks,
  swept from the right (above). The same idea counts **inversions**.
- **Reverse pairs** (493, count `nums[i] > 2 * nums[j]` for i < j): a BIT or a
  merge-sort count. Merge sort is often cleaner here (see below).
- **Range min or max**: use a segment tree (a BIT does not support min or max with
  updates, because min is not invertible the way sum is).
- **Range update, range query** (add v to a whole range, then query a range): a
  segment tree with **lazy propagation**, or two BITs for the range-add-range-sum
  trick.
- **Merge-sort counting**: inversions and reverse pairs can also be counted while
  merging, in O(n log n) with no extra structure. If a problem only needs a count
  once (not interleaved updates), prefer this to a BIT.
- **Order statistics without aggregates**: if you only need "kth smallest so far"
  or "how many in range", a [sorted container](../data-structures/10-sorted-container.md)
  (bisect or SortedList) is simpler than a segment tree.

## Canonical problems

| # | Problem | Difficulty | What it drills |
|---|---------|-----------|----------------|
| 307 | Range Sum Query - Mutable | Medium | The base BIT / segment tree: sum with point update |
| 303 | Range Sum Query - Immutable | Easy | The static contrast: plain prefix sum, no structure needed |
| 315 | Count of Smaller Numbers After Self | Hard | BIT over compressed ranks, swept right to left |
| 493 | Reverse Pairs | Hard | BIT with compression, or merge-sort counting |
| 327 | Count of Range Sum | Hard | Prefix sums plus a BIT or merge sort over sums |
| 218 | The Skyline Problem | Hard | Sweep line with a max structure (heap or segment tree) |
| 699 | Falling Squares | Hard | Segment tree with range max and range update (lazy) |
| 2179 | Count Good Triplets in an Array | Hard | Two BITs counting positions before and after |

## Pitfalls

- **Off-by-one and 0 vs 1 indexing.** The BIT is naturally 1-indexed (`i & (-i)`
  needs i > 0). Map your array positions to 1..n and keep them there consistently.
- **Forgetting coordinate compression.** If values can be up to 10^9 you cannot
  size the tree by value. Compress to ranks first; the tree size is the number of
  distinct values.
- **Using a BIT for min or max with updates.** A BIT relies on sum being
  invertible (`range = query(r) - query(l-1)`). Min and max are not invertible, so
  decreases cannot be undone. Use a segment tree for those.
- **Rebuilding instead of updating.** The whole point is O(log n) updates. If you
  find yourself recomputing prefix sums after each change, you have written an
  O(n) update and missed the pattern.
- **Reaching for a segment tree when merge sort suffices.** A one-shot inversion
  count does not need a persistent structure. Do not over-engineer.

## Follow-ups and related patterns

- "The array is static, no updates" pulls you back to plain
  [prefix sum](03-prefix-sum.md), which is O(1) per query and much simpler.
- "I only need order statistics or a range count, not arbitrary aggregates" points
  at a [sorted container](../data-structures/10-sorted-container.md) (bisect or
  SortedList), less code than a segment tree.
- "Count the inversions once" points at merge sort, a
  [divide-and-conquer](08-sorting.md) count rather than a BIT.
- The lowest-set-bit trick `i & (-i)` that drives the BIT is pure
  [bit manipulation](26-bit-manipulation.md).
- Range-min or range-max queries on a **static** array want a sparse table, a
  cousin of this pattern noted in [binary search](07-binary-search.md) contexts.
