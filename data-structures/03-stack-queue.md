# 03 - Stack, queue, and deque

A stack and a queue are the same idea (add items, remove items) with opposite
removal rules: a stack hands back the most recent item (last in, first out), a
queue hands back the oldest (first in, first out). The mechanism that matters is
where the cheap end is. A Python `list` gives you O(1) at its tail, which makes it
a perfect stack and a terrible queue, because dequeuing from the front is O(n).
`collections.deque` fixes that by being O(1) at both ends. Getting this right is
the difference between an O(n) BFS and an O(n^2) one.

## What it is

A stack is a LIFO container: you push onto the top and pop from the top, and both
touch the same end. Think of a stack of plates, or the call stack, or an undo
history. Because every operation happens at one end, a dynamic array's tail is a
natural fit and both push and pop are amortized O(1).

A queue is a FIFO container: you enqueue at the back and dequeue from the front, so
the two operations touch opposite ends. The frontier of a breadth-first search, a
task scheduler, a print spooler: all queues. The catch is that "remove from the
front" of an array is O(n), so a plain list is the wrong backing store.

A deque (double-ended queue, pronounced "deck") generalizes both: O(1) insert and
remove at both the front and the back. It can act as a stack, a queue, or a
sliding buffer you push and pop from either side. CPython implements it as a
doubly linked list of fixed-size blocks, which is why both ends are O(1) but random
access into the middle is O(n) (it has to walk).

The invariant that decides everything: you only ever pay O(1) at an end that the
structure is built to be cheap at. A list is cheap at its tail only; a deque is
cheap at both ends but not in the middle.

## Operations and complexity

| Operation | Cost | Note |
|---|---|---|
| stack `push` = `list.append(x)` | O(1) amortized | Add at the tail |
| stack `pop` = `list.pop()` | O(1) amortized | Remove from the tail |
| stack `peek` = `a[-1]` | O(1) | Index the tail, do not pop to look |
| queue on a list: `list.pop(0)` | O(n) | Every element shifts. This is the trap |
| queue on a list: `list.insert(0, x)` | O(n) | Same shift, the wrong tool |
| `deque.append(x)`, `deque.appendleft(x)` | O(1) | Both ends are cheap |
| `deque.pop()`, `deque.popleft()` | O(1) | Why a deque beats a list for queues |
| `deque[i]` (random access) | O(n) | Not an array; indexing the middle walks |
| `x in deque` | O(n) | Linear scan |
| `deque.rotate(k)` | O(k) | |

Why list-as-stack is O(1): push and pop both act on the tail, the exact end where a
dynamic array is amortized O(1) (occasional resize aside, same argument as
[array append](01-array.md)). Why list-as-queue is O(n): dequeuing means removing
index 0, and a contiguous array must slide every remaining element down one slot to
keep the layout intact. Do that n times and your queue is O(n^2). Why deque is O(1)
at both ends: it is a linked structure at the block level, so adding or removing an
end block never shifts anything; the price is that reaching element `i` in the
middle means walking there.

These numbers match the [complexity cheat sheet](../complexity.md).

## Python implementation

Stack: just use a list. No wrapper needed, `append` and `pop` are the whole API.

```python
stack = []
stack.append(1)          # push, O(1) amortized
stack.append(2)
top = stack[-1]          # peek, O(1), does not remove
x = stack.pop()          # pop -> 2, O(1) amortized
empty = not stack        # truthiness is the idiomatic emptiness check
```

Queue: use `collections.deque`, never a list. Enqueue with `append`, dequeue with
`popleft`, both O(1).

```python
from collections import deque

q = deque()
q.append(1)              # enqueue at the back, O(1)
q.append(2)
first = q.popleft()      # dequeue from the front -> 1, O(1)

# The canonical BFS: deque frontier, O(1) per node
def bfs(graph, start):
    seen = {start}
    q = deque([start])
    while q:
        node = q.popleft()          # O(1); list.pop(0) here would be O(n)
        for nxt in graph[node]:
            if nxt not in seen:
                seen.add(nxt)
                q.append(nxt)
```

Monotonic stack (and its deque cousin), in brief. A monotonic stack keeps its
contents sorted (increasing or decreasing) by popping any element that violates the
order before pushing the new one. Each element is pushed and popped at most once, so
a whole sweep is O(n) despite the inner while loop. It answers "next greater
element" and "largest rectangle" style questions. The deque version (a monotonic
deque) does the same for a sliding window maximum, popping from the back to keep
order and from the front to drop elements that slid out of the window.

