# 08 - Sorting and custom comparators

> **Problem shape:** "Arrange these numbers to form the largest possible number."
> "Merge all overlapping intervals." "Sort characters by frequency." "Can a person
> attend all these meetings?" Whenever the answer becomes obvious *once the data is
> in the right order*, or a comparison rule richer than `<` decides that order,
> sorting is the unlock and the whole problem is choosing the key.

Sorting is rarely the answer by itself; it is the O(n log n) preprocessing step
that turns a tangled problem into a linear scan. The skill is spotting that a sort
collapses the difficulty, then writing the comparator that encodes exactly the
order you need. Python gives you two knobs: a `key=` function (fast, one value per
element) and `functools.cmp_to_key` (a pairwise comparator, for when order depends
on how two elements combine).

## The signal

Reach for sorting when you see:

- **"The answer does not depend on original order."** If you may freely rearrange
  the input, sorting is almost always a legal and clarifying first move.
- **Adjacent elements become comparable after ordering.** Merge intervals,
  deduplicate, find the closest pair, detect overlaps: all trivial once sorted,
  because the only interactions are between neighbors.
- **You need a custom notion of "smaller".** Order by a derived key (length, then
  lexicographic), by frequency then value, or by a pairwise rule that no single key
  captures ("which concatenation is larger"). That is the comparator's job.
- **A greedy or two-pointer step needs a sorted precondition.** Interval scheduling,
  meeting rooms, and many [greedy](25-greedy.md) proofs open with "sort by end
  time" or "sort by start".
- **Bounded, small value range.** If values are integers in a known narrow band,
  counting sort or bucket sort gets you O(n) and sidesteps the comparison lower
  bound entirely.

## The idea

A comparison sort cannot beat **O(n log n)** in the worst case: with `n!` possible
orderings and each comparison yielding one bit, you need at least `log2(n!) ~ n log
n` comparisons. That bound is why "sort then scan" is the honest complexity of most
of these problems, and why counting/bucket sort (which do not compare, they index)
can break it when values are bounded.

Two ways to specify order in Python:

- **`key=f`** maps each element to a sort key; Python sorts by the keys' natural
  order and calls `f` once per element (a Schwartzian transform, so it is fast).
  Return a tuple for tie-breaks: `key=lambda x: (-freq[x], x)` sorts by frequency
  descending, then value ascending.
- **`cmp_to_key(cmp)`** wraps a pairwise comparator returning negative / zero /
  positive. You need this only when the order is defined by *combining two
  elements* and cannot be reduced to a per-element key. "Largest number" is the
  canonical case: compare `a+b` against `b+a` as strings.

Python's `sort` is Timsort: stable (equal elements keep input order, which you can
exploit for multi-level sorts) and adaptive (near-sorted input runs close to O(n)).

## The template

**Sort by a derived key, with tie-breaks via a tuple:**

```python
from collections import Counter

def sort_by_frequency(nums):
    freq = Counter(nums)
    # most frequent first; break ties by smaller value
    return sorted(nums, key=lambda x: (-freq[x], x))
```

**Pairwise comparator with `cmp_to_key` (largest number from concatenation):**

```python
from functools import cmp_to_key

def largest_number(nums):
    strs = list(map(str, nums))
    # a should come before b if a+b is the larger concatenation
    def cmp(a, b):
        if a + b > b + a:
            return -1              # a first
        if a + b < b + a:
            return 1              # b first
        return 0
    strs.sort(key=cmp_to_key(cmp))
    result = ''.join(strs)
    return '0' if result[0] == '0' else result   # all-zeros edge case
```

**Sort then scan (merge overlapping intervals):**

```python
def merge_intervals(intervals):
    intervals.sort(key=lambda iv: iv[0])          # by start
    merged = []
    for start, end in intervals:
        if merged and start <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], end)   # overlap: extend
        else:
            merged.append([start, end])               # disjoint: new run
    return merged
```

**Counting / bucket sort for a bounded value range (O(n + k)):**

```python
def counting_sort(nums, max_val):
    count = [0] * (max_val + 1)
    for x in nums:
        count[x] += 1
    out = []
    for value, c in enumerate(count):
        out.extend([value] * c)       # emit each value c times, in order
    return out
```

## Variations

