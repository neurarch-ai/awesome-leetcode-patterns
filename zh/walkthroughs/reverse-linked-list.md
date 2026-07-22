# 精解：反转链表 (LC 206)

> 中文版。English: [reverse-linked-list](../../walkthroughs/reverse-linked-list.md)

一个从头到尾在一道题上跑完六步框架的例题。目标是展示过程，而不只是答案。

## 题目

**LeetCode 206，简单。** 给定一个单链表的头节点 `head`，反转链表并返回新的头。每个节点有一个值和一个 `next` 指针；最后一个节点指向 `None`。

例子：`1 -> 2 -> 3 -> 4 -> 5` 变成 `5 -> 4 -> 3 -> 2 -> 1`。

![原地指针反转](../../assets/linked-list.svg)

*原地指针反转。完整模式见下方链接的文件。*

## 1. 厘清与复述

我会问的问题：

- **输入类型。** 由头节点给出的一个单链表。每个节点暴露 `.val` 和 `.next`。它是单向链接的，所以没有回指指针：从一个节点我只能到达它后面那个，而不能到达它前面那个。正是这一个事实让问题变得不平凡。
- **我要返回什么？** 反转后链表的头，也就是原来的尾。
- **原地还是新链表？** 期望的答案是就地反转指针、不分配新节点，给出 O(1) 额外空间。我也可以构建一个全新的链表，但那浪费内存、也偏离了重点。
- **约束。** 链表长度在 0 到 `5000` 之间。很小，所以长度不是这里有意思的约束；挑战在于指针操作，而不是渐近复杂度。
- **边界情况。** **空链表**（`head` 是 `None`）；**单个节点**（单元素链表反转后是它自己）；两节点链表（指针真正翻转的最小情形）。递归变体在长度 5000 时还有一个**栈深度**的顾虑，值得点出来。

复述：走一趟链表，把每个 `next` 指针翻转为指向后方，返回旧的最后一个节点作为新头，只用常数个额外指针。

## 2. 手算一个例子

`1 -> 2 -> 3`。诀窍在于，一旦我把一个节点的 `next` 重定向为指向后方，我就失去了唯一的前进方式，除非我先把它保存下来。所以我携带三个引用：`prev`（已反转的部分，在我身后）、`curr`（我正在翻转的节点）、`nxt`（链表的其余部分，在我覆写指针之前保存下来）。

开始：`prev = None`，`curr = 1`。

- 保存 `nxt = 2`。翻转 `1.next = prev = None`。向前滑动：`prev = 1`，`curr = 2`。目前已反转的部分：`1 -> None`。
- 保存 `nxt = 3`。翻转 `2.next = prev = 1`。滑动：`prev = 2`，`curr = 3`。已反转：`2 -> 1 -> None`。
- 保存 `nxt = None`。翻转 `3.next = prev = 2`。滑动：`prev = 3`，`curr = None`。已反转：`3 -> 2 -> 1 -> None`。

`curr` 现在是 `None`，所以我停下。`prev` 是 3，新的头。关键观察：如果不在翻转前保存 `nxt`，第一步就会把 `1.next` 设为 `None`，我就再也没有办法到达节点 2 了。

## 3. 暴力解

这里没什么慢与快的轴线；朴素方法并不更慢，它只是浪费空间。一个直接的版本把值收集进一个数组，然后从反转后的数组重建一个全新的链表。

```python
def reverse_list_brute(head):
    vals = []
    node = head
    while node:
        vals.append(node.val)
        node = node.next
    dummy = ListNode()
    tail = dummy
    for v in reversed(vals):
        tail.next = ListNode(v)
        tail = tail.next
    return dummy.next
```

这是 **O(n)** 时间但 **O(n)** 额外空间，用于值数组加上一整套新分配的节点。它能用，但为了反转第一个链表而分配第二个链表，正是面试官想看你去掉的那种浪费。

## 4. 找到瓶颈并挑选模式

暴力解花 O(n) 内存来持有链表的一份副本，但反转其实并不需要副本。节点已经以正确的顺序在内存里了；需要改变的只是每个 `next` 指针指向的方向。那个重构，「修改现有的指针而不是重建」，就是**链表原地反转**模式。

