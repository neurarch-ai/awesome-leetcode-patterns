# 24 - Heap and priority queue

> **Problem shape:** "Return the k largest (or k most frequent, or k closest)
> elements." "Merge k sorted lists." "Find the median of a data stream." "Schedule
> tasks by priority so the machine is idle as little as possible." Anytime you
> repeatedly need the current smallest or largest of a changing set, without paying
> to keep the whole set sorted, a heap is the tool.

A heap is a binary tree kept in an array where every parent is smaller than its
children (a min-heap). That single invariant gives you the minimum in O(1) and
push or pop in O(log n), which is exactly the interface you want when the "best
element" keeps moving as data arrives. Python ships one as `heapq`, and most heap
problems are really about what you choose to store in it.

## The signal

Reach for a heap when you see:

- **"Top k", "k largest", "k smallest", "k closest", "k most frequent".** You do
  not need the whole thing sorted, only the k best, and a size-k heap gets you
  there in O(n log k) instead of O(n log n).
- **"Merge k sorted sequences."** A heap of the k current heads picks the global
  minimum each step in O(log k).
- **"Median of a stream", "keep the middle", "balance two halves".** The
  two-heaps technique maintains a max-heap of the low half and a min-heap of the
  high half.
- **Scheduling and simulation**: "process the highest-priority job", "how many
  rooms do meetings need", "reorganize so no two adjacent are equal". You keep
  pulling the current extreme, mutate it, and push it back.
- **A running "next event" queue**: Dijkstra, Prim, event-driven sweeps. The heap
  is the frontier ordered by cost or time.

The tell is that a plain sort is wasteful because the set changes over time, or
because you only care about one end of it.

## The idea

A binary heap stores a complete tree in an array: node `i` has children `2i+1` and
`2i+2`. The heap property (parent <= children for a min-heap) is local, so
inserting or removing only has to sift one element up or down along a single
root-to-leaf path, which is O(log n). The root is always the minimum, read in
O(1). You never pay to fully sort, you pay only for the moves you actually make.

Three ideas carry most heap problems:

- **Bounded size for top-k.** To keep the k largest, run a min-heap capped at size
  k. Push each element, and when the heap exceeds k, pop the smallest. Whatever
  survives is the k largest, and the root is the kth largest. Cost is O(n log k),
  and memory is O(k) rather than O(n).
- **k pointers via one heap for k-way merge.** Seed the heap with the first
  element of each list. Pop the minimum, output it, and push the next element from
  the list it came from. Each pop is O(log k).
- **Two heaps for a median.** Split the values into a low half (a max-heap, so its
  root is the largest of the small values) and a high half (a min-heap). Keep the
  sizes balanced within one. The median is the top of the larger heap, or the
  average of the two tops when sizes are equal.

## The template

**Min-heap basics, and max-heap by negating:**

```python
import heapq

h = []
heapq.heappush(h, 5)
heapq.heappush(h, 1)
heapq.heappush(h, 3)
smallest = heapq.heappop(h)     # 1, O(log n)
peek = h[0]                     # current minimum, O(1), do not pop

# Python only has a min-heap. For a max-heap, negate on the way in and out.
maxh = []
for x in [5, 1, 3]:
    heapq.heappush(maxh, -x)
largest = -heapq.heappop(maxh)  # 5

# heapify turns a list into a heap in place in O(n), cheaper than n pushes.
nums = [5, 1, 3, 2]
heapq.heapify(nums)             # O(n)
```

**Top k with a size-k min-heap, O(n log k):**

```python
import heapq

def k_largest(nums, k):
    h = []
    for x in nums:
        heapq.heappush(h, x)
        if len(h) > k:
            heapq.heappop(h)    # drop the smallest, keep the k largest
    return h                    # h[0] is the kth largest
```

**k-way merge (merge k sorted lists), O(N log k) over N total elements:**

```python
import heapq

def merge_k(lists):
    h = []
    for i, lst in enumerate(lists):
        if lst:
            # store (value, list_index, elem_index); the index breaks ties
            heapq.heappush(h, (lst[0], i, 0))
    out = []
    while h:
        val, i, j = heapq.heappop(h)
        out.append(val)
        if j + 1 < len(lists[i]):
            heapq.heappush(h, (lists[i][j + 1], i, j + 1))
    return out
```

**Two heaps for a running median:**

```python
import heapq

class MedianFinder:
    def __init__(self):
        self.low = []           # max-heap (store negatives) of the smaller half
        self.high = []          # min-heap of the larger half

    def addNum(self, num):      # LeetCode 295 requires this exact method name
        heapq.heappush(self.low, -num)
        # move the largest of low into high to keep order between the halves
        heapq.heappush(self.high, -heapq.heappop(self.low))
        # rebalance so low is never smaller than high
        if len(self.high) > len(self.low):
            heapq.heappush(self.low, -heapq.heappop(self.high))

    def findMedian(self):       # LeetCode 295 requires this exact method name
        if len(self.low) > len(self.high):
            return -self.low[0]
        return (-self.low[0] + self.high[0]) / 2
```

