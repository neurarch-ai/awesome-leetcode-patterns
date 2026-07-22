# 精解：课程表 (LC 207)

> 中文版。English: [course-schedule](../../walkthroughs/course-schedule.md)

一个从头到尾在一道题上跑完六步框架的例题。目标是展示过程，而不只是答案。

## 题目

**LeetCode 207，中等。** 有 `numCourses` 门课程，标号从 `0` 到 `numCourses - 1`。给你 `prerequisites`，一个由若干对 `[a, b]` 组成的列表，表示你必须先修课程 `b` 才能修课程 `a`。如果你能修完所有课程返回 `True`，否则返回 `False`。

例子：`numCourses = 2`，`prerequisites = [[1, 0]]` 返回 `True`（先修 0，再修 1）。但 `numCourses = 2`，`prerequisites = [[1, 0], [0, 1]]` 返回 `False`，因为每门课都要求另一门。

![一个 DAG 的拓扑顺序](../../assets/topological-sort.svg)

*一个 DAG 的拓扑顺序。完整模式见下方链接的文件。*

## 1. 厘清与复述

我会问的问题：

- **这一对到底是什么意思？** `[a, b]` 表示 `b` 是 `a` 的先修课，所以依赖边指向 `b -> a`（「b 使 a 成为可能」）。把这个方向弄对是问题的一半；我会把它复述回去确认后再写代码。
- **我真正被问的是什么？** 是否存在任何有效的顺序来修完所有课程。当且仅当依赖图**没有环**时才存在有效顺序。如果课程互相成环依赖，就没有顺序能同时满足它们。所以我返回的布尔值是「这个有向图是无环的吗？」
- **输入类型。** `numCourses` 是一个正整数；`prerequisites` 是一个整数对列表，可能为空。即便没有边，节点也存在。
- **约束。** `numCourses` 到 `2000`，先修课到 `5000`。那是一个稀疏图，所以 O(V + E) 的遍历是目标，而 O(V + E) 在预算之内绰绰有余。
- **边界情况。** 完全没有先修课（平凡地 `True`）；一个**自环** `[0, 0]`（课程 0 要求它自己，一个即时的环，`False`）；一条没有环的长依赖链（`True`）；重复的边；不相连的分量（一些完全没有先修课的课程）。

复述：构建有向依赖图，当且仅当它没有环，也就是当一个完整的拓扑排序存在时，返回 `True`。

## 2. 手算一个例子

`numCourses = 4`，`prerequisites = [[1, 0], [2, 1], [3, 2]]`。把每一对读作 `b -> a`：`0 -> 1 -> 2 -> 3`。我会使用**入度**，也就是每门课仍有多少个未满足的先修课。

- 入度：课程 0 有 0，课程 1 有 1（需要 0），课程 2 有 1（需要 1），课程 3 有 1（需要 2）。
- 只有课程 0 入度为 0，所以它是我现在唯一能修的。修它。修 0 会移除它的出边 `0 -> 1`，把课程 1 的入度降到 0。
- 现在课程 1 可修了。修它，把课程 2 降到入度 0。
- 修课程 2，把课程 3 降到 0。
- 修课程 3。四门全修了。

我修了全部 4 门课，所以答案是 `True`。现在和成环的情形 `[[1, 0], [0, 1]]` 比较一下：入度都是 1，没有一门课从 0 起步，所以我永远无法开始。我修了 0 门课，少于 `numCourses`，所以答案是 `False`。那个落差（「我设法修完了每门课，还是卡住了？」）就是整个考察。

## 3. 暴力解

字面的解读是「存在环吗？」一个朴素的办法是从每个节点做深度优先搜索，追踪当前路径，如果我曾在当前路径上重访一个节点就报告有环。

```python
def can_finish_brute(num_courses, prerequisites):
    adj = [[] for _ in range(num_courses)]
    for a, b in prerequisites:
        adj[b].append(a)

    def has_cycle_from(node, visiting, path):
        path.add(node)
        for nxt in adj[node]:
            if nxt in path:            # back edge onto the current path
                return True
            if nxt not in visiting and has_cycle_from(nxt, visiting, path):
                return True
        path.discard(node)
        visiting.add(node)             # fully explored, no cycle through here
        return False

    visiting = set()
    for course in range(num_courses):
        if course not in visiting:
            if has_cycle_from(course, visiting, set()):
                return False
    return True
```

小心地配上一个「已完全完成」集合，这实际上是 O(V + E)。做得马虎（重新探索节点、传入全新的路径集合却不记忆化已完成的节点）则会严重退化，并且在「在当前路径上」与「之前见过」的区分上很容易出微妙的错。那种脆弱正是伸手去抓一个更干净、更难搞砸的表述的动机。

## 4. 找到瓶颈并挑选模式

真正的瓶颈不是速度，而是正确性和清晰度：递归的环检测必须区分「节点在当前 DFS 路径上」（一个真正的环）和「节点在某条其他路径上已被完全探索」（没问题），把这两者混淆是经典的 bug。我想要一个让环检查自然浮现出来的表述。

