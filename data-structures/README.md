# Data structures

The [patterns](../patterns/README.md) are algorithms: how to move through data to
an answer. This section is the layer underneath: the data structures those
algorithms run on, what each operation costs, and when to reach for which. A
pattern tells you "use a monotonic stack"; this section tells you what a stack is,
why `append` and `pop` are O(1), and why you build it on a Python list.

If you know the patterns but fumble "is a dict lookup O(1) or O(log n)", this is
the section to read. For the raw operation-cost tables, keep the
[complexity cheat sheet](../complexity.md) open alongside.

Each file follows the same shape:

1. **What it is** - the structure and its invariant, in plain terms.
2. **Operations and complexity** - the cost table you must know.
3. **Python implementation** - the idiomatic way to use or build it.
4. **When to use it (and when not)** - the decision cues.
5. **Tradeoffs and gotchas** - the O(n) surprise hiding in an innocent call.
6. **Related patterns** - which patterns are built on this structure.

## The structures

| # | Structure | The one-line reason it exists |
|---|-----------|-------------------------------|
| 01 | [Array and dynamic array](01-array.md) | O(1) indexed access; the default container |
| 02 | [Hash map and hash set](02-hash-map-set.md) | O(1) average lookup, insert, and membership |
| 03 | [Stack, queue, and deque](03-stack-queue.md) | O(1) push and pop at one end (stack) or both (deque) |
| 04 | [Linked list](04-linked-list.md) | O(1) insert and delete given the node, no shifting |
| 05 | [Heap (priority queue)](05-heap.md) | O(1) peek at the min or max, O(log n) to update |
| 06 | [Tree and binary search tree](06-tree-bst.md) | O(log n) ordered operations when balanced |
| 07 | [Trie (prefix tree)](07-trie.md) | Search by prefix in O(length), not O(number of words) |
| 08 | [Graph](08-graph.md) | Model arbitrary relationships; list vs matrix tradeoff |
| 09 | [Union-find (disjoint set)](09-union-find.md) | Near O(1) "are these connected" and "merge these groups" |
| 10 | [Sorted container (bisect, SortedList)](10-sorted-container.md) | O(log n) order statistics and range counts on changing data |

## Which structure when

The recognition table, from the problem to the structure that makes it cheap:

| You need to... | Reach for | Why |
|---|---|---|
| Access by index, iterate in order | Array / list | O(1) index, cache-friendly |
| Check "have I seen this" in O(1) | Hash set | O(1) average membership |
| Map keys to values, count things | Hash map / Counter | O(1) average get and set |
| Process most-recent-first (undo, matching) | Stack | O(1) push and pop at the top |
| Process first-in-first-out (BFS, scheduling) | Queue / deque | O(1) enqueue and dequeue |
| Insert or delete at both ends | Deque | O(1) both ends, unlike a list |
| Repeatedly pull the smallest or largest | Heap | O(1) peek, O(log n) pop |
| Keep data sorted with fast insert and delete | Balanced BST or [sorted container](10-sorted-container.md) | O(log n) ordered ops |
| Ask "kth smallest" or "how many in range" as data changes | [Sorted container](10-sorted-container.md) (bisect, SortedList) | O(log n) order statistics |
| Range aggregate (sum, min) with updates | [Fenwick or segment tree](../patterns/29-segment-tree-fenwick.md) | O(log n) query and update |
| Search or autocomplete by prefix | Trie | O(prefix length), shares prefixes |
| Model connections, find paths | Graph | edges are the relationships |
| Track connectivity as edges are added | Union-find | near O(1) union and find |
| Insert or delete in the middle without shifting | Linked list | O(1) splice given the node |

## Picking a structure is half the solution

Most "clever" interview solutions are just the right structure applied to the
obvious algorithm. "Two sum" is a hash map. "Valid parentheses" is a stack.
"Merge k lists" is a heap. "Number of provinces" is union-find. When you are
stuck, do not hunt for a trick; ask which structure would make the expensive
operation cheap, and the algorithm usually falls out. The
[cheatsheet](../cheatsheet.md) maps problem phrasing to patterns; this table maps
it to the structure underneath.
