# 05 - Heap (priority queue)

A heap is the structure you reach for when you repeatedly need the smallest (or
largest) item and nothing else about order. It gives you O(1) peek at the extreme
and O(log n) to remove it or add a new element, which is exactly the "priority
queue" contract. The surprising part is the implementation: a heap is not a
tangle of pointers, it is a plain array that you read as a tree. Understanding
that array-as-tree layout is what makes the O(log n) and O(n) costs obvious
instead of magic.

## What it is

A binary heap is a **complete binary tree** stored in an array. "Complete" means
every level is full except possibly the last, which fills left to right with no
gaps. That gaplessness is what lets you drop the pointers entirely: because there
are no holes, you can lay the tree out level by level in a contiguous array, and
parent-child relationships become index arithmetic.

For a node at index `i` (0-based):

- its parent is at `(i - 1) // 2`,
- its left child is at `2 * i + 1`,
- its right child is at `2 * i + 2`.

The **heap invariant** is a local property: in a min-heap, every parent is `<=`
both of its children. It says nothing about left-vs-right order between siblings,
and nothing about cousins. All it guarantees is that the smallest element in the
whole heap sits at the root, index 0, because "no child is smaller than its
parent" applied all the way up funnels the minimum to the top. That is why peek
is O(1): the answer is always `a[0]`. A max-heap is the same with the comparison
flipped (every parent `>=` its children), putting the maximum at the root.

A heap is deliberately *weakly* ordered. It does not keep everything sorted; it
keeps just enough order to surface one extreme cheaply. That weakness is the
whole efficiency story: maintaining only the parent-child relation is far cheaper
than maintaining a total order.

## Operations and complexity

For a heap of n elements:

| Operation | Cost | Note |
|---|---|---|
| Peek min / max (root) | O(1) | It is always `a[0]`; do not pop to look |
| Push (insert) | O(log n) | Append at the end, then sift up one path |
| Pop (extract min / max) | O(log n) | Swap root with last, remove, then sift down one path |
| Push-then-pop / replace | O(log n) | One sift instead of two; cheaper than push + pop |
| Heapify (build from n items) | O(n) | Not O(n log n); see below |
| Search for an arbitrary value | O(n) | No order to exploit; the heap only knows its root |
| Delete an arbitrary node | O(n) to find + O(log n) to fix | Heaps are bad at this; a BST or hash-indexed heap is better |

The O(log n) on push and pop is the height of the tree. A complete binary tree of
n nodes has height `floor(log2 n)`, and both operations restore the invariant by
walking a single root-to-leaf (or leaf-to-root) path, one swap per level. See the
[complexity cheat sheet](../complexity.md) for these numbers alongside `heapq`.

### Why push and pop are O(log n)

**Push** appends the new element at the first free slot (the end of the array,
keeping the tree complete), then **sift-up**: compare it with its parent, swap if
it violates the invariant, and repeat upward. It can climb at most the height of
the tree, so O(log n).

**Pop** cannot just delete the root, that would leave a hole. Instead it moves
the last element into the root slot (preserving completeness) and then
**sift-down**: compare the root with its smaller child, swap, and repeat downward
until the invariant holds. Again at most the height, O(log n).

### Why heapify is O(n), not O(n log n)

The naive way to build a heap is n pushes, which is O(n log n). But `heapify`
does something smarter: it takes the whole array as-is and sifts *down* every
non-leaf node, starting from the last parent and moving toward the root. The key
insight is that sift-down cost is bounded by a node's *height*, not the tree's
height, and most nodes are near the bottom where that height is tiny. Half the
nodes are leaves (height 0, zero work), a quarter are at height 1, an eighth at
height 2, and so on. Summing "number of nodes at height h times h" gives a series
`n * sum(h / 2^h)` that converges to a constant, so the total is O(n). The few
expensive nodes near the root are rare enough not to matter. This is why you
always `heapify` an existing array rather than pushing element by element.

## Python implementation

Python's `heapq` is a **min-heap only**, and it operates on a plain list in
place rather than wrapping it in a class:

```python
import heapq

a = [5, 3, 8, 1, 9, 2]
heapq.heapify(a)          # O(n), rearranges the list into a min-heap in place

heapq.heappush(a, 0)      # O(log n)
smallest = a[0]           # O(1) peek, do not pop just to look
smallest = heapq.heappop(a)   # O(log n), returns and removes the minimum

# One combined sift, cheaper than a separate push then pop:
heapq.heappushpop(a, 4)   # push 4, then pop and return the smallest
heapq.heapreplace(a, 4)   # pop the smallest first, then push 4
```

