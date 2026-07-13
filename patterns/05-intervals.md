# 05 - Intervals and sweep line

> **Problem shape:** "Merge all overlapping intervals." "Insert a new interval
> into a sorted list." "How many meeting rooms do you need?" "Can this person
> attend all meetings?" "Fewest arrows to burst all balloons." Anything about
> ranges that start and end on a line, and how they overlap, stack, or pack.

Interval problems are about ranges on a number line, and almost all of them yield
to one move: sort by the right key (usually start), then make one linear pass
deciding merge-or-not. When the question is "how many overlap at once", the sweep
line reframes each interval as two events (+1 at start, -1 at end) and scans a
running count. Sorting turns tangled ranges into a decidable left-to-right walk.

## The signal

Reach for the interval / sweep-line pattern when you see:

- **A list of `[start, end]` pairs** and a question about overlap, merging,
  coverage, or packing.
- **"Merge", "insert", "do any overlap", "remove the fewest to make them
  disjoint".** These are a sort-by-start (or sort-by-end) plus a single pass.
- **"How many are active at the same time" (max concurrency).** Meeting rooms,
  car pooling by seat count, maximum population alive in a year. This is the
  sweep line: count starts minus ends as you move along the axis.
- **"Minimum number of points / arrows / resources to cover everything".** A
  greedy sort-by-end interval-scheduling problem.
- **Anything where the objects have a natural order on one axis** and the
  interactions are purely local once you look in that order.

The tell is that after sorting by one endpoint, each interval only ever interacts
with the one immediately before it (for merging) or with a running counter (for
concurrency), so a single pass suffices.

## The idea

Sort intervals by start. Now overlaps are local: if the current interval starts
at or before the running merged interval's end, they overlap and you extend the
end to the max of the two; otherwise there is a gap, so you close the current
merged block and open a new one. Because sorting guarantees you never see an
earlier-starting interval later, one pass is enough. Sort is O(n log n), the pass
is O(n).

The sweep line answers concurrency questions the merge pass cannot. Split each
interval `[s, e]` into two events: a `+1` at `s` and a `-1` at `e`. Sort all
events by position, then sweep left to right maintaining a running sum. The sum at
any moment is the number of intervals currently open, and its maximum over the
sweep is the peak concurrency (the number of meeting rooms, the max passengers in
the car). The heap variant does the same thing without materializing events: keep
a min-heap of end times, and for each new meeting pop every end that is `<=` its
start (those rooms freed up), then push this meeting's end. The heap size is the
rooms in use; its peak is the answer.

The greedy "fewest points to stab all intervals" is a third face: sort by end,
take the end of the first interval as a stab point, skip every interval it
covers, and repeat. Sorting by end is what makes the greedy choice optimal,
because the earliest end leaves the most room for the rest.

## The template

**Merge overlapping intervals:**

```python
# Time: O(n log n), Space: O(n)
def merge(intervals):
    intervals.sort(key=lambda iv: iv[0])       # sort by start
    out = []
    for s, e in intervals:
        if out and s <= out[-1][1]:            # overlaps the last merged block
            out[-1][1] = max(out[-1][1], e)    # extend its end
        else:
            out.append([s, e])                 # gap: start a new block
    return out
```

**Insert an interval into a sorted, disjoint list:**

```python
# Time: O(n), Space: O(n)
def insert(intervals, new):
    out = []
    s, e = new
    i, n = 0, len(intervals)
    while i < n and intervals[i][1] < s:       # entirely before new
        out.append(intervals[i]); i += 1
    while i < n and intervals[i][0] <= e:      # overlaps new: absorb it
        s = min(s, intervals[i][0])
        e = max(e, intervals[i][1]); i += 1
    out.append([s, e])
    out.extend(intervals[i:])                  # entirely after new
    return out
```

**Meeting rooms II, minimum rooms via a heap of end times:**

```python
import heapq

# Time: O(n log n), Space: O(n)
def min_meeting_rooms(intervals):
    intervals.sort(key=lambda iv: iv[0])       # by start
    ends = []                                  # min-heap of end times in use
    for s, e in intervals:
        if ends and ends[0] <= s:              # earliest room has freed up
            heapq.heapreplace(ends, e)         # reuse it
        else:
            heapq.heappush(ends, e)            # need a new room
    return len(ends)                           # peak concurrency
```

**Sweep line via +1 / -1 events (general max concurrency):**

