# 识别速查表

> 中文版。English: [cheatsheet](../cheatsheet.md)

面试中最有用的单项技能，是在头两分钟内把问题映射到它的模式。这个页面就是那张地图。在你的问题里找到对应的短语或约束，它就会指向通常能破解它的模式。

识别是概率性的，不是查表。一个线索指向一个大概率的模式，你仍然需要通过检查机制是否契合来确认。但这些线索足够常常正确，值得作为你的起点。

## 关键信号（把这些背下来）

最快的识别训练：一行式的「如果你看到 X，就想到 Y」。把这些烂熟于心，大多数问题在第一句话里就会宣告它的模式。

- 如果输入是**有序的**，想到[二分查找](patterns/07-binary-search.md)
  或[双指针](patterns/01-two-pointers.md)。
- 如果你需要 **O(1) 查找或「我见过这个吗」**，想到
  [哈希表或集合](patterns/04-hashing.md)。
- 如果它要求某个约束下**最长或最短的连续**片段，
  想到[滑动窗口](patterns/02-sliding-window.md)。
- 如果它要求**下一个更大或更小的元素**，想到
  [单调栈](patterns/11-stacks.md)。
- 如果它要求**每个窗口的最大或最小值**，想到单调双端队列
  （[栈](patterns/11-stacks.md)）。
- 如果它要求**静态数组上的区间和或计数**，想到
  [前缀和](patterns/03-prefix-sum.md)；如果数组**还会被更新**，
  想到[树状数组或线段树](patterns/29-segment-tree-fenwick.md)。
- 如果它要求**前 k 或后 k 个**，想到[堆](patterns/24-heap.md)或
  [快速选择](patterns/09-top-k-quickselect.md)。
- 如果它涉及**数据流**且你需要一个运行中的顺序统计量，想到
  [堆](patterns/24-heap.md)、两个堆，或
  [有序容器](data-structures/10-sorted-container.md)。
- 如果给你一个**链表**，想到[双指针](patterns/10-linked-list.md)
  （快慢指针）。
- 如果给你一棵**树**，想到 [DFS](patterns/12-tree-dfs.md) 或
  [BFS](patterns/13-tree-bfs.md)。
- 如果给你一个**图或矩阵**，想到
  [DFS、BFS](patterns/16-graph-traversal.md)，或
  [并查集](patterns/18-union-find.md)。
- 如果它询问**连通性或分组**，想到
  [并查集](patterns/18-union-find.md)或 DFS。
- 如果它要求**依赖关系下的排序**，想到
  [拓扑排序](patterns/17-topological-sort.md)。
- 如果它要求**所有排列、子集或组合**，想到
  [回溯](patterns/20-backtracking.md)。
- 如果它要求**方案数**，或在有重叠子问题的**选择上求最小/最大值**，
  想到[动态规划](patterns/21-dp-linear-knapsack.md)。
- 如果每一步你都处在**若干种模式之一**（持有、冷冻期），想到
  [状态机 DP](patterns/30-state-machine-dp.md)。
- 如果它要求**在文本中查找模式**、检测**周期性**，或找出
  **重复的子串**，想到
  [字符串匹配（KMP、滚动哈希）](patterns/31-string-matching.md)。
- 如果你必须**原地用 O(1) 空间求解**，想到交换，或把两个值编码进一个槽位
  （存 `a + b * k`，用 `% k` 和 `// k` 还原）。
- 如果它涉及**重叠区间**，想到
  [排序后扫描](patterns/05-intervals.md)。
- 如果 n **很小（<= 约 20）**，想到[回溯](patterns/20-backtracking.md)或
  [状态压缩 DP](patterns/23-dp-grids-intervals.md)；这个小的上界就是允许你用指数级做法的许可。
- 如果其它都不契合：哈希表用 O(n) 空间换来 O(1) 查找，而对输入排序用
  O(n log n) 时间换来结构。抓住其一，再重新审视。

## 按问题中的短语

