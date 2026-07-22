# 05 - 堆（优先队列）

> 中文版。English: [05-heap](../../data-structures/05-heap.md)

当你反复需要最小（或最大）的元素、而对顺序别无所求时，堆就是你要拿起的结构。它给你 O(1) 查看极值，以及 O(log n) 移除极值或添加新元素，这正是"优先队列"的契约。令人意外的是它的实现：堆不是一团指针，它是一个你当作树来读的普通数组。理解那种数组即树的布局，正是让 O(log n) 和 O(n) 代价变得显而易见而非魔法的原因。

![作为二叉树的最小堆及其数组布局](../../assets/heap.svg)

*一个存为数组的最小堆：节点 i 的孩子在 2i+1 和 2i+2。*

## 是什么

二叉堆是一棵存在数组里的 **完全二叉树**。"完全"意味着除了可能的最后一层，每一层都是满的，而最后一层从左到右填充、没有空隙。正是这种无空隙让你能彻底丢掉指针：因为没有空洞，你可以把树一层一层地铺进一个连续数组，而父子关系就变成了索引算术。

对于索引为 `i` 的节点（0 起始）：

- 它的父节点在 `(i - 1) // 2`，
- 它的左孩子在 `2 * i + 1`，
- 它的右孩子在 `2 * i + 2`。

**堆不变量** 是一个局部性质：在最小堆中，每个父节点都 `<=` 它的两个孩子。它对兄弟之间的左右顺序什么都没说，对堂表节点也什么都没说。它唯一保证的是，整个堆中最小的元素坐在根部、索引 0，因为"没有孩子比父亲小"一路向上应用，把最小值汇聚到了顶端。这就是为什么查看是 O(1)：答案永远是 `a[0]`。最大堆是同样的东西，只是比较翻转（每个父节点 `>=` 它的孩子），把最大值放在根部。

堆是刻意 *弱* 有序的。它并不保持一切有序；它只保持刚好够用的顺序，以廉价地浮现出一个极值。这种弱正是全部效率的来龙去脉：只维护父子关系远比维护全序便宜。

## 操作与复杂度

对于一个有 n 个元素的堆：

| 操作 | 复杂度 | 说明 |
|---|---|---|
| 查看最小 / 最大（根） | O(1) | 它永远是 `a[0]`；不要为了查看而弹出 |
| Push（插入） | O(log n) | 追加到末尾，然后沿一条路径上浮 |
| Pop（取出最小 / 最大） | O(log n) | 把根和末尾交换、移除，然后沿一条路径下沉 |
| Push 后 Pop / 替换 | O(log n) | 只做一次下沉而非两次；比 push + pop 便宜 |
| Heapify（从 n 个元素建堆） | O(n) | 不是 O(n log n)；见下文 |
| 查找任意值 | O(n) | 没有顺序可利用；堆只知道它的根 |
| 删除任意节点 | O(n) 查找 + O(log n) 修复 | 堆不擅长这个；BST 或哈希索引堆更好 |

push 和 pop 上的 O(log n) 就是树的高度。一棵有 n 个节点的完全二叉树高度为 `floor(log2 n)`，两个操作都通过走一条根到叶（或叶到根）的路径来恢复不变量，每层一次交换。这些数字连同 `heapq` 一起见 [复杂度速查表](../complexity.md)。

### 为什么 push 和 pop 是 O(log n)

**Push** 把新元素追加到第一个空闲槽位（数组末尾，保持树完全），然后 **上浮**：把它和父节点比较，若违反不变量就交换，向上重复。它至多爬树的高度，所以是 O(log n)。

**Pop** 不能直接删除根，那会留下一个空洞。它转而把最后一个元素移到根槽位（保持完全性），然后 **下沉**：把根和它较小的孩子比较、交换，向下重复，直到不变量成立。同样至多树的高度，O(log n)。

### 为什么 heapify 是 O(n)，而不是 O(n log n)

建堆的朴素方式是做 n 次 push，那是 O(n log n)。但 `heapify` 做了更聪明的事：它原封不动地取整个数组，从最后一个父节点开始向根方向，对每个非叶节点做 *下沉*。关键洞察是，下沉代价被一个节点的 *高度* 所界定，而不是树的高度，而大多数节点都在底部附近、那里高度很小。一半节点是叶子（高度 0，零工作量），四分之一在高度 1，八分之一在高度 2，以此类推。把"高度为 h 的节点数乘以 h"求和，得到一个收敛到常数的级数 `n * sum(h / 2^h)`，所以总量是 O(n)。根附近那少数昂贵的节点稀少到无关紧要。这就是为什么你总是对现有数组做 `heapify`，而不是一个个元素地 push。

## Python 实现

Python 的 `heapq` 是 **只有最小堆**，并且它就地操作一个普通 list，而不是把它包在一个类里：

```python
import heapq

a = [5, 3, 8, 1, 9, 2]
heapq.heapify(a)          # O(n), rearranges the list into a min-heap in place

heapq.heappush(a, 0)      # O(log n)
smallest = a[0]           # O(1) peek, do not pop just to look
smallest = heapq.heappop(a)   # O(log n), returns and removes the minimum

# One combined sift, cheaper than a separate push then pop:
heapq.heappushpop(a, 4)   # push 4, then pop and return the smallest
heapq.heapreplace(a, 4)   # pop the smallest first, then push 4
```