**Max-heap via negation.** Since there is only a min-heap, negate the values (for
numbers) to make the largest become the smallest:

```python
nums = [5, 3, 8, 1]
max_heap = [-x for x in nums]
heapq.heapify(max_heap)
largest = -heapq.heappop(max_heap)   # remember to negate back on the way out
```

**Tuple tie-breakers.** To order by a priority while carrying a payload, push
`(priority, item)` tuples. Python compares tuples lexicographically, so it uses
the first element and falls back to the next on ties. The gotcha: if two
priorities tie, Python then compares the payloads, and if those are not
orderable (two dicts, two custom objects) it raises `TypeError`. Insert a unique,
monotonically increasing counter as a tie-breaker to guarantee comparison never
reaches the payload:

```python
import itertools
counter = itertools.count()
pq = []
heapq.heappush(pq, (priority, next(counter), task))   # (priority, seq, payload)
```

Top-k with a bounded heap, the pattern behind `nlargest`/`nsmallest`: keep a
size-k min-heap of the k largest seen so far, in O(n log k):

```python
def k_largest(nums, k):
    h = nums[:k]
    heapq.heapify(h)                 # O(k)
    for x in nums[k:]:
        if x > h[0]:                 # only if it beats the current k-th largest
            heapq.heapreplace(h, x)  # O(log k)
    return h                         # the k largest, unordered
```

## When to use it (and when not)

**Use a heap when:**

- You repeatedly pull the smallest or largest and re-insert, and you do not need
  full sorted order. Dijkstra, Prim, "merge k sorted lists", and event
  simulations are all this.
- You want the **top k** (or k-th) of a large or streaming input without sorting
  everything. A size-k heap gives O(n log k), which beats O(n log n) sorting and
  needs only O(k) space, and it works on a stream where you cannot sort.
- Priorities change and you keep pulling the current best: a scheduler, an A*
  frontier, a "next task" queue.

**Do not use a heap when:**

- You need everything in sorted order at once. Just `sorted()` it in O(n log n);
  n pops off a heap is the same asymptotic cost with a worse constant.
- You need to search, delete, or update an arbitrary (non-root) element often.
  Heaps have no order to search, so that is O(n). Use a balanced BST or a
  hash-indexed heap.
- You only ever need the single min or max once. `min()`/`max()` in one O(n) pass
  beats building a heap.

## Tradeoffs and gotchas

**A heap is not sorted.** Printing the underlying list shows heap order, not
sorted order. Only the root is guaranteed to be the extreme; everything else is
partially ordered. If you need sorted output, pop repeatedly or call `sorted()`.

**Peek, do not pop, to look.** `a[0]` is O(1). Popping and re-pushing to inspect
the min is O(log n) and a common accidental slowdown.

**Heapify, do not loop-push.** Building from an existing array with `heapify` is
O(n); n separate `heappush` calls is O(n log n). Always prefer `heapify`.

**Negation flips tie order too.** When you negate for a max-heap of tuples,
remember the tie-breaker fields get negated as well, which can invert your
intended secondary ordering. Design the tuple with that in mind.

**Unorderable payloads crash on ties.** As above, `(priority, payload)` raises
`TypeError` when two priorities tie and the payloads are not comparable. Always
add a unique sequence counter between the priority and the payload.

### Heap vs BST

Both give you ordered access, but they optimize different things. A heap gives
O(1) peek at *one* extreme and O(log n) push/pop, but it cannot answer "what is
the k-th smallest", "give me everything in sorted order cheaply", or "find and
delete this arbitrary value" (all O(n)). A balanced BST gives O(log n) search,
insert, delete, predecessor, and successor for *any* element, and O(n) in-order
traversal yields fully sorted output, but its single-minimum lookup is O(log n)
(walk left), not O(1). Rule of thumb: if you only ever want the min or max, use a
heap, it is simpler and has a better constant. If you need to query or mutate
arbitrary elements while staying ordered, use a balanced BST.

## Related patterns

- [Heap / priority queue pattern](../patterns/24-heap.md): the problem shapes
  that scream heap, including "merge k lists" and Dijkstra.
- [Top-k and quickselect](../patterns/09-top-k-quickselect.md): the size-k heap
  is one of the two standard top-k tools; quickselect is the other.
- [Tree and binary search tree](06-tree-bst.md): the BST is the "ordered on every
  element" alternative compared above.
- [Complexity cheat sheet](../complexity.md): the `heapq` cost table, including
  heapify O(n) and push/pop O(log n).
