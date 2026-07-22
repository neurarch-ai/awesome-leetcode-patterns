# 17 - 拓扑排序

> 中文版。English: [17-topological-sort](../../patterns/17-topological-sort.md)

> **题目形态:**「给定这些先决条件,你能修完所有课程吗?」「返回一个修课的合法顺序。」「给定一份有序的外星单词列表,还原它们的字母表。」凡是给你一组条目外加「X 必须排在 Y 之前」的约束,并要求一个合法的线性顺序、或者只问是否存在这样一个顺序的,都属于这一类。

拓扑排序为一个有向无环图(DAG)产出一个线性排序,使得每条边 `u -> v` 都指向前方:`u` 出现在 `v` 之前。它存在当且仅当图中没有环,所以拓扑排序兼作有向图的环检测。两种算法可以计算它:Kahn 算法(在入度上做 BFS)和带后序的 DFS,两者都会让你能挑读起来更顺的那个来用。

![有向无环图,边为 A 到 B、A 到 C、B 到 D、C 到 D](../../assets/topological-sort.svg)

*一个先决条件 DAG:A 解锁 B 和 C,而两者都必须在 D 之前完成。合法顺序包括 A, B, C, D 和 A, C, B, D。*

## 识别信号

看到以下情况就该想到拓扑排序:

- **依赖或排序约束:**「先决条件」、「必须先构建」、「X 依赖 Y」、「编译顺序」、「带依赖的任务调度」。
- **对带优先级规则的条目请求一个合法顺序**,或者只问一个一致的顺序是否可能存在(这和「有没有环」是一回事)。
- **一个必须检测环的有向图。** Kahn 算法免费报告环:如果你无法输出所有节点,就是环挡住了它们。
- **从成对证据里还原未知顺序:**外星字典,其中相邻单词各揭示一条优先关系,然后你对字母做拓扑排序。

标志是条目之间的优先关系,而不是距离或连通性。如果边是无向的,或者你想要最短跳数,这就不是这个模式。拓扑排序只在**有向**图上有意义,而且只在**无环**图上才产出顺序。

## 核心思想

两种算法都利用同一个事实:在 DAG 里,至少有一个节点没有入边(没有东西依赖它),你可以安全地把它放在最前面。

- **Kahn 算法(BFS)。** 计算每个节点的入度。用所有入度为 0 的节点开一个队列。反复弹出一个,把它追加到顺序里,并把它每个邻居的入度减一;每当某个邻居的入度降到 0,它就没有未满足的依赖了,于是入队。如果你输出的节点少于 `V` 个,剩下的都困在一个环里。O(V + E)。
- **带后序的 DFS。** 跑 DFS;一个节点只有在它的所有后代都完成后才算完成,所以按后序追加节点并反转,就得到一个合法的拓扑序。要捕捉环,你需要每个节点三种状态(未访问、在当前递归栈中、彻底完成):重访一个仍在栈上的节点意味着一条回边,也就是一个环。

对于「是否存在一个顺序」,Kahn 算法通常更容易推理,因为环检测只是一个计数。当你本来就因别的原因在做 DFS 时,DFS 版本更自然。

## 模板

**Kahn 算法(在入度上做 BFS),返回一个顺序,若存在环则返回 `[]`:**

```python
from collections import deque

# Time: O(V + E), Space: O(V + E)
def topo_sort_kahn(num_nodes, edges):        # edges: list of (u, v) meaning u -> v
    adj = [[] for _ in range(num_nodes)]
    indeg = [0] * num_nodes
    for u, v in edges:
        adj[u].append(v)
        indeg[v] += 1

    q = deque(n for n in range(num_nodes) if indeg[n] == 0)
    order = []
    while q:
        node = q.popleft()
        order.append(node)
        for nxt in adj[node]:
            indeg[nxt] -= 1                   # one dependency satisfied
            if indeg[nxt] == 0:              # all deps met, ready to place
                q.append(nxt)

    return order if len(order) == num_nodes else []   # [] means a cycle blocked some node
```

**带三色环检测和后序的 DFS:**