**通过取负实现最大堆。** 既然只有最小堆，就把值取负（对数字而言），让最大的变成最小的：

```python
nums = [5, 3, 8, 1]
max_heap = [-x for x in nums]
heapq.heapify(max_heap)
largest = -heapq.heappop(max_heap)   # remember to negate back on the way out
```

**元组做平局裁决。** 要按优先级排序同时携带一个载荷，就压入 `(priority, item)` 元组。Python 按字典序比较元组，所以它用第一个元素、平局时退回到下一个。陷阱在于：如果两个优先级打平，Python 接着会比较载荷，而如果它们不可排序（两个 dict、两个自定义对象），就会抛出 `TypeError`。插入一个唯一、单调递增的计数器作为平局裁决字段，以保证比较永远不会触及载荷：

```python
import itertools
counter = itertools.count()
pq = []
heapq.heappush(pq, (priority, next(counter), task))   # (priority, seq, payload)
```

用有界堆求 Top-k，即 `nlargest`/`nsmallest` 背后的模式：保留一个大小为 k 的最小堆，装着目前所见最大的 k 个，复杂度 O(n log k)：

```python
def k_largest(nums, k):
    h = nums[:k]
    heapq.heapify(h)                 # O(k)
    for x in nums[k:]:
        if x > h[0]:                 # only if it beats the current k-th largest
            heapq.heapreplace(h, x)  # O(log k)
    return h                         # the k largest, unordered
```

## 何时用（何时不用）

**在以下情况用堆：**

- 你反复取出最小或最大并重新插入，且你不需要完整的有序顺序。Dijkstra、Prim、"合并 k 个有序链表"和事件模拟都是这个。
- 你想要一个大或流式输入的 **top k**（或第 k 个）而不排序全部。一个大小为 k 的堆给你 O(n log k)，胜过 O(n log n) 的排序，且只需 O(k) 空间，而且它在你无法排序的流上也能工作。
- 优先级会变，而你不断取出当前最优：一个调度器、一个 A* 边界、一个"下一个任务"队列。

**在以下情况不要用堆：**

- 你需要一次性拿到全部有序顺序。直接 `sorted()`，O(n log n)；从堆上做 n 次 pop 是同样的渐进代价，只是常数更差。
- 你需要经常查找、删除或更新一个任意（非根）元素。堆没有顺序可查找，所以那是 O(n)。用平衡 BST 或哈希索引堆。
- 你只需要单个最小或最大一次。一趟 O(n) 的 `min()`/`max()` 胜过建一个堆。

## 权衡与陷阱

**堆不是有序的。** 打印底层 list 显示的是堆序，不是排序序。只有根被保证是极值；其余一切都是部分有序的。如果你需要有序输出，就反复 pop 或调用 `sorted()`。

**要查看，别为了看而弹出。** `a[0]` 是 O(1)。为了检查最小值而弹出再压回是 O(log n)，是常见的意外拖慢。

**用 heapify，别循环 push。** 用 `heapify` 从现有数组建堆是 O(n)；n 次单独的 `heappush` 调用是 O(n log n)。永远优先 `heapify`。

**取负也会翻转平局顺序。** 当你为元组的最大堆取负时，记住平局裁决字段也被一起取负了，这可能反转你意图的次级排序。设计元组时要把这一点考虑进去。

**不可排序的载荷会在平局时崩溃。** 如上，当两个优先级打平且载荷不可比较时，`(priority, payload)` 会抛出 `TypeError`。永远在优先级和载荷之间加一个唯一的序号计数器。

### 堆 vs BST

两者都给你有序访问，但它们优化的东西不同。堆给你对 *一个* 极值的 O(1) 查看和 O(log n) 的 push/pop，但它无法回答"第 k 小是什么"、"廉价地把一切按序给我"，或"找到并删除这个任意值"（都是 O(n)）。平衡 BST 给你对 *任意* 元素的 O(log n) 查找、插入、删除、前驱和后继，而且 O(n) 的中序遍历产出完全有序的输出，但它的单个最小值查找是 O(log n)（一路向左走），不是 O(1)。经验法则：如果你只想要最小或最大，用堆，它更简单、常数更好。如果你需要在保持有序的同时查询或变更任意元素，用平衡 BST。

## 相关模式

- [堆 / 优先队列模式](../patterns/24-heap.md)：那些高喊着"用堆"的问题形态，包括"合并 k 个链表"和 Dijkstra。
- [Top-k 与快速选择](../patterns/09-top-k-quickselect.md)：大小为 k 的堆是两个标准 top-k 工具之一；快速选择是另一个。
- [树与二叉搜索树](06-tree-bst.md)：BST 就是上面对比过的"对每个元素都有序"的替代方案。
- [复杂度速查表](../complexity.md)：`heapq` 的代价表，包括 heapify O(n) 和 push/pop O(log n)。
