# 精解：会议室 II (LC 253)

> 中文版。English: [meeting-rooms-ii](../../walkthroughs/meeting-rooms-ii.md)

一个在一道题上叙述六步解题框架的例题，让你看到过程在运转，而不只是最终的代码。

## 题目

**LeetCode 253，会议室 II，中等。** 给定一个会议时间区间数组 `intervals`，其中 `intervals[i] = [start_i, end_i]`，返回所需的最少会议室数量，使得共用一间会议室的任意两个会议都不重叠。

例子：`intervals = [[0, 30], [5, 10], [15, 20]]` 返回 `2`。会议 `[0, 30]` 与另外两个都重叠，但 `[5, 10]` 和 `[15, 20]` 彼此不重叠，所以两间会议室就够了。

![时间轴上的区间](../../assets/intervals.svg)

*时间轴上的区间。完整模式见下方链接的文件。*

## 1. 厘清与复述

我在动代码前会问的问题：

- **区间是左闭右开的吗？** 这是承重的问题。标准约定：一个会议 `[start, end]` 占用会议室的时间是 `[start, end)`，所以在时刻 `t` 结束的会议和在时刻 `t` 开始的另一个会议**不**冲突，可以共用一间。我会确认这一点，因为它决定了扫描里的一个平手打破规则，并会在像 `[[1, 5], [5, 10]]` 这样的输入上翻转答案（1 间，不是 2 间）。
- **我要返回什么？** 一个整数：最少会议室数。等价地说，任一瞬间同时进行的会议的最大数量。
- **输入排好序了吗？** 就假设没有。我会排序。
- **区间可以为空吗？** 可以，返回 `0`。单个会议返回 `1`。
- **start 可以等于 end（零长会议）吗？** 有可能；在左闭右开区间下它什么都不占用、不需要会议室，但除非面试官提起，我不会过度设计。
- **n 有多大？** 约束：`1 <= intervals.length <= 10^4`，`0 <= start < end <= 10^6`。`n <= 10^4` 加上需要排序，明确指向一个 `O(n log n)` 的解法。这排除了 `O(n^2)` 的两两重叠检查作为预期答案，并指向排序加堆或扫描线。

复述：答案就是**同时活跃的会议的最大数量**。每间会议室恰好在会议重叠时忙碌，所以峰值并发数就是会议室数。把「最少会议室」重构为「最大重叠」就是全部洞见。

## 2. 手算一个例子

`intervals = [[0, 30], [5, 10], [15, 20]]`。我会把所有开始时间和所有结束时间分开，各自排序，然后沿时间轴扫描，统计活跃的会议：

```
starts sorted: 0, 5, 15
ends   sorted: 10, 20, 30

time 0  : a meeting starts -> active = 1  (peak 1)
time 5  : a meeting starts -> active = 2  (peak 2)
time 10 : a meeting ends   -> active = 1
time 15 : a meeting starts -> active = 2  (peak 2)
time 20 : a meeting ends   -> active = 1
time 30 : a meeting ends   -> active = 0
```

峰值并发是 2，所以 2 间会议室。这个手工方法本身就是扫描线算法：按时间顺序处理事件，开始时 `+1`，结束时 `-1`，并追踪运行中的最大值。那个平手打破规则（当一个开始和一个结束共享同一时间戳时，先处理结束，因为左闭右开区间让腾出的会议室可被复用）正是我在第 1 步确认过的。

## 3. 暴力解

显然的解法：答案等于最大重叠数，所以对每个会议统计有多少会议与它重叠，或者更直接地，对 `2n` 个端点中的每一个统计有多少区间覆盖那个点。

```python
def min_rooms_brute(intervals):
    if not intervals:
        return 0
    # For each start time, count meetings active at that instant.
    best = 0
    for s, _ in intervals:
        active = 0
        for a, b in intervals:
            if a <= s < b:               # half-open: [a, b) covers s
                active += 1
        best = max(best, active)
    return best
```

复杂度：对 `n` 个候选时刻中的每一个我们扫描全部 `n` 个区间，所以是 `O(n^2)` 时间，`O(1)` 额外空间。它是正确的（峰值重叠总能在某个会议的开始时刻见证到），但在 `n = 10^4` 时那是 `10^8` 次操作，在太慢的边缘，显然不是预期的 `O(n log n)`。

## 4. 找到瓶颈并挑选模式

瓶颈在于暴力解在每个时间戳都从头重算完整的重叠数，忽略了活跃数在每个事件处只变化一。这是在一个移动前沿上的重复工作，而我没有利用的结构是**时间顺序**。

有两种模式都利用了这一点，都是 `O(n log n)`：

- **扫描线（两个有序数组）。** 分别对开始时间和结束时间排序。用两个指针按时间递增地走。遇到一个开始，活跃数加一并推进开始指针；遇到一个结束（其时间 `<=` 当前开始），减一并推进结束指针。追踪最大值。在相等的开始之前处理结束，编码了左闭右开的规则。
- **区间加最小堆。** 按开始时间对会议排序。维护一个最小堆，存放当前被占用的会议室的结束时间。对每个会议，如果最早结束的会议室（`heap[0]`）在这个会议开始时已空闲（`heap[0] <= start`），就弹出它（复用那间会议室）；然后压入这个会议的结束时间。堆的大小就是正在使用的会议室数，它在整趟运行中的最大值就是答案。

