# 09 - Top-K 与快速选择

> 中文版。English: [09-top-k-quickselect](../patterns/09-top-k-quickselect.md)

> **问题形态：** 「找第 k 大的元素。」「返回离原点最近的 k 个点。」
> 「给我出现频率最高的 k 个元素。」任何时候你只需要从一个大集合里挑出少数几个极值
> （或一个顺序统计量），而排序整个集合比问题所要求的工作还多。

排序能回答「给我最大的 k 个」，但它付出 O(n log n) 去排序那些你将要丢弃的元素。
当你只需要前 k，或只是那单个第 k 的元素时，存在两种更便宜的工具：
**快速选择**，它通过分区在 O(n) 平均时间内找到第 k 个元素；以及一个**有界堆**，
它以 O(n log k) 流式地取出前 k。在两者之间做选择才是这里真正的功课，
而它归结为一个问题：你是一次性拿到整个数组，还是它随时间陆续到达？

## 信号

当你看到以下情况时，考虑快速选择或 top-k 堆：

- **「第 k 大 / 第 k 小」**，一个单独的顺序统计量。快速选择在平均 O(n)
  内搞定，无需排序。
- **「前 k」/「最近 k」/「最频繁 k」**，从众多之中取出的一小组极值。
  要么分区一次（离线），要么维护一个大小为 k 的堆（流式）。
- **k 远小于 n。** 全部意义就在于避免完整排序的 `log n` 因子；如果 k 接近 n，就直接排序。
- **对你已在内存中持有的数据做一次性查询**偏向快速选择（平均最快，原地）。
  **一个流，或随数据增长的重复查询**偏向堆（你无法对尚未见过的数据分区）。

如果答案需要*按有序顺序*的前 k，注意快速选择留下的是已分区但未排序的它们；
你事后只对这 k 个排序（O(k log k)）。

## 思路

**快速选择**是只递归进一侧的快速排序。选一个枢轴，
把数组分区成一切更小的在左、一切更大的在右，然后看枢轴的最终索引 `p`。
如果 `p` 就是你想要的位置，完成。如果你的目标在 `p` 左边，递归左；在右边，递归右。
因为每一步都丢弃一侧，期望工作量是 `n + n/2 + n/4 + ... = O(n)`，
而非 `O(n log n)`。最坏情况在对抗性枢轴上是 O(n^2)，
通过随机选枢轴（或用中位数的中位数保证 O(n)）来化解。

![分区把数组分成小于枢轴、枢轴、大于枢轴三部分](../assets/partition.svg)

*分区围绕一个枢轴切分数组，然后快速选择只递归进一侧。*

**有界堆**在扫描时保持一个大小为 k 的小顶堆。对「最大 k」，压入每个元素，
每当堆超过 k 就弹出最小的，于是堆始终持有目前所见最大的 k 个，
其根就是第 k 大。每次压入/弹出是 O(log k)，总共 O(n log k)。
它从不需要整个数组同时在内存里，这正是它在流上取胜的原因。

一句话概括权衡：快速选择更快（O(n) 对 O(n log k)）且原地，
但它是**离线且破坏性的**（它重排数组且需要它全部在场）；
堆是**在线、非破坏性、可流式的**，但要付 log-k 的因子。

## 模板

**快速选择求第 k 大（Lomuto 分区，随机枢轴）：**

```python
import random

# Time: O(n) average, O(n^2) worst, Space: O(1)
def kth_largest(nums, k):
    target = len(nums) - k             # k-th largest == this index once sorted
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        p = partition(nums, lo, hi)
        if p == target:
            return nums[p]
        if p < target:
            lo = p + 1                 # answer is to the right
        else:
            hi = p - 1                 # answer is to the left

# Time: O(n), Space: O(1)  (n = hi - lo + 1, the sub-range length)
def partition(a, lo, hi):
    r = random.randint(lo, hi)         # random pivot defuses O(n^2)
    a[r], a[hi] = a[hi], a[r]
    pivot = a[hi]
    i = lo                             # a[lo..i-1] are < pivot
    for j in range(lo, hi):
        if a[j] < pivot:
            a[i], a[j] = a[j], a[i]
            i += 1
    a[i], a[hi] = a[hi], a[i]          # put pivot in its final place
    return i
```

上面的循环写法避免了递归深度问题；边界逻辑与二分查找是同样的下界/上界推理，
把 `[lo, hi]` 朝 `target` 收窄。

**有界小顶堆求最大 k 个（对流友好）：**

```python
import heapq

# Time: O(n log k), Space: O(k)
def k_largest(stream, k):
    heap = []                          # min-heap of the k largest so far
    for x in stream:
        heapq.heappush(heap, x)
        if len(heap) > k:
            heapq.heappop(heap)        # evict the smallest, keep the top k
    return heap                        # heap[0] is the k-th largest
```

**离原点最近的 k 个点（以负平方距离为 key 的堆）。** 用一个大小为 k 的大顶堆，
使当前 k 个中最远的坐在根上，随时准备被逐出。

