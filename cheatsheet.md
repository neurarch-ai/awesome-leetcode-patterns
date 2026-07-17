# The recognition cheatsheet

The single most useful interview skill is mapping a problem to its pattern in the
first two minutes. This page is that map. Find the phrase or the constraint in
your problem, and it points you at the pattern that usually cracks it.

Recognition is probabilistic, not a lookup. A cue points at a likely pattern; you
still confirm by checking the mechanism fits. But these cues are right often
enough to be where you start.

## The tells (memorize these)

The fastest recognition drill: a one-line "if you see X, think Y". Learn these cold
and most problems announce their pattern in the first sentence.

- If the input is **sorted**, think [binary search](patterns/07-binary-search.md)
  or [two pointers](patterns/01-two-pointers.md).
- If you need **O(1) lookup or "have I seen this"**, think a
  [hash map or set](patterns/04-hashing.md).
- If it asks for the **longest or shortest contiguous** run under a constraint,
  think [sliding window](patterns/02-sliding-window.md).
- If it asks for the **next greater or smaller element**, think a
  [monotonic stack](patterns/11-stacks.md).
- If it asks for the **max or min of every window**, think a monotonic deque
  ([stacks](patterns/11-stacks.md)).
- If it asks for **range sums or counts on a static array**, think
  [prefix sum](patterns/03-prefix-sum.md); if the array **also gets updated**,
  think [Fenwick or segment tree](patterns/29-segment-tree-fenwick.md).
- If it asks for the **top or bottom k**, think a [heap](patterns/24-heap.md) or
  [quickselect](patterns/09-top-k-quickselect.md).
- If it involves a **stream** and you need a running order statistic, think a
  [heap](patterns/24-heap.md), two heaps, or a
  [sorted container](data-structures/10-sorted-container.md).
- If you are given a **linked list**, think [two pointers](patterns/10-linked-list.md)
  (fast and slow).
- If you are given a **tree**, think [DFS](patterns/12-tree-dfs.md) or
  [BFS](patterns/13-tree-bfs.md).
- If you are given a **graph or a matrix**, think
  [DFS, BFS](patterns/16-graph-traversal.md), or
  [union-find](patterns/18-union-find.md).
- If it asks about **connectivity or grouping**, think
  [union-find](patterns/18-union-find.md) or DFS.
- If it asks for an **ordering under dependencies**, think
  [topological sort](patterns/17-topological-sort.md).
- If it asks for **all permutations, subsets, or combinations**, think
  [backtracking](patterns/20-backtracking.md).
- If it asks for the **number of ways** or a **min/max over choices** with
  overlapping subproblems, think [dynamic programming](patterns/21-dp-linear-knapsack.md).
- If at each step you are in **one of a few modes** (holding, cooldown), think
  [state-machine DP](patterns/30-state-machine-dp.md).
- If it asks to **find a pattern in a text**, test **periodicity**, or find a
  **repeated or duplicate substring**, think
  [string matching (KMP, rolling hash)](patterns/31-string-matching.md).
- If you must solve **in place with O(1) space**, think swapping, or encoding two
  values in one slot (store `a + b * k`, recover with `% k` and `// k`).
- If it involves **overlapping intervals**, think
  [sorting then sweeping](patterns/05-intervals.md).
- If n is **tiny (<= ~20)**, think [backtracking](patterns/20-backtracking.md) or
  [bitmask DP](patterns/23-dp-grids-intervals.md); the small bound is permission to
  be exponential.
- If nothing else fits: a hash map buys O(1) lookups for O(n) space, and sorting
  the input buys structure for O(n log n) time. Reach for one and re-examine.

## By phrase in the problem

