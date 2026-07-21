# 11 - 栈：单调栈与解析

> 中文版。English: [11-stacks](../patterns/11-stacks.md)

> **问题形态：** 「对每个元素，找到下一个更大的。」「还有几天会升温？」
> 「柱状图中最大的矩形。」「这串括号有效吗？」「求这个逆波兰表达式的值。」
> 「解码 `3[a2[c]]`。」任何一个元素的答案取决于最近的、尚未解决的元素的场景，
> 后进先出的顺序正是你所需要的。

当你接下来需要的东西总是最近见过、仍在等待解决的那个时，栈就大放异彩。
两个家族主导面试：**单调栈**，它让内容保持有序，使每个新元素以摊还 O(1)
解决掉一批更旧的；以及**栈解析**，它用栈来跟踪嵌套并推迟计算，直到一个闭合记号到来。
两者都用一趟 O(n) 取代了 O(n^2) 的「回头看遍所有」扫描。

![单调栈求解下一个更大元素](../assets/stacks.svg)

*单调栈：每根进来的柱子弹出它所击败的每一根更高的柱子，然后把自己压入。*

## 信号

当你看到以下情况时，考虑栈：

- **「下一个更大 / 下一个更小元素」、「还有几天升温」、「股票跨度」。**
  对每个项你想要击败它的最近的后一个（或前一个）项。这是单调栈的主场。
- **「柱状图中最大的矩形」、「最大矩形」、「接雨水」。**
  你需要对每根柱子，它在一根更矮（或更高）的柱子拦住它之前能延伸多远。
  那个「延伸到什么打破趋势为止」就是单调栈的记账。
- **「大小为 k 的每个滑动窗口的最大值」。** 一个单调*双端队列*
  （两端都开口的栈）把窗口候选保持在递减顺序。
- **匹配或嵌套的定界符**：括号、标签、`decode 3[a2[c]]`、嵌套表达式。
  栈镜像了嵌套：开时压入，闭时弹出并解决。
- **求后缀表达式的值，或一个带 `+ - ( )` 的中缀计算器。**
  操作数和待定的运算符或小计在栈上等待，直到一个运算符或一个闭括号告诉你把它们合并。
- **「设计一个 O(1) 取最小/最大的栈」。** 在每个值旁边存一个辅助的运行极值。

## 思路

**单调栈。** 让栈保持有序（比如递增）。在压入一个新值之前，
弹出每一个违反顺序的元素。关键洞见：*新元素是它弹出的每一样东西的答案。*
如果栈持有一个严格递增序列的索引，而进来的柱子更小，
那么对每个被弹出的（更高的）柱子，进来的柱子就是它的「右边下一个更小」，
而现在栈顶的东西就是它的「左边前一个更小」。一次压入和一连串弹出解决掉整整一个邻域。
每个索引被压入一次、弹出一次，所以尽管任何单步都可能弹出多次，总工作量是 O(n)。

方向和严格性决定变体：
- 递增栈，进来的更小时弹出：为被弹出者解决**下一个更小**，为幸存者解决**前一个更小**。
- 递减栈，进来的更大时弹出：解决**下一个更大**。

对于**柱状图最大矩形**，每根柱子的矩形左边被前一根更矮的柱子限定、
右边被下一根更矮的柱子限定；一个递增栈在你弹出的那一刻把两个边界都交给你。
对于**接雨水**，一个递减栈在一堵更高的右墙到来时弹出一个山谷，
那个山谷上的水由 `min(左墙, 右墙)` 乘以间隔限定。

**单调双端队列**（滑动窗口最大值）是同样的思路，只是也从前端移除：
把索引保持在递减值顺序，当前端滑出窗口时丢掉它，当后端小于进来的值时丢掉它。
前端始终是当前窗口的最大值。

![一个栈匹配括号：压入开括号，闭括号与栈顶匹配时弹出](../assets/stacks-parsing.svg)

*栈的另一种用途：解析。压入每个开括号；一个闭括号必须与栈顶匹配，否则字符串无效。*

**栈解析。** 栈编码「我正处在什么之中」。当你进入一个新作用域
（一个开括号、一个操作数、一个重复计数）时压入，闭合它时弹出以解决。
对**有效括号**，压入开括号并要求每个闭括号与栈顶匹配。对**后缀（RPN）**，
压入操作数，遇到运算符时弹出两个并压入结果。对**解码字符串**，在 `[`
上压入（乘数, 到目前为止的字符串）对，在 `]` 上合并。对一个**基础计算器**，
在 `(` 上压入符号和运行总数，在 `)` 上恢复。**最小栈**保持一个平行记录，
记下每一层可见的最小值，使 `getMin` 为 O(1)。

## 模板

**单调栈，下一个更大元素（返回下一个更大的索引，或 -1）：**

```python
# Time: O(n), Space: O(n)
def next_greater(nums):
    n = len(nums)
    ans = [-1] * n
    stack = []                      # holds indices, values strictly decreasing
    for i, x in enumerate(nums):
        while stack and nums[stack[-1]] < x:
            ans[stack.pop()] = i    # x is the next greater for the popped index
        stack.append(i)
    return ans
```

**柱状图最大矩形（递增栈，哨兵冲刷）：**

```python
# Time: O(n), Space: O(n)
def largest_rectangle(heights):
    stack = []                      # indices, heights increasing
    best = 0
    for i, h in enumerate(heights + [0]):   # trailing 0 flushes everything
        while stack and heights[stack[-1]] >= h:
            top = stack.pop()
            left = stack[-1] if stack else -1   # previous shorter bar
            width = i - left - 1                # bounded by next shorter (i) and prev shorter
            best = max(best, heights[top] * width)
        stack.append(i)
    return best
```