```python
def next_greater(nums):
    # For each element, the next element to its right that is larger, else -1
    res = [-1] * len(nums)
    stack = []                        # holds indices, values decreasing
    for i, x in enumerate(nums):
        while stack and nums[stack[-1]] < x:
            res[stack.pop()] = x      # x is the next greater for that index
        stack.append(i)
    return res
```

A queue from two stacks, the classic design question. Amortize the reversal: push
onto an inbox stack, and when you need to dequeue, pour the inbox into an outbox
stack once (which reverses the order), then pop the outbox. Each element moves
across at most once, so both operations are amortized O(1) even though a single
dequeue can be O(n).

```python
class MyQueue:
    def __init__(self):
        self.inbox = []               # newest on top
        self.outbox = []              # oldest on top

    def push(self, x):                # enqueue, O(1)
        self.inbox.append(x)

    def _shift(self):
        if not self.outbox:           # only refill when outbox is empty
            while self.inbox:
                self.outbox.append(self.inbox.pop())   # reverse once

    def pop(self):                    # dequeue, amortized O(1)
        self._shift()
        return self.outbox.pop()

    def peek(self):                   # amortized O(1)
        self._shift()
        return self.outbox[-1]

    def empty(self):
        return not self.inbox and not self.outbox
```

## When to use it (and when not)

Use a stack when:

- You process most-recent-first: matching brackets, undo, evaluating expressions,
  backtracking, iterative DFS.
- You need "the last unresolved thing", which is what a monotonic stack tracks for
  next-greater and histogram problems.

Use a queue or deque when:

- You process in arrival order: BFS, level-order tree traversal, scheduling, any
  frontier that must expand nearest-first.
- You add or remove at both ends: a sliding window maximum (monotonic deque), a
  work list you can push urgent items to the front of.

Reach for something else when:

- You need O(1) random access by index. A deque indexes the middle in O(n); use a
  [list/array](01-array.md).
- You need priority order, not arrival order ("process the smallest cost next").
  That is a [heap](05-heap.md), not a queue.
- You need membership tests on the contents. `x in deque` is O(n); keep a parallel
  [set](02-hash-map-set.md).

## Tradeoffs and gotchas

- **The one big mistake: a queue on a list.** `list.pop(0)` is O(n), turning any
  BFS into O(n^2). Always `collections.deque` for a queue. If you remember one thing
  from this file, this is it.
- **Deque random access is O(n).** It is not an array. If you find yourself doing
  `dq[i]` for arbitrary `i` in a loop, you picked the wrong structure.
- **Peek without popping.** For a stack, `a[-1]`; for a deque front, `dq[0]`. Do not
  pop just to inspect and then push back, that is a source of ordering bugs.
- **Empty checks.** Popping an empty list or deque raises `IndexError`. Guard with
  `while stack:` or `if q:`; the truthiness of the container is the idiomatic test.
- **Monotonic stacks store indices, not values, usually.** You almost always want
  the position (to compute a width or fill a result slot), so push `i` and read
  `nums[i]`, not `nums[i]` directly.
- **`deque(maxlen=k)` silently drops.** A bounded deque evicts from the opposite
  end on overflow. Handy for a fixed window, surprising if you did not intend it.
- **Two-stack queue: refill only when the outbox is empty.** Pouring on every
  dequeue breaks the amortization and reorders elements. Refill lazily.

## Related patterns

Stacks and queues are the backbone of the traversal and expression patterns:

- [stacks](../patterns/11-stacks.md) covers the monotonic stack, bracket matching,
  and expression evaluation in depth.
- [graph traversal](../patterns/16-graph-traversal.md) is BFS (a deque frontier)
  and DFS (an explicit stack or the call stack).
- [tree BFS](../patterns/13-tree-bfs.md) is level-order traversal, a deque
  processing one level at a time.
- [sliding window](../patterns/02-sliding-window.md) uses a monotonic deque for the
  window-maximum and window-minimum variants.
- [design](../patterns/28-design.md) problems ask you to build a queue from stacks,
  a stack with O(1) min, or a hit-counter on a deque.
- For the O(1)-versus-O(n) end costs that drive every choice here, keep the
  [complexity cheat sheet](../complexity.md) open.
