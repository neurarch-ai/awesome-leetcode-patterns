# 10 - 有序容器（bisect 与 SortedList）

> 中文版。English: [10-sorted-container](../../data-structures/10-sorted-container.md)

有序容器始终把元素保持在有序状态，因此你可以在 O(log n) 内询问「x 应该放在哪里」、「有多少元素小于 x」或者「第 k 小的是什么」。Python 给了你这方面的两个层次：标准库 `bisect` 模块，它在一个已经有序的列表上做二分查找；以及 `sortedcontainers.SortedList`，一个第三方但面试允许使用的结构，它在插入和删除时以 O(log n) 保持自身有序。当你不需要[线段树](../patterns/29-segment-tree-fenwick.md)所提供的那种任意区间聚合时，这就是处理动态顺序统计和区间计数的工具。

![在 bisect 位置向有序数组插入](../../assets/sorted-container.svg)

*有序容器随着值的到来保持顺序：bisect 在 O(log n) 内找到槽位，SortedList 在 O(log n) 内插入到那里。*

## 它是什么

- **`bisect`** 在一个有序的 Python 列表上做二分查找。`bisect_left(a, x)` 返回 x 可以插入以保持 a 有序的最左下标；`bisect_right(a, x)` 返回最右的这样的下标。两者之间的差距就是等于 x 的元素个数。`insort` 在保持顺序的同时插入。
- **`SortedList`**（来自 `sortedcontainers` 包）是一个自动保持有序的列表。它支持 O(log n) 的 `add` 和 `remove`、O(log n) 的 `bisect_left` / `bisect_right`，以及 O(log n) 的索引（`sl[k]` 取第 k 小），其底层通过把元素存储在一个由小列表构成的列表中实现。

真正重要的区别：对于一个普通列表，二分**查找**是 O(log n)，但**插入**是 O(n)，因为列表必须移动元素。`SortedList` 让插入也变成 O(log n)，这正是它能驱动一个移动窗口的原因。

## 操作与复杂度

| 操作 | 复杂度 | 说明 |
|---|---|---|
| `bisect_left(a, x)`, `bisect_right(a, x)` | O(log n) | 在有序列表上二分查找 |
| `bisect.insort(a, x)` | O(n) | 查找是 O(log n)，但插入时的移动是 O(n) |
| `SortedList.add(x)` | O(log n) | 保持有序，没有 O(n) 的移动 |
| `SortedList.remove(x)` | O(log n) | |
| `sl[k]`（第 k 小） | O(log n) | 顺序统计 |
| `sl.bisect_left(x)`（小于 x 的计数） | O(log n) | 区间计数 |
| `x in sl` | O(log n) | |

要点：对于**静态**有序数组，`bisect` 就是你所需的全部。对于一个**变化的**集合，你边走边插入和删除，请使用 `SortedList`，这样每个操作都保持 O(log n)。

## Python 实现

```python
import bisect

# Static array: count how many elements fall in [lo, hi], inclusive.
def count_in_range(sorted_a, lo, hi):
    left = bisect.bisect_left(sorted_a, lo)
    right = bisect.bisect_right(sorted_a, hi)
    return right - left

# Dynamic collection: order statistics and range counts while inserting.
from sortedcontainers import SortedList

sl = SortedList()
sl.add(5)
sl.add(1)
sl.add(3)
# sl is now [1, 3, 5]
kth_smallest = sl[0]                 # 1, in O(log n)
below_4 = sl.bisect_left(4)          # 2 elements are < 4
sl.remove(3)                         # O(log n)
```

## 何时使用它（以及何时不用）

在以下情况使用有序容器：

- 你需要从一个不断变化的集合中取**第 k 小或第 k 大**（[堆](05-heap.md)只给你单个极值，而不是任意的排名）。
- 你需要随着元素的到来和离开做**区间计数**（「当前有多少个值落在 [lo, hi] 内」）：两次 `bisect` 调用。
- 你在计算**滑动窗口中位数**或窗口内的顺序统计：`SortedList` 支持添加、删除和索引访问，全部为 O(log n)。
- 你需要离 x **最近的值**（前驱或后继）：`bisect` 给出插入点，它周围的邻居就是候选。

在以下情况不要使用它：

- 你需要一个**任意区间聚合**，比如区间和，尤其是带更新的。那是[树状数组或线段树](../patterns/29-segment-tree-fenwick.md)。有序容器回答顺序和计数问题，而不是求和问题。
- 你只需要**单个最小值或最大值**：[堆](05-heap.md)更轻量。
- 数组是**静态的且只被查找**：在列表上用普通的 `bisect`，不需要 `SortedList`。

## 权衡与陷阱

- **`bisect.insort` 是 O(n)，而不是 O(log n)。**查找是对数的，但插入会移动尾部。通过反复 `insort` 来构建一个有序列表是 O(n^2)；如果你经常插入，请使用 `SortedList`。
- **`SortedList` 是第三方的。**`sortedcontainers` 不在标准库中，尽管它在 LeetCode 判题机上可用。在没有它、需要从零实现的场合，你退而使用 BIT 或平衡二叉搜索树的实现。
- **在 Python 3.10 之前，`bisect` 没有 `key` 参数。**在较旧的运行时上，你要对元组排序，或者装饰值以按自定义键排序。
- **重复元素。**有意识地使用 `bisect_left` 还是 `bisect_right`：它们的差恰好是 x 的重数，这往往正是你想要的计数。

## 相关模式

- [二分查找](../patterns/07-binary-search.md)：`bisect` 是打包好的二分查找；同样的下界 / 上界逻辑驱动着两者。
- [线段树与树状数组（BIT）](../patterns/29-segment-tree-fenwick.md)：当你需要区间**聚合**（求和、最小值）而不是顺序统计和计数时的替代方案。
- [堆（优先队列）](05-heap.md)：当你只需要单个最小或最大值、而不是任意排名时更轻量的选择。
- [滑动窗口](../patterns/02-sliding-window.md)：窗口中位数和窗口顺序统计用 `SortedList` 作为窗口的底层存储。
