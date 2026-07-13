# Worked-example walkthroughs

The [patterns](../patterns/README.md) teach the technique; these walkthroughs show
the whole process in motion. Each one takes a single well-known problem and solves
it end to end using the [six-step framework](../framework/solving-framework.md):
clarify, work an example, state the brute force, find the bottleneck and name the
pattern, code it, then test and analyze. This is what a strong interview actually
sounds like, narrated.

Read a pattern file to learn the tool; read the matching walkthrough to watch it
get picked and applied under the framework. The value is in steps 1, 3, and 4, the
thinking before the code, which is exactly the part a bare solution hides.

## The walkthroughs

One per family, chosen to be the canonical teaching problem for its pattern:

| Problem | Pattern it demonstrates | Family |
|---|---|---|
| [Subarray Sum Equals K (560)](subarray-sum-equals-k.md) | Prefix sum plus hashing: `count[prefix - k]` | Arrays and strings |
| [Koko Eating Bananas (875)](koko-eating-bananas.md) | Binary search on the answer, a monotone `feasible(speed)` | Binary search |
| [Daily Temperatures (739)](daily-temperatures.md) | Monotonic stack: each pop resolves a "next greater" | Stacks |
| [Number of Islands (200)](number-of-islands.md) | Grid DFS/BFS, one traversal per unvisited component | Graphs |
| [Subsets (78)](subsets.md) | Backtracking: choose, explore, unchoose | Backtracking |
| [Coin Change (322)](coin-change.md) | DP: state, transition, base case; recursion to tabulation | Dynamic programming |
| [Meeting Rooms II (253)](meeting-rooms-ii.md) | Intervals plus a heap: max concurrent meetings | Heaps and intervals |
| [Two Sum (1)](two-sum.md) | Hashing: complement lookup in O(1) | Arrays and strings |
| [Reverse Linked List (206)](reverse-linked-list.md) | In-place pointer reversal (prev/curr/next) | Linked lists |
| [Course Schedule (207)](course-schedule.md) | Topological sort, cycle detection via Kahn | Graphs |

## How to use them

1. **Try the problem cold first.** Open the LeetCode problem, give it a real
   attempt with the framework, and only then read the walkthrough.
2. **Compare your process, not just your answer.** Did you clarify the constraints?
   State a brute force? Name the bottleneck before coding? The gaps in your
   *process* are what these are for.
3. **Notice the pattern hand-off.** Each walkthrough reaches step 4 and explicitly
   says "this repeated work is the signal for pattern X". Internalizing that move,
   from bottleneck to pattern, is the whole skill the [cheatsheet](../cheatsheet.md)
   drills.