```python
import heapq

# Time: O(n log k), Space: O(k)
def k_closest(points, k):
    heap = []                          # max-heap via negated distance
    for x, y in points:
        d = -(x * x + y * y)           # no sqrt needed; monotone in distance
        heapq.heappush(heap, (d, x, y))
        if len(heap) > k:
            heapq.heappop(heap)        # drop the current farthest
    return [[x, y] for _, x, y in heap]
```

对「最频繁 k 个」，先用 `Counter` 计数，然后对 `(count, value)`
对做快速选择或用大小为 k 的堆；`Counter.most_common(k)` 底层就用了一个堆。

## 变体

- **第 k 小。** 同样的快速选择，`target = k - 1`，或一个大小为 k 的大顶堆。
  与第 k 大对称。
- **前 k 高频元素 / 单词。** 计数，然后选择。对「前 k 个单词」平局裁决是字典序，
  所以堆必须用正确的符号比较 `(count, word)`，或者你按计数分桶再给每个桶的单词排序。
- **按计算出的 key 求最近 k / 最小 k。** 任何度量都行，只要它是单个可比较的值：
  平方距离、与目标的绝对差、到达时间。当平方在你所需之上单调时避免 `sqrt`。
- **数据流的中位数。** 不是固定的 k：用两个堆（下半部分的大顶堆、
  上半部分的小顶堆）保持平衡。见 [堆](24-heap.md)。
- **保证 O(n) 的选择。** 中位数的中位数挑选一个可证明良好的枢轴，
  使快速选择最坏情况线性。面试里很少需要（随机枢轴期望 O(n) 且更简单），
  但值得能叫出名字。
- **基于分区的有序前 k。** 快速选择隔离出最大的 k 个，然后只对这 k 个排序：
  平均 O(n) 加上 O(k log k)，在 k 小时胜过完整排序。

## 经典题目

| # | 题目 | 难度 | 训练点 |
|---|---------|-----------|----------------|
| 215 | Kth Largest Element in an Array | 中等 | 快速选择对比大小为 k 的堆 |
| 973 | K Closest Points to Origin | 中等 | 对平方距离的大小为 k 的大顶堆 |
| 347 | Top K Frequent Elements | 中等 | 先计数再选择（堆或桶） |
| 692 | Top K Frequent Words | 中等 | 计数再选择，带字典序平局裁决 |
| 703 | Kth Largest Element in a Stream | 简单 | 流式：大小为 k 的堆，不用快速选择 |
| 658 | Find K Closest Elements | 中等 | 按与目标的绝对差选择 |
| 378 | Kth Smallest Element in a Sorted Matrix | 中等 | 行堆，或对值做二分 |
| 451 | Sort Characters By Frequency | 中等 | 按计数完整排序（与 top-k 对照） |
| 295 | Find Median from Data Stream | 困难 | 双堆平衡，流式顺序统计量 |

## 陷阱

- **对流用快速选择。** 它不可能奏效：快速选择需要对整个数组随机访问来分区。
  如果数据随时间到达或装不进内存，你必须用大小为 k 的堆。
- **忘了快速选择是破坏性的。** 它重排输入数组。如果调用者仍需要原始顺序，
  先复制，或用堆。
- **O(n^2) 枢轴陷阱。** 固定枢轴（总是取第一个或最后一个）在有序或对抗性输入上
  退化为 O(n^2)。永远随机化枢轴。
- **堆极性搞反。** 对最大 k 你保持一个*小*顶堆（逐出最小的）；
  对最近 k 你保持一个按距离的*大*顶堆（逐出最远的）。搞反了会悄悄返回错误的 k。
  在 Python 里，取负 key 来伪造大顶堆。
- **只需要选择却去排序。** 为「那单个第 k 个元素」做一次完整的 O(n log n)
  排序是经典的过度求解；快速选择是 O(n)。
- **前 k 单词里的平局符号错误。** 当计数平局时，字典序更小的单词应排更高，
  但一个大小为 k 的*小*顶堆逐出「最小的」，所以你必须取负计数并保持单词升序，
  这是一个常见的差一符号 bug。按计数分桶再给单词排序能避免这种混乱。

## 后续追问与相关模式

- 这个模式是 [堆与优先队列](24-heap.md) 的孪生：堆是这里每个 top-k
  的流式、非破坏性引擎，而数据流中位数和合并 k 个链表的问题就住在那里。
- 「直接排序整个」是 [排序与自定义比较器](08-sorting.md)；
  当完整排序超过问题所需时，你就去够快速选择。
- 「在一个*有序*结构里找第 k 小」常常变成对值做
  [二分查找](07-binary-search.md)（对答案做二分），
  对有序矩阵问题这比堆更便宜。
- 分区那一步与快速排序是同一套机器，并与许多
  [数学](27-math.md) 风味的选择证明背后的分治步骤共享「选枢轴并递归」的形态。
- 选择之前计数频率是 [哈希与频率计数](04-hashing.md)；
  前 k 高频就是那个模式喂给这个模式。
