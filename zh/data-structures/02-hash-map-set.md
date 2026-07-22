# 02 - 哈希表与哈希集合

> 中文版。English: [02-hash-map-set](../../data-structures/02-hash-map-set.md)

哈希表用内存换速度：它把键通过一个哈希函数转成一个数组下标，于是无需扫描 n 个元素来找一个，你直接算出它必然所在的位置去看那里。这正是 `dict` 和 `set` 给你 O(1) 平均查找、插入与成员判断的全部原因。这也是为什么这个保证是「平均」而非「总是」，以及为什么键必须是可哈希的。简单题和中等题里有一半（「两数之和」「字母异位词分组」「无重复字符的最长子串」）都是披着外衣的哈希表。

![一个哈希表通过补数检查给出 O(1) 平均查找](../../assets/hashing.svg)

*O(1) 平均查找正是无序的两数之和成为一趟哈希表问题的原因。*

## 它是什么

哈希集合存储一组各不相同的元素，并支持快速成员判断。哈希表（字典）存储键到值的关联，并支持按键快速查找。两者底层建立在同一套机器上：一个桶数组加一个哈希函数。

机制是这样的：要存一个键，计算 `h = hash(key)`，把它归约成一个桶下标 `h % num_buckets`，把条目放在那里。要查它，计算出同一个下标，检查那个桶。因为你直接跳到桶而不是扫描，所以查找平均是 O(1)。数组是速度的来源，而哈希函数负责把任意键映射到一个数组下标。

两个键可能哈希到同一个桶。这就是冲突，而且无法避免（你是在把巨大的键空间映射到有限的数组上）。实现用链接法（每个桶存一个小 list）或开放寻址法（探测到下一个空槽；CPython 用开放寻址）来解决它。无论哪种，当一个桶里存了若干冲突的键，你就退化成在那个桶内扫描，这就是为什么最坏情况会退化到 O(n)，如果每个键都落进同一个桶的话。有了不错的哈希函数和随机化输入，那种情况基本永不发生，所以你报的是平均值。

装载因子让冲突保持罕见。它是已存条目数与桶数的比值。随着它攀升，冲突更可能发生、查找变慢，于是表会盯着它，一旦超过阈值（CPython 在表约三分之二满时扩容），就分配一个更大的桶数组，并把每个条目重新哈希进去。那次扩容是 O(n)，但在两次扩容之间的许多次插入上摊还掉了，跟动态数组的追加是同一套摊还逻辑。

## 操作与复杂度

| 操作 | 复杂度 | 说明 |
|---|---|---|
| `d[k]`、`d[k] = v`、`del d[k]` | 平均 O(1) / 最坏 O(n) | 哈希到一个桶；最坏是病态冲突 |
| `k in d`、`x in s` | 平均 O(1) / 最坏 O(n) | 这些结构存在的理由 |
| `s.add(x)`、`s.discard(x)` | 平均 O(1) / 最坏 O(n) | 同一条哈希路径 |
| `len(d)`、`len(s)` | O(1) | 已存，非现数 |
| 遍历 `d`、`d.items()`、`s` | O(n) | 视图 O(1) 生成，O(n) 走完 |
| `a | b`（集合并） | O(len a + len b) | 新集合 |
| `a & b`（集合交） | O(min(len a, len b)) | 遍历较小的一边 |
| `a - b`（集合差） | O(len a) | |
| `Counter(iterable)` | O(n) | 一趟完成计数 |
| `counter.most_common(k)` | O(n log k) | 内部用大小为 k 的堆 |
| `counter.most_common()`（全部） | O(n log n) | 完整排序 |

为什么查找是 O(1) 平均：你在常数时间内算出桶下标，而由于装载因子被压得低，目标桶里只有寥寥几个条目要检查。没有对 n 的扫描。为什么最坏情况是 O(n)：如果一个对手或一个糟糕的哈希函数把每个键都灌进一个桶，那个桶就变成一个线性 list，每次查找都扫遍它。你在正常数据上基本永远不会碰到最坏情况，但你还是要说出来，因为它是真实存在的。

数字必须与[复杂度速查表](../complexity.md)一致；那里按平均与最坏分列了同一张表。

## Python 实现

你会用到的三种容器，外加两个 `collections` 里的便利工具：

```python
# set: distinct elements, O(1) average membership
seen = set()
seen.add(3)
if 3 in seen:            # O(1) average
    ...

# dict: key -> value
count = {}
count["a"] = 1
count["a"] += 1          # KeyError if "a" was absent; guard or use defaultdict
val = count.get("b", 0)  # O(1), returns default instead of raising

# defaultdict: no "is the key there yet" boilerplate
from collections import defaultdict

groups = defaultdict(list)          # missing key auto-creates an empty list
groups["cat"].append(1)             # no setdefault, no membership check

freq = defaultdict(int)             # missing key defaults to 0
for ch in "banana":
    freq[ch] += 1                   # just works on first sight

# Counter: a dict subclass that counts for you
from collections import Counter

c = Counter("banana")               # O(n): {'a': 3, 'n': 2, 'b': 1}
top2 = c.most_common(2)             # O(n log 2): [('a', 3), ('n', 2)]
```