| 如果问题里说…… | 抓取 | 模式 |
|---|---|---|
| 「有序数组」、「找一对 / 三元组」 | 双指针 | [01](patterns/01-two-pointers.md) |
| 「原地」、「O(1) 额外空间」、「移动 / 划分」 | 双指针（读写） | [01](patterns/01-two-pointers.md) |
| 「最长 / 最短的连续子数组或子串」 | 滑动窗口 | [02](patterns/02-sliding-window.md) |
| 「至多 k 个」、「不含重复」、「包含全部的」 | 滑动窗口 | [02](patterns/02-sliding-window.md) |
| 「子数组和等于 k」、「区间和查询」 | 前缀和 | [03](patterns/03-prefix-sum.md) |
| 「区间更新」、「给 [i, j] 内所有元素加 x」 | 差分数组 | [03](patterns/03-prefix-sum.md) |
| 「我见过这个吗」、「统计出现次数」、「字母异位词」、「去重」 | 哈希 | [04](patterns/04-hashing.md) |
| 「合并区间」、「会议室」、「重叠」 | 区间 / 扫描线 | [05](patterns/05-intervals.md) |
| 「数字 1..n」、「找缺失 / 重复的」、O(1) 空间 | 循环排序 | [06](patterns/06-cyclic-sort.md) |
| 「有序」、「找目标」、「第一个 / 最后一个位置」 | 二分查找 | [07](patterns/07-binary-search.md) |
| 「最小化最大值」、「能行的最小容量 / 速度」 | 对答案二分 | [07](patterns/07-binary-search.md) |
| 「排序后就简单了」、「自定义顺序」 | 排序 | [08](patterns/08-sorting.md) |
| 「第 k 大 / 小」、「前 k 个」、「最接近的 k 个」 | 快速选择或堆 | [09](patterns/09-top-k-quickselect.md), [24](patterns/24-heap.md) |
| 「反转链表」、「检测环」、「找中点」 | 链表技巧 | [10](patterns/10-linked-list.md) |
| 「下一个更大 / 更小的元素」、「跨度」、「每日温度」 | 单调栈 | [11](patterns/11-stacks.md) |
| 「有效括号」、「求表达式的值」、「解码字符串」 | 栈解析 | [11](patterns/11-stacks.md) |
| 「路径和」、「深度」、「树的直径」、「从子节点返回值」 | 树 DFS | [12](patterns/12-tree-dfs.md) |
| 「层序」、「最小深度」、「右视图」、「按层」 | 树 BFS | [13](patterns/13-tree-bfs.md) |
| 「BST」、「BST 中第 k 小」、「验证 BST」、「中序」 | 二叉搜索树 | [14](patterns/14-bst.md) |
| 「前缀」、「自动补全」、「单词字典」、「以……开头」 | 字典树 | [15](patterns/15-trie.md) |
| 「岛屿数量」、「洪水填充」、「网格上的连通区域」 | 图 / 网格遍历 | [16](patterns/16-graph-traversal.md) |
| 「课程表」、「构建顺序」、「依赖」、「先修条件」 | 拓扑排序 | [17](patterns/17-topological-sort.md) |
| 「这两个连通吗」、「组 / 省份的数量」、「账户合并」 | 并查集 | [18](patterns/18-union-find.md) |
| 「带权重 / 代价的最短路径」、「最便宜的航班」 | Dijkstra / Bellman-Ford | [19](patterns/19-shortest-path.md) |
| 「最短路径，无权 / 均匀代价」 | BFS | [16](patterns/16-graph-traversal.md) |
| 「所有子集 / 排列 / 组合」、「生成每一个」 | 回溯 | [20](patterns/20-backtracking.md) |
| 「N 皇后」、「数独」、「单词搜索」、「按约束放置」 | 回溯 | [20](patterns/20-backtracking.md) |
| 「最小 / 最大代价」、「方案数」、「你能到达吗」、一维选择 | DP 线性 / 背包 | [21](patterns/21-dp-linear-knapsack.md) |
| 「零钱兑换」、「子集和」、「划分」、「目标和」 | 背包 DP | [21](patterns/21-dp-linear-knapsack.md) |
| 「最长递增 / 公共子序列」、「编辑距离」、「回文」 | 字符串上的 DP | [22](patterns/22-dp-strings.md) |
| 「不同路径」、「最小路径和」、「矩阵连乘」、「戳气球」 | 网格 / 区间 DP | [23](patterns/23-dp-grids-intervals.md) |
| 「n <= 20 且尝试所有子集」、「遍历所有城市」（TSP） | 状态压缩 DP | [23](patterns/23-dp-grids-intervals.md) |
| 「动态中位数」、「合并 k 个有序」、「流中最大的 k 个」 | 堆 | [24](patterns/24-heap.md) |
| 「最多不重叠」、「跳跃游戏」、「加油站」、「分配以最小化」 | 贪心 | [25](patterns/25-greedy.md) |
| 「只出现一次的数字」、「计算比特位」、「用掩码表示子集」、「……的异或」 | 位运算 | [26](patterns/26-bit-manipulation.md) |
| 「gcd / lcm」、「是否素数」、「模运算」、「统计位数」、「nCr」 | 数学 | [27](patterns/27-math.md) |
| 「设计一个支持……的结构」、「LRU」、「最小栈」、「迭代器」 | 设计 | [28](patterns/28-design.md) |
| 「带更新的区间和」、「更小元素的计数」、「逆序对」、「翻转对」 | 树状数组 / 线段树 | [29](patterns/29-segment-tree-fenwick.md) |
| 「买卖股票」、「至多 k 次交易」、「冷冻期」、「含手续费」 | 状态机 DP | [30](patterns/30-state-machine-dp.md) |
| 「变化过程中的第 k 小」、「滑动窗口中位数」、「动态统计区间内数量」 | 有序容器（bisect / SortedList） | [ds](data-structures/10-sorted-container.md) |
| 「在文本中查找模式」、「重复子串」、「最短回文串」、「最长重复子串」 | KMP / 滚动哈希 | [31](patterns/31-string-matching.md) |

