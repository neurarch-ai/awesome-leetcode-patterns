# 学习计划

> 中文版。English: [study-plan](../study-plan.md)

一份精选清单告诉你*该刷什么*。它没告诉你*什么时候*刷、按什么顺序刷，也没告诉你什么时候该停止死磕一个模式而继续往前。这就是那张时间表：把模式和问题排好序，让每一周都在上一周的基础上叠加，就像 [Grind 75](https://www.techinterviewhandbook.org/grind75/) 会把前置知识排在需要它们的问题之前一样。

这是八周版本，每周大约 8 到 10 小时。想更快，就把两周压成一周，并砍掉“加练”题。想更慢，就每个板块花两周，并从每个模式的代表性表格里补充问题。顺序比节奏更重要：不要在树之前开始图，也不要在递归之前开始 DP。

每周：读模式文件，然后按列出的顺序（先易后难）解它的题。如果你两分钟内还不能给一道题归类，那这个模式还不扎实；重读一遍，再多做一道，然后再往前走。

## 第 1 周 - 数组与字符串基础

最大的一桶，也是一切的基础。读[哈希](patterns/04-hashing.md)、[双指针](patterns/01-two-pointers.md)，然后[滑动窗口](patterns/02-sliding-window.md)。

- 1 Two Sum, 217 Contains Duplicate, 242 Valid Anagram（哈希）
- 167 Two Sum II, 125 Valid Palindrome, 15 3Sum（双指针）
- 643 Maximum Average Subarray I, 3 Longest Substring Without Repeating（滑动窗口）
- 加练：76 Minimum Window Substring

## 第 2 周 - 前缀和、区间与二分查找

读[前缀和](patterns/03-prefix-sum.md)、[区间](patterns/05-intervals.md)、[二分查找](patterns/07-binary-search.md)。

- 303 Range Sum Query Immutable, 560 Subarray Sum Equals K（前缀和）
- 56 Merge Intervals, 57 Insert Interval, 253 Meeting Rooms II（区间）
- 704 Binary Search, 35 Search Insert Position, 33 Search in Rotated Sorted Array
- 875 Koko Eating Bananas（在答案上二分）

## 第 3 周 - 链表与栈

读[链表技巧](patterns/10-linked-list.md)和[栈](patterns/11-stacks.md)。

- 206 Reverse Linked List, 141 Linked List Cycle, 21 Merge Two Sorted Lists, 143 Reorder List
- 20 Valid Parentheses, 155 Min Stack, 150 Evaluate Reverse Polish Notation
- 739 Daily Temperatures（单调栈）
- 加练：84 Largest Rectangle in Histogram

## 第 4 周 - 树

读[树的 DFS](patterns/12-tree-dfs.md)、[树的 BFS](patterns/13-tree-bfs.md)、[BST](patterns/14-bst.md)、[Trie](patterns/15-trie.md)。

- 104 Maximum Depth, 226 Invert Binary Tree, 543 Diameter, 112 Path Sum（DFS）
- 102 Level Order, 199 Right Side View（BFS）
- 98 Validate BST, 230 Kth Smallest in a BST（BST）
- 208 Implement Trie（Trie）
- 加练：124 Binary Tree Maximum Path Sum

## 第 5 周 - 图

读[图的遍历](patterns/16-graph-traversal.md)、
[拓扑排序](patterns/17-topological-sort.md)、
[并查集](patterns/18-union-find.md)、[最短路](patterns/19-shortest-path.md)。

- 200 Number of Islands, 994 Rotting Oranges, 133 Clone Graph（遍历）
- 207 Course Schedule, 210 Course Schedule II（拓扑排序）
- 547 Number of Provinces, 684 Redundant Connection（并查集）
- 743 Network Delay Time, 787 Cheapest Flights Within K Stops（最短路）

## 第 6 周 - 回溯与 DP 上篇

读[回溯](patterns/20-backtracking.md)，然后是
[DP I：线性与背包](patterns/21-dp-linear-knapsack.md)。这是大多数人撞上的那堵墙；在这里放慢。

- 78 Subsets, 46 Permutations, 39 Combination Sum, 22 Generate Parentheses（回溯）
- 70 Climbing Stairs, 198 House Robber, 53 Maximum Subarray（线性 DP）
- 322 Coin Change, 416 Partition Equal Subset Sum（背包）
- 读 [DP 子模式地图](patterns/dp-patterns.md)来看清各种形态

## 第 7 周 - DP 下篇与堆

读 [DP II：字符串](patterns/22-dp-strings.md)、
[DP III：网格与区间](patterns/23-dp-grids-intervals.md)、
[堆](patterns/24-heap.md)。

- 300 Longest Increasing Subsequence, 1143 LCS, 72 Edit Distance（字符串 DP）
- 62 Unique Paths, 64 Minimum Path Sum（网格 DP）
- 215 Kth Largest Element, 347 Top K Frequent, 295 Find Median from Data Stream（堆）
- 加练：312 Burst Balloons（区间 DP）

## 第 8 周 - 贪心、位运算、数学、设计与进阶工具

读[贪心](patterns/25-greedy.md)、[位运算](patterns/26-bit-manipulation.md)、
[数学](patterns/27-math.md)、[设计](patterns/28-design.md)，并略读
[线段树与树状数组](patterns/29-segment-tree-fenwick.md)和
[状态机 DP](patterns/30-state-machine-dp.md)。

- 55 Jump Game, 134 Gas Station, 763 Partition Labels（贪心）
- 136 Single Number, 191 Number of 1 Bits, 338 Counting Bits（位运算）
- 146 LRU Cache, 208 Implement Trie, 155 Min Stack（设计）
- 121 到 714 的股票系列（状态机 DP）
- 307 Range Sum Query Mutable, 315 Count of Smaller Numbers After Self（线段树，较难）

## 八周之后

你已经把每个模式都见过一遍了。现在从分块练习切换到**混合复习**：随机的问题，由你自己识别模式，而这正是面试所考察的。用[问题库](problems.md)来盲选，跑一遍[框架](framework/solving-framework.md)，并在几天后重做任何你做错的题。想在这个阶段用更大的题集，就刷 [NeetCode 150](https://neetcode.io/practice)；它的分类能对应到这些模式（见[资源](resources.md)）。

## 如何调整这份计划

- **两周后就要面试？**只做第 1、2、4、5、6 周（数组、二分查找、树、图、回溯与 DP）。那就是那 80%。
- **某个领域薄弱？**在它上面花整整一周，并把那个模式代表性表格里的每一道题都拉出来做。
- **只是手生，不是新手？**跳过阅读，把问题清单当作诊断来做，只重读你卡住的那些模式。
