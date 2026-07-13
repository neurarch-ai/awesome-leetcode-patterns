# 04 - Hashing and frequency counting

> **Problem shape:** "Two numbers that add up to a target, array not sorted."
> "Are these two strings anagrams?" "Group the anagrams together." "First
> non-repeating character." "Does this array contain a duplicate?" Anything that
> needs O(1) membership, complement lookup, or counting of how often things
> occur.

Hashing trades space for time: a hash set or map turns "is x present?" and "how
many x are there?" from an O(n) scan into an O(1) lookup. It is the workhorse
behind unsorted-array problems, and it is what you reach for the moment sorting
is not allowed or not worth its O(n log n).

![Complement lookup against a seen set](../assets/hashing.svg)

*One pass, O(1) lookups: for each x, check whether its complement is already in the seen set.*

## The signal

Reach for a hash set or map when you see:

- **"Have I seen this before?"** Deduplication, cycle detection on values,
  "contains duplicate", "first repeated element". A set answers membership in O(1).
- **Complement or pair lookup on an unsorted array.** Unsorted two-sum: for each
  `x`, ask whether `target - x` was already seen. No sort needed, O(n) time.
- **Counting occurrences.** Anagrams, "majority element", "first unique
  character", "top k frequent" all reduce to a frequency table. `collections.Counter`
  is the idiom.
- **Grouping by a shared property.** Group anagrams, group by a canonical key. Map
  each item to a key (sorted letters, a signature) and append into a list keyed by
  that signature.
- **Any brute force that is "for each element, scan the rest"** where the inner
  scan is really a membership or count question. That inner O(n) collapses to O(1).

The tell: the data has no exploitable order, and the question is about presence,
pairing, or frequency rather than about ranges or the best contiguous run.

## The idea

A hash set stores elements and answers membership in expected O(1) by hashing the
element to a bucket. A hash map stores key-to-value and does the same for lookups
by key. You pay O(n) space and get O(1) average-case access, which is the trade
that turns quadratic pair-scans into linear passes.

The complement trick is the sharpest instance. In unsorted two-sum you do not
need both numbers at once: walk the array, and for each `x` check whether its
partner `target - x` is already in the map. If yes, you have the pair; if no,
record `x` and move on. Each element is inserted once and queried once, so the
whole thing is O(n) time and O(n) space, with no sorting.

Frequency counting is the other half. Build a map from element to count in one
pass, then the answer (most frequent, uniquely occurring, matching multiset) is a
read over that map. Anagram checking is just "do these two strings produce equal
count maps", and grouping is "collect everything that produces the same key".

**Contrast with two pointers.** [Two pointers](01-two-pointers.md) solves
sorted-array pair problems in O(n) time and O(1) space by exploiting order.
Hashing solves the same shape when the array is unsorted (or must keep its
original indices) in O(n) time but O(n) space. The choice is a space-versus-order
trade: if the input is already sorted, or you cannot spend the extra space, two
pointers wins; if it is unsorted and sorting would destroy indices or cost too
much, hashing wins.

## The template

**Seen-set for membership and dedup:**

```python
# Time: O(n), Space: O(n)
def contains_duplicate(nums):
    seen = set()
    for x in nums:
        if x in seen:
            return True
        seen.add(x)
    return False
```

**Complement map, unsorted two-sum (returns indices):**

```python
# Time: O(n), Space: O(n)
def two_sum(nums, target):
    pos = {}                          # value -> index
    for i, x in enumerate(nums):
        if target - x in pos:
            return [pos[target - x], i]
        pos[x] = i                    # record only after the check, avoids reusing i
    return [-1, -1]
```

**Frequency counter, anagram check:**

```python
# Time: O(n), Space: O(k) distinct characters (O(1) for a fixed alphabet)
def is_anagram(s, t):
    from collections import Counter
    return Counter(s) == Counter(t)   # equal multisets of characters
```

**Grouping by a canonical key, group anagrams:**

```python
# Time: O(n*k log k), Space: O(n*k)  (n words of length up to k)
def group_anagrams(words):
    from collections import defaultdict
    groups = defaultdict(list)
    for w in words:
        key = tuple(sorted(w))        # canonical signature shared by anagrams
        groups[key].append(w)
    return list(groups.values())
```

