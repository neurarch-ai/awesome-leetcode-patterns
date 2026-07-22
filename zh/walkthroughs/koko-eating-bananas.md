# 精解：爱吃香蕉的珂珂 (LC 875)

> 中文版。English: [koko-eating-bananas](../../walkthroughs/koko-eating-bananas.md)

一个从头到尾在一道题上跑完六步框架的例题。目标是展示过程，而不只是答案。

## 题目

**LeetCode 875，中等。** 珂珂有一些 `piles` 香蕉堆，警卫在 `h` 小时后返回。她为整段时间选定一个吃香蕉的速度 `k`（每小时几根）。每小时她只从一堆吃：如果那堆至少有 `k` 根，她就吃 `k` 根，然后下一小时换下一堆；否则她把整堆吃完，这一小时就结束（她不会把剩下的时间挪到另一堆上）。返回让她能在 `h` 小时内吃完所有堆的最小整数速度 `k`。

例子：`piles = [3, 6, 7, 11]`，`h = 8` 返回 `4`。

![对答案做二分](../../assets/binary-search.svg)

*对答案做二分。完整模式见下方链接的文件。*

## 1. 厘清与复述

我会问的问题：

- **输入类型。** `piles` 是一个正整数列表，`h` 是一个正整数。`h` 保证至少是 `len(piles)` 吗？是的，题目保证了这一点，这很重要，因为她每堆至少需要一小时，所以总是能吃完。
- **我要返回什么？** 最小的整数速度。速度必须是正整数（按规则她不能每小时吃 2.5 根；`k` 是 int）。
- **约束。** `piles` 长度到 `10^4`，堆大小到 `10^9`。第二个数字就是线索。答案 `k` 位于 `[1, max(pile)]` 之间，这是一个大小可达 `10^9` 的范围。我不会去线性地扫它。一个 `10^9` 的范围配上一个是/否判定，就在大喊**对答案做二分**，目标 O(n log(max_pile))。
- **边界情况。** 只有一堆；`h` 等于堆的数量（她必须在一小时内吃掉最大的堆，所以答案是 `max(piles)`）；一个巨大的 `h`（答案触底到 `1`）；所有堆一样大。

复述：在一个可达十亿的速度范围内，找出其「她能否及时吃完」的判定通过的最小整数速度。

## 2. 手算一个例子

`piles = [3, 6, 7, 11]`，`h = 8`。以速度 `k` 清空一堆所需的小时数是 `ceil(pile / k)`。

试 `k = 4`：
- 堆 3：`ceil(3/4) = 1` 小时
- 堆 6：`ceil(6/4) = 2` 小时
- 堆 7：`ceil(7/4) = 2` 小时
- 堆 11：`ceil(11/4) = 3` 小时
- 合计 `1 + 2 + 2 + 3 = 8`，`<= 8`。可行。

试 `k = 3`：
- `ceil(3/3) + ceil(6/3) + ceil(7/3) + ceil(11/3) = 1 + 2 + 3 + 4 = 10`，`> 8`。不可行。

所以 `k = 4` 行而 `k = 3` 不行，`4` 就是最小值。注意这个规律：每个大于等于 4 的速度都可行，每个小于它的都不可行。可行性对 `k` 是**单调的**，这恰恰是二分所需要的。

## 3. 暴力解

从 1 开始向上逐个走遍速度，返回第一个能及时吃完的。

```python
import math

def min_eating_speed_brute(piles, h):
    def hours_needed(speed):
        return sum(math.ceil(pile / speed) for pile in piles)

    speed = 1
    while hours_needed(speed) > h:
        speed += 1
    return speed
```

每次 `hours_needed` 调用是 O(n)。最坏情况下答案接近 `max(piles)`（可达 `10^9`），所以这是 **O(n * max_pile)** 时间，多达 `10^13` 次操作。正确，但慢得没救。

## 4. 找到瓶颈并挑选模式

暴力解逐个测试每一个候选速度，但候选值有它忽略的结构：如果速度 `s` 能及时吃完，那么每个高于 `s` 的速度也能（吃得更快绝不会更花时间）；如果 `s` 太慢，那么每个低于 `s` 的速度也太慢。可行性是一个阶跃函数：假、假、……、假、真、真、……、真。我要的是那个边界，也就是第一个 `true`。

