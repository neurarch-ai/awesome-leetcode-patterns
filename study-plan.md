# The study plan

A curated list tells you *what* to solve. It does not tell you *when*, or in what
order, or when to stop drilling one pattern and move on. This is the schedule:
patterns and problems sequenced so each week builds on the last, the way
[Grind 75](https://www.techinterviewhandbook.org/grind75/) orders prerequisites
before the problems that need them.

This is the eight-week version at roughly 8 to 10 hours per week. To go faster,
compress two weeks into one and drop the "extra" problems. To go slower, spend two
weeks per block and add problems from each pattern's canonical table. The order
matters more than the pace: do not start graphs before trees, or DP before
recursion.

Each week: read the pattern file, then solve its problems in the listed order
(easier first). If you cannot classify a problem in two minutes, that pattern is
not solid yet; re-read and do one more before moving on.

## Week 1 - Array and string foundations

The largest bucket, and the base for everything. Read
[hashing](patterns/04-hashing.md), [two pointers](patterns/01-two-pointers.md),
then [sliding window](patterns/02-sliding-window.md).

- 1 Two Sum, 217 Contains Duplicate, 242 Valid Anagram (hashing)
- 167 Two Sum II, 125 Valid Palindrome, 15 3Sum (two pointers)
- 643 Maximum Average Subarray I, 3 Longest Substring Without Repeating (sliding window)
- Stretch: 76 Minimum Window Substring

## Week 2 - Prefix sums, intervals, and binary search

Read [prefix sum](patterns/03-prefix-sum.md), [intervals](patterns/05-intervals.md),
[binary search](patterns/07-binary-search.md).

- 303 Range Sum Query Immutable, 560 Subarray Sum Equals K (prefix sum)
- 56 Merge Intervals, 57 Insert Interval, 253 Meeting Rooms II (intervals)
- 704 Binary Search, 35 Search Insert Position, 33 Search in Rotated Sorted Array
- 875 Koko Eating Bananas (binary search on the answer)

## Week 3 - Linked lists and stacks

Read [linked list techniques](patterns/10-linked-list.md) and
[stacks](patterns/11-stacks.md).

- 206 Reverse Linked List, 141 Linked List Cycle, 21 Merge Two Sorted Lists, 143 Reorder List
- 20 Valid Parentheses, 155 Min Stack, 150 Evaluate Reverse Polish Notation
- 739 Daily Temperatures (monotonic stack)
- Stretch: 84 Largest Rectangle in Histogram

## Week 4 - Trees

Read [tree DFS](patterns/12-tree-dfs.md), [tree BFS](patterns/13-tree-bfs.md),
[BST](patterns/14-bst.md), [trie](patterns/15-trie.md).

- 104 Maximum Depth, 226 Invert Binary Tree, 543 Diameter, 112 Path Sum (DFS)
- 102 Level Order, 199 Right Side View (BFS)
- 98 Validate BST, 230 Kth Smallest in a BST (BST)
- 208 Implement Trie (trie)
- Stretch: 124 Binary Tree Maximum Path Sum

## Week 5 - Graphs

Read [graph traversal](patterns/16-graph-traversal.md),
[topological sort](patterns/17-topological-sort.md),
[union-find](patterns/18-union-find.md), [shortest path](patterns/19-shortest-path.md).

- 200 Number of Islands, 994 Rotting Oranges, 133 Clone Graph (traversal)
- 207 Course Schedule, 210 Course Schedule II (topological sort)
- 547 Number of Provinces, 684 Redundant Connection (union-find)
- 743 Network Delay Time, 787 Cheapest Flights Within K Stops (shortest path)

## Week 6 - Backtracking and DP part one

Read [backtracking](patterns/20-backtracking.md), then
[DP I: linear and knapsack](patterns/21-dp-linear-knapsack.md). This is the wall
most people hit; slow down here.

- 78 Subsets, 46 Permutations, 39 Combination Sum, 22 Generate Parentheses (backtracking)
- 70 Climbing Stairs, 198 House Robber, 53 Maximum Subarray (linear DP)
- 322 Coin Change, 416 Partition Equal Subset Sum (knapsack)
- Read the [DP sub-pattern map](patterns/dp-patterns.md) to see the shapes

## Week 7 - DP part two and heaps

Read [DP II: strings](patterns/22-dp-strings.md),
[DP III: grids and intervals](patterns/23-dp-grids-intervals.md),
[heap](patterns/24-heap.md).

- 300 Longest Increasing Subsequence, 1143 LCS, 72 Edit Distance (string DP)
- 62 Unique Paths, 64 Minimum Path Sum (grid DP)
- 215 Kth Largest Element, 347 Top K Frequent, 295 Find Median from Data Stream (heap)
- Stretch: 312 Burst Balloons (interval DP)

## Week 8 - Greedy, bits, math, design, and the advanced tools

Read [greedy](patterns/25-greedy.md), [bit manipulation](patterns/26-bit-manipulation.md),
[math](patterns/27-math.md), [design](patterns/28-design.md), and skim
[segment tree and Fenwick](patterns/29-segment-tree-fenwick.md) and
[state-machine DP](patterns/30-state-machine-dp.md).

- 55 Jump Game, 134 Gas Station, 763 Partition Labels (greedy)
- 136 Single Number, 191 Number of 1 Bits, 338 Counting Bits (bits)
- 146 LRU Cache, 208 Implement Trie, 155 Min Stack (design)
- 121 to 714 the stock series (state-machine DP)
- 307 Range Sum Query Mutable, 315 Count of Smaller Numbers After Self (segment tree, harder)

## After the eight weeks

You have seen every pattern once. Now switch from blocked practice to **mixed
review**: random problems where you identify the pattern yourself, which is what
the interview tests. Use the [problem bank](problems.md) to pick blind, run the
[framework](framework/solving-framework.md), and re-solve anything you missed a few
days later. For a broader problem set at this stage, work
[NeetCode 150](https://neetcode.io/practice); its categories map onto these
patterns (see [resources](resources.md)).

## How to tune this

- **Interview in two weeks?** Do weeks 1, 2, 4, 5, 6 only (arrays, binary search,
  trees, graphs, backtracking and DP). That is the 80 percent.
- **Weak on one area?** Spend a whole week on it and pull every problem from that
  pattern's canonical table.
- **Rusty, not new?** Skip the reading, do the problem lists as a diagnostic, and
  only re-read the patterns where you stalled.
