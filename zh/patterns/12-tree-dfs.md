# 12 - 树的 DFS 与递归

> 中文版。English: [12-tree-dfs](../../patterns/12-tree-dfs.md)

> **问题形态：** 「求一棵二叉树的最大深度。」「计算直径。」
> 「有没有一条从根到叶的路径之和等于目标值？」「求两个节点的最近公共祖先。」
> 任何一个节点的答案是用它子树上的答案来定义、且一次递归行走就能收集它们的场景。

树的 DFS 是二叉树的主力模式：一个递归函数，每个节点访问一次，
在 O(n) 时间和 O(h) 栈空间内完成，其中 h 是高度。全部技巧是学会把一个问题表述为
「每个节点向它的父节点返回什么」，于是递归会自己写出来。

## 信号

当你看到以下情况时，考虑树的 DFS：

- **一棵二叉树和一个递归定义的量**：深度、高度、大小、和、平衡、「这是不是一个有效的 X」。
  节点上的值只取决于该节点加上它两个子节点的值。
- **从根到叶的路径**：路径和、所有路径、所有从根到叶数字之和。
  DFS 自然地把一条路径从根往下穿到每个叶。
- **「最近公共祖先」、「直径」、「最大路径和」**：答案位于某个内部节点，
  由每棵子树向上报告的东西组装而成。
- **结构变换**：反转树、拉平它、从遍历构建它。
  你递归，修好当前节点，让那些调用处理其余部分。

判断标志是你能把解法描述为一个基础情况（空节点或叶）
加上一条组合两个子结果的规则。如果能，DFS 就是这个模式。

## 思路

树上的 DFS 只是把两个子节点当作子问题的递归。基础情况几乎总是空节点（`None`），
它返回一个恒等值（高度和求和为 0，「全部满足」检查为 `True`）。
每个非空节点递归左、递归右，然后组合。

![带前序和中序遍历的二叉树](../../assets/tree-dfs.svg)

*前序（节点、左、右）：1, 2, 4, 5, 3, 6, 7。中序（左、节点、右）：4, 2, 5, 1, 6, 3, 7。后序（左、右、节点）：4, 5, 2, 6, 7, 3, 1。*

塑造一切的那个决定是**信息流的方向**：

- **自底向上（向上返回状态）。** 每次调用返回一个从其子节点计算出的聚合值：
  高度、子树和、「是否平衡」。这是「从子节点向上返回一个聚合」的模型，
  它覆盖大多数困难的树问题。你常常保留一个旁路变量（一个目前最优值），
  在返回时更新它，就像直径和最大路径和那样，你*返回*给父节点的值
  与你*记录*为答案的值不同。
- **自顶向下（向下传递状态）。** 你把累积的上下文作为参数带进递归：
  运行的路径和、当前深度、允许的值边界。叶节点用从根传下来的状态做出决定。

因为每个节点只被触碰一次，DFS 是 O(n) 时间。栈深度是树高 h，
平衡树是 O(log n)，退化树是 O(n)。

## 模板

**节点定义和核心的自底向上形态：**

```python
# Space: O(1)
class TreeNode:
    # Time: O(1)
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

# Time: O(n), Space: O(h)  (h = tree height, the recursion stack)
def max_depth(root):
    if not root:                       # base case: empty subtree has depth 0
        return 0
    left = max_depth(root.left)        # aggregate from children
    right = max_depth(root.right)
    return 1 + max(left, right)        # combine, return up to parent
```

**带旁路答案的自底向上（直径和最大路径和共享这个形态）：**

```python
# Time: O(n), Space: O(h)  (h = tree height, the recursion stack)
def diameter(root):
    best = 0
    def height(node):
        nonlocal best
        if not node:
            return 0
        lh = height(node.left)
        rh = height(node.right)
        best = max(best, lh + rh)      # record: path THROUGH this node
        return 1 + max(lh, rh)         # return: height, what the parent needs
    height(root)
    return best
```

**自顶向下（向下传递状态），从根到叶的路径和：**

```python
# Time: O(n), Space: O(h)  (h = tree height, the recursion stack)
def has_path_sum(root, target):
    if not root:
        return False
    remaining = target - root.val
    if not root.left and not root.right:   # at a leaf, check the accumulated sum
        return remaining == 0
    return has_path_sum(root.left, remaining) or has_path_sum(root.right, remaining)
```

