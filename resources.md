# Curated problem lists and external resources

This repo teaches the patterns. To drill them, you want a curated problem list,
not the raw 3000-problem firehose. The three lists below are the community
standards, in increasing size. Pick one and work it, mapping each problem back to
the [pattern](patterns/README.md) it exercises as you go. The mapping is the
point: a problem you cannot classify is a pattern you have not learned yet.

## The three standard lists

| List | Size | Best for | Link |
|---|---|---|---|
| **Grind 75** | 75 (tunable) | A first pass. Sortable by time budget and difficulty, ordered so early problems teach prerequisites for later ones. | [techinterviewhandbook.org/grind75](https://www.techinterviewhandbook.org/grind75/) |
| **Blind 75** | 75 | The classic minimum set, grouped by topic. Terser than Grind 75, assumes you fill gaps yourself. | [neetcode.io/practice (Blind 75 tab)](https://neetcode.io/practice) |
| **NeetCode 150** | 150 | Blind 75 plus 75 more for fuller coverage, with video walkthroughs per problem. The most complete single list. | [neetcode.io/practice](https://neetcode.io/practice) |

Recommended path: **Grind 75 first** (it sequences prerequisites well), then
**NeetCode 150** for breadth. Blind 75 is a strict subset of NeetCode 150, so if
you do the 150 you have done the 75.

Do not do all three end to end; that is 300 problems with heavy overlap. Do one
fully, then only the non-overlapping remainder of a second if you have time.

## How those lists map onto this repo

All three lists group problems into roughly the same buckets, and those buckets
are our pattern families. Use this to translate a list's section into the pattern
file that explains it:

| List category (Blind 75 / NeetCode) | Our pattern |
|---|---|
| Arrays and Hashing | [04 hashing](patterns/04-hashing.md), [03 prefix sum](patterns/03-prefix-sum.md) |
| Two Pointers | [01 two pointers](patterns/01-two-pointers.md) |
| Sliding Window | [02 sliding window](patterns/02-sliding-window.md) |
| Stack | [11 stacks](patterns/11-stacks.md) |
| Binary Search | [07 binary search](patterns/07-binary-search.md) |
| Linked List | [10 linked list](patterns/10-linked-list.md) |
| Trees | [12 tree DFS](patterns/12-tree-dfs.md), [13 tree BFS](patterns/13-tree-bfs.md), [14 BST](patterns/14-bst.md) |
| Tries | [15 trie](patterns/15-trie.md) |
| Heap / Priority Queue | [24 heap](patterns/24-heap.md) |
| Backtracking | [20 backtracking](patterns/20-backtracking.md) |
| Graphs | [16 graph traversal](patterns/16-graph-traversal.md), [17 topological sort](patterns/17-topological-sort.md), [19 shortest path](patterns/19-shortest-path.md) |
| Advanced Graphs | [18 union-find](patterns/18-union-find.md), [19 shortest path](patterns/19-shortest-path.md) |
| 1-D Dynamic Programming | [21 DP linear and knapsack](patterns/21-dp-linear-knapsack.md) |
| 2-D Dynamic Programming | [22 DP strings](patterns/22-dp-strings.md), [23 DP grids and intervals](patterns/23-dp-grids-intervals.md) |
| Greedy | [25 greedy](patterns/25-greedy.md) |
| Intervals | [05 intervals](patterns/05-intervals.md) |
| Math and Geometry | [27 math](patterns/27-math.md) |
| Bit Manipulation | [26 bit manipulation](patterns/26-bit-manipulation.md) |

Two of our families do not have a dedicated list section but show up throughout:
[08 sorting](patterns/08-sorting.md) (a prerequisite for intervals, greedy, and
two pointers) and [28 design](patterns/28-design.md) (LRU cache and friends,
usually filed under "Stack" or a "Design" section).

## A study routine that works

1. **Learn the pattern first, then drill it.** Read the pattern file, then do 3 to
   5 problems from that list section back to back. Massed practice on one pattern
   builds recognition fast.
2. **Then interleave.** Once you have seen every pattern once, switch to mixed
   review: random problems where you must identify the pattern yourself. This is
   what the real interview tests, and blocked practice does not build it.
3. **Time-box.** Give a medium 25 minutes. If you are stuck, read the approach (not
   the full code), then implement it yourself. Struggling past 40 minutes teaches
   less than seeing the idea and coding it.
4. **Re-solve the ones you failed** a few days later, from scratch. Spaced
   repetition is what moves a pattern from "I understood the solution" to "I can
   produce it under pressure".

## External cheat sheets worth bookmarking

Deep single-topic references that go further than a pattern file can:

- **Binary search**, the definitive template writeup:
  [LeetCode discuss, "Powerful Ultimate Binary Search Template"](https://leetcode.com/discuss/general-discussion/786126/python-powerful-ultimate-binary-search-template-solved-many-problems).
- **Sliding window**, one template for most substring problems:
  [LeetCode discuss, "Sliding Window Template"](https://leetcode.com/discuss/general-discussion/657507/sliding-window-for-beginners-problems-template-sliding-window-1d-array).
- **Monotonic stack**, a summary of the family:
  [LeetCode discuss, "Monotonic Stack"](https://leetcode.com/discuss/general-discussion/index).
- **Backtracking**, a single template that covers subsets, permutations, and
  combinations:
  [LeetCode discuss, "A general approach to backtracking questions"](https://leetcode.com/problems/permutations/solutions/18239/a-general-approach-to-backtracking-questions-in-java-subsets-permutations-combination-sum-palindrome-partitioning/).
- **Python complexity reference**, the official source for the numbers in our
  [complexity cheat sheet](complexity.md):
  [wiki.python.org/moin/TimeComplexity](https://wiki.python.org/moin/TimeComplexity).
- **NeetCode**, video walkthroughs for the full 150:
  [neetcode.io](https://neetcode.io/).

Treat external cheat sheets as depth, not a substitute. The recognition skill,
mapping a problem to a pattern in the first two minutes, is what our
[cheatsheet](cheatsheet.md) and [problem bank](problems.md) train, and it is the
part interviews actually reward.
