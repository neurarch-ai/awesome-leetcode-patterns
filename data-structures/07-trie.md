# 07 - Trie (prefix tree)

A trie is a tree of characters. Each path from the root spells out a prefix, and a
whole word is just a path that ends on a node flagged as terminal. That single
idea, "share the common prefix instead of storing each word whole", is what turns
prefix questions from O(number of words) into O(length of the query). If you have
ever wanted autocomplete, a dictionary matcher, or "does any word start with this",
the trie is the structure that makes it cheap.

![A trie storing the words cat, car, dog with a shared prefix](../assets/trie.svg)

*A trie stores shared prefixes once, so a prefix query is O(length) regardless of dictionary size.*

## What it is

A trie stores a set of strings as a rooted tree. Every node holds a map from a
single character to a child node, plus an `is_end` boolean marking whether the path
from the root to this node spells a complete inserted word. The root itself spells
the empty string.

Inserting `"cat"` and `"car"` creates a shared `c -> a` spine, then the paths fork:
one child `t` (with `is_end = True`), one child `r` (with `is_end = True`). The
shared prefix `ca` is stored exactly once. That sharing is the whole point: the
tree's shape is the set of prefixes, and any prefix query is a walk down from the
root.

The invariant: a node is reachable by exactly one character sequence (its path from
the root), and `is_end` on that node means that sequence was inserted as a word. A
node can be an interior node of longer words and a word terminal at the same time
(insert `"car"` and `"cars"`: the `r` node is both `is_end` and has a child `s`).

## Operations and complexity

L is the length of the word or prefix. A is the alphabet size (26 for lowercase
letters). N is the number of words in the trie, and none of these operations depend
on N, which is the entire reason the structure exists.

| Operation | Cost | Note |
|---|---|---|
| `insert(word)` | O(L) | Walk L nodes, create missing children |
| `search(word)` | O(L) | Walk L nodes, then check `is_end` |
| `startsWith(prefix)` | O(L) | Walk L nodes, existence is the answer |
| Wildcard search (`.` matches any) | O(A^k · L) worst | k wildcards branch A ways each; DFS |
| Space | O(total characters · A) | A node per character, each with a child map |
| Collect all words under a prefix | O(size of subtree) | DFS from the prefix node |

The headline: `search` and `startsWith` are O(L) regardless of how many words the
trie holds. A hash set answers full-word `search` in O(L) too, but it cannot answer
`startsWith` without scanning every key, which is O(N · L). See the
[complexity cheat sheet](../complexity.md) for the hash set numbers.

## Python implementation

The idiomatic form is a small `TrieNode` plus a `Trie` wrapper. Using a `dict` for
children keeps it alphabet-agnostic and only allocates the branches that exist.

```python
class TrieNode:
    def __init__(self):
        self.children = {}      # char -> TrieNode
        self.is_end = False     # True if a word ends here


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.is_end = True

    def search(self, word):
        node = self._walk(word)
        return node is not None and node.is_end

    def startsWith(self, prefix):
        return self._walk(prefix) is not None

    def _walk(self, s):
        node = self.root
        for ch in s:
            if ch not in node.children:
                return None
            node = node.children[ch]
        return node
```

Wildcard search, where `.` matches any single character, needs DFS because a `.`
forces you to try every child. This is the "Add and Search Word" data structure:

```python
def search_wildcard(self, word):
    def dfs(node, i):
        if i == len(word):
            return node.is_end
        ch = word[i]
        if ch == '.':
            return any(dfs(child, i + 1) for child in node.children.values())
        if ch not in node.children:
            return False
        return dfs(node.children[ch], i + 1)

    return dfs(self.root, 0)
```

A concrete letter still narrows to one child in O(1), so only the `.` positions
branch. With k wildcards the cost is O(A^k) in the worst case, which is why "match
any" queries are the expensive corner of an otherwise linear structure.

## When to use it (and when not)

Reach for a trie when:

- You need **prefix queries**: autocomplete, "count words with prefix", "longest
  common prefix of the set", search-as-you-type.
- You match **many words against a text** and want to share their common prefixes
  (word-search boards, replacing words with roots, the Aho-Corasick family).
- You need **ordered traversal by prefix**, for example all words under `"ca"` in
  sorted order, which falls out of iterating each node's children in key order.

Skip it when:

- You only ever do **full-word membership**. A `set` is O(L) for that too, with far
  less overhead and no per-node allocation. The trie earns its cost only when
  prefixes matter.
- The alphabet is **huge and the set is small**. The per-node child map cost adds up
  and a hash set is leaner.
- Keys are **not strings** with meaningful shared prefixes (arbitrary integers,
  say). There is nothing to share, so the tree buys you nothing.

## Tradeoffs and gotchas

- **Space is the price of speed.** A trie can use more memory than the raw strings,
  because you pay a node (and a child map) per character. Shared prefixes claw some
  of that back, but a set of unrelated words is memory-hungry as a trie.
- **`is_end` is not "is a leaf".** A word can end at an interior node (`"car"`
  inside `"cars"`). Check the flag, never "has no children", or you will miss
  prefixes that are also words.
- **Deletion is fiddly.** You cannot just clear `is_end` and forget it: to reclaim
  space you must remove nodes that no longer sit on any word's path, walking back up
  and stopping at the first node that is still `is_end` or still has other children.
  Most interview solutions never delete; if yours must, be careful.
- **Wildcards blow up.** A single leading `.` fans out to every child. Many
  wildcards make the DFS exponential in the number of wildcards, so do not treat
  wildcard search as O(L).
- **A dict of children vs a fixed array.** A 26-slot list child array is faster and
  simpler when the alphabet is fixed lowercase, at the cost of always allocating 26
  slots per node. A dict allocates only used branches. Pick per problem.

## Related patterns

- [trie](../patterns/15-trie.md) is the pattern that drives this structure:
  autocomplete, word dictionaries, and prefix counting.
- [graph traversal](../patterns/16-graph-traversal.md) shares the DFS mechanics used
  for wildcard search and for collecting every word under a prefix.
- For the underlying operation costs and how the trie's O(L) compares to a hash
  set's, keep the [complexity cheat sheet](../complexity.md) open.
