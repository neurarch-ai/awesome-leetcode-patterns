# 06 - 循环排序与「下标即哈希」
> 中文版。English: [06-cyclic-sort](../patterns/06-cyclic-sort.md)

> **问题形态：** 「一个数组存放着 1 到 n 这些数，缺了一个，把它找出来。」「在一个含 n+1 个、取值范围为 1 到 n 的数组里找出那个重复的数。」「找出所有消失的数字。」「最小的缺失正整数。」当值就是（或映射进）下标范围，而你想要 O(n) 时间加 O(1) 额外空间时，数组本身就是它自己的哈希表。

循环排序利用一个特殊的承诺：这些值是 `1..n` 的一个排列（或近似排列），因此每个值都有一个归属下标。一趟就把每个值放到它的归属处，会让缺失和重复的数字按位置自然显露，达到 O(n) 时间、O(1) 空间，无需哈希集合。符号标记变体做同样的把戏，甚至不移动元素，靠的是用 `a[index]` 的符号位当作访问标志。

![循环排序把一个值交换到它的归属下标](../assets/cyclic-sort.svg)

*把每个值放到它的下标处；那唯一一个仍然不对的槽位揭示出缺失或重复的数。*

## 信号特征

看到以下情形时，考虑使用循环排序或「下标即哈希」：

- **值被限定在 `1..n`（或 `0..n-1`）**，在一个长度约为 `n` 的数组里。值与下标之间的这个双射就是全部前提。
- **「找出缺失 / 重复 / 消失的数字」**，在这样一个数组里，而后续要求 **O(1) 额外空间**（所以哈希集合被排除）。
- **「第一个缺失的正数」**，你必须忽略越界的杂物，却仍要在线性时间、常数空间内找出最小的缺席正数。
- **一个暗示你可以修改数组**（重排它，或翻转符号）的提示，正是这一点为你换来 O(1) 空间。

判断依据：题目实际上直接把一个已知范围的排列交到你手上，并且专门要求常数额外空间，这就排除了显而易见的哈希集合答案，指向用数组自己的下标作为桶。

## 核心思想

如果一个数组是 `1..n` 的排列，那么值 `v` 归属于下标 `v - 1`。循环排序遍历数组，每当 `a[i]` 尚未在它的归属下标处时，就把它交换过去。每次交换都至少把一个值永久放回家，因此交换总数至多为 `n`：尽管内含一个嵌套的 `while`，这趟遍历仍是 O(n)。遍历结束后，第一个满足 `a[i] != i + 1` 的下标 `i`，恰好就是某个数缺失或出错的地方，缺失和重复的值就是这样按位置显露自己的。

「下标即哈希」（符号标记）变体避免移动任何东西。要记录「我见过值 `v`」，就把 `a[abs(v) - 1]` 的符号翻成负。一趟之后，任何仍持有正值的下标从未被访问过，所以 `index + 1` 是缺失的；一个你试图标记两次的下标则揭示出一个重复。你用 `abs()` 读取幅值，因为符号如今携带的是访问位，而非值。这是一张真正的哈希表，建在数组内部，用每个槽位的符号作为它那一位元数据。

两者都给出 O(n) 时间、O(1) 额外空间，胜过哈希集合的 O(n) 空间，代价是修改了输入。

## 模板

**循环排序（把每个值放到它的归属下标处）：**

```python
# Time: O(n), Space: O(1)
def cyclic_sort(a):                 # a is a permutation of 1..n
    i = 0
    while i < len(a):
        home = a[i] - 1             # value v belongs at index v-1
        if a[i] != a[home]:         # not yet home: swap it there
            a[i], a[home] = a[home], a[i]
        else:
            i += 1                  # correct value here (or a dup): advance
    return a
```

**找出 0..n 中缺失的数字（按归属下标找缺失数）：**

```python
# Time: O(n), Space: O(1)
def missing_number(nums):           # values 0..n with one missing, length n
    i, n = 0, len(nums)
    while i < n:
        home = nums[i]
        if home < n and nums[i] != nums[home]:
            nums[i], nums[home] = nums[home], nums[i]
        else:
            i += 1
    for i in range(n):
        if nums[i] != i:            # first slot whose value is not its index
            return i
    return n
```

**用符号标记找出所有消失的数字（下标即哈希，不做交换）：**

```python
# Time: O(n), Space: O(1) auxiliary (the returned list is not counted)
def find_disappeared(nums):         # values 1..n, some appear twice
    for x in nums:
        idx = abs(x) - 1            # magnitude, sign is now a visited flag
        if nums[idx] > 0:
            nums[idx] = -nums[idx]  # mark "value idx+1 was seen"
    missing = [i + 1 for i, v in enumerate(nums) if v > 0]
    for i in range(len(nums)):      # restore signs if the caller needs the array
        nums[i] = abs(nums[i])
    return missing
```