那就是**用 Kahn 算法做拓扑排序**。这个想法直接映射到我手算的方式：反复取任何**入度为 0**的课程（没有未满足的先修课），然后把它所解锁的一切的入度减一。一个队列持有当前可修的课程。如果我设法修完了全部 `numCourses` 门，一个完整的拓扑顺序存在、图是无环的。如果队列提前排空（因为每门剩下的课程仍有一个未满足的先修课），剩下的课程构成一个环，我返回 `False`。

环检测变成一次简单的计数：把修过的课程数和 `numCourses` 比较。不需要路径追踪集合，不需要推理递归深度。Kahn 算法把「检测一个环」变成「我能不能一次一个零入度节点地把图抽干」，那要难搞砸得多。

## 5. 写出代码

```python
from collections import deque

def can_finish(num_courses, prerequisites):
    indeg = [0] * num_courses          # unmet prerequisites per course
    adj = [[] for _ in range(num_courses)]
    for course, pre in prerequisites:  # pair is [course, prerequisite]
        adj[pre].append(course)        # edge pre -> course
        indeg[course] += 1

    queue = deque(c for c in range(num_courses) if indeg[c] == 0)
    taken = 0
    while queue:
        node = queue.popleft()
        taken += 1                     # this course is now takeable, take it
        for nxt in adj[node]:
            indeg[nxt] -= 1            # one prerequisite satisfied
            if indeg[nxt] == 0:
                queue.append(nxt)      # newly unblocked, ready to take
    return taken == num_courses        # took everything iff acyclic
```

我用每一门起步时没有先修课的课程给队列播种。每次我弹出一门课就把它计数，并松弛它的出边，任何最后一个先修课刚刚清除的邻居就加入队列。循环不变式：`indeg[c]` 始终等于 `c` 尚未被修的先修课数量，而队列恰好持有那些先修课全部满足、但尚未被修的课程。如果存在一个环，环里的课程永远无法达到入度 0（每一个都被环里的另一个阻塞），所以它们永远不进队列，`taken` 就会不够。

## 6. 测试、追踪与分析

追踪 `numCourses = 2`，`prerequisites = [[1, 0]]`。边 `0 -> 1`，入度 `[0, 1]`。

| 队列（队首..队尾） | 弹出 | taken | 松弛的边 | 之后的队列 |
|---------------------|-----|-------|---------------|-------------|
| [0] | 0 | 1 | 1 的入度 1 -> 0，入队 1 | [1] |
| [1] | 1 | 2 | 无 | [] |

队列空，`taken = 2 == numCourses`，返回 `True`。正确。

现在是成环的情形 `numCourses = 2`，`prerequisites = [[1, 0], [0, 1]]`。边 `0 -> 1` 和 `1 -> 0`，入度 `[1, 1]`。初始队列为空，因为没有课程入度为 0，所以循环从不执行，`taken = 0`，而 `0 != 2` 返回 `False`。正确。

边界情况：
- **没有先修课**，`numCourses = 3`，`prerequisites = []`：三个入度都是 0，三门都进队列，都被修，`taken = 3`，返回 `True`。没有边的不相连节点被免费处理了。
- **自环**，`numCourses = 1`，`prerequisites = [[0, 0]]`：边是 `0 -> 0`，所以课程 0 入度为 1、永远到不了 0。队列一开始就空，`taken = 0 != 1`，返回 `False`。正确，一门课不能是它自己的先修课。
- **三元环**，`numCourses = 3`，`prerequisites = [[0, 1], [1, 2], [2, 0]]`：每个入度都是 1，队列一开始就空，返回 `False`。正确。

**复杂度：O(V + E) 时间**，其中 `V = numCourses` 而 `E = len(prerequisites)`：构建图触碰每条边一次，Kahn 循环访问每个节点一次、松弛时访问每条边一次。**O(V + E) 空间**用于邻接表和入度数组加上队列。这轻松通过 2000 节点、5000 边的上限。

时间更充裕的话，我会提一下后续 LC 210「课程表 II」，它要求给出一个实际的有效顺序而不只是一个是/否。它是同一个 Kahn 循环，只是我把每个弹出的节点追加到一个结果列表并返回那个列表（如果检测到环则返回空列表），所以这篇精解离那道题只差一行。

## 面试官真正考察的是什么

你能否把一个文字问题（「我能修完所有课程吗？」）翻译成正确的图抽象：一个有向图，问题其实是「这无环吗？」第一跃是把先修课建模成有向边并把方向弄对；第二跃是认得出「修完所有课程」等于「存在一个拓扑顺序」等于「没有环」。用入度的 Kahn 算法是测试这一点的干净方式，而一个候选人是否理解它的信号，就是最后那个 `taken == numCourses` 检查，它悄无声息地完成了环检测，不需要任何显式的找环代码。

> 模式：[17 拓扑排序](../patterns/17-topological-sort.md)