这个模式消除的瓶颈是额外的存储。机制是第 2 步的三指针滑动：`prev`、`curr`、`nxt`。在每个节点我恰好做四个常数时间操作，保存下一个节点、把当前节点重定向到后方、推进 `prev`、推进 `curr`。不分配，一趟。之所以需要小心，恰恰是因为单向链接的约束：因为我不能往回走，我必须在覆写 `curr.next` 之前把 `nxt` 藏好，否则我就把链表的其余部分弄丢了。

## 5. 写出代码

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def reverse_list(head):
    prev = None                 # reversed portion, initially empty
    curr = head                 # node currently being flipped
    while curr:
        nxt = curr.next         # save the rest before we clobber the pointer
        curr.next = prev        # flip this node to point backward
        prev = curr             # prev advances into the reversed portion
        curr = nxt              # curr advances into the untouched portion
    return prev                 # prev is the old tail, the new head
```

循环内那四行的顺序没有商量余地。`nxt = curr.next` 必须放在最前，因为紧接的下一行就摧毁了 `curr.next`。然后那两个推进把窗口向前滑动一步。循环不变式：在每次迭代的顶部，`prev` 是 `curr` 之前所有节点正确反转后的链表之头，而 `curr` 是未触碰的余下部分之头。当 `curr` 到达 `None` 时，整个链表已被反转，`prev` 是它的头。

一个递归版本先反转尾部，再把当前节点挂到末尾：

```python
def reverse_list_rec(head):
    if head is None or head.next is None:
        return head             # empty or single node reverses to itself
    new_head = reverse_list_rec(head.next)
    head.next.next = head       # the node after head now points back at head
    head.next = None            # head becomes the new tail
    return new_head
```

递归很优雅，但用 **O(n) 栈**空间，在长度 5000 时有很深的调用栈的风险，所以我会以迭代版本打头，把递归版本作为替代方案提一下。

## 6. 测试、追踪与分析

用迭代代码追踪 `1 -> 2 -> 3 -> 4 -> 5`。

| 步 | curr | nxt（已保存） | 动作 | 之后的 prev |
|------|------|-------------|--------|------------|
| 1 | 1 | 2 | 1.next = None | 1 -> None |
| 2 | 2 | 3 | 2.next = 1 | 2 -> 1 -> None |
| 3 | 3 | 4 | 3.next = 2 | 3 -> 2 -> 1 -> None |
| 4 | 4 | 5 | 4.next = 3 | 4 -> 3 -> 2 -> 1 -> None |
| 5 | 5 | None | 5.next = 4 | 5 -> 4 -> 3 -> 2 -> 1 -> None |

`curr` 变成 `None`，循环结束，返回 `prev`，它是 `5 -> 4 -> 3 -> 2 -> 1` 的头。与手算答案吻合。

边界情况：
- **空链表**，`head = None`：`curr` 从 `None` 起步，循环体从不执行，我们返回仍是 `None` 的 `prev`。正确，空链表的反转是空。
- **单个节点**，`head = 7`：一次迭代保存 `nxt = None`，设置 `7.next = None`（不变），推进 `prev = 7`、`curr = None`，循环结束，返回 7。正确，单元素链表反转后是它自己。
- **两个节点**，`1 -> 2`：第一次翻转设 `1.next = None`，第二次设 `2.next = 1`，返回 `2 -> 1`。这是指针真正改变方向的最小情形。

**复杂度：O(n) 时间**，一趟扫描，恰好触碰每个节点一次、每个节点做常数工作，以及迭代版本的 **O(1) 额外空间**（不论链表多长，只有那三个指针）。递归版本也是 O(n) 时间，但由于调用栈有 **O(n) 空间**。

时间更充裕的话，我会指出这套指针腾挪的例程是更难问题的构件：反转两个位置之间的子链表（LC 92）、每 k 个一组反转（LC 25）、以及回文判断链表，都复用这个完全一样的三指针翻转。

## 面试官真正考察的是什么

你能否在不弄丢链表的前提下操作指针，这归结为一个习惯：在覆写 `next` 之前把它保存下来。单向链接的约束意味着一次不小心的赋值就会把下游的一切弄丢，所以这个考察其实是关于有纪律、有次序的指针更新，以及把循环不变式记在脑子里。伸手去抓 O(n) 值数组的候选人暴露出他们没有内化原地指针操作；强的信号是点名那三个指针、说清为什么必须先保存 `nxt`、并用一趟干净的扫描漂亮地完成反转。

> 模式：[10 链表](../patterns/10-linked-list.md)