**第一个缺失的正数（循环排序，忽略越界值）：**

```python
# Time: O(n), Space: O(1)
def first_missing_positive(nums):
    n = len(nums)
    i = 0
    while i < n:
        home = nums[i] - 1
        if 0 <= home < n and nums[i] != nums[home]:  # only place in-range values
            nums[i], nums[home] = nums[home], nums[i]
        else:
            i += 1
    for i in range(n):
        if nums[i] != i + 1:        # first index missing its home value
            return i + 1
    return n + 1                    # 1..n all present, answer is n+1
```

循环守卫是 `while i < n` 加一个有条件的 `i += 1`，而不是 `for`：只有当前槽位安定下来才推进，而一次交换可能带进一个仍需安置的值。

## 变体

- **单个缺失数字。** 要么循环排序再扫描，要么用 XOR / 求和技巧（`n*(n+1)/2 - sum`）。循环排序可推广到「所有缺失」；算术技巧不能。
- **重复数字。** 循环排序后，一个满足 `a[i] != i + 1` 的下标持有一个重复值（那个挤掉缺失数的值）。对「找出所有重复」，符号标记那一趟会报告任何你试图标记两次的下标。
- **不修改数组地找出重复（LeetCode 287）。** 当你不能修改数组时，把它重新表述为一个链表环，在 `next = a[i]` 上用 Floyd 的龟兔赛跑。那是 [快慢指针](10-linked-list.md) 模式，而非循环排序，它是预期中的 O(1) 空间、只读解法。
- **错误的集合（一个数重复，一个数缺失）。** 循环排序，然后那个唯一出错的下标同时给出重复数（它的值）和缺失数（它的下标 + 1）。
- **第一个缺失的正数。** 困难情形：安置期间忽略越界和非正的值，因此只有 `1..n` 重要，第一个未被填充的归属处就是答案。

## 经典题目

| # | 题目 | 难度 | 训练点 |
|---|---------|-----------|----------------|
| 268 | Missing Number | 简单 | 归属下标安置或 XOR 技巧 |
| 448 | Find All Numbers Disappeared in an Array | 简单 | 符号标记，收集为正的槽位 |
| 645 | Set Mismatch | 简单 | 一个出错下标同时给出重复和缺失 |
| 442 | Find All Duplicates in an Array | 中等 | 符号标记报告双重标记 |
| 287 | Find the Duplicate Number | 中等 | 只读：Floyd 环检测 |
| 41 | First Missing Positive | 困难 | 循环排序，忽略越界值 |
| 765 | Couples Holding Hands | 困难 | 循环交换贪心以修复一个排列 |
| 1539 | Kth Missing Positive Number | 简单 | 统计每个下标之前缺失的个数 |

## 陷阱

- **每一步都推进下标。** 用 `while i < n`，只有当槽位已经正确时才 `i += 1`。一个普通的 `for` 循环会破坏「交换可能带进另一个错位值」的逻辑。
- **重复值上的无限交换循环。** 用 `a[i] != a[home]`（而非 `a[i] != i + 1`）来守卫交换。比较「位置上的值」在目标槽位已经持有相同值（一个重复）时就停下，否则你会永远交换两个相等的值。
- **第一个缺失正数里的越界值。** 安置期间跳过任何不在 `1..n` 的值；试图安置像 `1000000` 或 `-3` 这样的值会破坏扫描或抛出下标错误。
- **符号标记下丢失了值。** 翻转符号后，你必须用 `abs()` 读取幅值，并在最后用 `abs()` 还原数组，如果调用方仍需要真实的数字。
- **零没有符号。** 符号标记无法记录对一个值为 0 的槽位的访问。移动范围，或当 0 是合法值时改用循环排序。
- **假设你可以修改。** 如果题目禁止修改输入（287），循环排序和符号标记都出局；退回到环检测。

## 延伸与相关模式

- 「你不能修改数组」把 287 变成一道在 `next = a[i]` 上的 [快慢指针](10-linked-list.md) 环检测问题。
- 「你可以用 O(n) 额外空间」让这整个家族变成一道平凡的 [哈希](04-hashing.md) 练习；循环排序恰恰是当哈希集合被禁用时你才伸手去拿的东西。
- 「统计每个下标之前缺失个数」的变体（1539），一旦你看出这个计数是单调的，就是一道 [二分查找](07-binary-search.md)。
- 把每个值放到它的归属下标处是一种受限的 [排序](08-sorting.md)：它之所以奏效，只是因为键是一个已知的稠密范围，正是这一点把它从 O(n log n) 降到 O(n)。
