# 20 - 回溯

> 中文版。English: [20-backtracking](../../patterns/20-backtracking.md)

> **问题形态：**「返回所有子集。」「生成每一个排列。」「找出所有和为目标值的
> 组合。」「摆放 N 个皇后使其互不攻击。」「解数独。」凡是要求你枚举或搜索所有
> 合法的选择组合，且每个部分组合都是逐个决策构建出来、一旦无法通向解就立即放弃
> 的问题，都属于这一类。

回溯是在决策树上做深度优先搜索。你逐步构建一个候选解，每当一个部分候选注定失败时
就撤销上一个选择，改试下一个。它是「枚举一切」以及约束满足问题的模式，其代价天然
是指数级的，这也正是为什么这类题的输入规模都很小。

![1,2,3 的所有子集的决策树](../../assets/backtracking.svg)

*决策树：在每个元素上你都分叉为跳过或选取，叶子节点枚举出每一个子集。*

## 信号

出现以下情况时考虑回溯：

- **「所有」「每一个」「枚举」「生成」「列出全部」**，并伴随子集、排列、组合、
  划分或安排。答案是一个集合的集合，而不是单个数字。
- **很小的输入上界。** `n <= 15`、`n <= 20`、像 `9 x 9` 这样的棋盘尺寸。只有当 n
  很小时指数级或阶乘级的爆炸才可承受，因此一个很紧的 n 是最响亮的提示：题目意图是
  带剪枝的暴力搜索。
- **约束满足**：在规则约束下摆放物件（N 皇后、数独），或在相邻规则下穿过网格追踪
  一条路径（单词搜索）。你需要尝试一次摆放、递归、若违反约束则撤回。
- **每一步都有一个决策**，分支集合很小，各个选择组合成一个完整解，且部分解可以在
  构建过程中被验证。

如果题目转而问的是安排的*数量*或*最优*的那一个，且 n 很大，那通常是
[DP](21-dp-linear-knapsack.md)，而不是纯回溯。

## 思路

每个回溯问题都是在一棵隐式的**决策树**上行走。每个节点是一个部分候选；每条边是一个
选择；每个叶子是一个完整候选，你要么记录它、要么拒绝它。递归在每个节点做三件事，即
选择 / 探索 / 撤销的循环：

1. **选择**当前位置的一个候选（把它追加到路径中）。
2. **探索**，通过递归去决定下一个位置。
3. **撤销**，移除你刚刚加入的东西，恢复状态，让下一个兄弟分支从干净的状态开始。

撤销这一步正是它被称为「回溯」的原因：一个可变的 `path` 在整棵树上共享，向下时压入、
向上时弹出，因此除了在记录一个完成的叶子时之外，你从不需要为复制状态付出代价。

**剪枝**是另一半。如果一个部分候选已经违反了约束（和超过目标、一个皇后攻击另一个），
你就在递归之前返回，砍掉整个子树。好的剪枝是「能跑完的解」与「会超时的解」之间的
区别，尽管最坏情况的复杂度并未改变。

复杂度天然是指数级的：子集有 `O(2^n)` 个节点，排列有 `O(n!)` 个，每个叶子复制需要
`O(n)`，因此典型的界是 `O(n * 2^n)` 或 `O(n * n!)`。没有多项式的捷径；这场游戏就是
狠狠剪枝并把常数因子压低。

## 模板

**通用的选择 / 探索 / 撤销骨架（子集）：**

```python
# Time: O(n * 2^n), Space: O(n) (recursion depth plus path, output aside)
def subsets(nums):
    res = []
    path = []

    def backtrack(start):
        res.append(path[:])                # every node is a valid subset
        for i in range(start, len(nums)):
            path.append(nums[i])           # choose
            backtrack(i + 1)               # explore (i + 1: no reuse, no reorder)
            path.pop()                     # unchoose

    backtrack(0)
    return res
```

`start` 下标是组合与子集的关键：它禁止往回走，因此 `[1,2]` 和 `[2,1]` 不会都被生成。
排列则丢掉 `start`，改为追踪哪些元素已被使用。

**排列（顺序重要，所以用 `used` 集合而不是 `start`）：**

```python
# Time: O(n * n!), Space: O(n) (recursion depth plus path and used, output aside)
def permute(nums):
    res = []
    path = []
    used = [False] * len(nums)

    def backtrack():
        if len(path) == len(nums):
            res.append(path[:])
            return
        for i in range(len(nums)):
            if used[i]:
                continue
            used[i] = True
            path.append(nums[i])
            backtrack()
            path.pop()
            used[i] = False

    backtrack()
    return res
```

**组合总和（可无限重复使用，当运行和超出时剪枝）：**

```python
# Time: O(exponential in target/min candidate), Space: O(target / min candidate) recursion depth
def combination_sum(candidates, target):
    candidates.sort()                      # enables the early break prune
    res = []
    path = []

    def backtrack(start, remaining):
        if remaining == 0:
            res.append(path[:])
            return
        for i in range(start, len(candidates)):
            if candidates[i] > remaining:  # sorted: all later are bigger too
                break                      # prune the rest of this level
            path.append(candidates[i])
            backtrack(i, remaining - candidates[i])   # i, not i + 1: reuse allowed
            path.pop()

    backtrack(0, target)
    return res
```