```python
# Time: O(V + E), Space: O(V)
def topo_sort_dfs(num_nodes, adj):
    WHITE, GRAY, BLACK = 0, 1, 2             # unseen, on stack, done
    color = [WHITE] * num_nodes
    order = []
    ok = True

    def dfs(u):
        nonlocal ok
        color[u] = GRAY
        for v in adj[u]:
            if color[v] == GRAY:            # back edge to a node on the stack: cycle
                ok = False
            elif color[v] == WHITE:
                dfs(v)
        color[u] = BLACK
        order.append(u)                      # post-order: children finished first

    for n in range(num_nodes):
        if color[n] == WHITE:
            dfs(n)
    return order[::-1] if ok else []         # reverse post-order is the topo order
```

GRAY 状态是 DFS 环检测的全部诀窍:一个朴素的已访问标志无法区分「已经在另一条分支上彻底处理完」(没问题)和「在当前路径上仍然打开着」(一个环)。

## 变体

- **课程表 I(只判可行性)。** 你只需要「是否存在一个合法顺序」,所以跑 Kahn 并返回 `len(order) == num_courses`。不需要保留顺序。
- **课程表 II(返回顺序)。** 同样地跑,返回 `order` 列表,或者存在环时返回 `[]`。
- **字典序最小的拓扑序。** 用一个最小堆代替队列,这样你总是产出可用的、入度为 0 的最小节点。O((V + E) log V)。
- **外星字典。** 先*构建*图:比较每一对相邻单词,找到第一个不同的字符,这产出一条边(较前的字母 -> 较后的字母)。留意较长单词是较前单词前缀的非法情形(「abc」在「ab」之前),它没有合法顺序。然后对字母做拓扑排序。
- **统计不同拓扑序的数量**,或检测一个*唯一*顺序(队列在任何时刻都不超过一个节点)。对「顺序是否被完全确定」很有用。

## 经典题目

| # | 题目 | 难度 | 训练点 |
|---|---------|-----------|----------------|
| 207 | Course Schedule | 中等 | 通过 Kahn 计数做环检测 |
| 210 | Course Schedule II | 中等 | 产出一个合法拓扑序 |
| 269 | Alien Dictionary | 困难 | 从证据构建图,再排序 |
| 802 | Find Eventual Safe States | 中等 | 反图拓扑 / DFS 着色 |
| 310 | Minimum Height Trees | 中等 | 逐层剥叶(Kahn 风格) |
| 444 | Sequence Reconstruction | 中等 | 唯一拓扑序检查 |
| 1136 | Parallel Courses | 中等 | 拓扑层数 = 最少学期数 |
| 630 | Course Schedule III | 困难 | 贪心加堆(对照:并非纯拓扑) |

## 常见坑

- **在 Kahn 里错误地报告环。** 信号是 `len(order) < num_nodes`,而不是运行途中队列空了。在结尾把输出计数和节点数比较。
- **用朴素已访问标志做 DFS 环检测。** 你需要三态颜色。两态的已访问会把已完成节点和在栈上的节点标成一样,从而漏掉回边(或误报交叉边)。
- **忘了反转 DFS 后序。** 后序先追加依赖;拓扑序是它的反转。跳过反转会给出恰好相反的方向。
- **外星字典前缀陷阱。** 如果单词 A 排在单词 B 之前、A 是 B 的前缀、且 A 更长(像「abc」然后「ab」),输入是非法的:返回 ""。在你去找不同字符之前先处理这一点。
- **没有把每个入度为 0 的节点都播种进去。** 所有的根都必须进入初始队列,而不只是节点 0。一个不连通的 DAG 有好几个起点。
- **节点数算错。** 有 `k` 个字母或 `n` 门课时,把你的入度和邻接结构按完整节点集来定尺寸,包括那些不出现在任何边里、但仍需被产出的孤立节点。

## 延伸与相关模式

- 「只要检测环,我不需要顺序」是同一套机制,见这里的有向环检测,以及 [并查集](18-union-find.md) 里的无向版本。
- 「依赖形成层次,我想要最少轮数」是 Kahn 每次处理一整层,是 [树的 BFS](13-tree-bfs.md) 层序的表亲。
- 「现在边有权重了,我想要 DAG 里的最长 / 最短路径」把拓扑序和一趟松弛结合起来,与 [最短路](19-shortest-path.md) 和 [线性 DP](21-dp-linear-knapsack.md) 相关。
- 排序之前先构建图(外星字典)复用了 [图遍历](16-graph-traversal.md) 里表示边的直觉。
