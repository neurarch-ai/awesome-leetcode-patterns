# The solving framework

Coding interviews reward a repeatable process, not flashes of insight. The strong
candidate looks calm because they are running the same six steps on every problem,
whether it is easy or hard. The content changes; the shape does not. Run these
steps out loud. The interviewer is grading how you think, and silence hides your
thinking.

This maps onto a 35 to 45 minute slot with time to spare.

## 1. Clarify and restate (2 to 3 min)

Do not start coding. The fastest way to fail is to solve the wrong problem
confidently. Pin down:

- **Inputs and outputs.** Exact types and shapes. Is the array sorted? Can it be
  empty? Are values integers, and can they be negative or zero? Is the string
  ASCII or Unicode? What exactly do you return: the value, the index, the count,
  the boolean, all solutions?
- **Constraints.** The size of n is the single most important number in the room.
  It tells you the target complexity before you have written a line. n up to 10 is
  "brute force or backtracking is fine". n up to a few thousand allows O(n^2). n
  up to 10^5 or 10^6 means you need O(n log n) or O(n). n up to 10^9 means you are
  not iterating over n at all: think binary search on the answer, math, or bit
  tricks.
- **Edge cases.** Empty input, one element, all duplicates, all the same,
  negatives, overflow, and "no valid answer exists". Name them now so they do not
  ambush you later.

Restate the problem in your own words and get a nod before designing. Write the
assumptions down.

### Read n like a compiler reads a type

| Constraint on n | Target complexity | Patterns it points at |
|---|---|---|
| n <= 12 or so | O(2^n) or O(n!) | Backtracking, bitmask DP, brute force |
| n <= 500 | O(n^3) | Interval DP, Floyd-Warshall |
| n <= 5000 | O(n^2) | Pairwise DP, two nested loops |
| n <= 10^5 | O(n log n) or O(n) | Sort, heap, binary search, sliding window, two pointers |
| n <= 10^7 | O(n) or O(n log log n) | Single pass, sieve, prefix sums |
| n up to 10^9+ | O(log n) or O(1) | Binary search on the answer, math, matrix power |

The constraint is a hint the problem setter is handing you. Read it first.

## 2. Work a concrete example by hand (2 min)

Take a small, non-trivial input and solve it manually on the whiteboard. This
does three things: it confirms you understood the problem, it surfaces edge cases,
and it often reveals the structure of the solution. If you cannot solve one
example by hand, you cannot code the general case. Pick an example that is not
degenerate: not empty, not already sorted, with at least one interesting case.

## 3. State a brute force (2 min)

Say the obvious, correct, slow solution out loud, with its complexity. Two
reasons: it proves you understand the problem, and it is your fallback if you run
out of time (a working brute force beats a broken clever solution). "I could check
every pair, that is O(n^2). Let me see if I can do better" is exactly the right
sentence. Never skip straight to the optimal; you lose the process credit and you
risk building on a misunderstanding.

## 4. Find the bottleneck, then reach for a pattern (5 min)

This is the crux. Look at the brute force and ask: what work am I repeating, and
what structure am I not using?

- **Repeated work over a moving range** points at a **sliding window** or a
  **prefix sum**: you are recomputing a sum or a count that only changes at the
  edges.
- **Repeated lookups** ("have I seen this value") point at a **hash map** or
  **set** to make the lookup O(1).
- **A sorted input** you are scanning linearly points at **binary search** or
  **two pointers**.
- **Repeated subproblems** in a recursion point at **memoization** and then
  **dynamic programming**.
- **"All possible" or "every combination"** points at **backtracking**.
- **"Kth largest", "top k", "merge k"** point at a **heap**.
- **A monotonic answer space** ("smallest capacity that works") points at
  **binary search on the answer**.

The [cheatsheet](../cheatsheet.md) is the full version of this mapping. The skill
is matching the shape of the bottleneck to the pattern that removes it. State
which pattern you are reaching for and why, before you code.

## 5. Code it cleanly (10 to 15 min)

Only now do you write. Habits that read as senior:

- **Name things for meaning**, not `i2` and `tmp2`. `left`, `right`, `window_sum`,
  `seen`.
- **Handle the edge cases you named in step 1** at the top, not as an afterthought.
- **Keep one idea per line.** An interviewer cannot grade a line they cannot
  parse.
- **Talk while you type.** Narrate the invariant the loop maintains ("after this
  iteration, `window_sum` is the sum of everything between left and right").

If you freeze, go back to the brute force and optimize it incrementally. A
partial, correct, improving solution is a strong signal.

## 6. Test, trace, and analyze (3 to 5 min)

You are not done when the code is written. You are done when you have convinced
the interviewer it is correct.

- **Trace your hand example** through the code, line by line. This catches most
  bugs.
- **Run the edge cases** from step 1: empty, single element, all duplicates,
  the "no answer" case. The [edge-case checklist](../edge-cases.md) is the full
  list interviewers probe for, per pattern.
- **State the final complexity**, time and space, and justify it. If it is not
  optimal, say so and say what the optimal would take.
- **Mention one improvement** you would make with more time (better space,
  handling a follow-up). This shows you know where the bodies are buried.

## The one-paragraph version

Clarify the inputs, constraints, and edge cases; read n to guess the target
complexity. Solve one example by hand. State the brute force and its complexity.
Find the repeated work or unused structure, and name the pattern that removes it.
Code it cleanly while narrating the invariant. Trace an example, run the edge
cases, and state the final complexity. Then stop and breathe.

## Common ways people lose an interview they could have won

- **Coding before clarifying.** Solving the wrong problem is the number one
  killer. Two minutes of questions saves twenty of rework.
- **Silence.** If you are quiet, the interviewer has nothing to grade and assumes
  the worst. Think out loud, even when stuck.
- **Chasing the clever solution and never landing anything.** A working O(n^2)
  beats a broken O(n). Land the brute force first, then improve.
- **Ignoring the constraints.** The size of n is a free hint about the intended
  complexity. Use it.
- **Not testing.** Handing over untraced code and saying "I think that works"
  reads as junior. Trace it.
