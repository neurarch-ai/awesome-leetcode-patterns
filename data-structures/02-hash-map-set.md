# 02 - Hash map and hash set

A hash map trades memory for speed: it turns a key into an array index by running
it through a hash function, so instead of scanning n items to find one, you compute
where it must be and look there. That is the whole reason `dict` and `set` give you
O(1) average lookup, insert, and membership. It is also why the guarantee is
"average" and not "always", and why keys have to be hashable. Half of easy and
medium interview problems ("two sum", "group anagrams", "longest substring without
repeats") are a hash map wearing a costume.

## What it is

A hash set stores a collection of distinct elements with fast membership testing. A
hash map (dictionary) stores key to value associations with fast lookup by key.
Both are built on the same machine underneath: an array of buckets plus a hash
function.

The mechanism: to store a key, compute `h = hash(key)`, reduce it to a bucket index
`h % num_buckets`, and put the entry there. To look it up, compute the same index
and check that bucket. Because you jump straight to the bucket instead of scanning,
lookup is O(1) on average. The array is the source of the speed, and the hash
function is what maps an arbitrary key onto an array index.

Two keys can hash to the same bucket. That is a collision, and it is unavoidable
(you are mapping a huge key space onto a finite array). Implementations resolve it
by chaining (each bucket holds a small list) or open addressing (probe to the next
free slot; CPython uses open addressing). Either way, when a bucket holds several
colliding keys, you fall back to scanning within that bucket, which is why the
worst case degrades to O(n) if every key lands in one bucket. With a decent hash
function and randomized inputs that essentially never happens, so you quote the
average.

The load factor keeps collisions rare. It is the ratio of stored entries to
buckets. As it climbs, collisions get more likely and lookups slow down, so the
table watches it and, past a threshold (CPython resizes when the table is about
two-thirds full), allocates a larger bucket array and rehashes every entry into it.
That resize is O(n) but amortizes away over the many inserts between resizes, the
same amortization logic as a dynamic array's append.

## Operations and complexity

| Operation | Cost | Note |
|---|---|---|
| `d[k]`, `d[k] = v`, `del d[k]` | O(1) average / O(n) worst | Hash to a bucket; worst is pathological collisions |
| `k in d`, `x in s` | O(1) average / O(n) worst | The reason these structures exist |
| `s.add(x)`, `s.discard(x)` | O(1) average / O(n) worst | Same hashing path |
| `len(d)`, `len(s)` | O(1) | Stored, not counted |
| iterate `d`, `d.items()`, `s` | O(n) | The view is O(1) to make, O(n) to walk |
| `a | b` (set union) | O(len a + len b) | New set |
| `a & b` (set intersection) | O(min(len a, len b)) | Iterates the smaller side |
| `a - b` (set difference) | O(len a) | |
| `Counter(iterable)` | O(n) | Counts in a single pass |
| `counter.most_common(k)` | O(n log k) | Size-k heap internally |
| `counter.most_common()` (all) | O(n log n) | Full sort |

Why the lookup is O(1) average: you compute the bucket index in constant time and,
because the load factor is kept low, the target bucket holds only a handful of
entries to check. No scan over n. Why the worst case is O(n): if an adversary or a
bad hash function funnels every key into one bucket, that bucket becomes a linear
list and each lookup scans all of it. You will basically never see the worst case
on normal data, but you state it because it is real.

Numbers must match the [complexity cheat sheet](../complexity.md); it carries the
same table split by average and worst.

## Python implementation

The three containers you reach for, plus the two `collections` conveniences:

```python
# set: distinct elements, O(1) average membership
seen = set()
seen.add(3)
if 3 in seen:            # O(1) average
    ...

# dict: key -> value
count = {}
count["a"] = 1
count["a"] += 1          # KeyError if "a" was absent; guard or use defaultdict
val = count.get("b", 0)  # O(1), returns default instead of raising

# defaultdict: no "is the key there yet" boilerplate
from collections import defaultdict

groups = defaultdict(list)          # missing key auto-creates an empty list
groups["cat"].append(1)             # no setdefault, no membership check

freq = defaultdict(int)             # missing key defaults to 0
for ch in "banana":
    freq[ch] += 1                   # just works on first sight

# Counter: a dict subclass that counts for you
from collections import Counter

c = Counter("banana")               # O(n): {'a': 3, 'n': 2, 'b': 1}
top2 = c.most_common(2)             # O(n log 2): [('a', 3), ('n', 2)]
```

Hashability. A key must be hashable, which in practice means immutable: numbers,
strings, and tuples of immutables are fine; lists, sets, and dicts are not, because
their contents can change and a key's hash must never change while it is stored.
This is why you store coordinates as tuples.

```python
visited = set()
visited.add((r, c))          # tuple: hashable, correct for a grid cell
# visited.add([r, c])        # TypeError: unhashable type 'list'

# A frozenset is the hashable, immutable set, so you can key on a group of items
seen_groups = set()
seen_groups.add(frozenset({"a", "b"}))
```

Canonical two-sum, the archetype: turn an O(n^2) pair search into O(n) by
remembering what you have seen and asking the map for the complement.

```python
def two_sum(nums, target):
    seen = {}                         # value -> index
    for i, x in enumerate(nums):
        if target - x in seen:        # O(1) average lookup
            return [seen[target - x], i]
        seen[x] = i
    return []
```

Insertion order. Since Python 3.7 a `dict` preserves insertion order as a language
guarantee (it was an implementation detail in 3.6). Iteration yields keys in the
order they were first inserted. That is occasionally the entire trick: an LRU cache
is a dict where you re-insert on access so the oldest key sits at the front and
`next(iter(d))` gives you the eviction candidate.

```python
d = {}
d["x"] = 1
d["y"] = 2
d["z"] = 3
list(d)                    # ['x', 'y', 'z'], first-inserted first
oldest = next(iter(d))     # 'x', front of the insertion order
```

## When to use it (and when not)

Use a hash set or map when:

- You ask "have I seen this before" or "does this exist", repeatedly. That is O(1)
  average membership versus O(n) on a list.
- You map keys to values: index by id, count occurrences, cache a computed result,
  memoize a recursion.
- You need to dedupe. `set(iterable)` in one O(n) pass.
- You are turning an O(n^2) "compare every pair" into O(n) by remembering
  complements or seen states (two sum, subarray sum equals k, longest consecutive
  sequence).

Reach for something else when:

- You need order by value or the min/max repeatedly. A dict is unordered by value;
  use a [heap](05-heap.md) for extremes or a balanced tree for sorted order.
- You need range queries ("all keys between a and b"). Hashing destroys ordering;
  use a sorted structure or [tree/BST](06-tree-bst.md).
- Keys are not hashable (mutable). Convert to a tuple or frozenset, or rethink.
- Memory is tight and n is small. The constant factor and bucket overhead of a hash
  table can lose to a plain array scan for tiny n.

## Tradeoffs and gotchas

- **"O(1)" is average, not guaranteed.** Adversarial keys or a bad hash can force
  O(n). It almost never bites on interview data, but know the caveat.
- **Unhashable keys.** Lists and dicts cannot be keys or set members. Store
  coordinates as `(r, c)` tuples; use `frozenset` for an order-insensitive group
  key.
- **`d[k]` raises, `d.get(k)` does not.** Reaching for a missing key with `[]`
  throws `KeyError`. Use `.get(k, default)` or a `defaultdict` when absence is
  normal.
- **`defaultdict` inserts on read.** Merely reading `dd[missing]` creates the key
  with the default value. Iterate over `.items()` after and you will see keys you
  never explicitly set. Use `.get` if you want to peek without inserting.
- **Iteration order is insertion order, not sorted order.** Do not assume a dict is
  sorted; it preserves the order you added keys, which is a different thing.
- **A set of lists is impossible.** Convert inner lists to tuples first.
- **Sizing a `Counter` difference.** `Counter` subtraction drops non-positive
  counts silently with `-`, but keeps them with `.subtract()`. Pick deliberately.

## Related patterns

The hash map is the workhorse behind most O(n) reductions:

- [hashing](../patterns/04-hashing.md) is the pattern built directly on this
  structure: seen-sets, complement maps, frequency dicts, grouping by a computed
  key.
- [sliding window](../patterns/02-sliding-window.md) uses a dict or Counter to
  track the character or element frequencies inside the current window in O(1) per
  step.
- [prefix sum](../patterns/03-prefix-sum.md) pairs with a hash map for "count
  subarrays with sum k": store each prefix sum's frequency and look up the
  complement.
- [two pointers](../patterns/01-two-pointers.md) is the sorted-input alternative;
  when you cannot sort, the hash map is how you solve the same problem in O(n).
- [design](../patterns/28-design.md) problems (LRU cache, insert-delete-getRandom
  in O(1)) lean on the dict's O(1) ops plus its insertion-order guarantee.
- For the average-versus-worst cost split, see the
  [complexity cheat sheet](../complexity.md).
