# 14 - Binary search tree

> **Problem shape:** "Validate that this binary tree is a BST." "Find the kth
> smallest element." "Search, insert, or delete a value." "Find two nodes that sum
> to a target." "Which values fall in the range [low, high]?" Anything on a binary
> tree where an ordering invariant lets you skip half the tree at each step.

A binary search tree encodes sorted order in its shape: for every node, all keys in
the left subtree are smaller and all keys in the right subtree are larger. That one
invariant gives O(h) search, insert, and delete, and makes an inorder traversal
emit the keys in sorted order, which is the backbone of most BST problems.

## The signal

Reach for BST-specific reasoning when:

- **The problem states the tree is a BST** (or asks you to validate one). The
  ordering is a tool: never traverse the whole tree when the invariant lets you
  pick a side.
- **"Kth smallest / kth largest", "the sorted order", "in-order successor"**:
  these are inorder-traversal problems, because inorder on a BST is a sorted scan.
- **"Search / insert / delete a value", "closest value", "floor / ceiling"**: you
  walk one root-to-leaf path, branching left or right by comparison, in O(h).
- **"All keys in a range [low, high]"**: prune entire subtrees that cannot contain
  in-range keys, so you touch only the relevant band.
- **"Lowest common ancestor in a BST"**: the split point where the two targets
  diverge (one goes left, one goes right) is the LCA, found in O(h) without a full
  DFS.

If the tree is *not* a BST, none of this applies and you fall back to generic
[tree DFS](12-tree-dfs.md) or [tree BFS](13-tree-bfs.md).

## The idea

The BST invariant is recursive: it must hold at *every* node, not just locally. A
node whose immediate children obey `left < node < right` can still violate the
invariant if a deep-left descendant exceeds the node. That is why validation uses
**recursive bounds**: each node must lie strictly inside an open interval `(low,
high)` that tightens as you descend. Going left lowers the upper bound to the
current value; going right raises the lower bound to it.

The second pillar is that **inorder traversal yields sorted order**. Visit left,
then the node, then right, and values come out ascending. This turns "kth smallest"
into "stop at the kth emitted value", "validate BST" into "check the sequence is
strictly increasing", and "two-sum in a BST" into two-pointers over the sorted
stream.

Search, insert, and delete all walk a single path guided by comparison, so they
cost O(h): O(log n) on a balanced tree, O(n) on a degenerate (linked-list-shaped)
one.

## The template

**Validate a BST with recursive bounds (the correct, deep-safe way):**

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def is_valid_bst(root, low=float('-inf'), high=float('inf')):
    if not root:
        return True                              # empty subtree is valid
    if not (low < root.val < high):              # must fit the open interval
        return False
    return (is_valid_bst(root.left, low, root.val) and
            is_valid_bst(root.right, root.val, high))
```

**Kth smallest via inorder, stopping early:**

```python
def kth_smallest(root, k):
    stack = []
    node = root
    while stack or node:
        while node:                # go as far left as possible
            stack.append(node)
            node = node.left
        node = stack.pop()         # smallest unvisited
        k -= 1
        if k == 0:
            return node.val
        node = node.right          # then the right subtree
```

**Search and insert (single-path walks):**

```python
def search_bst(root, target):
    while root and root.val != target:
        root = root.left if target < root.val else root.right
    return root

def insert_bst(root, val):
    if not root:
        return TreeNode(val)                     # found the empty slot
    if val < root.val:
        root.left = insert_bst(root.left, val)
    else:
        root.right = insert_bst(root.right, val)
    return root
```

**Delete (the three-case node with the successor swap):**

```python
def delete_bst(root, key):
    if not root:
        return None
    if key < root.val:
        root.left = delete_bst(root.left, key)
    elif key > root.val:
        root.right = delete_bst(root.right, key)
    else:                                        # found the node to remove
        if not root.left:                        # 0 or 1 child: splice up
            return root.right
        if not root.right:
            return root.left
        succ = root.right                        # 2 children: inorder successor
        while succ.left:
            succ = succ.left
        root.val = succ.val                      # copy successor value in
        root.right = delete_bst(root.right, succ.val)  # delete successor
    return root
