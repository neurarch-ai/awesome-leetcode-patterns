# 05 - 区间与扫描线
> 中文版。English: [05-intervals](../../patterns/05-intervals.md)

> **问题形态：** 「合并所有重叠区间。」「把一个新区间插入到有序列表中。」「你需要多少间会议室？」「这个人能参加所有会议吗？」「射爆所有气球所需的最少箭数。」凡是关于在一条数轴上有起点和终点的范围，以及它们如何重叠、堆叠或排布的问题。

区间问题是关于数轴上的范围的，而它们几乎都屈服于同一招：按正确的键（通常是起点）排序，然后做一趟线性遍历，逐个决定合并与否。当问题是「同一时刻有多少个重叠」时，扫描线把每个区间重新表述为两个事件（起点处 +1，终点处 -1），扫描一个运行计数。排序把纠缠的范围变成一次可判定的从左到右的行走。

![时间轴上被合并的重叠区间](../../assets/intervals.svg)

*按起点排序，然后一趟遍历把重叠区间合并成互不相交的块。*

## 信号特征

看到以下情形时，考虑使用区间 / 扫描线模式：

- **一列 `[start, end]` 对**，以及一个关于重叠、合并、覆盖或排布的问题。
- **「合并」、「插入」、「是否有任何重叠」、「移除最少的以使它们互不相交」。** 这些都是「按起点（或按终点）排序」加一趟遍历。
- **「同一时刻有多少个处于活动状态」（最大并发数）。** 会议室、按座位数的拼车、某一年活着的最多人口。这是扫描线：沿轴移动时，用起点数减去终点数来计数。
- **「覆盖一切所需的最少点 / 箭 / 资源数」。** 一个贪心的「按终点排序」区间调度问题。
- **任何对象在某一个轴上有天然顺序**、且一旦按那个顺序观察其相互作用纯粹是局部的问题。

判断依据是：按一个端点排序后，每个区间只会与紧邻它之前的那个（用于合并）或与一个运行计数器（用于并发）发生交互，因此一趟遍历就够了。

## 核心思想

按起点对区间排序。此时重叠是局部的：如果当前区间的起点在正被合并区间的终点处或之前，它们就重叠，你把终点扩展到二者的最大值；否则中间有间隙，于是你关闭当前的合并块，再开一个新的。因为排序保证你绝不会在后面才看到一个起点更早的区间，所以一趟就够。排序是 O(n log n)，遍历是 O(n)。

扫描线回答合并遍历无法回答的并发问题。把每个区间 `[s, e]` 拆成两个事件：`s` 处一个 `+1`，`e` 处一个 `-1`。把所有事件按位置排序，然后从左到右扫描，维护一个运行和。任一时刻的和就是当前打开的区间数，而它在整趟扫描中的最大值就是并发峰值（会议室数量、车上的最多乘客数）。堆变体在不具体生成事件的情况下做同样的事：维护一个终点的最小堆，对每场新会议，弹出所有 `<=` 其起点的终点（那些会议室已腾出），然后压入这场会议的终点。堆的大小就是正在使用的会议室数；它的峰值就是答案。

贪心的「刺穿所有区间所需的最少点数」是第三张面孔：按终点排序，取第一个区间的终点作为刺穿点，跳过它覆盖的每个区间，然后重复。按终点排序正是让这个贪心选择最优的原因，因为最早的终点为其余区间留下了最多的空间。

## 模板

**合并重叠区间：**

```python
# Time: O(n log n), Space: O(n)
def merge(intervals):
    intervals.sort(key=lambda iv: iv[0])       # sort by start
    out = []
    for s, e in intervals:
        if out and s <= out[-1][1]:            # overlaps the last merged block
            out[-1][1] = max(out[-1][1], e)    # extend its end
        else:
            out.append([s, e])                 # gap: start a new block
    return out
```

**把一个区间插入到一个有序、互不相交的列表中：**

```python
# Time: O(n), Space: O(n)
def insert(intervals, new):
    out = []
    s, e = new
    i, n = 0, len(intervals)
    while i < n and intervals[i][1] < s:       # entirely before new
        out.append(intervals[i]); i += 1
    while i < n and intervals[i][0] <= e:      # overlaps new: absorb it
        s = min(s, intervals[i][0])
        e = max(e, intervals[i][1]); i += 1
    out.append([s, e])
    out.extend(intervals[i:])                  # entirely after new
    return out
```

**会议室 II，通过一个终点最小堆求最少会议室数：**

```python
import heapq

# Time: O(n log n), Space: O(n)
def min_meeting_rooms(intervals):
    intervals.sort(key=lambda iv: iv[0])       # by start
    ends = []                                  # min-heap of end times in use
    for s, e in intervals:
        if ends and ends[0] <= s:              # earliest room has freed up
            heapq.heapreplace(ends, e)         # reuse it
        else:
            heapq.heappush(ends, e)            # need a new room
    return len(ends)                           # peak concurrency
```