两者都是 `O(n log n)`。堆版本是面试官最常想要的，因为它能推广（你可以附上会议室 ID，它也映射到任务调度问题）。我会写堆版本，并把扫描线作为替代方案提一下。

## 5. 写出代码

```python
import heapq
from typing import List

class Solution:
    def minMeetingRooms(self, intervals: List[List[int]]) -> int:
        if not intervals:
            return 0

        # Process meetings in start-time order.
        intervals.sort(key=lambda meeting: meeting[0])

        # Min-heap of end times for rooms currently in use.
        rooms = []                       # rooms[0] is the soonest-freeing room

        for start, end in intervals:
            # If the earliest-ending room is free by the time this meeting
            # starts, reuse it (half-open: end == start counts as free).
            if rooms and rooms[0] <= start:
                heapq.heappop(rooms)
            heapq.heappush(rooms, end)   # this meeting occupies a room until `end`

        # The heap never shrank below its peak concurrency, and each remaining
        # entry is a distinct room, so its final... no: track the peak instead.
        return len(rooms)
```

一个值得叙述的正确性微妙之处：因为我每个会议至多弹出一间会议室、恰好压入一间，处理完会议 `i` 后堆的大小等于与会议 `i` 重叠的会议数（在按开始排序的前提下），而这个大小在「只有真正需要一间新会议室时才增长」这个意义上是单调的。因此最终的 `len(rooms)` 等于峰值并发，也就是曾经同时被占用的最多会议室数。如果那套推理在现场感觉不牢靠，稳妥的做法是显式追踪最大值：

```python
import heapq
from typing import List

class Solution:
    def minMeetingRooms(self, intervals: List[List[int]]) -> int:
        if not intervals:
            return 0
        intervals.sort(key=lambda meeting: meeting[0])
        rooms = []
        best = 0
        for start, end in intervals:
            if rooms and rooms[0] <= start:
                heapq.heappop(rooms)
            heapq.heappush(rooms, end)
            best = max(best, len(rooms))
        return best
```

不变式：处理完一个会议后，`rooms` 持有在那个会议开始时每间忙碌会议室的结束时间（减去任何已腾出的），而 `best` 是堆曾经达到过的最大值。显式追踪 `best` 是我会交出去的版本，因为它不需要单调性论证就显然正确。

## 6. 测试、追踪与分析

追踪 `intervals = [[0, 30], [5, 10], [15, 20]]`（已按开始排序）：

- `[0, 30]`：堆为空，压入 30。`rooms = [30]`，best = 1。
- `[5, 10]`：`rooms[0] = 30 > 5`，没有空闲会议室，压入 10。`rooms = [10, 30]`，best = 2。
- `[15, 20]`：`rooms[0] = 10 <= 15`，弹出 10（那间会议室腾空），压入 20。`rooms = [20, 30]`，best = 2。

返回 `2`。与手算追踪吻合。正确。

边界情况：

- `intervals = []`：守卫返回 `0`。正确。
- `intervals = [[7, 10]]`：压入 10，best = 1，返回 `1`。正确。
- 首尾相接，`[[1, 5], [5, 10]]`：第一个压入 5。第二个：`rooms[0] = 5 <= 5`，弹出（会议室被复用，左闭右开），压入 10，大小保持 1，返回 `1`。正确，左闭右开约定被遵守了。
- 完全嵌套，`[[1, 10], [2, 9], [3, 8]]`：大小走 1、2、3，没有一间提早腾出，返回 `3`。正确，三个都重叠。
- 全部相同，`[[2, 4], [2, 4]]`：第一个压入 4；第二个 `rooms[0] = 4 > 2`，不复用，大小 2，返回 `2`。正确。

复杂度：**O(n log n) 时间**，由排序加上 `n` 次各 `O(log n)` 的堆操作主导。**O(n) 空间**用于最坏情况下的堆（所有会议都重叠）。这是最优的，因为任何基于比较的解法至少都得排序。时间更充裕的话，我会给出扫描线变体（两个有序端点数组，无需堆）作为同复杂度的替代方案，并指出如果会议室数量有界且时间是小整数，一个差分数组 / 桶扫描能给出 `O(n + T)`。

## 面试官真正考察的是什么

你能否把「最少资源」重构为「峰值并发需求」，这是一整类调度与区间问题背后可迁移的洞见。左闭右开的平手打破规则（结束在相等的开始之前）是把推理过模型的候选人和套了个模板的候选人区分开来的那处细节，而堆与扫描线的选择让你能展示你对同一形状不止掌握一种工具。

> 模式：[05 区间](../patterns/05-intervals.md) 与 [24 堆](../patterns/24-heap.md)
