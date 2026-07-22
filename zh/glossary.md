# 术语表

> 中文版。English: [glossary](../glossary.md)

那些在面试中让人栽跟头的术语，在此精确定义。在头两分钟里把这些区分弄对
（「等等，这是在问子序列还是子串？」）常常决定了你会抓取哪个模式。

## 子数组 vs 子串 vs 子序列（Subarray vs substring vs subsequence）

这是 LeetCode 上最重要的一个区分，因为它决定了答案是
[滑动窗口](patterns/02-sliding-window.md)（连续）还是
[动态规划](patterns/22-dp-strings.md)（不连续）。

- **子数组（Subarray）**（数组）：一段**连续**的切片。`[2, 3, 4]` 是
  `[1, 2, 3, 4, 5]` 的子数组；`[2, 4]` 不是。共有 O(n^2) 个子数组。
- **子串（Substring）**（字符串）：同样的概念，连续。`"bcd"` 是
  `"abcde"` 的子串；`"bd"` 不是。
- **子序列（Subsequence）**：保持相对顺序，但**不**要求连续。
  `[2, 4]` 是 `[1, 2, 3, 4, 5]` 的子序列。共有 O(2^n) 个子序列。

经验法则：「子数组」和「子串」意味着连续（窗口或前缀和）。
「子序列」意味着你可以跳过元素（通常是 DP）。

## 摊还（Amortized）

**在一系列操作上平均**的代价，即使某个操作偶尔很昂贵。`list.append` 是
O(1) 摊还：大多数 append 是 O(1)，但每隔一段时间列表会以 O(n) 的代价把容量翻倍。
在许多次 append 上平均，每次 append 的代价是常数。摊还 O(1) 和最坏情况 O(1)
不是一回事，但就面试而言，你把 append 当成 O(1) 处理。

## 原地与 O(1) 额外空间（In-place and O(1) extra space）

**原地（In-place）**意味着你只用常数量的额外内存（几个指针或变量）来修改输入，
而不是分配一个大小为 n 的第二个结构。通过从两端交换来反转数组是原地的。注意递归的注意事项：
递归解法不是 O(1) 空间，因为调用栈会随递归深度增长。见
[复杂度速查表](complexity.md#the-recursion-space-caveat)。

## 稳定排序（Stable sort）

如果一次排序保持了比较相等的元素的相对顺序，它就是**稳定的**。Python 的 `sorted` 和
`list.sort`（Timsort）是稳定的。当你按一个键排序并希望以原始顺序打破平局时，
或者当你分多趟按多个键排序时，稳定性就很重要。堆排序和典型的快速排序不是稳定的。

## 单调（Monotonic）

如果一个序列或一个栈只会一直递增（或只会一直递减），它就是**单调的**。
[单调栈](patterns/11-stacks.md)通过弹出会违反该性质的元素来维持这个不变量；
每次弹出都解决一个「下一个更大」或「下一个更小」的关系。单调双端队列对滑动窗口的
最小值和最大值做同样的事。

## 最优子结构与重叠子问题（Optimal substructure and overlapping subproblems）

使[动态规划](patterns/21-dp-linear-knapsack.md)适用的两个性质：

- **最优子结构（Optimal substructure）**：问题的最优答案是由较小子问题的最优答案构建而成的。
  最短路径具有这个性质；最长简单路径不具有。
- **重叠子问题（Overlapping subproblems）**：朴素的递归会多次求解同一个子问题。
  这正是记忆化所利用的。如果子问题不重叠，普通的分治（比如归并排序）才是合适的工具，
  而不是 DP。

## 贪心选择性质（Greedy-choice property）

使[贪心](patterns/25-greedy.md)正确的性质：全局最优解可以通过在每一步做出局部最优的选择、
且从不反悔来达到。当它成立时，贪心又对又快。当它不成立时（面额任意的零钱兑换、0/1 背包），
贪心给出错误答案，你需要 DP。你必须论证该性质成立，通常用一个交换论证。

## 记忆化 vs 制表（Memoization vs tabulation）

实现 DP 的两种方式：

- **记忆化（Memoization）**（自顶向下）：写出自然的递归，第一次计算某个结果时把它缓存起来。
  容易推导，使用调用栈。
- **制表（Tabulation）**（自底向上）：在循环中从基础情形往上填一张表。没有递归，
  更容易做空间优化，但你必须把求值顺序弄对。

它们以相同的复杂度计算相同的东西。先用记忆化找出递推式，如果你需要速度或空间，再转成制表。

## 图的词汇（Graph vocabulary）

- **有向 vs 无向（Directed vs undirected）**：边是否有方向。友谊是无向的；
  「先修条件」是有向的。
- **DAG**：有向无环图，一个没有环的有向图。唯一具有
  [拓扑序](patterns/17-topological-sort.md)的图。
- **入度（In-degree）**：指向一个节点的边的数量。拓扑排序的 Kahn 算法反复移除
  入度为零的节点。
- **连通分量（Connected component）**：一个互相可达节点的极大集合。统计它们是一个
  [并查集](patterns/18-union-find.md)或[遍历](patterns/16-graph-traversal.md)问题。
- **带权 vs 无权（Weighted vs unweighted）**：边是否带有代价。无权最短路径是
  BFS；带正代价的用 Dijkstra；带负代价的用 Bellman-Ford。见
  [最短路径](patterns/19-shortest-path.md)。
- **邻接表 vs 邻接矩阵（Adjacency list vs matrix）**：存储图的两种方式。邻接表使用
  O(V + E) 空间，适合稀疏图；邻接矩阵使用 O(V^2) 并提供 O(1) 的边查找。见
  [图数据结构](data-structures/08-graph.md)。

## 树的词汇（Tree vocabulary）

- **高度 vs 深度（Height vs depth）**：深度是从根往下到某个节点的距离；高度是从某个节点
  往下到它最深叶子的距离。根的深度为 0；叶子的高度为 0。
- **平衡（Balanced）**：没有哪个叶子比其它叶子离根远太多，所以高度保持 O(log n)。
  BST 操作是 O(高度)，只有当树平衡时才是 O(log n)，如果它退化成一个列表则是 O(n)。
- **完全 vs 满 vs 完美（Complete vs full vs perfect）**：**完全（complete）**树在除可能最后一层外的
  每一层都从左到右填满（堆是完全的）；**满（full）**树的每个节点要么有 0 个要么有 2 个孩子；
  **完美（perfect）**树在每一层都被完全填满。
- **BST 不变量（BST invariant）**：对每个节点，左子树中所有的键都更小，右子树中所有的键都更大。
  一棵 [BST](patterns/14-bst.md) 的中序遍历按有序顺序产出这些键。

## 可哈希（Hashable）

如果一个对象有稳定的哈希值，它就是**可哈希的**，在 Python 中这意味着它是不可变的：
数字、字符串，以及由可哈希元素构成的元组是可哈希的；列表、集合和字典不是。
只有可哈希的对象才能作为字典的键或集合的元素。这就是为什么网格坐标作为元组
`(r, c)` 放进集合，而绝不作为列表。

## 双指针 vs 滑动窗口（Two-pointer vs sliding window）

两者都在不用嵌套循环的情况下移动下标，但意图不同。**双指针（Two pointers）**
通常从一个有序数组的两端收敛，或以不同的速度移动（快慢指针）。**滑动窗口
（Sliding window）**是双指针的一种特化，两个指针都从左往右移动，它们之间的区域
（窗口）是关注的对象。见[双指针](patterns/01-two-pointers.md)和
[滑动窗口](patterns/02-sliding-window.md)。
