# 28 - Design

> **Problem shape:** "Design an LRU cache with O(1) get and put." "Implement an
> iterator." "Insert, delete, and getRandom, all in O(1)." "Design a min stack."
> "Design Twitter." The task is not a single algorithm, it is: build a data
> structure that meets a spec, where each named operation has a target complexity
> you must hit by composing the right primitives.

Design problems test whether you can pick and glue data structures rather than
invent an algorithm. The method is always the same: list the operations, write
the complexity target next to each, then choose structures so that every operation
lands at O(1) or O(log n). The winning combinations are a small set (hashmap plus
doubly linked list, hashmap plus array, two heaps, stack plus auxiliary stack), and
most problems are one of them wearing a costume.

## The signal

Reach for the design pattern when the problem says:

- **"Implement a class" / "design a structure"** with a fixed set of named methods,
  rather than "return the answer to this query".
- **A hard per-operation complexity target**: "O(1) get and put", "O(1) getRandom",
  "O(log n) insert". The target dictates the structure; if `get` must be O(1) you
  need a hashmap, if you also need ordering you need a second structure alongside
  it.
- **Two requirements that no single structure satisfies.** O(1) lookup wants a
  hashmap; ordered eviction wants a linked list; random access wants an array.
  When the spec demands two at once, the answer is to run two structures in lockstep
  and keep them pointing at each other.
- **A stream you consume on demand**: "implement an iterator", "hasNext / next",
  "peeking iterator". You wrap a source and buffer just enough to answer the next
  call.

The tell is that there is no clever recurrence to find; the cleverness is entirely
in the choice and coordination of containers.

## The idea

Every operation has a natural home:

- **O(1) keyed lookup** -> hashmap.
- **O(1) insert / delete at a known position, ordered** -> doubly linked list (you
  can splice a node out in O(1) if you hold a pointer to it).
- **O(1) random access by index, O(1) append / pop-last** -> dynamic array.
- **O(log n) min / max extraction** -> heap.

You compose them so that the hashmap holds pointers *into* the other structure.
The LRU cache is the canonical example: a hashmap gives O(1) key -> node lookup,
and a doubly linked list gives O(1) move-to-front and O(1) evict-from-back. Neither
alone can do both; together each operation is O(1). The recurring trick for O(1)
delete-from-the-middle (LRU, insert-delete-getRandom) is that the hashmap stores a
*handle* (a node reference, or an index) so you never have to search for the item
you are about to remove.

## The template

**LRU cache with `OrderedDict` (the concise, interview-fast version):**

```python
from collections import OrderedDict

# Space: O(capacity)
class LRUCache:
    # Time: O(1)
    def __init__(self, capacity):
        self.cache = OrderedDict()      # insertion order == recency order
        self.cap = capacity

    # Time: O(1)
    def get(self, key):
        if key not in self.cache:
            return -1
        self.cache.move_to_end(key)     # mark as most recently used
        return self.cache[key]

    # Time: O(1)
    def put(self, key, value):
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.cap:
            self.cache.popitem(last=False)   # evict least recently used (front)
```

`OrderedDict` *is* a hashmap plus a doubly linked list under the hood;
`move_to_end` and `popitem(last=False)` are the O(1) splice operations. If the
interviewer bans it, build the two structures by hand:

**LRU cache, explicit hashmap + doubly linked list (what OrderedDict does for you):**

```python
# Space: O(1)
class Node:
    __slots__ = ('key', 'val', 'prev', 'next')
    # Time: O(1)
    def __init__(self, key=0, val=0):
        self.key, self.val, self.prev, self.next = key, val, None, None

# Space: O(capacity)
class LRUCache:
    # Time: O(1)
    def __init__(self, capacity):
        self.cap = capacity
        self.map = {}                       # key -> Node
        self.head, self.tail = Node(), Node()   # sentinels: head<->...<->tail
        self.head.next, self.tail.prev = self.tail, self.head

    # Time: O(1)
    def _remove(self, node):                # unlink in O(1)
        node.prev.next, node.next.prev = node.next, node.prev

    # Time: O(1)
    def _add_front(self, node):             # splice right after head (most recent)
        node.prev, node.next = self.head, self.head.next
        self.head.next.prev = node
        self.head.next = node

    # Time: O(1)
    def get(self, key):
        if key not in self.map:
            return -1
        node = self.map[key]
        self._remove(node); self._add_front(node)   # bump to most recent
        return node.val

    # Time: O(1)
    def put(self, key, value):
        if key in self.map:
            self._remove(self.map[key])
        node = Node(key, value)
        self.map[key] = node
        self._add_front(node)
        if len(self.map) > self.cap:
            lru = self.tail.prev            # least recent is just before tail
            self._remove(lru)
            del self.map[lru.key]           # the node stored its key for this delete
```