那个单调的是/否答案空间正是**对答案做二分**的确切信号。不是在一个有序值数组里搜索，而是在可能答案的范围 `[1, max(piles)]` 里搜索，并用一个判定 `feasible(speed)` 代替比较。每一步把范围减半，把 `10^9` 个候选变成大约 30 次判定求值。

判定：

```
feasible(speed) := sum(ceil(pile / speed) for pile in piles) <= h
```

它是单调的：随着 `speed` 增大，每个 `ceil` 项都不增，所以整个和不增，于是一旦它降到 `<= h` 就会一直保持。正是这种单调性让二分有效。我要找到 `feasible` 为真的最左侧速度。

## 5. 写出代码

```python
def min_eating_speed(piles, h):
    def feasible(speed):
        # hours to clear each pile at this speed; ceil without floats:
        # (pile + speed - 1) // speed
        hours = 0
        for pile in piles:
            hours += (pile + speed - 1) // speed
            if hours > h:            # early exit, cannot get better
                return False
        return hours <= h

    lo, hi = 1, max(piles)           # slowest usable speed .. fastest ever needed
    while lo < hi:
        mid = (lo + hi) // 2
        if feasible(mid):
            hi = mid                 # mid works, but maybe something slower does too
        else:
            lo = mid + 1             # mid too slow, answer is strictly faster
    return lo                        # lo == hi is the smallest feasible speed
```

我用整数向上取整 `(pile + speed - 1) // speed` 而不是 `math.ceil(pile / speed)`，以避免在 `10^9` 量级上的浮点误差。循环不变式：答案始终落在 `[lo, hi]` 里。当 `feasible(mid)` 为真时我保留 `mid` 作为候选（`hi = mid`，不是 `mid - 1`）；为假时我丢弃 `mid` 及其以下的一切（`lo = mid + 1`）。循环在 `lo == hi` 时结束，那就是边界。

## 6. 测试、追踪与分析

追踪 `piles = [3, 6, 7, 11]`，`h = 8`。从 `lo = 1`、`hi = 11` 开始。

| lo | hi | mid | feasible(mid) | hours | 动作 |
|----|----|-----|---------------|-------|------|
| 1 | 11 | 6 | true | 1+1+2+2 = 6 | hi = 6 |
| 1 | 6 | 3 | false | 1+2+3+4 = 10 | lo = 4 |
| 4 | 6 | 5 | true | 1+2+2+3 = 8 | hi = 5 |
| 4 | 5 | 4 | true | 1+2+2+3 = 8 | hi = 4 |

此时 `lo == hi == 4`，返回 `4`。与手算答案吻合。

边界情况：
- **一堆**，`piles = [11], h = 4`：搜索收敛到速度 3 时 `ceil(11/3) = 4` 小时，而速度 4 时 `ceil(11/4) = 3 <= 4`……追踪下来，`lo` 稳定在满足 `ceil(11/speed) <= 4` 的最小速度，也就是 3。正确。
- **h 等于堆数**，`piles = [3, 6, 7, 11], h = 4`：她必须在恰好一小时内清掉每堆，所以答案是 `max(piles) = 11`。任何低于 11 的速度都会让那堆 11 花两小时或更多，超出 `h`。搜索返回 11。正确。
- **巨大的 h**：即便 `mid = 1` 可行性也通过，于是 `hi` 一路塌到 1，答案是 `1`，最慢的合法速度。正确。

**复杂度：O(n log(max_pile)) 时间**，其中 `log` 因子是二分步数（对 `10^9` 约 30），每一步跑一次 O(n) 的判定，以及 **O(1) 额外空间**。这就是预期解法，远胜暴力解。

时间更充裕的话，我会提一下这道题实例化的通用配方：任何「在一个单调可行性判定下最小化/最大化某个值」的问题（在 D 天内送达、分割数组的最大值），都是同一个对答案做二分的形状，只是换了个判定。

## 面试官真正考察的是什么

你能否看出答案本身位于一个可搜索、单调有序的空间里，即便输入中没有任何东西是一个有序数组。关键的一跃是把「找最小速度」重构为「找一个真/假判定的边界」，并证明这个判定是单调的。只把二分与在有序列表里搜索绑在一起的候选人会错过一整类问题；而内化了它的人会先写判定，再写搜索。

> 模式：[07 二分查找](../patterns/07-binary-search.md)