注意区分整个家族的两个旋钮：`start` 对比 `used` 控制顺序，递归调用中的 `i` 对比
`i + 1` 控制是否可重复使用。

## 变体

- **处理重复（排序 + 跳过）。** 当输入含有重复且你不能产生重复结果时，先排序，然后
  在每一层跳过与其前驱相等的值：`if i > start and nums[i] == nums[i-1]: continue`。
  这禁止了同一树深处出现两个相同的分支。组合总和 II 与子集 II 是训练题。
- **大小为 k 的组合。** 与子集相同，但只在 `len(path) == k` 时记录，并在剩余元素无法
  填满 k 个空位时剪枝。
- **生成括号。** 每一步的决策是「加 `(`」或「加 `)`」，由两个计数器剪枝：当
  `open < n` 时可以开括号，只有当 `close < open` 时才可以闭括号。这是一个不带显式
  输入数组的干净的约束剪枝例子。
- **棋盘上的约束满足（N 皇后、数独）。** 摆放一个单位（每行一个皇后、每个空格一个
  数字），对照约束检查它，递归，然后撤销。维护 O(1) 的约束集合（皇后的列、两条
  对角线），使得合法性检查是一次集合查找，而不是一次全盘扫描。
- **网格路径搜索（单词搜索）。** 从每个格子做 DFS，标记该格已访问，递归进入与下一个
  字符匹配的四个邻居，然后在返回时取消标记。这个「取消标记」就是应用在网格上的撤销
  步骤。
- **回文划分 / IP 地址复原。** 选择一个前缀切分，验证它，在后缀上递归。所做的选择是
  下一个分割点放在哪里。

## 经典题目

| # | 题目 | 难度 | 训练点 |
|---|---------|-----------|----------------|
| 78 | Subsets | 中等 | `start` 下标骨架；每个节点都是一个答案 |
| 46 | Permutations | 中等 | 用 `used` 数组而不是 `start`；顺序重要 |
| 39 | Combination Sum | 中等 | 无限重复使用（在 `i` 上递归）加上和的剪枝 |
| 40 | Combination Sum II | 中等 | 通过排序 + 跳过处理重复；每个元素只用一次 |
| 22 | Generate Parentheses | 中等 | 用开 / 闭计数器剪枝，无输入数组 |
| 79 | Word Search | 中等 | 在网格上做 DFS，带访问标记与取消标记 |
| 51 | N-Queens | 困难 | 列与对角线的约束集合；每行摆放一个 |
| 37 | Sudoku Solver | 困难 | 试数字 / 递归 / 撤销，成功即返回 |

## 陷阱

- **忘了在叶子处复制。** `res.append(path)` 存的是那个共享列表的引用，之后它会被弹到
  空。你必须用 `path[:]`（或 `list(path)`）做一次快照。
- **忘了撤销。** 跳过 `path.pop()` 或留着 `used[i] = True` 会把状态泄漏到兄弟分支，
  污染之后的每一个结果。每一次选择都需要在所有返回路径上有其配对的撤销。
- **`i` 对比 `i + 1` 弄混。** 在 `i` 上递归允许重复使用当前元素（完全背包形态）；
  `i + 1` 禁止重复使用。选错会悄无声息地改变问题。
- **重复跳过用在了错误的范围。** `if i > start` 跳过的是*同一层兄弟之间*的重复
  （正确）。`if i > 0` 还会跳过来自父节点路径上的那个元素，丢掉合法结果。排序是两者
  的前提。
- **约束问题上的剪枝太弱。** 为检查合法性而重新扫描整个棋盘，会把一个本就指数级的
  搜索变成会超时的东西。要维护增量式的 O(1) 约束结构。
- **只需一个解时不提前停止。** 数独和「是否存在一条路径」只需要第一个成功解，所以要
  沿栈向上返回一个布尔值并短路；枚举所有解是白费功夫。

## 后续问题与相关模式

- 「只是数一数安排的种数，而且 n 很大」会推向
  [DP](21-dp-linear-knapsack.md)：目标和与子集和计数就是同一棵决策树用记忆化坍缩
  而成，用一张表换掉了枚举。
- 「网格搜索重复了子问题」或「状态是一个已访问集合的位掩码」会推向
  [位掩码 DP](23-dp-grids-intervals.md)，那里一个指数级的状态集合被缓存，而不是被
  重新探索。
- 回溯就是在一棵隐式树上做 [DFS](12-tree-dfs.md)；递归的形态与树递归完全相同，只是
  多了一个显式的撤销。
- 网格回溯紧挨着 [图遍历](16-graph-traversal.md)；区别在于回溯会取消对格子的访问，
  好让其他路径能重复使用它们。
- 当一个贪心选择可被证明无需探索整棵树就能达到最优时，问题就坍缩为
  [贪心](25-greedy.md)。