## 按 n 的约束

n 的大小是关于预期复杂度的免费提示。完整表格见
[解题框架](framework/solving-framework.md)。

| n | 大概的目标 | 首先考虑的模式 |
|---|---|---|
| <= 12 | O(2^n)、O(n!) | 回溯、状态压缩 DP |
| <= 500 | O(n^3) | 区间 DP、Floyd-Warshall |
| <= 5000 | O(n^2) | 成对 DP、两层嵌套循环 |
| <= 10^5 | O(n log n)、O(n) | 排序、堆、二分查找、滑动窗口、双指针、并查集 |
| <= 10^7 | O(n) | 单次遍历、前缀和、筛法 |
| >= 10^9 | O(log n)、O(1) | 对答案二分、数学 |

## 按你要优化的目标

| 你想要…… | 常用工具箱 |
|---|---|
| 最优的连续片段 | 滑动窗口、前缀和 |
| 最优的一对 / 三元组 | 双指针（有序）、哈希（无序） |
| 第 k 个 / 前 k 个元素 | 快速选择、堆 |
| 最短路径 | BFS（无权）、Dijkstra（带权）、DP（在 DAG 上） |
| 选择上的方案数 / 最小代价 | 动态规划 |
| 所有合法的配置 | 回溯 |
| 局部贪心即全局最优的答案 | 贪心（证明它，或退回到 DP） |
| 连通性 / 分组 | 并查集、DFS/BFS |
| 依赖关系下的排序 | 拓扑排序 |

## 当两个模式看起来都契合时

- **贪心 vs DP。** 如果某个局部规则看起来有效，先试贪心，但要准备好证明它或给出反例。
  如果你无法证明它，DP 是永远正确的安全退路（只是更慢）。
- **BFS vs Dijkstra。** 边权相同（或无权）：BFS。非均匀的正权：Dijkstra。负权：Bellman-Ford。
- **堆 vs 快速选择求前 k 个。** 只需要一次、离线：快速选择，平均 O(n)。
  流式或需要 k 个有序：堆，O(n log k)。
- **哈希 vs 双指针求一对。** 有序，或你可以排序且不需要原始下标：双指针，O(1) 空间。
  无序且顺序重要：哈希表，O(n) 空间。
- **树 / 图上的 DFS vs BFS。** 最短路径或层次结构：BFS。路径是否存在、所有路径，或子树聚合：DFS。