```

## Variations

- **Range sum / range keys.** DFS but prune: if `node.val < low`, skip the whole
  left subtree; if `node.val > high`, skip the right. Only descend into subtrees
  that can hold in-range keys.
- **Two-sum in a BST.** Run inorder to get a sorted array, then two-pointer it. Or,
  to save space, use an inorder iterator and a reverse-inorder iterator as the two
  pointers directly on the tree.
- **Closest value / floor / ceiling.** Single-path walk, updating the best
  candidate as you branch; the answer is always on the path from root to the
  insertion point.
- **LCA of a BST.** Walk from the root: while both targets are less than the node
  go left, while both are greater go right; the first node that splits them (or
  equals one of them) is the LCA. O(h), no recursion into both sides.
- **Build a balanced BST from a sorted array.** Pick the middle as the root,
  recurse on halves. Guarantees O(log n) height. The inverse of "inorder gives
  sorted order".
- **In-order successor / predecessor.** Successor is the leftmost node of the right
  subtree, or the lowest ancestor for which the node is in the left subtree.

## Canonical problems

| # | Problem | Difficulty | What it drills |
|---|---------|-----------|----------------|
| 700 | Search in a Binary Search Tree | Easy | Single-path comparison walk |
| 98 | Validate Binary Search Tree | Medium | Recursive open-interval bounds |
| 230 | Kth Smallest Element in a BST | Medium | Inorder with an early stop |
| 701 | Insert into a Binary Search Tree | Medium | Recurse to the empty slot |
| 450 | Delete Node in a BST | Medium | Three cases, successor swap |
| 235 | Lowest Common Ancestor of a BST | Medium | Split point via comparison |
| 653 | Two Sum IV - Input is a BST | Easy | Inorder to sorted, then two pointers |
| 938 | Range Sum of BST | Easy | Prune subtrees out of range |
| 108 | Convert Sorted Array to Binary Search Tree | Easy | Middle-as-root for balance |

## Pitfalls

- **Validating with only local comparisons.** Checking `left.val < node.val <
  right.val` per node is wrong: a far-down-left node can exceed a high ancestor.
  You must carry min/max bounds down the recursion.
- **Non-strict bounds when duplicates matter.** Standard BST validation is strict
  (`low < val < high`). If the problem allows duplicates, decide up front which
  side they live on and adjust the inequality consistently.
- **Using `float('inf')` incorrectly at boundaries.** Node values can be
  `INT_MIN`/`INT_MAX`; use `-inf`/`+inf` (or `None` sentinels) as the initial
  bounds so real extreme values still pass.
- **Deleting a two-child node wrong.** You must replace it with its inorder
  successor (or predecessor) and then delete that successor, not just detach a
  child, or you break the ordering.
- **Assuming O(log n).** A BST built from sorted inserts degenerates to a linked
  list, making every operation O(n). If balance matters, a self-balancing tree
  (AVL, red-black) is the real answer, but interviews rarely ask you to code one.
- **Forgetting inorder is ascending, reverse-inorder is descending.** Right, node,
  left gives you kth *largest* for free.

## Follow-ups and related patterns

- "Now the tree is not a BST" drops you back to generic [tree DFS](12-tree-dfs.md)
  for aggregates and [tree BFS](13-tree-bfs.md) for level structure.
- "Keep it balanced under many inserts and deletes" points to self-balancing trees;
  in practice interviewers pivot to a [heap](24-heap.md) or a sorted container.
- The single-path comparison walk is [binary search](07-binary-search.md) realized
  as a data structure: each step discards one subtree, just as binary search
  discards half an array.
- "Support order-statistics queries (rank, select) at scale" points to augmented
  BSTs or a Fenwick / segment tree, adjacent to the range structures in
  [prefix sum](03-prefix-sum.md).