思路上的分野：自底向上通过返回值返回答案；自顶向下把答案穿过参数传递并在叶节点做决定。

## 变体

- **三种遍历顺序。** 前序（节点、左、右）在处理子节点之前处理节点：
  用它来序列化一棵树或自顶向下复制它。中序（左、节点、右）以有序顺序访问一棵 BST：
  用它做验证和第 k 小（见 [BST](14-bst.md)）。后序（左、右、节点）在节点之前处理子节点：
  当节点需要先拿到两棵子树的结果时用它，这就是每一个自底向上的聚合
  （高度、和、删除、「是否平衡」）。
- **从遍历构建一棵树。** 前序给你根；在中序里找到它以切分左右子树；递归。
  同样的思路对后序加中序也有效（根是最后一个前序 / 最后一个后序元素）。
- **最近公共祖先（LCA）。** 后序搜索：如果一个节点或其某个后代是两个目标之一，
  它就返回非空。第一个看到两侧都返回非空的节点就是 LCA。O(n)，一趟，无需父指针。
- **最大路径和。** 像直径但是对值求和，且一棵子树只在它最好的向下和为正时才贡献
  （否则钳到 0）。向上返回最好的单臂和；记录穿过该节点的最好的双臂和。
- **路径枚举。** 下降时带一个列表，追加当前值，递归，然后在返回途中弹出（回溯）。
  这列出所有从根到叶的路径，或所有命中一个目标的路径。

## 经典题目

| # | 题目 | 难度 | 训练点 |
|---|---------|-----------|----------------|
| 104 | Maximum Depth of Binary Tree | 简单 | 基础的自底向上模板 |
| 226 | Invert Binary Tree | 简单 | 通过递归做结构变换 |
| 112 | Path Sum | 简单 | 自顶向下，向下传递运行总数 |
| 543 | Diameter of Binary Tree | 简单 | 返回高度，记录穿过的路径 |
| 110 | Balanced Binary Tree | 简单 | 带提前退出信号的自底向上高度 |
| 236 | Lowest Common Ancestor of a Binary Tree | 中等 | 后序「两侧都找到」 |
| 105 | Construct Binary Tree from Preorder and Inorder | 中等 | 从前序取根，在中序上切分 |
| 129 | Sum Root to Leaf Numbers | 中等 | 自顶向下累积的数字 |
| 124 | Binary Tree Maximum Path Sum | 困难 | 钳掉负数，记录双臂，返回单臂 |

## 陷阱

- **混淆返回的值与记录的值。** 在直径和最大路径和里，父节点需要最好的*单*臂，
  但答案是穿过该节点最好的*双臂*路径。返回一个、记录另一个，
  否则你会在偏斜的树上得到错误答案。
- **错误的基础情况。** 空子树对高度和求和返回 0，但单个叶子的深度是 1。
  这里的差一错误会破坏深度和路径问题。
- **路径枚举里忘记回溯。** 如果你追加到一个共享列表，且递归后不弹出，
  兄弟路径会继承彼此的节点。
- **最大路径和里的负值。** 一棵最好和为负的子树应贡献 0，而不是把总数往下拖。
  相加前先 `max(0, arm)`。
- **深而偏斜的树撑爆栈。** Python 的默认递归限制约为 1000。
  对对抗性的线性树，要么提高限制，要么转成显式栈。
- **叶子判定是「无左且无右」，而非「是 None」。** 只检查一个子节点
  会把有单个子节点的节点误分类为叶子。

## 后续追问与相关模式

- 「按层级而非按分支处理树」推向
  [树的 BFS](13-tree-bfs.md)，它用一个队列，是最短深度和逐层答案的天然选择。
- 「这棵树是二叉*搜索*树」让中序 DFS 能利用有序性做验证和第 k 小，
  在 [二叉搜索树](14-bst.md) 中讲述。
- 「它是一个一般图，不是树，且可能有环」推向
  [图遍历](16-graph-traversal.md)，那里你加一个已访问集合。
- 带一个共享、被修改的列表的路径枚举，恰好是
  [回溯](20-backtracking.md) 的「追加-递归-弹出」动作。