**单调双端队列，滑动窗口最大值：**

```python
from collections import deque

# Time: O(n), Space: O(k)
def max_sliding_window(nums, k):
    dq = deque()                    # indices, values decreasing
    out = []
    for i, x in enumerate(nums):
        if dq and dq[0] <= i - k:   # front slid out of the window
            dq.popleft()
        while dq and nums[dq[-1]] <= x:
            dq.pop()                # x dominates smaller trailing candidates
        dq.append(i)
        if i >= k - 1:
            out.append(nums[dq[0]]) # front is the window max
    return out
```

**栈解析，有效括号：**

```python
# Time: O(n), Space: O(n)
def is_valid(s):
    match = {')': '(', ']': '[', '}': '{'}
    stack = []
    for ch in s:
        if ch in match:
            if not stack or stack.pop() != match[ch]:
                return False        # nothing to match, or wrong opener
        else:
            stack.append(ch)
    return not stack                # leftover openers means unbalanced
```

## 变体

- **循环数组中的下一个更大。** 用 `i % n` 迭代 `2n` 次，
  使元素能找到一个绕回来的更大者。只有第一趟填充栈；第二趟解决绕回的情况。
- **接雨水，栈版本。** 递减栈；当一根更高的柱子到来，弹出山谷，
  加水 `= (min(左, 右) - 山谷) * 宽度`。双指针版本（见双指针）如果你偏好，是 O(1) 空间。
- **二进制矩阵中的最大矩形。** 逐行构建一个柱状图（连续 1 的高度）
  并在每行上运行最大矩形。把柱状图模板复用为内层循环。
- **逆波兰（RPN）。** 压入数字；遇到运算符弹出两个、应用、压回。
  注意 `-` 和 `/` 的操作数顺序（第二个弹出的是左操作数）。
- **带括号的基础计算器。** 保持一个运行的 `result`、一个当前的 `sign`，
  在 `(` 上压入 `(result, sign)` 然后重置；在 `)` 上弹出并折叠。
  无需递归就能处理 `1 - (2 + 3)`。
- **解码字符串 `k[...]`。** 在 `[` 上压入 `(count, current_string)`；
  在 `]` 上弹出并设 `current = prev_string + count * current`。嵌套自然解决。
- **最小栈。** 存 `(value, current_min)` 对，或保持第二个存最小值的栈。
  每次压入都记录目前可见的最小值，所以弹出和 getMin 保持 O(1)。

## 经典题目

| # | 题目 | 难度 | 训练点 |
|---|---------|-----------|----------------|
| 20 | Valid Parentheses | 简单 | 压入开括号，闭合时匹配 |
| 496 | Next Greater Element I | 简单 | 单调栈，然后一个查找映射 |
| 155 | Min Stack | 中等 | 跟踪每层的运行最小值 |
| 739 | Daily Temperatures | 中等 | 对索引的单调栈（到升温的间隔） |
| 150 | Evaluate Reverse Polish Notation | 中等 | 操作数栈，运算符折叠两个 |
| 394 | Decode String | 中等 | 栈上嵌套的（count, string）帧 |
| 84 | Largest Rectangle in Histogram | 困难 | 递增栈，弹出时得到两个边界 |
| 42 | Trapping Rain Water | 困难 | 递减栈在更高的墙上弹出山谷 |
| 239 | Sliding Window Maximum | 困难 | 单调双端队列，前端是窗口最大值 |
| 224 | Basic Calculator | 困难 | 在 `(` 上压入 sign+total，在 `)` 上折叠 |

## 陷阱

- **严格与非严格比较。** 弹出时 `<` 对 `<=` 决定了相等元素是否算作
  「更大/更小」。搞错了矩形会重复计数，或「下一个更大」会跳过平局。每题都要刻意选择。
- **存值而非索引。** 对「还有几天」或柱状图宽度你需要位置来计算距离。
  压入索引并通过 `nums[idx]` 读取值。
- **忘了在结尾冲刷栈。** 从未弹出的元素仍需要它们的答案。
  用一个哨兵（追加一个 `0` 高度，或一个 `+inf`）或一个最终的排空循环，
  否则它们的结果保持未初始化。
- **双端队列：不逐出越界的前端。** 在滑动窗口最大值里，一旦前端的索引落在
  `[i-k+1, i]` 之外你就必须弹出它，否则最大值是过期的。
- **RPN 操作数顺序。** 对非交换运算符，*第一个*弹出的值是右操作数。
  `a b -` 意味着 `a - b`，所以 `left = second_pop`，`right = first_pop`。
- **计算器符号处理。** 把符号跟踪为 `+1 / -1`，并在你遇到一个数字或一个 `(`
  时应用它；括号前一个孤零零的 `-` 是经典的失败点。跨括号压入并恢复 `(result, sign)`。

## 后续追问与相关模式

- 「给我每个窗口的最大值」是滑动窗口与单调双端队列相遇之处；
  窗口那一半见 [滑动窗口](02-sliding-window.md)。
- 「以 O(1) 空间接雨水」把栈换成相向收敛的
  [双指针](01-two-pointers.md)。
- 「第 k 大，而不是下一个更大」把你带到
  [堆](24-heap.md) 或 [快速选择](09-top-k-quickselect.md)。
- 「按层级而非按作用域处理嵌套」镜像了
  [树的 BFS 与层序](13-tree-bfs.md) 中的队列行走。