```python
# Time: O(n log n), Space: O(n)
def max_concurrent(intervals):
    events = []
    for s, e in intervals:
        events.append((s, 1))                  # a range opens
        events.append((e, -1))                 # a range closes
    events.sort()                              # end (-1) sorts before start (+1) at a tie
    active = best = 0
    for _, delta in events:
        active += delta
        best = max(best, active)
    return best
```

The tie-break in the event sort encodes whether touching intervals (`[1,2]` and
`[2,3]`) count as overlapping. Sorting `-1` before `+1` at equal positions treats
a shared endpoint as non-overlapping, which is the usual meeting-room convention.

## Variations

- **Overlap detection / "can attend all meetings".** Sort by start, return False
  the moment one interval starts before the previous ends. No merging needed.
- **Non-overlapping intervals (remove the fewest).** Sort by end, greedily keep
  each interval whose start is at or after the last kept end, count the rest as
  removals. Classic interval scheduling.
- **Minimum arrows to burst balloons.** Same greedy as above, sort by end and
  count the groups; each group needs one arrow.
- **Interval intersection of two sorted lists.** Two pointers over both lists,
  the overlap of the two fronts is `[max(starts), min(ends)]`; advance whichever
  ends first.
- **Car pooling / booking counts.** A [difference array](03-prefix-sum.md) over
  the axis when coordinates are small integers, or a sweep line when they are
  sparse. Both compute peak load.
- **Sort by start vs sort by end.** Merging and concurrency want sort-by-start;
  greedy scheduling and stabbing want sort-by-end. Picking the wrong key is the
  most common structural mistake.

## Canonical problems

| # | Problem | Difficulty | What it drills |
|---|---------|-----------|----------------|
| 252 | Meeting Rooms | Easy | Sort by start, adjacent overlap check |
| 56 | Merge Intervals | Medium | The base sort-and-merge pass |
| 57 | Insert Interval | Medium | Three-phase absorb into a sorted list |
| 253 | Meeting Rooms II | Medium | Max concurrency via heap or sweep |
| 435 | Non-overlapping Intervals | Medium | Greedy sort-by-end scheduling |
| 452 | Minimum Number of Arrows to Burst Balloons | Medium | Sort-by-end stabbing groups |
| 1094 | Car Pooling | Medium | Sweep line / difference array on load |
| 986 | Interval List Intersections | Medium | Two pointers over two sorted lists |
| 763 | Partition Labels | Medium | Sweep of last-occurrence, greedy cut |
| 1288 | Remove Covered Intervals | Medium | Sort by start then end, track max end |

## Pitfalls

- **Sorting by the wrong endpoint.** Merge and concurrency need start; greedy
  scheduling and arrows need end. If the greedy fails on a case, check the sort key
  first.
- **Inclusive vs exclusive endpoints.** Does `[1,2]` overlap `[2,3]`? Decide the
  convention, then encode it: `s <= prev_end` vs `s < prev_end` in the merge, and
  the `-1`-before-`+1` tie-break in the sweep.
- **Mutating the input in place** when you sort. If the caller keeps the original
  order, copy first. Also, `out[-1][1] = ...` mutates the appended interval;
  append a fresh list, not a reference into the input.
- **Empty input.** Merge and sweep should return cleanly on an empty list; the
  `if out` guard handles the first interval.
- **Sweep tie-breaks flip the answer.** At equal coordinates, whether you process
  the end or the start first changes peak concurrency by one at touch points. This
  is the single most common off-by-one in sweep-line code.
- **Heap holds ends, compared against the next start.** Popping while
  `ends[0] <= s` (not `< s`) matches the "touching does not overlap" convention;
  keep it consistent with your merge choice.

## Follow-ups and related patterns

- "Max concurrency" leans on a [heap](24-heap.md) of end times, or on a
  [difference array](03-prefix-sum.md) when the axis is small integers.
- The insert and intersection variants are [two pointers](01-two-pointers.md) over
  one or two sorted lists.
- Every template here starts with a [sort](08-sorting.md) on a chosen key; the
  custom comparator (start vs end) is the whole game.
- The greedy "remove fewest" and "fewest arrows" are instances of
  [greedy](25-greedy.md) interval scheduling, where sort-by-end makes the local
  choice provably optimal.
- When coordinates need compression before a sweep, that bucketing is
  [hashing](04-hashing.md) on positions.
