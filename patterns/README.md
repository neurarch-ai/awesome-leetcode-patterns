# Patterns

Each file is a self-contained pattern walkthrough. They all follow the same seven
sections, mirroring the [solving framework](../framework/solving-framework.md), so
once you have read one you know how to read the rest:

1. **The signal** - how to recognize the pattern from the problem statement:
   trigger phrases, input shape, and the tell-tale constraints.
2. **The idea** - the core mechanism and why it works, plus the complexity it
   buys you over brute force.
3. **The template** - clean, memorizable Python you can reproduce from memory.
4. **Variations** - the sub-patterns and common twists on the base template.
5. **Canonical problems** - a table of LeetCode problems that drill the pattern,
   with difficulty and what each one teaches.
6. **Pitfalls** - the bugs and edge cases that cost people the solve.
7. **Follow-ups and related patterns** - how interviewers push deeper, and which
   patterns sit next to this one.

## Pattern index

**Arrays and strings**
- [01 - Two pointers](01-two-pointers.md)
- [02 - Sliding window](02-sliding-window.md)
- [03 - Prefix sum and difference arrays](03-prefix-sum.md)
- [04 - Hashing and frequency counting](04-hashing.md)
- [05 - Intervals and sweep line](05-intervals.md)
- [06 - Cyclic sort and index-as-hash](06-cyclic-sort.md)

**Binary search and sorting**
- [07 - Binary search](07-binary-search.md)
- [08 - Sorting and custom comparators](08-sorting.md)
- [09 - Top-K and quickselect](09-top-k-quickselect.md)

**Linked lists and stacks**
- [10 - Linked list techniques](10-linked-list.md)
- [11 - Stacks: monotonic and parsing](11-stacks.md)

**Trees**
- [12 - Tree DFS and recursion](12-tree-dfs.md)
- [13 - Tree BFS and level-order](13-tree-bfs.md)
- [14 - Binary search tree](14-bst.md)
- [15 - Trie](15-trie.md)

**Graphs**
- [16 - Graph traversal and grids](16-graph-traversal.md)
- [17 - Topological sort](17-topological-sort.md)
- [18 - Union-find (DSU)](18-union-find.md)
- [19 - Shortest path](19-shortest-path.md)

**Recursion, backtracking, and dynamic programming**
- [20 - Backtracking](20-backtracking.md)
- [21 - DP I: linear and knapsack](21-dp-linear-knapsack.md)
- [22 - DP II: subsequences and strings](22-dp-strings.md)
- [23 - DP III: grids, intervals, bitmask](23-dp-grids-intervals.md)

**Heaps, greedy, math, and design**
- [24 - Heap and priority queue](24-heap.md)
- [25 - Greedy](25-greedy.md)
- [26 - Bit manipulation](26-bit-manipulation.md)
- [27 - Math and number theory](27-math.md)
- [28 - Design](28-design.md)

**Advanced structures and algorithms**
- [29 - Segment tree and Fenwick (BIT)](29-segment-tree-fenwick.md)
- [30 - State-machine DP (stock series)](30-state-machine-dp.md)
- [31 - String matching (KMP and rolling hash)](31-string-matching.md)

**Deep dives**
- [Dynamic programming: the full sub-pattern map](dp-patterns.md) - the eleven DP shapes above and below 21-23 and 30, as a recognition index

## Contributing a pattern

Follow the seven-section shape above. Rules:

- **Be honest about complexity.** State time and space for every template, and
  do not claim an optimum you have not argued for.
- **Prefer mechanism over name-dropping.** Explain what the monotonic stack
  maintains and why it stays monotonic, do not just say "use a monotonic stack".
- **Templates are Python 3 and memorizable.** If a template is longer than a
  screen, it is doing too much; split the variation into its own snippet.
- **Cite real LeetCode numbers** in the canonical problems table, with the
  correct difficulty.