- **Sort by frequency, then by a tie-break.** "Sort characters by frequency" and
  "top k frequent" both key on `(-count, value)`. Bucket-by-count is the O(n)
  alternative when you only need the top slice.
- **Multi-level sort via stable passes.** Because Timsort is stable, you can sort
  by the least significant key first, then the most significant, and earlier order
  survives within ties. Often cleaner than one giant tuple key.
- **Custom lexicographic rules.** "Reorder data in log files": letter-logs sort by
  content then identifier, digit-logs keep original relative order and go last.
  Encode the whole rule in one `key` that returns a tuple whose first element
  buckets the two log types.
- **Sort as greedy setup.** Meeting rooms (sort by start, sweep with a min-heap of
  end times), interval scheduling (sort by end), "minimum arrows to burst
  balloons" (sort by end). The sort is what makes the greedy choice provably
  optimal.
- **Radix / bucket sort for bounded keys.** Fixed-width integers or strings sort in
  O(nk) without comparisons. Bucket sort also shines for uniformly distributed
  floats in a known range.
- **Partial order only (top k, or a median).** You may not need a full sort at all;
  see [top-k and quickselect](09-top-k-quickselect.md) for O(n) selection.

## Canonical problems

| # | Problem | Difficulty | What it drills |
|---|---------|-----------|----------------|
| 937 | Reorder Data in Log Files | Easy | A tuple key that buckets and orders two log types |
| 179 | Largest Number | Medium | Pairwise `cmp_to_key` on concatenation |
| 451 | Sort Characters By Frequency | Medium | Key on `(-count, char)`, or bucket by count |
| 56 | Merge Intervals | Medium | Sort by start, then a neighbor scan |
| 252 | Meeting Rooms | Easy | Sort by start, check adjacent overlap |
| 253 | Meeting Rooms II | Medium | Sort starts and ends, sweep for max concurrency |
| 75 | Sort Colors | Medium | Counting sort (or Dutch-flag) over 3 values |
| 274 | H-Index | Medium | Sort descending, scan for the crossover |
| 973 | K Closest Points to Origin | Medium | Sort by squared distance (or quickselect) |
| 912 | Sort an Array | Medium | Implement a real O(n log n) sort from scratch |

## Pitfalls

- **Reaching for `cmp_to_key` when a `key` would do.** Pairwise comparators are
  slower (Python calls back into your function for every comparison) and easier to
  get wrong. Only use them when the order genuinely depends on combining two
  elements, like "largest number".
- **Comparator not defining a total order.** A `cmp` that is inconsistent
  (`cmp(a,b) < 0` and `cmp(b,c) < 0` but `cmp(a,c) > 0`) produces garbage or a
  wrong answer. The concatenation comparator works precisely because it is a
  provable total order.
- **Losing original indices.** If you must return positions, sort `(value, index)`
  pairs or `sorted(range(n), key=...)`, not the values alone.
- **Assuming your sort is stable in another language.** Python and Java object
  sorts are stable; C++ `std::sort` is not (`std::stable_sort` is). Multi-pass
  sorting only works on a stable sort.
- **Forgetting the all-zeros / empty edge cases.** "Largest number" of `[0, 0]` is
  `"0"`, not `"00"`. Empty input, single element, and all-equal elements deserve a
  quick mental check.
- **Counting sort on an unbounded or huge range.** It is O(n + k); if `k` (the
  value range) dwarfs `n`, the array of counts is wasteful. It pays off only when
  values are densely packed in a small band.

## Follow-ups and related patterns

- "I only need the top k, not the whole order" pushes to
  [top-k and quickselect](09-top-k-quickselect.md) (O(n) average) or a bounded
  [heap](24-heap.md) (O(n log k)).
- "The data is already mostly sorted / arrives as a stream" pushes to a
  [heap](24-heap.md) or to insertion-style maintenance rather than a full re-sort.
- "After sorting, pair or partition the elements" is [two pointers](01-two-pointers.md);
  sorting is the precondition that makes the pointer moves valid.
- "After sorting by end/start, make one greedy choice per element" is
  [greedy](25-greedy.md), and "sweep the sorted endpoints" is
  [intervals and sweep line](05-intervals.md).
- Bounded-range counting connects to [hashing and frequency counting](04-hashing.md),
  which is counting sort without the final ordered emit.