| If the problem says... | Reach for | Pattern |
|---|---|---|
| "sorted array", "find a pair / triplet" | Two pointers | [01](patterns/01-two-pointers.md) |
| "in place", "O(1) extra space", "move / partition" | Two pointers (read-write) | [01](patterns/01-two-pointers.md) |
| "longest / shortest contiguous subarray or substring" | Sliding window | [02](patterns/02-sliding-window.md) |
| "at most k", "without repeating", "containing all of" | Sliding window | [02](patterns/02-sliding-window.md) |
| "subarray sum equals k", "range sum query" | Prefix sum | [03](patterns/03-prefix-sum.md) |
| "range update", "add x to all in [i, j]" | Difference array | [03](patterns/03-prefix-sum.md) |
| "have I seen this", "count occurrences", "anagram", "dedup" | Hashing | [04](patterns/04-hashing.md) |
| "merge intervals", "meeting rooms", "overlap" | Intervals / sweep line | [05](patterns/05-intervals.md) |
| "numbers 1..n", "find the missing / duplicate", O(1) space | Cyclic sort | [06](patterns/06-cyclic-sort.md) |
| "sorted", "find target", "first / last position" | Binary search | [07](patterns/07-binary-search.md) |
| "minimize the maximum", "smallest capacity / speed that works" | Binary search on the answer | [07](patterns/07-binary-search.md) |
| "gets easy once sorted", "custom order" | Sorting | [08](patterns/08-sorting.md) |
| "kth largest / smallest", "top k", "k closest" | Quickselect or heap | [09](patterns/09-top-k-quickselect.md), [24](patterns/24-heap.md) |
| "reverse a list", "detect a cycle", "find the middle" | Linked list techniques | [10](patterns/10-linked-list.md) |
| "next greater / smaller element", "spans", "daily temperatures" | Monotonic stack | [11](patterns/11-stacks.md) |
| "valid parentheses", "evaluate expression", "decode string" | Stack parsing | [11](patterns/11-stacks.md) |
| "path sum", "depth", "tree diameter", "return value from children" | Tree DFS | [12](patterns/12-tree-dfs.md) |
| "level order", "minimum depth", "right side view", "by level" | Tree BFS | [13](patterns/13-tree-bfs.md) |
| "BST", "kth smallest in a BST", "validate BST", "in-order" | Binary search tree | [14](patterns/14-bst.md) |
| "prefix", "autocomplete", "word dictionary", "starts with" | Trie | [15](patterns/15-trie.md) |
| "number of islands", "flood fill", "connected region on a grid" | Graph / grid traversal | [16](patterns/16-graph-traversal.md) |
| "course schedule", "build order", "dependencies", "prerequisites" | Topological sort | [17](patterns/17-topological-sort.md) |
| "are these two connected", "number of groups / provinces", "accounts merge" | Union-find | [18](patterns/18-union-find.md) |
| "shortest path with weights / cost", "cheapest flights" | Dijkstra / Bellman-Ford | [19](patterns/19-shortest-path.md) |
| "shortest path, unweighted / uniform cost" | BFS | [16](patterns/16-graph-traversal.md) |
| "all subsets / permutations / combinations", "generate every" | Backtracking | [20](patterns/20-backtracking.md) |
| "N-Queens", "sudoku", "word search", "place with constraints" | Backtracking | [20](patterns/20-backtracking.md) |
| "min / max cost", "number of ways", "can you reach", 1D choice | DP linear / knapsack | [21](patterns/21-dp-linear-knapsack.md) |
| "coin change", "subset sum", "partition", "target sum" | Knapsack DP | [21](patterns/21-dp-linear-knapsack.md) |
| "longest increasing / common subsequence", "edit distance", "palindrome" | DP on strings | [22](patterns/22-dp-strings.md) |
| "unique paths", "min path sum", "matrix chain", "burst balloons" | Grid / interval DP | [23](patterns/23-dp-grids-intervals.md) |
| "n <= 20 and try all subsets", "visit all cities" (TSP) | Bitmask DP | [23](patterns/23-dp-grids-intervals.md) |
| "running median", "merge k sorted", "k largest in a stream" | Heap | [24](patterns/24-heap.md) |
| "maximum non-overlapping", "jump game", "gas station", "assign to minimize" | Greedy | [25](patterns/25-greedy.md) |
| "single number", "count bits", "subset via mask", "XOR of..." | Bit manipulation | [26](patterns/26-bit-manipulation.md) |
| "gcd / lcm", "is prime", "modular", "count digits", "nCr" | Math | [27](patterns/27-math.md) |
| "design a structure that supports...", "LRU", "min stack", "iterator" | Design | [28](patterns/28-design.md) |
| "range sum with updates", "count of smaller", "inversions", "reverse pairs" | Fenwick / segment tree | [29](patterns/29-segment-tree-fenwick.md) |
| "buy/sell stock", "at most k transactions", "cooldown", "with a fee" | State-machine DP | [30](patterns/30-state-machine-dp.md) |
| "kth smallest as it changes", "sliding window median", "count in a range dynamically" | Sorted container (bisect / SortedList) | [ds](data-structures/10-sorted-container.md) |
| "find pattern in text", "repeated substring", "shortest palindrome", "longest duplicate substring" | KMP / rolling hash | [31](patterns/31-string-matching.md) |

## By constraint on n

The size of n is a free hint about the intended complexity. See the full table in
the [solving framework](framework/solving-framework.md).

| n | Likely target | First patterns to consider |
|---|---|---|
| <= 12 | O(2^n), O(n!) | Backtracking, bitmask DP |
| <= 500 | O(n^3) | Interval DP, Floyd-Warshall |
| <= 5000 | O(n^2) | Pairwise DP, two nested loops |
| <= 10^5 | O(n log n), O(n) | Sort, heap, binary search, sliding window, two pointers, union-find |
| <= 10^7 | O(n) | Single pass, prefix sum, sieve |
| >= 10^9 | O(log n), O(1) | Binary search on the answer, math |

## By what you are optimizing

| You want the... | Usual toolkit |
|---|---|
| best contiguous run | Sliding window, prefix sum |
| best pair / triplet | Two pointers (sorted), hashing (unsorted) |
| kth / top-k element | Quickselect, heap |
| shortest path | BFS (unweighted), Dijkstra (weighted), DP (on a DAG) |
| number of ways / min cost over choices | Dynamic programming |
| all valid configurations | Backtracking |
| a locally-greedy-is-globally-optimal answer | Greedy (prove it, or fall back to DP) |
| connectivity / grouping | Union-find, DFS/BFS |
| ordering under dependencies | Topological sort |

## When two patterns both seem to fit

- **Greedy vs DP.** Try greedy first if a local rule seems to work, but be ready
  to prove it or produce a counterexample. If you cannot prove it, DP is the safe
  fallback that is always correct (just slower).
- **BFS vs Dijkstra.** Uniform edge weight (or unweighted): BFS. Non-uniform
  positive weights: Dijkstra. Negative weights: Bellman-Ford.
- **Heap vs quickselect for top-k.** Need it once, offline: quickselect, O(n)
  average. Streaming or need the k sorted: heap, O(n log k).
- **Hashing vs two pointers for a pair.** Sorted or you can sort and do not need
  original indices: two pointers, O(1) space. Unsorted and order matters: hash
  map, O(n) space.
- **DFS vs BFS on a tree/graph.** Shortest path or level structure: BFS. Path
  existence, all paths, or subtree aggregation: DFS.
