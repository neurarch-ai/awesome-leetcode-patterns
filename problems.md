# The problem bank

This repo is organized by **pattern**, because patterns are the reusable building
blocks. But you meet problems one at a time, phrased as concrete tasks, and you
have to name the pattern yourself. This page is the reverse index: famous problems
and problem archetypes, mapped to the pattern that solves them.

Practice like this: pick a problem, run the [solving
framework](framework/solving-framework.md) to derive the pattern yourself, then
check your guess here and read the linked pattern to fill the gaps.

## Classic problems by pattern

| Problem archetype (and a canonical LeetCode number) | What it is really testing | Pattern |
|---|---|---|
| Two Sum on a sorted array (167) | Converging pointers, safe elimination | [01 two pointers](patterns/01-two-pointers.md) |
| Two Sum, unsorted, return indices (1) | Complement lookup in O(1) | [04 hashing](patterns/04-hashing.md) |
| Longest substring without repeats (3) | Variable window with a seen-map | [02 sliding window](patterns/02-sliding-window.md) |
| Minimum window substring (76) | Cover a multiset, then minimize | [02 sliding window](patterns/02-sliding-window.md) |
| Subarray sum equals k (560) | Prefix sums stored in a hash map | [03 prefix sum](patterns/03-prefix-sum.md), [04 hashing](patterns/04-hashing.md) |
| Merge intervals (56), meeting rooms II (253) | Sort by start, sweep, count overlap | [05 intervals](patterns/05-intervals.md) |
| Find all missing numbers 1..n (448), find the duplicate (287) | Place each number at its index | [06 cyclic sort](patterns/06-cyclic-sort.md) |
| Search in rotated sorted array (33) | Binary search with a pivot invariant | [07 binary search](patterns/07-binary-search.md) |
| Koko eating bananas (875), split array largest sum (410) | Binary search on the answer space | [07 binary search](patterns/07-binary-search.md) |
| Kth largest element (215) | Quickselect, or a size-k heap | [09 top-k](patterns/09-top-k-quickselect.md), [24 heap](patterns/24-heap.md) |
| Reverse a linked list (206), linked list cycle (141) | Pointer reversal, fast-slow | [10 linked list](patterns/10-linked-list.md) |
| Daily temperatures (739), next greater element (496) | Monotonic stack of unresolved indices | [11 stacks](patterns/11-stacks.md) |
| Valid parentheses (20), basic calculator (224) | Stack-based matching and parsing | [11 stacks](patterns/11-stacks.md) |
| Binary tree max path sum (124), diameter (543) | Return an aggregate up from children | [12 tree DFS](patterns/12-tree-dfs.md) |
| Binary tree level order (102), right side view (199) | BFS one level at a time | [13 tree BFS](patterns/13-tree-bfs.md) |
| Validate BST (98), kth smallest in a BST (230) | In-order traversal is sorted | [14 BST](patterns/14-bst.md) |
| Implement Trie (208), word search II (212) | Prefix tree, DFS over a grid with a trie | [15 trie](patterns/15-trie.md) |
| Number of islands (200), rotting oranges (994) | Grid BFS/DFS, connected components | [16 graph traversal](patterns/16-graph-traversal.md) |
| Course schedule (207, 210) | Topological order, cycle detection | [17 topological sort](patterns/17-topological-sort.md) |
| Number of provinces (547), accounts merge (721) | Dynamic connectivity | [18 union-find](patterns/18-union-find.md) |
| Network delay time (743), cheapest flights within k stops (787) | Dijkstra, Bellman-Ford | [19 shortest path](patterns/19-shortest-path.md) |
| Subsets (78), permutations (46), combination sum (39) | Enumerate a decision tree | [20 backtracking](patterns/20-backtracking.md) |
| Coin change (322), house robber (198), word break (139) | 1D optimal choice / knapsack | [21 DP linear](patterns/21-dp-linear-knapsack.md) |
| Longest increasing subsequence (300), edit distance (72) | Two-index string / sequence DP | [22 DP strings](patterns/22-dp-strings.md) |
| Unique paths (62), burst balloons (312) | Grid DP, interval DP | [23 DP grids](patterns/23-dp-grids-intervals.md) |
| Merge k sorted lists (23), find median from data stream (295) | K-way merge, two heaps | [24 heap](patterns/24-heap.md) |
| Jump game (55), gas station (134), task scheduler (621) | Provable local optimum | [25 greedy](patterns/25-greedy.md) |
| Single number (136), sum of two integers (371), subsets via mask (78) | XOR and bitmask tricks | [26 bit manipulation](patterns/26-bit-manipulation.md) |
| Count primes (204), pow(x, n) (50), excel column number (171) | Number theory, fast exponentiation | [27 math](patterns/27-math.md) |
| LRU cache (146), min stack (155), design Twitter (355) | Compose structures to a spec | [28 design](patterns/28-design.md) |

