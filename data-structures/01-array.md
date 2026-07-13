# 01 - Array and dynamic array

An array is a block of contiguous memory holding elements of the same size, which
is exactly what makes `a[i]` O(1): the address of element `i` is `base + i * width`,
a single multiply and add, no walking. The Python `list` is a dynamic array, an
array that grows itself when it fills up. Almost everything you do in an interview
sits on top of it, so knowing precisely which of its operations are O(1) and which
secretly shift the whole thing is the difference between an O(n) and an O(n^2)
solution.

## What it is

A static array is a fixed-size, contiguous run of memory. You pick the length up
front, and every slot has a known address, so indexing is a pointer computation,
not a search. The cost of that speed is rigidity: you cannot grow it, and
inserting in the middle means shifting everything after the gap.

A dynamic array (Python's `list`, C++'s `vector`, Java's `ArrayList`) wraps a
static array and hides the resizing. It keeps a backing buffer with some spare
capacity and a length. Appends fill the spare slots; when the buffer is full, it
allocates a bigger one (CPython grows it by roughly 1.125x, other languages often
2x), copies the old elements over, and continues. The contiguous layout is
preserved, so indexing stays O(1), and you get amortized O(1) append on top. A
Python `list` also holds pointers to objects rather than the objects inline, so it
can be heterogeneous, but the pointer array itself is still contiguous.

The invariant to hold in your head: elements live back to back with no gaps, and
that is the source of both the O(1) index and the O(n) front insert.

## Operations and complexity

| Operation | Cost | Note |
|---|---|---|
| `a[i]`, `a[i] = x` | O(1) | Address is `base + i * width`, direct |
| `a.append(x)`, `a.pop()` | O(1) amortized | Occasionally reallocates and copies |
| `a.pop(0)`, `a.insert(0, x)` | O(n) | Every element shifts one slot. Use a deque |
| `a.insert(i, x)`, `del a[i]` | O(n) | Shifts the tail after `i` |
| `x in a` | O(n) | Linear scan. Use a set for membership |
| `a[i:j]` (slice) | O(k) | k = j - i, copies the sliced elements |
| `len(a)` | O(1) | Stored on the object, not counted |
| `min(a)`, `max(a)`, `sum(a)` | O(n) | Full scan |
| `a.sort()`, `sorted(a)` | O(n log n) | Timsort, stable |
| `a.reverse()`, `a[::-1]` | O(n) | The slice form also copies |
| `a + b` | O(n + m) | Builds a new list |

Why `append` is amortized O(1): most appends land in a spare slot and cost O(1).
The occasional append that triggers a resize costs O(n) to copy, but because the
buffer grows by a constant factor, those expensive copies happen geometrically
less often. Spread the total copy work across all the appends and each one pays a
constant on average. That is amortized analysis, not a promise every single append
is cheap.

Why front insert and `pop(0)` are O(n): contiguity means index `k` must physically
be at position `k`. Remove or add at the front and every remaining element has to
slide one slot to keep the layout intact. There is no shortcut. This is the single
most common accidental O(n^2): a BFS or a queue built on `list.pop(0)`.

See the [complexity cheat sheet](../complexity.md) for the same table alongside the
other structures.

## Python implementation

Idiomatic list usage, the operations you actually reach for:

```python
a = [3, 1, 4, 1, 5]

a.append(9)          # O(1) amortized, add to the end
last = a.pop()       # O(1), remove and return the end
a[2] = 42            # O(1), index assignment

# Build with a comprehension instead of append in a loop when you can
squares = [x * x for x in range(10)]      # O(n)

# Slicing copies; a[:] is the standard shallow copy
head = a[:3]         # O(3)
copy = a[:]          # O(n), independent list

# Membership on a list is O(n); if you test it repeatedly, build a set once
seen = set(a)        # O(n) to build
found = 42 in seen   # O(1) average, not O(n)
```

2D arrays and grids. Represent a grid as a list of row lists. The one trap that
bites everyone: build rows independently, never by multiplying a shared inner
list, or every row aliases the same object.

```python
rows, cols = 3, 4

grid = [[0] * cols for _ in range(rows)]     # correct: rows independent
grid[0][1] = 7                                # only row 0 changes

# WRONG: all rows are the SAME list object
bad = [[0] * cols] * rows
bad[0][1] = 7                                 # every row now shows 7

# Iterate with coordinates
for r in range(rows):
    for c in range(cols):
        cell = grid[r][c]                     # O(1) each, O(rows*cols) total
```

A fixed-size ring buffer is the classic "static array behaving like a queue"
wrapper, useful when you want O(1) both ends without a deque and know the capacity:

```python
class RingBuffer:
    def __init__(self, capacity):
        self.buf = [None] * capacity          # static backing array
        self.cap = capacity
        self.head = 0                          # next read
        self.size = 0

    def push(self, x):                         # O(1), overwrites oldest if full
        tail = (self.head + self.size) % self.cap
        self.buf[tail] = x
        if self.size < self.cap:
            self.size += 1
        else:
            self.head = (self.head + 1) % self.cap

    def pop(self):                             # O(1)
        if self.size == 0:
            raise IndexError("empty")
        x = self.buf[self.head]
        self.head = (self.head + 1) % self.cap
        self.size -= 1
        return x
```

## When to use it (and when not)

Use an array or list when:

- You need indexed access or you iterate in order. Nothing beats O(1) index and
  the cache-friendliness of contiguous memory.
- You are appending and reading, which is the overwhelmingly common access pattern.
  Append and end-pop are both amortized O(1).
- You need a grid, a matrix, a DP table, or any fixed-shape 2D structure.
- The problem is fundamentally sequential: prefix sums, sliding windows, two
  pointers, in-place partitioning.

Reach for something else when:

- You test membership repeatedly. `x in list` is O(n); use a
  [hash set](02-hash-map-set.md) for O(1) average.
- You add or remove at the front, or at both ends. `pop(0)` is O(n); use a
  [deque](03-stack-queue.md).
- You insert or delete in the middle a lot given a reference to the spot. That is a
  [linked list](04-linked-list.md), where a splice is O(1) once you hold the node.
- You need the smallest or largest repeatedly. That is a [heap](05-heap.md).

## Tradeoffs and gotchas

- **The front is expensive.** `insert(0, x)` and `pop(0)` are O(n). If your loop
  does either, you have quietly built O(n^2). A queue on a list is the canonical
  form of this bug.
- **Slicing copies.** `a[i:j]` is O(k), not a view. Slicing inside a loop to peel
  off a prefix each iteration is a hidden O(n^2). Pass indices, not slices, on hot
  paths.
- **`x in a` is a linear scan.** It looks O(1) and is O(n). Repeated membership
  tests belong in a set.
- **Aliased 2D grids.** `[[0] * c] * r` makes `r` references to one row. Always use
  a comprehension for the outer dimension.
- **Building a string with `+=` is not an array problem but the same trap.** Strings
  are immutable, so `s += c` in a loop is O(n^2); collect into a list and
  `''.join()`. See the str section of the [cheat sheet](../complexity.md).
- **`list.remove(x)` and `del a[i]` are O(n).** They find or shift. Deleting many
  elements one at a time is O(n^2); filter into a new list in one pass instead.
- **Amortized is not worst case.** A single append can spike to O(n) during a
  resize. It rarely matters, but say "amortized O(1)" when you mean it, especially
  if the interviewer asks about latency rather than throughput.

## Related patterns

The array is the substrate for most of the sequence patterns:

- [two pointers](../patterns/01-two-pointers.md) walk indices inward or in
  read-write pairs, all O(1) index moves.
- [sliding window](../patterns/02-sliding-window.md) maintains a contiguous
  subarray by advancing two indices over the array.
- [prefix sum](../patterns/03-prefix-sum.md) precomputes an O(n) auxiliary array so
  any range sum is O(1).
- [hashing](../patterns/04-hashing.md) is what you switch to when array membership
  (O(n)) is the bottleneck.
- Grid problems feed straight into [graph traversal](../patterns/16-graph-traversal.md),
  where each cell is a node and its four neighbors are edges.
- For the raw operation costs, keep the [complexity cheat sheet](../complexity.md)
  open.
