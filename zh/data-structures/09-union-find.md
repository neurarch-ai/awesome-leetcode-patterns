# 09 - 并查集（不相交集合）

> 中文版。English: [09-union-find](../../data-structures/09-union-find.md)

并查集能快速回答一个问题：「这两个东西是否属于同一组，如果不是，就把它们所在的组合并。」它维护一组把元素划分到若干不相交集合中的分区，并且恰好支持两种操作：`find`（x 在哪个集合里）和 `union`（合并两个集合）。配合两项标准优化，它能在接近常数的摊还时间内完成这两种操作，因此它是处理随边到来而增长的连通性、统计连通分量数量、以及检测无向图中环的合适工具。

![一个由两棵树及其根节点构成的不相交集合森林](../../assets/union-find.svg)

*一个不相交集合森林：find 沿父指针爬到根节点；当且仅当两个节点共享同一个根时它们才连通。*

## 它是什么

这个结构是一片**由树构成的森林**，每个集合对应一棵树，其中每个元素指向一个父节点，而一棵树的根节点是该集合的代表（它的「名字」）。当且仅当两个元素向上爬到同一个根时，它们才属于同一个集合。初始时每个元素都是自己的父节点，因此有 n 个单元素集合。

`find(x)` 沿父指针向上走到根。`union(x, y)` 找到两个根，并把其中一个指向另一个，从而把两棵树合并成一棵。这就是全部的思路。微妙之处，也是并查集之所以出名的原因，在于朴素版本会退化成很长的链，使得 `find` 变成 O(n)。下面这两项优化让树保持扁平。

- **路径压缩**（在 `find` 中）：找到根之后，把路径上的每个节点直接重新指向根，这样下一次 `find` 就是 O(1)。每次 `find` 都会把它走过的路径压平。
- **按秩或按大小合并**（在 `union` 中）：始终把较小或较矮的树挂到较大或较高的树下面，这样树就不会不必要地变深。

## 操作与复杂度

n 是元素的数量。α(n) 是反阿克曼函数，对于任何你会遇到的 n 它都至多为 4，所以「O(α(n))」在所有实用意义上都是「常数」。

| 操作 | 复杂度 | 说明 |
|---|---|---|
| `find(x)` | O(α(n)) 摊还 | 配合路径压缩接近常数 |
| `union(x, y)` | O(α(n)) 摊还 | 两次 find 加一次指针重指向 |
| `connected(x, y)` | O(α(n)) 摊还 | 就是 `find(x) == find(y)` |
| 在 m 次操作上构建 | O(m · α(n)) | 实际上等于 O(m)，在实践中是线性的 |
| 空间 | O(n) | 两个数组：parent 和 size（或 rank） |

为什么这两项优化合在一起能给出接近 O(1) 的复杂度：**按大小合并**单独就能把树高界定在 O(log n)，因为一棵树只有在与一棵至少同样大的树合并时才会变高，所以它每变深一次大小就翻倍。**路径压缩**单独也有帮助，但两者结合能把摊还成本压到 O(α(n))，这是 Tarjan 的结果。任何一项优化单独使用都是 O(log n) 摊还；你两个都要用。底层的数组访问成本见[复杂度速查表](../complexity.md)。

## Python 实现

一个可复用的不相交集合类，带路径压缩和按大小合并。`union` 返回是否真的发生了合并，这正是环检测所依赖的。

```python
class DSU:
    def __init__(self, n):
        self.parent = list(range(n))   # each element is its own root
        self.size = [1] * n            # size of the tree rooted at i
        self.count = n                 # number of disjoint sets

    def find(self, x):
        # path compression: point every node on the path at the root
        root = x
        while self.parent[root] != root:
            root = self.parent[root]
        while self.parent[x] != root:
            self.parent[x], x = root, self.parent[x]
        return root

    def union(self, x, y):
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return False               # already together: no merge
        # union by size: hang the smaller tree under the larger
        if self.size[rx] < self.size[ry]:
            rx, ry = ry, rx
        self.parent[ry] = rx
        self.size[rx] += self.size[ry]
        self.count -= 1
        return True

    def connected(self, x, y):
        return self.find(x) == self.find(y)
```

**统计连通分量**是免费的：从 `count = n` 开始，每次成功的 `union` 就减一。处理完所有边之后，`dsu.count` 就是分量的数量。

```python
def count_components(n, edges):
    dsu = DSU(n)
    for u, v in edges:
        dsu.union(u, v)
    return dsu.count
```

**无向图中的环检测**从同一个返回值中自然得出：如果 `union` 报告两个端点已经连通，那么这条边就闭合了一个环。

```python
def has_cycle(n, edges):
    dsu = DSU(n)
    for u, v in edges:
        if not dsu.union(u, v):   # already in the same set -> cycle
            return True
    return False
```

## 何时使用它（以及何时不用）

在以下情况选择并查集：

- 你**增量地处理边**，并不断询问「它们现在是否连通」，尤其是当边只会被添加时（并查集不太能处理删除）。
- 你需要**统计连通分量**，或者把元素分组成等价类：省份数量、朋友圈、账户合并、冗余连接。
- 你想要**无向图中的环检测**，或者你正在用 Kruskal 算法构建最小生成树（对边排序，合并端点，跳过任何会闭合环的边）。

在以下情况跳过它：

- 图是**静态的，而你需要实际的路径或距离**。并查集告诉你两个节点*是否*连通，从不告诉你*如何*连通；要得到路径本身，请使用[图遍历](../patterns/16-graph-traversal.md)或[最短路径](../patterns/19-shortest-path.md)。
- 你必须**移除边**或拆分组。并查集只能合并；没有廉价的反合并操作。反转问题（把删除倒过来当作添加来处理）是通常的变通做法。
- 连通性是**有向的**，而你需要尊重方向的可达性。并查集把每条边都当作无向的；请改用 DFS 或强连通分量算法。

## 权衡与陷阱

- **两项优化都要，否则你就失去了保证。**只有路径压缩而没有按大小合并，或者反过来，都是 O(log n)，而不是 O(α(n))。两个都不用，最坏情况下每次 find 是 O(n)，也就是一条链。始终两个都带上。
- **比较前先 `find`。**`parent[x] == parent[y]` 是错的；两个节点可以属于同一集合却有不同的直接父节点。始终比较*根*：`find(x) == find(y)`。
- **先把非整数元素映射掉。**DSU 是用下标索引数组的，所以字符串或坐标元素在使用数组版本之前，需要一个从元素到整数 id 的字典（或者改用字典而不是列表来支撑 DSU）。
- **有向边会欺骗并查集。**合并 `u` 和 `v` 会抹掉方向。如果问题中的环或连通性取决于边的方向，那么并查集是错误的工具。
- **`find` 中的双重 while 循环就是压缩。**第一个循环找到根，第二个循环重指向路径。一行的递归 `find` 也能用，但在很深的链上有触及 Python 递归限制的风险；对于大的 n，迭代形式更安全。

## 相关模式

- [并查集](../patterns/18-union-find.md)是这个结构所驱动的模式：分量、环检测、Kruskal 最小生成树、动态连通性。
- [图遍历](../patterns/16-graph-traversal.md)是当图固定且你可以一趟 BFS 或 DFS 遍历它时，用于分量统计的替代方案。
- [拓扑排序](../patterns/17-topological-sort.md)处理并查集无法表达的连通性中那有向的、带次序的一面。
- [复杂度速查表](../complexity.md)列出了 DSU 数组所构建于其上的 `list` 和 `dict` 成本。
