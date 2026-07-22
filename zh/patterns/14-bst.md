# 14 - 二叉搜索树

> 中文版。English: [14-bst](../../patterns/14-bst.md)

> **题目形态:**「验证这棵二叉树是不是 BST。」「找第 k 小的元素。」「搜索、插入或删除一个值。」「找两个和为目标值的节点。」「哪些值落在区间 [low, high] 里?」凡是在二叉树上、靠某个有序不变量让你每一步都能砍掉半棵树的,都属于这一类。

二叉搜索树把有序信息编码进了它的形状里:对每个节点,左子树的所有键都更小,右子树的所有键都更大。这一个不变量带来了 O(h) 的搜索、插入和删除,并让中序遍历按有序顺序吐出键,这正是大多数 BST 问题的主干。

## 识别信号

在以下情况使用 BST 专属推理:

- **题目说明这棵树是 BST**(或要你验证一棵)。有序性是一个工具:当不变量允许你选一边时,永远不要遍历整棵树。
- **「第 k 小 / 第 k 大」、「有序顺序」、「中序后继」**:这些都是中序遍历问题,因为 BST 上的中序就是一次有序扫描。
- **「搜索 / 插入 / 删除一个值」、「最接近的值」、「floor / ceiling」**:你沿一条根到叶的路径走,靠比较向左或向右分支,复杂度 O(h)。
- **「区间 [low, high] 内的所有键」**:剪掉不可能包含区间内键的整棵子树,这样你只碰到相关的那一带。
- **「BST 的最近公共祖先」**:两个目标分岔的那个分裂点(一个往左、一个往右)就是 LCA,在 O(h) 内找到,无需完整 DFS。

如果这棵树*不是* BST,以上都不适用,你要退回到通用的 [树的 DFS](12-tree-dfs.md) 或 [树的 BFS](13-tree-bfs.md)。

## 核心思想

BST 不变量是递归的:它必须在*每个*节点成立,而不只是局部成立。

![以 8 为根的二叉搜索树](../../assets/bst.svg)

*对每个节点,左子树 < 节点 < 右子树。根 8:左侧的键(3, 1, 6)都小于 8,右侧的键(10, 14)都大于 8。中序遍历得到有序顺序:1, 3, 6, 8, 10, 14。*

一个直接孩子满足 `left < node < right` 的节点,如果它某个很深的左侧后代超过了它,仍然可能违反不变量。这就是为什么验证要用**递归边界**:每个节点都必须严格落在一个开区间 `(low, high)` 内,这个区间随着你往下走而收紧。往左走把上界降到当前值,往右走把下界升到当前值。

第二根支柱是**中序遍历产出有序顺序**。先访问左、再访问节点、再访问右,值就会升序出来。这把「第 k 小」变成「在第 k 个产出的值处停下」,把「验证 BST」变成「检查这个序列严格递增」,把「BST 里的两数之和」变成对有序流做双指针。

搜索、插入和删除都沿一条由比较引导的单一路径走,所以代价是 O(h):平衡树上 O(log n),退化(链表形状)的树上 O(n)。

## 模板

**用递归边界验证 BST(正确且对深层安全的写法):**

```python
# Space: O(1)
class TreeNode:
    # Time: O(1)
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

# Time: O(n), Space: O(h), worst O(n)
def is_valid_bst(root, low=float('-inf'), high=float('inf')):
    if not root:
        return True                              # empty subtree is valid
    if not (low < root.val < high):              # must fit the open interval
        return False
    return (is_valid_bst(root.left, low, root.val) and
            is_valid_bst(root.right, root.val, high))
```

**用中序找第 k 小,提前停下:**

```python
# Time: O(h + k), worst O(n), Space: O(h), worst O(n)
def kth_smallest(root, k):
    stack = []
    node = root
    while stack or node:
        while node:                # go as far left as possible
            stack.append(node)
            node = node.left
        node = stack.pop()         # smallest unvisited
        k -= 1
        if k == 0:
            return node.val
        node = node.right          # then the right subtree
```

**搜索与插入(单路径行走):**

```python
# Time: O(h), worst O(n), Space: O(1)
def search_bst(root, target):
    while root and root.val != target:
        root = root.left if target < root.val else root.right
    return root

# Time: O(h), worst O(n), Space: O(h), worst O(n)
def insert_bst(root, val):
    if not root:
        return TreeNode(val)                     # found the empty slot
    if val < root.val:
        root.left = insert_bst(root.left, val)
    else:
        root.right = insert_bst(root.right, val)
    return root
```

