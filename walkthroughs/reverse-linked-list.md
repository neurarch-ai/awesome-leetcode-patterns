# Walkthrough: Reverse Linked List (LC 206)

A worked example that runs the six-step framework on one problem end to end.
The goal is to show the process, not just the answer.

## The problem

**LeetCode 206, Easy.** Given the `head` of a singly linked list, reverse the list
and return the new head. Each node has a value and a `next` pointer; the last node
points at `None`.

Example: `1 -> 2 -> 3 -> 4 -> 5` becomes `5 -> 4 -> 3 -> 2 -> 1`.

![In-place pointer reversal](../assets/linked-list.svg)

*In-place pointer reversal. See the full pattern in the linked file below.*

## 1. Clarify and restate

The questions I would ask:

- **Input type.** A singly linked list given by its head node. Each node exposes
  `.val` and `.next`. It is singly linked, so there are no back pointers: from a
  node I can only reach the one after it, not the one before it. That single fact
  is what makes the problem non-trivial.
- **What do I return?** The head of the reversed list, which is the original tail.
- **In place or new list?** The expected answer reverses the pointers in place and
  allocates no new nodes, giving O(1) extra space. I could also build a fresh list,
  but that wastes memory and misses the point.
- **Constraints.** The list length is between 0 and `5000`. Small, so the length is
  not the interesting constraint here; the challenge is the pointer manipulation,
  not the asymptotics.
- **Edge cases.** The **empty list** (`head` is `None`); a **single node** (reverse
  of a one-element list is itself); a two-node list (the smallest case where a
  pointer actually flips). The recursive variant also has a **stack depth** concern
  at length 5000, worth naming.

Restated: walk the list once and flip every `next` pointer to point backward,
returning the old last node as the new head, using only a constant number of extra
pointers.

## 2. Work an example by hand

`1 -> 2 -> 3`. The trick is that the moment I redirect a node's `next` to point
backward, I lose my only way forward unless I saved it first. So I carry three
references: `prev` (the part already reversed, behind me), `curr` (the node I am
flipping now), and `nxt` (the rest of the list, saved before I clobber the
pointer).

Start: `prev = None`, `curr = 1`.

- Save `nxt = 2`. Flip `1.next = prev = None`. Slide forward: `prev = 1`,
  `curr = 2`. Reversed portion so far: `1 -> None`.
- Save `nxt = 3`. Flip `2.next = prev = 1`. Slide: `prev = 2`, `curr = 3`.
  Reversed: `2 -> 1 -> None`.
- Save `nxt = None`. Flip `3.next = prev = 2`. Slide: `prev = 3`, `curr = None`.
  Reversed: `3 -> 2 -> 1 -> None`.

`curr` is now `None`, so I stop. `prev` is 3, the new head. The key observation:
without saving `nxt` before the flip, step one would set `1.next = None` and I
would have no way to ever reach node 2.

## 3. Brute force

There is not much of a slow-versus-fast axis here; the naive approach is not
slower, it just wastes space. One straightforward version collects the values into
an array, then rebuilds a brand new list from the reversed array.

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

This is **O(n)** time but **O(n)** extra space for the value array plus a whole set
of freshly allocated nodes. It works, but allocating a second list to reverse the
first is exactly the waste an interviewer wants to see you remove.

## 4. Find the bottleneck and pick the pattern

The brute force spends O(n) memory to hold a copy of the list, but reversing does
not actually need a copy. The nodes are already in memory in the right order; all
that has to change is the direction each `next` pointer points. That reframing,
"mutate the existing pointers rather than rebuild", is the **linked list in place
reversal** pattern.

The bottleneck the pattern removes is the extra storage. The mechanism is the
three-pointer slide from step 2: `prev`, `curr`, `nxt`. At each node I do exactly
four constant-time operations, save the next node, redirect the current node
backward, advance `prev`, advance `curr`. No allocation, one pass. The reason this
needs care is precisely the singly linked constraint: because I cannot walk
backward, I must stash `nxt` before overwriting `curr.next`, or I strand the rest
of the list.

## 5. Code it

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

The order of the four lines inside the loop is not negotiable. `nxt = curr.next`
must come first, because the very next line destroys `curr.next`. Then the two
advances slide the window forward by one. The loop invariant: at the top of each
iteration, `prev` heads a correctly reversed list of everything before `curr`, and
`curr` heads the untouched remainder. When `curr` reaches `None`, the whole list is
reversed and `prev` is its head.

A recursive version reverses the tail first, then hooks the current node onto the
end:

```python
def reverse_list_rec(head):
    if head is None or head.next is None:
        return head             # empty or single node reverses to itself
    new_head = reverse_list_rec(head.next)
    head.next.next = head       # the node after head now points back at head
    head.next = None            # head becomes the new tail
    return new_head
```

The recursion is elegant but uses **O(n) stack** space, and at length 5000 that
risks a deep call stack, so I would lead with the iterative version and mention the
recursive one as an alternative.

## 6. Test, trace, and analyze

Trace `1 -> 2 -> 3 -> 4 -> 5` through the iterative code.

| step | curr | nxt (saved) | action | prev after |
|------|------|-------------|--------|------------|
| 1 | 1 | 2 | 1.next = None | 1 -> None |
| 2 | 2 | 3 | 2.next = 1 | 2 -> 1 -> None |
| 3 | 3 | 4 | 3.next = 2 | 3 -> 2 -> 1 -> None |
| 4 | 4 | 5 | 4.next = 3 | 4 -> 3 -> 2 -> 1 -> None |
| 5 | 5 | None | 5.next = 4 | 5 -> 4 -> 3 -> 2 -> 1 -> None |

`curr` becomes `None`, loop ends, return `prev` which heads `5 -> 4 -> 3 -> 2 -> 1`.
Matches the hand answer.

Edge cases:
- **Empty list**, `head = None`: `curr` starts `None`, the loop body never runs, we
  return `prev` which is still `None`. Correct, the reverse of an empty list is
  empty.
- **Single node**, `head = 7`: one iteration saves `nxt = None`, sets `7.next =
  None` (unchanged), advances `prev = 7`, `curr = None`, loop ends, returns 7.
  Correct, a one-element list reverses to itself.
- **Two nodes**, `1 -> 2`: the first flip sets `1.next = None`, the second sets
  `2.next = 1`, returning `2 -> 1`. This is the smallest case where a pointer
  actually reverses direction.

**Complexity: O(n) time**, one pass touching each node exactly once with
constant work per node, and **O(1) extra space** for the iterative version (only
the three pointers, regardless of list length). The recursive version is also O(n)
time but **O(n) space** from the call stack.

With more time I would note that this pointer-juggling routine is the building
block for harder problems: reverse a sublist between two positions (LC 92), reverse
in groups of k (LC 25), and palindrome-check a list all reuse this exact three
pointer flip.

## What the interviewer is really testing

Whether you can manipulate pointers without losing the list, which comes down to
one habit: saving `next` before you overwrite it. The singly linked constraint
means a single careless assignment strands everything downstream, so the test is
really about disciplined, ordered pointer updates and holding the loop invariant in
your head. A candidate who reaches for an O(n) value array reveals they have not
internalized in-place pointer work; the strong signal is naming the three pointers,
stating why `nxt` must be saved first, and landing the reversal in one clean pass.

> Pattern: [10 linked list](../patterns/10-linked-list.md)