可哈希性。键必须是可哈希的，实践中这意味着不可变：数字、字符串、以及由不可变元素构成的元组都可以；list、set 和 dict 不行，因为它们的内容会变，而一个键的哈希在它被存储期间绝不能改变。这就是为什么你把坐标存成元组。

```python
visited = set()
visited.add((r, c))          # tuple: hashable, correct for a grid cell
# visited.add([r, c])        # TypeError: unhashable type 'list'

# A frozenset is the hashable, immutable set, so you can key on a group of items
seen_groups = set()
seen_groups.add(frozenset({"a", "b"}))
```

经典的两数之和，原型题：把一次 O(n^2) 的配对搜索变成 O(n)，办法是记住你已见过的东西，再向哈希表询问那个补数。

```python
def two_sum(nums, target):
    seen = {}                         # value -> index
    for i, x in enumerate(nums):
        if target - x in seen:        # O(1) average lookup
            return [seen[target - x], i]
        seen[x] = i
    return []
```

插入顺序。自 Python 3.7 起，`dict` 保留插入顺序成为一项语言层面的保证（在 3.6 里这还只是实现细节）。遍历会按键首次插入的顺序产出它们。这偶尔就是整个诀窍所在：一个 LRU 缓存就是一个在访问时重新插入的 dict，于是最旧的键坐在最前面，`next(iter(d))` 给你淘汰候选者。

```python
d = {}
d["x"] = 1
d["y"] = 2
d["z"] = 3
list(d)                    # ['x', 'y', 'z'], first-inserted first
oldest = next(iter(d))     # 'x', front of the insertion order
```

## 何时用（何时不用）

在以下情况使用哈希集合或哈希表：

- 你反复地问「我以前见过这个吗」或「这个存在吗」。那是 O(1) 平均成员判断，对比 list 上的 O(n)。
- 你把键映射到值：按 id 索引、统计出现次数、缓存一个算好的结果、给递归做记忆化。
- 你需要去重。`set(iterable)` 一趟 O(n) 搞定。
- 你在把一次 O(n^2) 的「两两比较」变成 O(n)，靠的是记住补数或已见状态（两数之和、和为 k 的子数组、最长连续序列）。

在以下情况改选别的结构：

- 你需要按值排序，或反复取最小/最大值。dict 按值是无序的；用[堆](05-heap.md)取极值，或用平衡树取有序。
- 你需要区间查询（「a 和 b 之间的所有键」）。哈希破坏了顺序；用有序结构或[树/BST](06-tree-bst.md)。
- 键不可哈希（可变）。转成元组或 frozenset，或者重新思考。
- 内存紧张且 n 很小。哈希表的常数因子和桶开销，在 n 极小时可能输给一次朴素的数组扫描。

## 权衡与陷阱

- **「O(1)」是平均，不是保证。** 对抗性的键或糟糕的哈希会逼出 O(n)。它在面试数据上几乎从不咬人，但要知道这条注意事项。
- **不可哈希的键。** list 和 dict 不能当键或集合成员。把坐标存成 `(r, c)` 元组；对顺序无关的分组键用 `frozenset`。
- **`d[k]` 会抛异常，`d.get(k)` 不会。** 用 `[]` 去取一个缺失的键会抛 `KeyError`。当缺失是正常情况时，用 `.get(k, default)` 或 `defaultdict`。
- **`defaultdict` 在读取时插入。** 仅仅读一下 `dd[missing]` 就会用默认值创建那个键。之后遍历 `.items()`，你会看到从没显式设过的键。如果想窥视而不插入，用 `.get`。
- **遍历顺序是插入顺序，不是排序顺序。** 别假设 dict 是排好序的；它保留你添加键的顺序，那是另一回事。
- **一个由 list 构成的 set 是不可能的。** 先把内层 list 转成元组。
- **给 `Counter` 做差时的尺寸问题。** `Counter` 减法用 `-` 会静默丢弃非正的计数，但用 `.subtract()` 会保留它们。有意识地做选择。

## 相关模式

哈希表是大多数 O(n) 化简背后的主力：

- [哈希](../patterns/04-hashing.md)是直接建立在这个结构之上的模式：已见集合、补数映射、频率字典、按算出的键分组。
- [滑动窗口](../patterns/02-sliding-window.md)用一个 dict 或 Counter 来追踪当前窗口内字符或元素的频率，每步 O(1)。
- [前缀和](../patterns/03-prefix-sum.md)与哈希表搭档解决「统计和为 k 的子数组」：存下每个前缀和的频率，再查那个补数。
- [双指针](../patterns/01-two-pointers.md)是有序输入下的替代方案；当你无法排序时，哈希表就是你用 O(n) 解决同一问题的办法。
- [设计](../patterns/28-design.md)类问题（LRU 缓存、O(1) 的插入-删除-getRandom）依赖 dict 的 O(1) 操作外加它的插入顺序保证。
- 想看平均与最坏的开销分列，参见[复杂度速查表](../complexity.md)。