The tuple trick in the merge is worth internalizing: when you push comparable
payloads, add a monotonic tiebreaker (a counter or an index) so Python never tries
to compare the payloads themselves.

## Variations

- **Top-k by frequency.** Count with a `Counter`, then run the size-k heap over
  `(freq, value)` pairs. `heapq.nlargest(k, counter, key=counter.get)` is the
  one-liner, but the size-k heap is the version you should be able to write.
- **k closest points.** Same size-k heap, keyed by squared distance (no need for
  the square root). Keep a max-heap of size k so you can evict the farthest.
- **Scheduling by priority (task scheduler).** Put task counts in a max-heap, pop
  the most frequent, decrement, and hold it aside for `n` cooldown ticks before it
  can return. Time advances one slot per step, idle when nothing is ready.
- **Meeting rooms II.** Sort by start time, keep a min-heap of end times. For each
  meeting, if the earliest end is <= its start, pop (reuse a room), then push its
  end. The heap size at any moment is the rooms in use, and its max is the answer.
- **Reorganize string.** Max-heap by remaining count. Pop the most frequent
  letter, append it, and hold it back until you have placed a different letter, so
  no two equal letters are adjacent. Infeasible when one letter exceeds
  `(n + 1) // 2`.
- **Lazy deletion.** Heaps do not support "remove this specific element"
  cheaply. Instead, mark entries stale (in a separate set or via a version stamp)
  and skip them when they surface at the top. Push the replacement; discard the
  ghost when it pops. This keeps the amortized cost at O(log n) without an
  indexed heap.

## Canonical problems

| # | Problem | Difficulty | What it drills |
|---|---------|-----------|----------------|
| 1046 | Last Stone Weight | Easy | Max-heap by negation, pop two and push back |
| 215 | Kth Largest Element in an Array | Medium | Size-k heap; contrast with quickselect |
| 347 | Top K Frequent Elements | Medium | Count then size-k heap over frequencies |
| 973 | K Closest Points to Origin | Medium | Size-k max-heap keyed by squared distance |
| 621 | Task Scheduler | Medium | Max-heap scheduling with a cooldown window |
| 253 | Meeting Rooms II | Medium | Sort by start, min-heap of end times |
| 767 | Reorganize String | Medium | Greedy max-heap, hold the last letter back |
| 23 | Merge k Sorted Lists | Hard | k-way merge with a heap of heads |
| 295 | Find Median from Data Stream | Hard | Two-heaps balanced-halves median |

## Pitfalls

- **Forgetting Python only has a min-heap.** For a max-heap you must negate on
  push and negate again on pop, or store `(-key, payload)` tuples. Forgetting the
  second negation returns wrong signs.
- **Comparing unorderable payloads.** Pushing `(dist, point)` where `point` is a
  list blows up when two distances tie and Python compares the lists. Add an
  index or counter as a middle tiebreaker: `(dist, i, point)`.
- **Wrong heap direction for top-k.** For the k largest you want a min-heap of
  size k (evict the smallest); for the k smallest, a max-heap of size k. Getting
  this backwards evicts the wrong end.
- **Rebalancing the median heaps in one direction only.** After every insert you
  must both push across and rebalance sizes, otherwise the halves drift and the
  median reads from the wrong heap.
- **Using a heap when you should heapify.** Building a heap with n individual
  pushes is O(n log n); `heapq.heapify` on the full list is O(n). If you have all
  the data up front, heapify.
- **Reaching for a heap when one-shot top-k would do.** If you only need the top k
  once (no streaming, no repeated queries), quickselect is O(n) average versus the
  heap's O(n log k). See the follow-up.

## Follow-ups and related patterns

- "You only need the top k once, not as a stream" pushes to
  [top-k and quickselect](09-top-k-quickselect.md): partition-based selection is
  O(n) average and beats the heap when there is a single query and mutation of the
  input is allowed.
- "The heap orders a frontier by cost" is exactly Dijkstra and Prim in
  [shortest path](19-shortest-path.md); the priority queue is the same structure
  applied to graph edges.
- "Sort first, then greedily pull the extreme" links to
  [sorting and custom comparators](08-sorting.md) and to [greedy](25-greedy.md);
  many scheduling heaps are a greedy choice made efficient.
- "Overlapping intervals and room counts" generalizes to the sweep line in
  [intervals](05-intervals.md), where the heap of end times is one way to run the
  sweep.
```
