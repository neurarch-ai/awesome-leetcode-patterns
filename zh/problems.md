# 问题库

> 中文版。English: [problems](../problems.md)

本仓库按**模式**组织，因为模式是可复用的构建块。但你遇到问题时是一个一个来的，它们以具体任务的形式出现，你得自己说出对应的模式。本页就是那个反向索引：把著名问题和问题原型映射到能解决它们的模式。

这样练习：挑一道题，跑一遍[解题框架](framework/solving-framework.md)自己推导出模式，然后在这里核对你的猜测，并阅读所链接的模式来补齐空缺。

## 按模式分类的经典问题

| 问题原型（以及一个代表性的 LeetCode 编号） | 它真正考察的是什么 | 模式 |
|---|---|---|
| 有序数组上的 Two Sum (167) | 相向指针，安全地排除 | [01 双指针](patterns/01-two-pointers.md) |
| 无序数组的 Two Sum，返回下标 (1) | O(1) 内查找补数 | [04 哈希](patterns/04-hashing.md) |
| 无重复字符的最长子串 (3) | 带 seen 映射的可变窗口 | [02 滑动窗口](patterns/02-sliding-window.md) |
| 最小覆盖子串 (76) | 先覆盖一个多重集，再最小化 | [02 滑动窗口](patterns/02-sliding-window.md) |
| 和为 k 的子数组 (560) | 存进哈希表的前缀和 | [03 前缀和](patterns/03-prefix-sum.md), [04 哈希](patterns/04-hashing.md) |
| 合并区间 (56)，会议室 II (253) | 按起点排序，扫描，统计重叠 | [05 区间](patterns/05-intervals.md) |
| 找出 1..n 中所有缺失的数 (448)，寻找重复数 (287) | 把每个数放到它对应的下标位置 | [06 循环排序](patterns/06-cyclic-sort.md) |
| 搜索旋转排序数组 (33) | 带枢轴不变量的二分查找 | [07 二分查找](patterns/07-binary-search.md) |
| 爱吃香蕉的珂珂 (875)，分割数组的最大值 (410) | 在答案空间上二分 | [07 二分查找](patterns/07-binary-search.md) |
| 第 K 大的元素 (215) | 快速选择，或大小为 k 的堆 | [09 Top-K](patterns/09-top-k-quickselect.md), [24 堆](patterns/24-heap.md) |
| 反转链表 (206)，环形链表 (141) | 指针反转，快慢指针 | [10 链表](patterns/10-linked-list.md) |
| 每日温度 (739)，下一个更大元素 (496) | 存放未解决下标的单调栈 | [11 栈](patterns/11-stacks.md) |
| 有效的括号 (20)，基本计算器 (224) | 基于栈的匹配与解析 | [11 栈](patterns/11-stacks.md) |
| 二叉树中的最大路径和 (124)，直径 (543) | 从子节点向上返回一个聚合值 | [12 树的 DFS](patterns/12-tree-dfs.md) |
| 二叉树的层序遍历 (102)，右视图 (199) | 逐层进行 BFS | [13 树的 BFS](patterns/13-tree-bfs.md) |
| 验证 BST (98)，BST 中第 K 小的元素 (230) | 中序遍历结果是有序的 | [14 BST](patterns/14-bst.md) |
| 实现 Trie (208)，单词搜索 II (212) | 前缀树，借助 trie 在网格上做 DFS | [15 Trie](patterns/15-trie.md) |
| 岛屿数量 (200)，腐烂的橘子 (994) | 网格 BFS/DFS，连通分量 | [16 图的遍历](patterns/16-graph-traversal.md) |
| 课程表 (207, 210) | 拓扑序，环检测 | [17 拓扑排序](patterns/17-topological-sort.md) |
| 省份数量 (547)，账户合并 (721) | 动态连通性 | [18 并查集](patterns/18-union-find.md) |
| 网络延迟时间 (743)，K 站中转内最便宜的航班 (787) | Dijkstra，Bellman-Ford | [19 最短路](patterns/19-shortest-path.md) |
| 子集 (78)，全排列 (46)，组合总和 (39) | 枚举一棵决策树 | [20 回溯](patterns/20-backtracking.md) |
| 零钱兑换 (322)，打家劫舍 (198)，单词拆分 (139) | 一维最优选择 / 背包 | [21 线性 DP](patterns/21-dp-linear-knapsack.md) |
| 最长递增子序列 (300)，编辑距离 (72) | 双索引的字符串 / 序列 DP | [22 字符串 DP](patterns/22-dp-strings.md) |
| 不同路径 (62)，戳气球 (312) | 网格 DP，区间 DP | [23 网格 DP](patterns/23-dp-grids-intervals.md) |
| 合并 K 个升序链表 (23)，数据流的中位数 (295) | K 路归并，双堆 | [24 堆](patterns/24-heap.md) |
| 跳跃游戏 (55)，加油站 (134)，任务调度器 (621) | 可证明的局部最优 | [25 贪心](patterns/25-greedy.md) |
| 只出现一次的数字 (136)，两整数之和 (371)，用掩码枚举子集 (78) | 异或与位掩码技巧 | [26 位运算](patterns/26-bit-manipulation.md) |
| 计数质数 (204)，pow(x, n) (50)，Excel 表列序号 (171) | 数论，快速幂 | [27 数学](patterns/27-math.md) |
| LRU 缓存 (146)，最小栈 (155)，设计推特 (355) | 组合数据结构以满足规格 | [28 设计](patterns/28-design.md) |
| 区域和检索（可变）(307)，计算右侧小于当前元素的个数 (315)，翻转对 (493) | 带更新的区间查询，逆序对计数 | [29 线段树 / 树状数组](patterns/29-segment-tree-fenwick.md) |
| 买卖股票的最佳时机 I-IV (121, 122, 123, 188)，含冷冻期 (309)，含手续费 (714) | 几种带固定转移的状态 | [30 状态机 DP](patterns/30-state-machine-dp.md) |
| 滑动窗口中位数 (480)，存在重复元素 III (220)，区间和的个数 (327) | 动态顺序统计与区间计数 | [有序容器](data-structures/10-sorted-container.md) |
| 找出字符串中第一个匹配项 / strStr (28)，重复的子字符串 (459)，最短回文串 (214)，最长重复子串 (1044) | 子串搜索、周期性与重复检测 | [31 字符串匹配](patterns/31-string-matching.md) |