For grouping, the art is choosing a key that is identical for exactly the items
that belong together: sorted letters for anagrams, a 26-length count tuple if you
want O(word length) instead of O(word length log) per key.

## Variations

- **Complement with counts, not just presence** (two-sum where an element may pair
  with an equal element). Store counts and check the count of the complement,
  handling the `x == target - x` self-pair case.
- **Sliding-window frequency signatures.** "Find all anagrams in a string" and
  "permutation in string" are a fixed [sliding window](02-sliding-window.md) over
  a running count map compared against a target count map.
- **Longest consecutive sequence.** Put everything in a set, then for each number
  that has no predecessor in the set (a run start), walk forward counting. O(n)
  despite looking like sorting, because each element is visited by exactly one run.
- **Canonical-key grouping beyond anagrams.** Group strings by their shifting
  pattern, group points by slope, group by "sorted digits". The pattern is: design
  a normal form, hash it.
- **Counter arithmetic.** `Counter` supports `+`, `-`, `&`, `|`, and
  `most_common(k)`, which collapse "merge frequencies", "multiset difference", and
  "top k frequent" into one-liners.
- **Fixed-alphabet arrays instead of a dict.** When keys are a small fixed set
  (lowercase letters), a length-26 list is a faster hash map with O(1) constant
  factors and no hashing overhead.

## Canonical problems

| # | Problem | Difficulty | What it drills |
|---|---------|-----------|----------------|
| 1 | Two Sum | Easy | The complement-map template |
| 217 | Contains Duplicate | Easy | Seen-set membership |
| 242 | Valid Anagram | Easy | Frequency counter equality |
| 383 | Ransom Note | Easy | Multiset containment via counts |
| 349 | Intersection of Two Arrays | Easy | Set intersection |
| 387 | First Unique Character in a String | Easy | Count pass, then first with count 1 |
| 49 | Group Anagrams | Medium | Canonical-key grouping |
| 347 | Top K Frequent Elements | Medium | Frequency map plus selection |
| 128 | Longest Consecutive Sequence | Medium | Set membership, walk from run starts |
| 205 | Isomorphic Strings | Easy | Two consistent key-to-key maps |
| 454 | 4Sum II | Medium | Hash pair sums of two arrays, complement the other two |

## Pitfalls

- **Recording before checking** in two-sum. Insert `x` into the map only after
  testing for its complement, or a single element pairs with itself and you return
  a bogus `[i, i]`.
- **Mutable or unhashable keys.** Lists are not hashable; convert to a `tuple`
  before using as a key. A count-signature key must be a tuple, not a list.
- **Stale zero counts.** When decrementing a count in a window, delete keys that
  reach zero if you compare on `len(map)` or on map equality, otherwise a
  zero-count key makes two "equal" multisets compare unequal.
- **Assuming O(1) is free.** Hashing costs O(n) space and has constant-factor
  overhead; for a tiny fixed alphabet an array is faster, and if space is the
  bottleneck, sorting plus [two pointers](01-two-pointers.md) may beat it.
- **Hash order is not sorted order.** Do not rely on dict or set iteration order
  for anything but insertion order (Python preserves insertion order for dicts,
  not for sets). If you need sorted output, sort explicitly.
- **Counting the self-pair wrong.** In pair-sum-with-counts, `x + x == target`
  needs at least two occurrences of `x`, not one.

## Follow-ups and related patterns

- "The array is sorted, can you drop the extra space?" pushes to
  [two pointers](01-two-pointers.md), which does pair-finding in O(1) space by
  exploiting order.
- "Answer range-sum or subarray-count questions" combines this with
  [prefix sum](03-prefix-sum.md): the prefix-count-in-a-map trick is hashing
  applied to cumulative sums.
- "Maintain the top k as data streams in" pushes to a [heap](24-heap.md); a plain
  frequency map is not enough when you need the running best k.
- "Find the k most frequent without a full sort" pairs the frequency map with
  [top-k and quickselect](09-top-k-quickselect.md).
- The window-count bookkeeping in [sliding window](02-sliding-window.md) is this
  pattern applied to a moving range.