**删除(三种情况的节点加后继替换):**

```python
# Time: O(h), worst O(n), Space: O(h), worst O(n)
def delete_bst(root, key):
    if not root:
        return None
    if key < root.val:
        root.left = delete_bst(root.left, key)
    elif key > root.val:
        root.right = delete_bst(root.right, key)
    else:                                        # found the node to remove
        if not root.left:                        # 0 or 1 child: splice up
            return root.right
        if not root.right:
            return root.left
        succ = root.right                        # 2 children: inorder successor
        while succ.left:
            succ = succ.left
        root.val = succ.val                      # copy successor value in
        root.right = delete_bst(root.right, succ.val)  # delete successor
    return root
```

## 变体

- **区间求和 / 区间取键。** 做 DFS 但剪枝:如果 `node.val < low`,跳过整棵左子树;如果 `node.val > high`,跳过右子树。只下探可能包含区间内键的子树。
- **BST 里的两数之和。** 跑中序得到有序数组,然后双指针。或者为了省空间,直接在树上用一个中序迭代器和一个逆中序迭代器充当两个指针。
- **最接近的值 / floor / ceiling。** 单路径行走,一边分支一边更新最优候选;答案总在从根到插入点的那条路径上。
- **BST 的 LCA。** 从根出发:当两个目标都小于当前节点就往左,都大于就往右;第一个把它们分开(或等于其中之一)的节点就是 LCA。O(h),不递归进两侧。
- **由有序数组构建平衡 BST。** 取中间元素作为根,对两半递归。保证 O(log n) 高度。这是「中序给出有序顺序」的逆过程。
- **中序后继 / 前驱。** 后继是右子树的最左节点,或者是使该节点位于其左子树中的最低祖先。

## 经典题目

| # | 题目 | 难度 | 训练点 |
|---|---------|-----------|----------------|
| 700 | Search in a Binary Search Tree | 简单 | 单路径比较行走 |
| 98 | Validate Binary Search Tree | 中等 | 递归开区间边界 |
| 230 | Kth Smallest Element in a BST | 中等 | 中序加提前停止 |
| 701 | Insert into a Binary Search Tree | 中等 | 递归到空槽位 |
| 450 | Delete Node in a BST | 中等 | 三种情况,后继替换 |
| 235 | Lowest Common Ancestor of a BST | 中等 | 靠比较找分裂点 |
| 653 | Two Sum IV - Input is a BST | 简单 | 中序转有序,再双指针 |
| 938 | Range Sum of BST | 简单 | 剪掉区间外的子树 |
| 108 | Convert Sorted Array to Binary Search Tree | 简单 | 中间作根以求平衡 |

## 常见坑

- **只做局部比较来验证。** 每个节点检查 `left.val < node.val < right.val` 是错的:一个很深的左侧节点可能超过某个高处的祖先。你必须把 min/max 边界一路带进递归。
- **有重复值时用了非严格边界。** 标准 BST 验证是严格的(`low < val < high`)。如果题目允许重复,先决定它们放在哪一侧,并一致地调整不等号。
- **在边界处误用 `float('inf')`。** 节点值可能是 `INT_MIN`/`INT_MAX`;用 `-inf`/`+inf`(或 `None` 哨兵)作为初始边界,这样真正的极端值仍能通过。
- **删除双孩子节点时写错。** 你必须用它的中序后继(或前驱)替换它,然后删除那个后继,而不是简单地摘掉一个孩子,否则会破坏有序性。
- **想当然地认为是 O(log n)。** 由有序插入构建的 BST 会退化成链表,使每个操作变成 O(n)。如果平衡很重要,自平衡树(AVL、红黑树)才是真正的答案,但面试很少要你手写一个。
- **忘了中序是升序、逆中序是降序。** 右、节点、左的顺序能免费给你第 k *大*。

## 延伸与相关模式

- 「现在这棵树不是 BST 了」把你打回通用的 [树的 DFS](12-tree-dfs.md) 做聚合、[树的 BFS](13-tree-bfs.md) 处理层结构。
- 「在大量插入和删除下保持平衡」指向自平衡树;实践中面试官会转向 [堆](24-heap.md) 或有序容器。
- 单路径比较行走就是把 [二分查找](07-binary-search.md) 实现成一种数据结构:每一步丢弃一棵子树,正如二分查找丢弃半个数组。
- 「大规模支持顺序统计查询(rank、select)」指向增强型 BST 或树状数组 / 线段树,和 [前缀和](03-prefix-sum.md) 里的区间结构相邻。
