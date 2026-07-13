# Glossary

The terms that trip people up in interviews, defined precisely. Getting these
distinctions right in the first two minutes ("wait, is this asking for a
subsequence or a substring?") often decides which pattern you reach for.

## Subarray vs substring vs subsequence

The single most important distinction on LeetCode, because it decides whether the
answer is a [sliding window](patterns/02-sliding-window.md) (contiguous) or
[dynamic programming](patterns/22-dp-strings.md) (not contiguous).

- **Subarray** (arrays): a **contiguous** slice. `[2, 3, 4]` is a subarray of
  `[1, 2, 3, 4, 5]`; `[2, 4]` is not. There are O(n^2) subarrays.
- **Substring** (strings): the same idea, contiguous. `"bcd"` is a substring of
  `"abcde"`; `"bd"` is not.
- **Subsequence**: keeps the relative order but does **not** require contiguity.
  `[2, 4]` is a subsequence of `[1, 2, 3, 4, 5]`. There are O(2^n) subsequences.

Rule of thumb: "subarray" and "substring" mean contiguous (window or prefix sum).
"Subsequence" means you may skip elements (usually DP).

## Amortized

The cost **averaged over a sequence of operations**, even if one operation is
occasionally expensive. `list.append` is O(1) amortized: most appends are O(1),
but every so often the list doubles its capacity in O(n). Averaged over many
appends, the per-append cost is constant. Amortized O(1) is not the same as
worst-case O(1), but for interview purposes you treat append as O(1).

## In-place and O(1) extra space

**In-place** means you modify the input using only a constant amount of extra
memory (a few pointers or variables), rather than allocating a second structure
of size n. Reversing an array by swapping from both ends is in-place. Note the
recursion caveat: a recursive solution is not O(1) space, because the call stack
grows with the recursion depth. See the
[complexity cheat sheet](complexity.md#the-recursion-space-caveat).

## Stable sort

A sort is **stable** if it preserves the relative order of elements that compare
equal. Python's `sorted` and `list.sort` (Timsort) are stable. Stability matters
when you sort by one key and want ties broken by the original order, or when you
sort by multiple keys in passes. Heapsort and typical quicksort are not stable.

## Monotonic

A sequence or a stack is **monotonic** if it only ever increases (or only ever
decreases). A [monotonic stack](patterns/11-stacks.md) maintains this invariant by
popping elements that would violate it; each pop resolves a "next greater" or
"next smaller" relationship. A monotonic deque does the same for sliding-window
minimum and maximum.

## Optimal substructure and overlapping subproblems

The two properties that make [dynamic programming](patterns/21-dp-linear-knapsack.md)
apply:

- **Optimal substructure**: the optimal answer to the problem is built from
  optimal answers to smaller subproblems. Shortest paths have it; longest simple
  paths do not.
- **Overlapping subproblems**: the naive recursion solves the same subproblem many
  times. This is what memoization exploits. If subproblems do not overlap, plain
  divide and conquer (like merge sort) is the right tool, not DP.

## Greedy-choice property

The property that makes [greedy](patterns/25-greedy.md) correct: a globally
optimal solution can be reached by making a locally optimal choice at each step,
never reconsidering. When it holds, greedy is right and fast. When it does not
(coin change with arbitrary denominations, 0/1 knapsack), greedy gives a wrong
answer and you need DP. You must argue the property holds, usually with an
exchange argument.

## Memoization vs tabulation

Two ways to implement DP:

- **Memoization** (top-down): write the natural recursion, cache each result the
  first time you compute it. Easy to derive, uses the call stack.
- **Tabulation** (bottom-up): fill a table from the base cases upward in a loop.
  No recursion, easier to space-optimize, but you must get the evaluation order
  right.

They compute the same thing with the same complexity. Start with memoization to
find the recurrence, convert to tabulation if you need the speed or the space.

## Graph vocabulary

- **Directed vs undirected**: whether edges have a direction. A friendship is
  undirected; a "prerequisite" is directed.
- **DAG**: a directed acyclic graph, a directed graph with no cycles. The only
  graphs that have a [topological order](patterns/17-topological-sort.md).
- **In-degree**: the number of edges pointing into a node. Kahn's algorithm for
  topological sort repeatedly removes in-degree-zero nodes.
- **Connected component**: a maximal set of mutually reachable nodes. Counting
  them is a [union-find](patterns/18-union-find.md) or a
  [traversal](patterns/16-graph-traversal.md) problem.
- **Weighted vs unweighted**: whether edges carry a cost. Unweighted shortest
  path is BFS; weighted with positive costs is Dijkstra; with negative costs it is
  Bellman-Ford. See [shortest path](patterns/19-shortest-path.md).
- **Adjacency list vs matrix**: two ways to store a graph. List uses O(V + E)
  space and is right for sparse graphs; matrix uses O(V^2) and gives O(1) edge
  lookup. See the [graph data structure](data-structures/08-graph.md).

## Tree vocabulary

- **Height vs depth**: depth is the distance from the root down to a node; height
  is the distance from a node down to its deepest leaf. The root has depth 0; a
  leaf has height 0.
- **Balanced**: no leaf is much farther from the root than any other, so the
  height stays O(log n). BST operations are O(height), which is O(log n) only if
  the tree is balanced and O(n) if it degenerates into a list.
- **Complete vs full vs perfect**: a **complete** tree is filled left to right on
  every level except possibly the last (heaps are complete); a **full** tree has
  every node with either 0 or 2 children; a **perfect** tree is completely filled
  on every level.
- **BST invariant**: for every node, all keys in the left subtree are smaller and
  all keys in the right subtree are larger. An in-order traversal of a
  [BST](patterns/14-bst.md) yields the keys in sorted order.

## Hashable

An object is **hashable** if it has a stable hash value, which in Python means it
is immutable: numbers, strings, and tuples of hashable things are hashable; lists,
sets, and dicts are not. Only hashable objects can be dict keys or set elements.
This is why grid coordinates go into a set as tuples `(r, c)`, never as lists.

## Two-pointer vs sliding window

Both walk indices without nested loops, but the intent differs. **Two pointers**
usually converge from both ends of a sorted array, or run at different speeds
(fast and slow). **Sliding window** is a two-pointer specialization where both
pointers move left to right and the region between them (the window) is the object
of interest. See [two pointers](patterns/01-two-pointers.md) and
[sliding window](patterns/02-sliding-window.md).