## 组合多种模式的问题

难的面试题会叠加两三种模式。看出接缝在哪里才是本事。

| 问题 | 分层方式 |
|---|---|
| 单词搜索 II (212) | 用 [Trie](patterns/15-trie.md) 剪枝在网格上的[回溯](patterns/20-backtracking.md) DFS |
| 滑动窗口最大值 (239) | [滑动窗口](patterns/02-sliding-window.md)配合来自[栈](patterns/11-stacks.md)的单调双端队列 |
| 和为 k 的子数组 (560) | [前缀和](patterns/03-prefix-sum.md)加[哈希](patterns/04-hashing.md) |
| 火星词典 (269) | 建图，然后[拓扑排序](patterns/17-topological-sort.md) |
| K 站中转内最便宜的航班 (787) | 把[最短路](patterns/19-shortest-path.md)当作有步数上限的 [DP](patterns/21-dp-linear-knapsack.md) |
| LFU 缓存 (460) | [设计](patterns/28-design.md)配合[哈希](patterns/04-hashing.md)加有序桶 |
| 寻找两个正序数组的中位数 (4) | 在划分点上做[二分查找](patterns/07-binary-search.md) |
| 接雨水 (42) | [双指针](patterns/01-two-pointers.md)，或[单调栈](patterns/11-stacks.md)，或[前缀](patterns/03-prefix-sum.md)最大值数组 |

## 一条学习路径

如果你从零起步，按这个顺序来练模式。每一个都依赖前一个。

1. **基础：**[哈希](patterns/04-hashing.md)，
   [双指针](patterns/01-two-pointers.md)，
   [滑动窗口](patterns/02-sliding-window.md)，
   [前缀和](patterns/03-prefix-sum.md)。一半的简单和中等数组题都靠它们。
2. **搜索与排序：**[二分查找](patterns/07-binary-search.md)，
   [排序](patterns/08-sorting.md)，[区间](patterns/05-intervals.md)，
   [Top-K](patterns/09-top-k-quickselect.md)，[堆](patterns/24-heap.md)。
3. **线性结构：**[链表](patterns/10-linked-list.md)，
   [栈](patterns/11-stacks.md)。
4. **树：**[DFS](patterns/12-tree-dfs.md)，[BFS](patterns/13-tree-bfs.md)，
   [BST](patterns/14-bst.md)，[Trie](patterns/15-trie.md)。
5. **图：**[遍历](patterns/16-graph-traversal.md)，
   [拓扑排序](patterns/17-topological-sort.md)，
   [并查集](patterns/18-union-find.md)，
   [最短路](patterns/19-shortest-path.md)。
6. **在决策上搜索：**[回溯](patterns/20-backtracking.md)，然后是
   [DP I](patterns/21-dp-linear-knapsack.md)，
   [DP II](patterns/22-dp-strings.md)，[DP III](patterns/23-dp-grids-intervals.md)。
7. **补齐拼图：**[贪心](patterns/25-greedy.md)，
   [位运算](patterns/26-bit-manipulation.md)，
   [数学](patterns/27-math.md)，[设计](patterns/28-design.md)。
8. **进阶（更难的轮次）：**[状态机 DP](patterns/30-state-machine-dp.md)，
   [线段树与树状数组](patterns/29-segment-tree-fenwick.md)，以及
   [有序容器](data-structures/10-sorted-container.md)技巧。第一遍先跳过这些；当某道题需要带更新的区间查询或动态顺序统计时再来用它们。

不要试图刷完一个家族再开始下一个。要交错进行：每个家族做几道，循环回来。间隔重复胜过集中攻坚。
