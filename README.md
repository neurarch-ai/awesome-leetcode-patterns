# LeetCode Patterns

A pattern-first guide to the coding interview. LeetCode has thousands of
problems, but they are assembled from a small number of reusable patterns. Once
you can name the pattern, most "new" problems collapse into one you have already
solved. Grinding problem count is the slow path. Learning the ~30 patterns below,
and drilling how to *recognize* each one from the problem statement, is the fast
one.

This repo organizes the patterns the way the problems actually cluster on
[leetcode.com/problemset](https://leetcode.com/problemset/) (by topic tag) and
[leetcode.com/explore](https://leetcode.com/explore/) (by learning card): arrays
and strings, binary search, linked lists, stacks, trees, graphs, backtracking,
dynamic programming, heaps, and the math or bit tricks that show up everywhere.

Each pattern is a self-contained walkthrough: how to spot it, the core idea, a
clean code template, complexity, the canonical problems that drill it, the
variations, and the mistakes that cost people the offer.

---

## How to use this repo

1. **Read the [solving framework](framework/solving-framework.md) first.** It is
   the spine every problem hangs off: clarify, example, brute force, spot the
   bottleneck, optimize, code, test. Interviewers grade your process as much as
   your final code.
2. **Learn to recognize before you memorize.** The
   [pattern cheatsheet](cheatsheet.md) is a lookup table: a phrase or a
   constraint in the problem, mapped to the pattern it usually signals. Internalize
   that table and half the battle is won in the first two minutes.
3. **Work the patterns in family order.** They build on each other. Two pointers
   and hashing set up sliding window; tree traversal sets up graph traversal;
   graph traversal and recursion set up backtracking and DP.
4. **For each pattern, solve two or three of the canonical problems yourself
   before reading the solution notes.** The gap between your attempt and the
   template is your study list.
5. **When stuck on a real problem, reverse-lookup.** The
   [problem bank](problems.md) maps famous problems and problem archetypes
   ("find a pair that sums to a target", "kth largest", "can you partition") to
   the pattern that cracks them.

> Templates are written in Python 3, the most common interview language on
> LeetCode. They are meant to be typed from memory after a few reps, not
> copy-pasted. The point is the shape, not the syntax.

---

## Patterns

Grouped the way production problem sets group them. Start at the top; the later
families assume the earlier ones.

### Arrays and strings
*The largest bucket on LeetCode. Almost all of it is a pointer, a window, a
running total, or a hash map.*

| # | Pattern | When to reach for it |
|---|---------|----------------------|
| 01 | [Two pointers](patterns/01-two-pointers.md) | Sorted array or string, find a pair or triplet, partition in place, compare from both ends |
| 02 | [Sliding window](patterns/02-sliding-window.md) | Longest or shortest contiguous subarray or substring satisfying a constraint |
| 03 | [Prefix sum and difference arrays](patterns/03-prefix-sum.md) | Many range-sum queries, subarray sums equal to k, range updates |
| 04 | [Hashing and frequency counting](patterns/04-hashing.md) | "Have I seen this before", anagrams, dedup, complement lookup in O(1) |
| 05 | [Intervals and sweep line](patterns/05-intervals.md) | Merge, insert, or overlap intervals; meeting rooms; count concurrent events |
| 06 | [Cyclic sort and index-as-hash](patterns/06-cyclic-sort.md) | Numbers in a fixed range 1..n, find the missing or duplicate in O(1) space |

### Binary search and sorting
*Sorted structure, or a monotonic answer space you can binary search over.*

| # | Pattern | When to reach for it |
|---|---------|----------------------|
| 07 | [Binary search](patterns/07-binary-search.md) | Sorted array, or "minimize the maximum" over a monotonic predicate |
| 08 | [Sorting and custom comparators](patterns/08-sorting.md) | The problem gets easy once sorted; custom order; sort-then-scan |
| 09 | [Top-K and quickselect](patterns/09-top-k-quickselect.md) | Kth largest or smallest, k closest, without a full sort |

### Linked lists and stacks
*Pointer surgery and last-in-first-out logic.*

| # | Pattern | When to reach for it |
|---|---------|----------------------|
| 10 | [Linked list techniques](patterns/10-linked-list.md) | Reverse in place, detect a cycle, find the middle, merge lists |
| 11 | [Stacks: monotonic and parsing](patterns/11-stacks.md) | Next greater element, spans, matching brackets, evaluate expressions |

### Trees
*Recursion over a hierarchy, or a level-by-level walk.*

| # | Pattern | When to reach for it |
|---|---------|----------------------|
| 12 | [Tree DFS and recursion](patterns/12-tree-dfs.md) | Path sums, depth, "return a value up from children", traversals |
| 13 | [Tree BFS and level-order](patterns/13-tree-bfs.md) | Level order, minimum depth, right-side view, level-by-level anything |
| 14 | [Binary search tree](patterns/14-bst.md) | Sorted-order traversal, validate, kth smallest, range queries in a BST |
| 15 | [Trie](patterns/15-trie.md) | Prefix search, autocomplete, word dictionaries, XOR maximization |

### Graphs
*Nodes and edges: reachability, ordering, connectivity, shortest path.*

| # | Pattern | When to reach for it |
|---|---------|----------------------|
| 16 | [Graph traversal and grids](patterns/16-graph-traversal.md) | Islands, flood fill, connected components, reachability on a grid or graph |
| 17 | [Topological sort](patterns/17-topological-sort.md) | Ordering under dependencies, course schedule, cycle detection in a DAG |
| 18 | [Union-find (DSU)](patterns/18-union-find.md) | Dynamic connectivity, "are these two connected", count groups, Kruskal |
| 19 | [Shortest path](patterns/19-shortest-path.md) | Weighted shortest path (Dijkstra), 0-1 BFS, Bellman-Ford, grid with cost |

### Recursion, backtracking, and dynamic programming
*Explore a decision tree, then prune it or memoize it.*

| # | Pattern | When to reach for it |
|---|---------|----------------------|
| 20 | [Backtracking](patterns/20-backtracking.md) | Generate all subsets, permutations, combinations; constraint search; N-Queens |
| 21 | [DP I: linear and knapsack](patterns/21-dp-linear-knapsack.md) | Optimal value over a 1D choice; take-or-skip; coin change; subset sum |
| 22 | [DP II: subsequences and strings](patterns/22-dp-strings.md) | LIS, LCS, edit distance, palindromes, two-string alignment |
| 23 | [DP III: grids, intervals, bitmask](patterns/23-dp-grids-intervals.md) | Grid paths, interval DP, matrix-chain, state compression over subsets |

### Heaps, greedy, math, and design
*The cross-cutting toolkit that shows up inside every other family.*

| # | Pattern | When to reach for it |
|---|---------|----------------------|
| 24 | [Heap and priority queue](patterns/24-heap.md) | K-way merge, running median, schedule by priority, top-k streaming |
| 25 | [Greedy](patterns/25-greedy.md) | A locally optimal choice provably leads to the global optimum; jump game, intervals |
| 26 | [Bit manipulation](patterns/26-bit-manipulation.md) | Single number, subsets via bitmask, counting bits, XOR tricks |
| 27 | [Math and number theory](patterns/27-math.md) | GCD, primes, modular arithmetic, combinatorics, digit problems |
| 28 | [Design](patterns/28-design.md) | Build a data structure to a spec: LRU, min stack, iterators, rate limiter |

### Advanced structures and DP
*The tools for harder rounds: dynamic range queries, and DP where the state is a
mode you move between.*

| # | Pattern | When to reach for it |
|---|---------|----------------------|
| 29 | [Segment tree and Fenwick (BIT)](patterns/29-segment-tree-fenwick.md) | Range query with updates, count of smaller, inversions, reverse pairs |
| 30 | [State-machine DP (stock series)](patterns/30-state-machine-dp.md) | Buy/sell stock variants, cooldown, fee, at most k transactions; a few modes with transitions |

---

## The 20 percent that covers 80 percent

If you have limited time, these ten patterns clear the majority of interview
questions. Drill them first:

two pointers, sliding window, binary search, hashing, tree and graph traversal
(BFS/DFS), backtracking, dynamic programming (linear + strings), heaps,
monotonic stack, and union-find.

Everything else in this repo is either a specialization of one of these or a tool
you reach for less often but must not fumble when it appears.

---

## Reference material

The patterns are the core. These pages are the supporting reference you keep open
alongside them:

- **[Data structures](data-structures/README.md)** - the layer underneath the
  patterns: what a heap, a trie, or a union-find actually is, what each operation
  costs, and when to reach for which. Includes a "which structure when" table.
- **[Complexity cheat sheet](complexity.md)** - the operation costs you must know
  cold for Python list, deque, set, dict, Counter, heapq, and str, plus the
  recursion-space caveat.
- **[Glossary](glossary.md)** - the distinctions that decide which pattern you
  reach for: subarray vs substring vs subsequence, amortized, stable sort,
  optimal substructure, and the graph and tree vocabulary.
- **[Curated problem lists](resources.md)** - Grind 75, Blind 75, and NeetCode
  150, each mapped back to the patterns here, plus a study routine and external
  cheat sheets worth bookmarking.
- **[Edge-case checklist](edge-cases.md)** - the empty, single, duplicate,
  negative, and overflow cases interviewers hunt for, as a checklist to run before
  and after you code. More offers are lost here than to the wrong pattern.
- **[Worked-example walkthroughs](walkthroughs/README.md)** - seven canonical
  problems solved end to end with the six-step framework, so you can watch a
  pattern get picked and applied, not just read the finished code.
- **[DP sub-pattern map](patterns/dp-patterns.md)** - the eleven recurring shapes
  of dynamic programming (linear, knapsack, two-sequence, grid, interval, bitmask,
  state-machine, tree, digit, probability), each with its state and transition, so
  you can name the shape and get the recurrence.

---

## Sources of the taxonomy

- [LeetCode problem set](https://leetcode.com/problemset/) tags: the topic labels
  (Array, Two Pointers, Sliding Window, DP, Graph, and so on) are the closest
  thing to an official pattern list. This repo mirrors them, then adds the
  recognition cues LeetCode does not give you.
- [LeetCode Explore](https://leetcode.com/explore/) cards: the guided learning
  paths (Arrays 101, Binary Search, Recursion, Trees, Graph, DP) map almost
  one-to-one onto the families above.

## Contributing

New patterns and new canonical problems welcome. Follow the fixed section shape
in [patterns/README.md](patterns/README.md). Two rules: be honest about
complexity, and prefer explaining the mechanism over name-dropping the trick.

Before opening a PR, run `python3 scripts/check.py`. It enforces the three house
invariants: no em or en dashes, every relative link resolves, and every Python
block compiles. It has no third-party dependencies and is ready to wire into CI as
a single step.