## Problems that combine patterns

The hard interview questions layer two or three patterns. Recognizing the seam is
the skill.

| Problem | The layering |
|---|---|
| Word search II (212) | [Trie](patterns/15-trie.md) to prune a [backtracking](patterns/20-backtracking.md) DFS over the grid |
| Sliding window maximum (239) | [Sliding window](patterns/02-sliding-window.md) with a monotonic deque from [stacks](patterns/11-stacks.md) |
| Subarray sum equals k (560) | [Prefix sum](patterns/03-prefix-sum.md) plus [hashing](patterns/04-hashing.md) |
| Alien dictionary (269) | Build a graph, then [topological sort](patterns/17-topological-sort.md) |
| Cheapest flights within k stops (787) | [Shortest path](patterns/19-shortest-path.md) as a bounded-step [DP](patterns/21-dp-linear-knapsack.md) |
| LFU cache (460) | [Design](patterns/28-design.md) with [hashing](patterns/04-hashing.md) plus ordered buckets |
| Median of two sorted arrays (4) | [Binary search](patterns/07-binary-search.md) on the partition point |
| Trapping rain water (42) | [Two pointers](patterns/01-two-pointers.md), or a [monotonic stack](patterns/11-stacks.md), or [prefix](patterns/03-prefix-sum.md) max arrays |

## A study path

If you are starting from zero, work the patterns in this order. Each leans on the
one before.

1. **Foundations:** [hashing](patterns/04-hashing.md),
   [two pointers](patterns/01-two-pointers.md),
   [sliding window](patterns/02-sliding-window.md),
   [prefix sum](patterns/03-prefix-sum.md). Half of all easy and medium array
   problems.
2. **Search and sort:** [binary search](patterns/07-binary-search.md),
   [sorting](patterns/08-sorting.md), [intervals](patterns/05-intervals.md),
   [top-k](patterns/09-top-k-quickselect.md), [heap](patterns/24-heap.md).
3. **Linear structures:** [linked lists](patterns/10-linked-list.md),
   [stacks](patterns/11-stacks.md).
4. **Trees:** [DFS](patterns/12-tree-dfs.md), [BFS](patterns/13-tree-bfs.md),
   [BST](patterns/14-bst.md), [trie](patterns/15-trie.md).
5. **Graphs:** [traversal](patterns/16-graph-traversal.md),
   [topological sort](patterns/17-topological-sort.md),
   [union-find](patterns/18-union-find.md),
   [shortest path](patterns/19-shortest-path.md).
6. **Search over decisions:** [backtracking](patterns/20-backtracking.md), then
   [DP I](patterns/21-dp-linear-knapsack.md),
   [DP II](patterns/22-dp-strings.md), [DP III](patterns/23-dp-grids-intervals.md).
7. **Rounding out:** [greedy](patterns/25-greedy.md),
   [bit manipulation](patterns/26-bit-manipulation.md),
   [math](patterns/27-math.md), [design](patterns/28-design.md).

Do not try to finish a family before starting the next. Interleave: a few problems
from each, cycling back. Spaced repetition beats blocking.
