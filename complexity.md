# Complexity cheat sheet

The operation costs you are expected to know cold, so you can say "that lookup is
O(1), so the whole thing is O(n)" without pausing. Every number below is for
CPython (the reference interpreter). "Average" means amortized or expected under
normal hashing; the worst case is noted where it bites.

The most common interview mistake is using a structure whose innocent-looking
operation is secretly O(n): inserting at the front of a list, checking membership
in a list, or building a string by repeated concatenation. Learn these so you do
not build an O(n^2) solution by accident.

## list (dynamic array)

| Operation | Cost | Note |
|---|---|---|
| `a[i]`, `a[i] = x` | O(1) | Indexing is direct |
| `a.append(x)`, `a.pop()` | O(1) amortized | Append reallocates occasionally |
| `a.pop(0)`, `a.insert(0, x)` | O(n) | Everything shifts. Use a deque instead |
| `a.insert(i, x)`, `del a[i]` | O(n) | Shifts the tail |
| `x in a` | O(n) | Linear scan. Use a set for membership |
| `a[i:j]` (slice) | O(k) | k = j - i, copies the slice |
| `len(a)` | O(1) | Stored, not counted |
| `min(a)`, `max(a)`, `sum(a)` | O(n) | Full scan |
| `a.sort()`, `sorted(a)` | O(n log n) | Timsort, stable |
| `a.reverse()`, `a[::-1]` | O(n) | The slice form also copies |
| `a + b` | O(n + m) | Builds a new list |

The trap: `a.pop(0)` and `a.insert(0, x)` are O(n). A queue built on a list is
O(n) per dequeue. Reach for `collections.deque`.

## collections.deque (double-ended queue)

| Operation | Cost | Note |
|---|---|---|
| `d.append(x)`, `d.appendleft(x)` | O(1) | Both ends are cheap |
| `d.pop()`, `d.popleft()` | O(1) | This is why it beats a list for queues |
| `d[i]` (random access) | O(n) | Not an array; indexing the middle walks |
| `x in d` | O(n) | Linear scan |
| `d.rotate(k)` | O(k) | |

Use a deque for any queue, any BFS frontier, any sliding-window-maximum monotonic
buffer. Do not use it when you need O(1) random access; that is a list's job.

## set and frozenset (hash set)

| Operation | Average | Worst | Note |
|---|---|---|---|
| `s.add(x)`, `s.discard(x)` | O(1) | O(n) | Worst case is pathological hashing |
| `x in s` | O(1) | O(n) | The reason sets exist |
| `a | b` (union) | O(len a + len b) | | New set |
| `a & b` (intersection) | O(min(len a, len b)) | | Iterates the smaller |
| `a - b` (difference) | O(len a) | | |

Elements must be hashable (immutable): numbers, strings, tuples yes; lists and
dicts no. When you need a set of coordinates, store tuples `(r, c)`, not lists.

## dict and collections.Counter, defaultdict (hash map)

| Operation | Average | Worst | Note |
|---|---|---|---|
| `d[k]`, `d[k] = v`, `del d[k]` | O(1) | O(n) | Hashing |
| `k in d` | O(1) | O(n) | |
| `len(d)` | O(1) | | |
| iterate `d`, `d.items()` | O(n) | | The view is O(1) to make, O(n) to walk |
| `Counter(iterable)` | O(n) | | Counts in one pass |
| `counter.most_common(k)` | O(n log k) | | Uses a heap internally |
| `counter.most_common()` (all) | O(n log n) | | Full sort |

`defaultdict(list)` or `defaultdict(int)` removes the "check if key exists first"
boilerplate and does not change the complexity. Since Python 3.7, dicts preserve
insertion order, which is occasionally the whole trick (see the LRU cache).

## heapq (binary heap on a list)

| Operation | Cost | Note |
|---|---|---|
| `heapq.heapify(a)` | O(n) | Cheaper than n pushes, which is O(n log n) |
| `heapq.heappush(a, x)` | O(log n) | |
| `heapq.heappop(a)` | O(log n) | Always the smallest (min-heap) |
| `a[0]` (peek min) | O(1) | Do not pop just to look |
| `heapq.heappushpop`, `heapreplace` | O(log n) | One sift, not two |
| `heapq.nlargest(k, a)`, `nsmallest(k, a)` | O(n log k) | Size-k heap under the hood |

Python only has a min-heap. For a max-heap, push `-x` (numbers) or a
`(-priority, item)` tuple. To build a heap from data you already have, `heapify`
in O(n), do not push one at a time.

## str (immutable sequence)

| Operation | Cost | Note |
|---|---|---|
| `s[i]`, `len(s)` | O(1) | |
| `s + t` | O(n + m) | Builds a brand new string every time |
| building a string by `+=` in a loop | O(n^2) | The classic accidental blowup |
| `''.join(list_of_str)` | O(total length) | The correct way to build a string |
| `sub in s` | O(n * m) worst | Usually near O(n) in practice |
| `s[i:j]`, `s.split()`, `s.replace(...)` | O(n) | All produce new strings |

Because strings are immutable, every "edit" allocates. If you are assembling
output character by character, collect into a list and `''.join()` at the end.

## The complexity ladder (what each order feels like at n = 10^6)

| Big-O | Name | Roughly |
|---|---|---|
| O(1) | constant | instant |
| O(log n) | logarithmic | ~20 steps |
| O(n) | linear | one pass, fine |
| O(n log n) | linearithmic | a sort, fine up to ~10^6 |
| O(n^2) | quadratic | dies above ~10^4 |
| O(2^n), O(n!) | exponential, factorial | only for n up to ~20, ~12 |

Cross-reference this with the "read n like a type" table in the
[solving framework](framework/solving-framework.md): the constraint on n tells you
which row you are allowed to land in.

## The recursion space caveat

A "clever O(1) space" claim is wrong if your solution recurses. Every recursive
call frame sits on the call stack, so a recursion of depth d uses O(d) space even
when it allocates nothing. Tree and DFS solutions are O(h) space for the stack (h
= height), which is O(log n) for a balanced tree and O(n) for a degenerate one.
Genuine O(1) space usually means an iterative solution with a fixed number of
pointers. Say "O(1) extra space, iterative" only when you mean it.