The two sentinels (`head`, `tail`) remove all the null-check branches: every real
node always has a real neighbor on both sides. Note the node stores its own `key`
so eviction can delete the hashmap entry in O(1) without a reverse lookup.

## Variations

- **Min stack.** Keep a second stack that, at each level, holds the minimum so far.
  Push the min of (incoming, current-min) alongside every push; the top of the aux
  stack is always the current minimum, so `getMin` is O(1). Alternative: store
  `(value, running_min)` tuples in one stack.
- **LFU cache.** Harder than LRU: you evict the least *frequently* used, breaking
  ties by least recently used. Keep a hashmap key -> node, a hashmap frequency ->
  ordered list of nodes at that frequency, and a running `min_freq`. On access,
  move the node from its freq bucket to freq+1; evict from the `min_freq` bucket's
  oldest.
- **Insert-delete-getRandom O(1).** Hashmap value -> index into a dynamic array.
  Insert appends to the array; delete swaps the target with the last element, pops,
  and fixes the moved element's index in the map; getRandom indexes the array with
  a random integer. The swap-with-last trick is what keeps delete O(1).
- **Iterators.** Wrap a source and buffer the next item. A *peeking* iterator caches
  one look-ahead; a *flatten nested list* iterator pushes the structure onto a stack
  and lazily unwraps on `hasNext`.
- **Design Twitter.** Hashmap user -> set of followees and user -> list of
  (timestamp, tweet). `getNewsFeed` merges the recent tweets of all followees with a
  heap (k-way merge), taking the 10 most recent. Heap plus hashmap.
- **Implement queue with stacks / stack with queues.** Two stacks give an amortized
  O(1) queue: push onto an `in` stack, pop from an `out` stack, refilling `out` from
  `in` only when it empties.

## Canonical problems

| # | Problem | Difficulty | What it drills |
|---|---------|-----------|----------------|
| 232 | Implement Queue using Stacks | Easy | Two stacks, amortized O(1) |
| 155 | Min Stack | Medium | Auxiliary stack tracking the running min |
| 146 | LRU Cache | Medium | Hashmap + doubly linked list, O(1) both |
| 208 | Implement Trie (Prefix Tree) | Medium | Nested-dict nodes, insert and search |
| 380 | Insert Delete GetRandom O(1) | Medium | Hashmap + array, swap-with-last delete |
| 355 | Design Twitter | Medium | Heap k-way merge over follow lists |
| 460 | LFU Cache | Hard | Freq buckets plus min_freq bookkeeping |

## Pitfalls

- **Forgetting to update the hashmap on eviction.** In LRU, when you unlink the
  tail node you must also `del self.map[node.key]`, which is why the node stores its
  own key. Miss this and the map leaks stale entries.
- **getRandom's delete not fixing the moved index.** After swapping the target with
  the last array element, you must update the moved element's index in the map
  *before* popping, or the map points at a hole.
- **Min stack popping the aux stack out of sync.** Every `push` must push to both
  stacks and every `pop` must pop both, or the min history drifts from the values.
- **Missing sentinels in the hand-built linked list.** Without `head`/`tail`
  sentinels every splice needs null checks for the empty-list and single-node cases;
  sentinels make `_remove` and `_add_front` branch-free.
- **LFU tie-breaking.** Least-frequently-used ties must break by least-recently-used
  within the frequency bucket, so each bucket has to preserve insertion order (an
  `OrderedDict` per frequency).
- **Iterator computing everything up front.** The point of an iterator is laziness;
  materializing the whole sequence in the constructor defeats it and can blow memory
  on an infinite or huge source.

## Follow-ups and related patterns

- "Make getMin / getMax also O(1) in a queue" pushes the min-stack idea into a
  monotonic deque, see [stacks: monotonic and parsing](11-stacks.md).
- "Merge the feeds of all followees" is a k-way merge on a
  [heap and priority queue](24-heap.md); Design Twitter is a heap problem wearing a
  design costume.
- The LRU and getRandom deletes both lean on O(1) splicing and pointer bookkeeping
  from [linked list techniques](10-linked-list.md).
- "Implement Trie" is really the [trie](15-trie.md) pattern posed as a design task;
  the design skill is choosing the nested-dictionary node representation.
- Rate limiters, autocomplete, and other "design X" system-flavored questions reuse
  the same compose-two-structures method, often adding a
  [heap](24-heap.md) or a hashmap of counts from
  [hashing and frequency counting](04-hashing.md).
