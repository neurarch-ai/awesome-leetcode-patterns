# 04 - Linked list

A linked list stores elements as separate nodes, each holding a value and a
pointer to the next node. There is no contiguous block of memory and no index:
to reach the k-th element you walk k pointers from the head. That single fact,
no random access, is what you trade away, and in return you get O(1) insert and
delete anywhere in the list, provided you already hold the node. Almost every
linked-list interview problem is really about pointer discipline: not losing the
rest of the list when you rewire a link.

## What it is

A **singly linked list** is a chain of nodes. Each node holds a value and a
`next` reference to the following node; the last node points at `None`. You keep
a `head` reference to the first node, and that is the only handle you have into
the structure. To find anything you follow `next` pointers from the head.

A **doubly linked list** adds a `prev` pointer to each node, so you can walk
backward as well as forward, and you can delete a node given only that node (you
reach its neighbor on both sides through `prev` and `next`). The cost is one
extra pointer per node to store and to keep consistent on every splice.

The defining property is that nodes are not laid out contiguously in memory.
There is no arithmetic that turns an index into an address, so there is no O(1)
`a[i]`. What you get instead: inserting or deleting a node does not shift any
other element, it just rewires a couple of pointers. An array insert in the
middle is O(n) because the tail must slide over; a linked-list splice is O(1)
because nothing moves.

## Operations and complexity

For a list of n nodes:

| Operation | Cost | Note |
|---|---|---|
| Access / index the k-th node | O(n) | Walk k `next` pointers from the head; no random access |
| Search for a value | O(n) | Linear scan, same as an unsorted array |
| Insert at head (prepend) | O(1) | Rewire `head`; nothing shifts |
| Insert at tail | O(1) with a tail pointer, else O(n) | O(n) if you must walk to find the tail |
| Insert / delete GIVEN the node | O(1) | The whole point: splice two pointers |
| Insert / delete at a position i | O(n) | Dominated by the O(n) walk to find the node |
| Delete given only the node (singly) | O(1) trick | Copy the next node's value in and skip it; fails on the tail |
| Delete given only the node (doubly) | O(1) | `prev` and `next` are both in hand |
| Length | O(n) | Not stored; you count unless you track it separately |

The theme: the mutation itself is O(1), but *locating* the node is O(n). When a
problem hands you the node (or you already hold a pointer to it from a previous
step), you get the O(1) benefit. When you must search first, the search cost
dominates and you are back to O(n). See the
[complexity cheat sheet](../complexity.md) for how this compares against a list.

## Python implementation

Python has no built-in linked list you use in interviews (`collections.deque` is
a doubly linked list under the hood, but you never touch its nodes). You define
the node yourself. The canonical `ListNode`:

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
```

Insert and delete given a node, the O(1) operations:

```python
def insert_after(node, val):
    # Splice a new node in after `node`. O(1), nothing else moves.
    node.next = ListNode(val, node.next)

def delete_after(node):
    # Remove node.next by skipping it. O(1).
    if node.next:
        node.next = node.next.next
```

The **dummy-head sentinel** is the trick that removes almost every edge case.
Instead of special-casing "what if I delete the head" or "what if the list is
empty", you prepend a throwaway node and always operate one step behind it. The
real answer is `dummy.next` at the end:

```python
def remove_all(head, target):
    dummy = ListNode(0, head)   # sentinel sits before the real head
    prev = dummy
    while prev.next:
        if prev.next.val == target:
            prev.next = prev.next.next   # unlink; works even for the head
        else:
            prev = prev.next
    return dummy.next           # the head may have changed; this is safe
```

Without the sentinel you would need a separate branch for deleting the head node,
because there is no `prev` in front of it. With the sentinel there always is.

Reversing a singly linked list in place is the pointer-discipline exercise every
interview expects, O(n) time and O(1) space:

```python
def reverse(head):
    prev = None
    curr = head
    while curr:
        nxt = curr.next     # save the rest before you overwrite the link
        curr.next = prev    # reverse this one pointer
        prev = curr         # advance both pointers
        curr = nxt
    return prev             # prev is the new head
```

The `nxt = curr.next` line is load-bearing: once you overwrite `curr.next` you
have lost your only reference to the remainder of the list, so you must stash it
first.

## When to use it (and when not)

**Use a linked list when:**

- You insert and delete in the middle frequently and you already hold the node,
  so you get the O(1) splice with no shifting. An LRU cache is the canonical
  case: a doubly linked list gives O(1) move-to-front and eviction, and a hash
  map gives O(1) lookup of the node.
- You are building a stack or queue and want guaranteed O(1) ends with no
  amortized reallocation. (In Python you would just use a `deque`, which is one.)
- The problem literally hands you nodes and asks you to rewire them: reverse,
  merge, detect a cycle, reorder. These are linked-list problems by construction.

**Do not use a linked list when:**

- You need random access or binary search. Indexing is O(n), so binary search on
  a linked list is O(n) per step and pointless. Use an array.
- You iterate a lot and care about speed. Nodes are scattered in memory, so you
  get no cache locality; an array walk is dramatically faster in practice even
  though both are O(n).
- You just need a resizable sequence. A Python `list` (dynamic array) is simpler,
  denser, and O(1) amortized append. Reach for the list by default.

## Tradeoffs and gotchas

**Array vs linked list, the honest comparison.** An array gives O(1) indexed
access and cache-friendly iteration but O(n) insert/delete in the middle because
elements shift. A linked list gives O(1) insert/delete given the node but O(n)
access and poor locality. Neither dominates: pick by which operation you do most.
In interviews the linked list wins only when the O(1)-splice-given-the-node
property is the crux (LRU cache, in-place reordering); otherwise the array wins.

**The O(1)-delete-given-a-node trick has a catch.** In a singly linked list, if
you are given only a node to delete and not its predecessor, you cannot rewire
`prev.next`. The workaround is to copy the *next* node's value into the current
node and delete the next node instead. It works for O(1), but it fails on the
tail node (there is no next to copy from), and it is a value copy, not a true
unlink.

**Losing the rest of the list.** The number-one bug: overwriting a `next` pointer
before saving what it pointed to. Always stash `curr.next` in a temp before you
reassign it during a reversal or reorder.

**Cycles.** A corrupted or intentionally cyclic list makes a naive traversal loop
forever. Detect cycles with Floyd's fast-and-slow pointers (two walkers, one
moving twice as fast; they meet inside a cycle) in O(n) time and O(1) space.

**Length is not free.** There is no stored count. If you need the length, you
walk the list (O(n)) or maintain a counter yourself on every insert and delete.

## Related patterns

- [Linked list techniques](../patterns/10-linked-list.md): reversal, merge,
  fast-and-slow pointers, cycle detection, the dummy-head sentinel in anger.
- [Two pointers](../patterns/01-two-pointers.md): the fast-and-slow idea is the
  two-pointer method adapted to a structure you cannot index.
- [Stack, queue, and deque](03-stack-queue.md): a deque is a doubly linked list;
  this is what you actually use in Python instead of hand-rolling nodes.
- [Complexity cheat sheet](../complexity.md): the operation-cost table to keep
  open when you argue about array vs linked list.