**通过 +1 / -1 事件的扫描线（通用最大并发数）：**

```python
# Time: O(n log n), Space: O(n)
def max_concurrent(intervals):
    events = []
    for s, e in intervals:
        events.append((s, 1))                  # a range opens
        events.append((e, -1))                 # a range closes
    events.sort()                              # end (-1) sorts before start (+1) at a tie
    active = best = 0
    for _, delta in events:
        active += delta
        best = max(best, active)
    return best
```

事件排序中的平局处理，编码了相接触的区间（`[1,2]` 与 `[2,3]`）是否算作重叠。在相等位置把 `-1` 排在 `+1` 之前，就把共享端点当作不重叠，这是通常的会议室约定。

## 变体

- **重叠检测 / 「能参加所有会议」。** 按起点排序，一旦有某个区间在前一个结束之前就开始，就返回 False。无需合并。
- **无重叠区间（移除最少的）。** 按终点排序，贪心地保留每个起点在上一个被保留终点处或之后的区间，其余计为移除。经典的区间调度。
- **射爆气球所需的最少箭数。** 与上面同样的贪心，按终点排序并统计组数；每组需要一支箭。
- **两个有序列表的区间交集。** 在两个列表上用双指针，两个前沿的重叠是 `[max(starts), min(ends)]`；推进先结束的那个。
- **拼车 / 预订计数。** 当坐标是较小整数时用一个沿轴的 [差分数组](03-prefix-sum.md)，当它们稀疏时用扫描线。二者都计算峰值负载。
- **按起点排序对按终点排序。** 合并和并发要按起点排序；贪心调度和刺穿要按终点排序。选错键是最常见的结构性错误。

## 经典题目

| # | 题目 | 难度 | 训练点 |
|---|---------|-----------|----------------|
| 252 | Meeting Rooms | 简单 | 按起点排序，相邻重叠检查 |
| 56 | Merge Intervals | 中等 | 基础的排序并合并遍历 |
| 57 | Insert Interval | 中等 | 三阶段吸收进有序列表 |
| 253 | Meeting Rooms II | 中等 | 通过堆或扫描求最大并发 |
| 435 | Non-overlapping Intervals | 中等 | 贪心的按终点排序调度 |
| 452 | Minimum Number of Arrows to Burst Balloons | 中等 | 按终点排序的刺穿分组 |
| 1094 | Car Pooling | 中等 | 在负载上做扫描线 / 差分数组 |
| 986 | Interval List Intersections | 中等 | 在两个有序列表上用双指针 |
| 763 | Partition Labels | 中等 | 最后出现位置的扫描，贪心切割 |
| 1288 | Remove Covered Intervals | 中等 | 先按起点再按终点排序，跟踪最大终点 |

## 陷阱

- **按错误的端点排序。** 合并和并发需要起点；贪心调度和箭需要终点。如果贪心在某个用例上失败，先检查排序键。
- **端点闭区间对开区间。** `[1,2]` 与 `[2,3]` 重叠吗？确定约定，然后编码它：合并中的 `s <= prev_end` 对 `s < prev_end`，以及扫描中的「`-1` 先于 `+1`」平局处理。
- **排序时原地修改了输入。** 如果调用方要保留原始顺序，先拷贝。另外，`out[-1][1] = ...` 会修改已追加的区间；追加一个新的列表，而不是一个指向输入的引用。
- **空输入。** 合并和扫描在空列表上应干净地返回；`if out` 守卫处理第一个区间。
- **扫描平局处理会翻转答案。** 在相等坐标处，你先处理终点还是先处理起点，会在接触点上把并发峰值改变 1。这是扫描线代码里最常见的差一错误。
- **堆保存的是终点，用来和下一个起点比较。** 在 `ends[0] <= s`（而非 `< s`）时弹出，符合「接触不算重叠」的约定；保持它与你的合并选择一致。

## 延伸与相关模式

- 「最大并发」依赖一个终点的 [堆](24-heap.md)，或者当轴是较小整数时依赖一个 [差分数组](03-prefix-sum.md)。
- 插入和交集变体是在一个或两个有序列表上的 [双指针](01-two-pointers.md)。
- 这里每个模板都以在一个选定键上的 [排序](08-sorting.md) 开头；自定义比较器（起点对终点）就是全部关键。
- 贪心的「移除最少」和「最少箭数」是 [贪心](25-greedy.md) 区间调度的实例，其中按终点排序让局部选择可证明最优。
- 当坐标在扫描前需要压缩时，那个分桶就是在位置上做 [哈希](04-hashing.md)。
