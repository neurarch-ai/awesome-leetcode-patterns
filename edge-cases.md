# The edge-case checklist

More offers are lost to unhandled edge cases than to picking the wrong pattern. A
solution that works on the happy path and crashes on `[]` reads as careless, and
interviewers probe for exactly these. The [solving framework](framework/solving-framework.md)
folds edge cases into step 1 (clarify) and step 6 (test); this page is the
consolidated checklist to run before you code and again before you say "done".

The discipline: name the edge cases out loud during clarification, handle the ones
that matter at the top of the function, and trace them at the end. Naming them
early also signals seniority, and the interviewer will tell you which ones are in
scope.

## The five that cover most problems

Run this list against every problem. These five account for the large majority of
the traps.

1. **Empty input.** `[]`, `""`, a null tree, a graph with no nodes. Does your loop
   run zero times cleanly, or does `a[0]` throw? Decide the return value for empty
   before coding: 0, an empty list, -1, or a raised error.
2. **Single element.** `[x]`, a one-node list or tree. Two-pointer and fast-slow
   solutions often assume at least two elements; a window or a `while left < right`
   may skip the only element.
3. **Duplicates.** Repeated values break uniqueness assumptions in hash-set logic,
   produce duplicate results in [backtracking](patterns/20-backtracking.md) and
   [kSum](patterns/01-two-pointers.md), and change what "the kth distinct" means.
   Ask whether the input can contain duplicates and whether the output must be
   deduped.
4. **Negative numbers (and zero).** Negatives break the monotonic-growth assumption
   behind [sliding window](patterns/02-sliding-window.md) on sums, invalidate the
   prefix-sum-remainder trick, and change greedy arguments. Zero breaks division
   and "product of array" logic. Ask about the value range explicitly.
5. **Integer overflow.** A sum or product exceeding 2^31 - 1. Harmless in Python
   (arbitrary precision), but you must still mention it, because the interviewer is
   checking whether you know it would bite in Java or C++. Say "in a fixed-width
   language I would use a 64-bit type or take a mod here".

## By pattern: the edge case that specifically bites

| Pattern | The edge case to pre-empt |
|---|---|
| [Two pointers](patterns/01-two-pointers.md) | Empty or single element; the pointers crossing; duplicates producing repeat tuples |
| [Sliding window](patterns/02-sliding-window.md) | Negative numbers (monotonic shrink no longer holds); window larger than the array; no valid window exists |
| [Prefix sum](patterns/03-prefix-sum.md) | The subarray starting at index 0 (needs a prefix of 0); negative numbers with the remainder trick |
| [Binary search](patterns/07-binary-search.md) | Target absent; target at the first or last index; empty array; overflow in `(lo + hi)` in fixed-width languages |
| [Linked list](patterns/10-linked-list.md) | Empty list; single node; a cycle; operating on the head (use a dummy node) |
| [Stacks](patterns/11-stacks.md) | Popping an empty stack; unmatched brackets left at the end |
| [Trees](patterns/12-tree-dfs.md) | Null root; a single node; a skewed (degenerate) tree that makes recursion O(n) deep |
| [Graphs](patterns/16-graph-traversal.md) | Disconnected components; self-loops; a node with no edges; revisiting without a visited set |
| [Backtracking](patterns/20-backtracking.md) | Duplicates in the input needing sort-and-skip; the empty subset; n = 0 |
| [DP](patterns/21-dp-linear-knapsack.md) | The base cases (index 0, capacity 0); an unreachable target (return -1 or infinity cleanly) |
| [Heap](patterns/24-heap.md) | k larger than the input size; an empty heap; popping to peek |
| [Math](patterns/27-math.md) | Division by zero; negative operands with modulo; the value 0 and 1 as special cases |

## Input-shape questions to ask before coding

Turn the checklist into clarifying questions. Ask these in step 1, not after you
have built the wrong thing:

- Can the input be **empty or null**? What do I return then?
- Can there be **one element**? A single-node list or tree?
- Are there **duplicate values**? Must the output be unique?
- Can values be **negative, zero, or very large**? What is the exact range?
- Is the input **sorted**, partially sorted, or unsorted? Can I assume it?
- For strings: **ASCII or Unicode**? Case-sensitive? Can it be whitespace only?
- For graphs: **connected**? **Cyclic**? **Directed**? Can there be self-loops or
  parallel edges?
- Is a **valid answer guaranteed to exist**, or must I signal "none"?

## The habit

- **Before coding**, state the two or three edge cases most likely to break your
  approach, and write the boundary checks first.
- **After coding**, trace `[]`, `[single]`, an all-duplicates input, and a
  negatives input through the code. Most bugs surface here, not on the example.
- **Say the overflow sentence** even in Python. It is a free signal that you think
  about the language boundary, and it costs one line.

Edge cases are not a pattern you apply to some problems. They are a pass you run on
every problem. The candidates who never get caught by "what if the array is empty"
are the ones who ask it themselves first.
