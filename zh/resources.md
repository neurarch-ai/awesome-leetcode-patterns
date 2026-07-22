# 精选题单与外部资源

> 中文版。English: [resources](../resources.md)

这个仓库教的是模式。要刷题练它们，你需要一份精选的题单，而不是原始的 3000 道题的洪流。
下面这三份题单是社区的标准，按大小递增排列。挑一份把它做完，边做边把每道题映射回它所锻炼的
[模式](patterns/README.md)。这个映射才是重点：一道你无法归类的题，就是一个你还没学会的模式。

## 三份标准题单

| 题单 | 数量 | 最适合 | 链接 |
|---|---|---|---|
| **Grind 75** | 75（可调） | 第一遍。可按时间预算和难度排序，编排顺序让靠前的题为后面的题打好先修基础。 | [techinterviewhandbook.org/grind75](https://www.techinterviewhandbook.org/grind75/) |
| **Blind 75** | 75 | 经典的最小集合，按主题分组。比 Grind 75 更精简，假设你自己补上空缺。 | [neetcode.io/practice（Blind 75 标签）](https://neetcode.io/practice) |
| **NeetCode 150** | 150 | Blind 75 再加 75 道以获得更全面的覆盖，每道题都有视频讲解。最完整的单份题单。 | [neetcode.io/practice](https://neetcode.io/practice) |
| **LeetCode 75** | 75 | LeetCode 自家当前的官方计划，保存在 App 中并带进度跟踪。一个不错的现代第一遍。 | [leetcode.com/studyplan/leetcode-75](https://leetcode.com/studyplan/leetcode-75/) |
| **Top Interview 150** | 150 | LeetCode 官方的「面试必做」计划，按主题分组，更新以反映当前的题库。 | [leetcode.com/studyplan/top-interview-150](https://leetcode.com/studyplan/top-interview-150/) |

推荐路径：**先做 Grind 75**（它很好地编排了先修顺序），然后为了拓宽广度做
**NeetCode 150** 或 LeetCode 的 **Top Interview 150**。Blind 75 是 NeetCode 150 的严格子集，
所以如果你做了 150，就等于做了这 75。两份 LeetCode 计划（LeetCode 75、Top Interview 150）
是当前的官方题单，并在 App 中跟踪你的进度，这正是它们值得在那里做的原因。

> 更愿意按计划刷我们自己的模式？[学习计划](study-plan.md)
> 是一个为期八周、按先修顺序排列的序列，由本仓库中的经典题目构建而成，秉承 Grind 75 的精神。

不要把三份都从头到尾做一遍；那是 300 道有大量重叠的题。完整做一份，然后如果有时间，
只做第二份中不重叠的剩余部分。

## 那些题单如何映射到本仓库

三份题单都把题目分成大致相同的几组，而那些组就是我们的模式家族。用这个来把某份题单的一个章节
翻译成解释它的模式文件：

| 题单分类（Blind 75 / NeetCode） | 我们的模式 |
|---|---|
| 数组与哈希（Arrays and Hashing） | [04 哈希](patterns/04-hashing.md), [03 前缀和](patterns/03-prefix-sum.md) |
| 双指针（Two Pointers） | [01 双指针](patterns/01-two-pointers.md) |
| 滑动窗口（Sliding Window） | [02 滑动窗口](patterns/02-sliding-window.md) |
| 栈（Stack） | [11 栈](patterns/11-stacks.md) |
| 二分查找（Binary Search） | [07 二分查找](patterns/07-binary-search.md) |
| 链表（Linked List） | [10 链表](patterns/10-linked-list.md) |
| 树（Trees） | [12 树 DFS](patterns/12-tree-dfs.md), [13 树 BFS](patterns/13-tree-bfs.md), [14 BST](patterns/14-bst.md) |
| 字典树（Tries） | [15 字典树](patterns/15-trie.md) |
| 堆 / 优先队列（Heap / Priority Queue） | [24 堆](patterns/24-heap.md) |
| 回溯（Backtracking） | [20 回溯](patterns/20-backtracking.md) |
| 图（Graphs） | [16 图遍历](patterns/16-graph-traversal.md), [17 拓扑排序](patterns/17-topological-sort.md), [19 最短路径](patterns/19-shortest-path.md) |
| 进阶图（Advanced Graphs） | [18 并查集](patterns/18-union-find.md), [19 最短路径](patterns/19-shortest-path.md) |
| 一维动态规划（1-D Dynamic Programming） | [21 DP 线性与背包](patterns/21-dp-linear-knapsack.md), [30 状态机 DP](patterns/30-state-machine-dp.md) |
| 二维动态规划（2-D Dynamic Programming） | [22 DP 字符串](patterns/22-dp-strings.md), [23 DP 网格与区间](patterns/23-dp-grids-intervals.md) |
| 贪心（Greedy） | [25 贪心](patterns/25-greedy.md) |
| 区间（Intervals） | [05 区间](patterns/05-intervals.md) |
| 数学与几何（Math and Geometry） | [27 数学](patterns/27-math.md) |
| 位运算（Bit Manipulation） | [26 位运算](patterns/26-bit-manipulation.md) |
| 进阶（线段树 / BIT、区间查询） | [29 线段树与树状数组](patterns/29-segment-tree-fenwick.md) |
| 字符串（子串搜索、KMP、滚动哈希） | [31 字符串匹配](patterns/31-string-matching.md) |

我们有两个家族没有专属的题单章节，但贯穿始终地出现：
[08 排序](patterns/08-sorting.md)（区间、贪心和双指针的先修）和
[28 设计](patterns/28-design.md)（LRU 缓存及同类，通常归在「Stack」或某个「Design」章节下）。

## 一套行之有效的学习流程

1. **先学模式，再刷它。** 读模式文件，然后从该题单章节连续做 3 到 5 道题。
   在单个模式上的集中练习能快速建立识别能力。
2. **然后交错练习。** 一旦你把每个模式都见过一遍，就切换到混合复习：随机的题目，
   你必须自己识别出模式。这才是真实面试所考的，而分块练习建立不了这种能力。
3. **限时。** 给一道中等题 25 分钟。如果卡住了，读思路（不是完整代码），然后自己实现。
   在 40 分钟后还在硬撑，其收获比看到思路再把它写出来要少。
4. **几天后重做你失败的那些**，从零开始。间隔重复正是把一个模式从「我看懂了解法」
   推进到「我能在压力下把它写出来」的方法。

## 值得收藏的外部速查表

比一个模式文件走得更深的单主题深度参考：

- **二分查找**，权威的模板长文：
  [LeetCode discuss，「Powerful Ultimate Binary Search Template」](https://leetcode.com/discuss/general-discussion/786126/python-powerful-ultimate-binary-search-template-solved-many-problems)。
- **滑动窗口**，一个模板搞定大多数子串问题：
  [LeetCode discuss，「Sliding Window Template」](https://leetcode.com/discuss/general-discussion/657507/sliding-window-for-beginners-problems-template-sliding-window-1d-array)。
- **单调栈**，这个家族及其视频讲解：
  [NeetCode practice（Stack 章节）](https://neetcode.io/practice)，以及我们自己的
  [模式 11](patterns/11-stacks.md)。
- **回溯**，一个模板涵盖子集、排列和组合：
  [LeetCode discuss，「A general approach to backtracking questions」](https://leetcode.com/problems/permutations/solutions/18239/a-general-approach-to-backtracking-questions-in-java-subsets-permutations-combination-sum-palindrome-partitioning/)。
- **Python 复杂度参考**，我们[复杂度速查表](complexity.md)中数字的官方来源：
  [wiki.python.org/moin/TimeComplexity](https://wiki.python.org/moin/TimeComplexity)。
- **NeetCode**，完整 150 道题的视频讲解：
  [neetcode.io](https://neetcode.io/)。

把外部速查表当成深度，而不是替代品。识别技能，即在头两分钟内把一道题映射到一个模式，
是我们的[识别速查表](cheatsheet.md)和[题库](problems.md)所训练的，也是面试真正奖励的部分。
