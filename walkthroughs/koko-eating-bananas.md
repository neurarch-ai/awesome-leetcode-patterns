# Walkthrough: Koko Eating Bananas (LC 875)

A worked example that runs the six-step framework on one problem end to end.
The goal is to show the process, not just the answer.

## The problem

**LeetCode 875, Medium.** Koko has `piles` of bananas and a guard returns in `h`
hours. She picks one eating speed `k` (bananas per hour) for the whole time. Each
hour she eats from a single pile: if that pile has at least `k` bananas she eats
`k` and moves on next hour, otherwise she eats the whole pile and is done with it
for that hour (she does not roll the leftover time onto another pile). Return the
smallest integer speed `k` that lets her finish all the piles within `h` hours.

Example: `piles = [3, 6, 7, 11]`, `h = 8` returns `4`.

![Binary search on the answer](../assets/binary-search.svg)

*Binary search on the answer. See the full pattern in the linked file below.*

## 1. Clarify and restate

The questions I would ask:

- **Input types.** `piles` is a list of positive integers, `h` is a positive
  integer. Is `h` guaranteed to be at least `len(piles)`? Yes, the problem
  guarantees it, which matters because she needs at least one hour per pile, so a
  finish is always possible.
- **What do I return?** The minimum integer speed. Speed must be a positive
  integer (she cannot eat 2.5 bananas per hour under the rules; `k` is an int).
- **Constraints.** `piles` length up to `10^4`, and pile sizes up to `10^9`. That
  second number is the tell. The answer `k` lives somewhere in `[1, max(pile)]`,
  which is a range of size up to `10^9`. I am not going to scan that linearly.
  A range of `10^9` with a yes/no test screams **binary search on the answer**,
  target O(n log(max_pile)).
- **Edge cases.** One pile; `h` equal to the number of piles (she must eat the
  biggest pile in one hour, so the answer is `max(piles)`); a huge `h` (the answer
  bottoms out at `1`); all piles the same size.

Restated: find the smallest integer speed whose "can she finish in time" test
passes, over a speed range up to a billion.

## 2. Work an example by hand

`piles = [3, 6, 7, 11]`, `h = 8`. The hours to clear a pile at speed `k` is
`ceil(pile / k)`.

Try `k = 4`:
- pile 3: `ceil(3/4) = 1` hour
- pile 6: `ceil(6/4) = 2` hours
- pile 7: `ceil(7/4) = 2` hours
- pile 11: `ceil(11/4) = 3` hours
- total `1 + 2 + 2 + 3 = 8`, which is `<= 8`. Feasible.

Try `k = 3`:
- `ceil(3/3) + ceil(6/3) + ceil(7/3) + ceil(11/3) = 1 + 2 + 3 + 4 = 10`, which is
  `> 8`. Not feasible.

So `k = 4` works and `k = 3` does not, making `4` the minimum. Notice the pattern:
every speed at or above 4 is feasible, every speed below is not. The feasibility
is **monotonic** in `k`, which is precisely what binary search needs.

## 3. Brute force

Walk speeds upward from 1 and return the first that finishes in time.

```python
import math

def min_eating_speed_brute(piles, h):
    def hours_needed(speed):
        return sum(math.ceil(pile / speed) for pile in piles)

    speed = 1
    while hours_needed(speed) > h:
        speed += 1
    return speed
```

Each `hours_needed` call is O(n). In the worst case the answer is near
`max(piles)` (up to `10^9`), so this is **O(n * max_pile)** time, up to
`10^13` operations. Correct but hopelessly slow.

## 4. Find the bottleneck and pick the pattern

The brute force tests every candidate speed one by one, but the candidates have
structure it ignores: if speed `s` finishes in time, every speed above `s` also
finishes (eating faster never takes more hours), and if `s` is too slow, every
speed below `s` is also too slow. Feasibility is a step function: false, false,
..., false, true, true, ..., true. I want the boundary, the first `true`.

That monotonic yes/no answer space is the exact signal for **binary search on the
answer**. Instead of searching a sorted array of values, I search the range of
possible answers `[1, max(piles)]` and use a predicate `feasible(speed)` in place
of a comparison. Each step halves the range, turning `10^9` candidates into about
30 predicate evaluations.

The predicate:

```
feasible(speed) := sum(ceil(pile / speed) for pile in piles) <= h
```

It is monotonic: as `speed` increases, each `ceil` term is non-increasing, so the
whole sum is non-increasing, so once it drops to `<= h` it stays there. That
monotonicity is what makes binary search valid. I search for the leftmost speed
where `feasible` is true.

## 5. Code it

```python
def min_eating_speed(piles, h):
    def feasible(speed):
        # hours to clear each pile at this speed; ceil without floats:
        # (pile + speed - 1) // speed
        hours = 0
        for pile in piles:
            hours += (pile + speed - 1) // speed
            if hours > h:            # early exit, cannot get better
                return False
        return hours <= h

    lo, hi = 1, max(piles)           # slowest usable speed .. fastest ever needed
    while lo < hi:
        mid = (lo + hi) // 2
        if feasible(mid):
            hi = mid                 # mid works, but maybe something slower does too
        else:
            lo = mid + 1             # mid too slow, answer is strictly faster
    return lo                        # lo == hi is the smallest feasible speed
```

I use integer ceiling `(pile + speed - 1) // speed` rather than `math.ceil(pile /
speed)` to avoid floating-point error at the `10^9` scale. The loop invariant:
the answer always lies in `[lo, hi]`. When `feasible(mid)` is true I keep `mid` as
a candidate (`hi = mid`, not `mid - 1`); when false I discard `mid` and everything
below it (`lo = mid + 1`). The loop ends when `lo == hi`, which is the boundary.

## 6. Test, trace, and analyze

Trace `piles = [3, 6, 7, 11]`, `h = 8`. Start `lo = 1`, `hi = 11`.

| lo | hi | mid | feasible(mid) | hours | action |
|----|----|-----|---------------|-------|--------|
| 1 | 11 | 6 | true | 1+1+2+2 = 6 | hi = 6 |
| 1 | 6 | 3 | false | 1+2+3+4 = 10 | lo = 4 |
| 4 | 6 | 5 | true | 1+2+2+3 = 8 | hi = 5 |
| 4 | 5 | 4 | true | 1+2+2+3 = 8 | hi = 4 |

Now `lo == hi == 4`, return `4`. Matches the hand answer.

Edge cases:
- **One pile**, `piles = [11], h = 4`: the search converges to `ceil(11/3) = 4`
  hours at speed 3, and `ceil(11/4) = 3 <= 4` at speed 4... tracing it, `lo`
  settles on the smallest speed with `ceil(11/speed) <= 4`, which is 3. Correct.
- **h equals number of piles**, `piles = [3, 6, 7, 11], h = 4`: she must clear
  each pile in exactly one hour, so the answer is `max(piles) = 11`. Any speed
  below 11 makes the 11-pile take two or more hours and overflow `h`. The search
  returns 11. Correct.
- **Huge h**: feasibility passes even at `mid = 1`, so `hi` keeps collapsing to 1
  and the answer is `1`, the slowest legal speed. Correct.

**Complexity: O(n log(max_pile)) time**, where the `log` factor is the number of
binary-search steps (about 30 for `10^9`) and each step runs the O(n) predicate,
and **O(1) extra space**. This is the intended solution and vastly beats the
brute force.

With more time I would mention the general recipe this instantiates: any
"minimize/maximize a value subject to a monotonic feasibility test" problem
(ship-within-days, split-array-largest-sum) is the same binary-search-on-the-answer
shape with a different predicate.

## What the interviewer is really testing

Whether you can spot that the answer itself lives in a searchable, monotonically
ordered space, even though nothing in the input is a sorted array. The leap is
reframing "find the minimum speed" as "find the boundary of a true/false
predicate" and proving the predicate is monotonic. Candidates who only associate
binary search with searching a sorted list miss this entire class; the ones who
have internalized it write the predicate first and the search second.

> Pattern: [07 binary search](../patterns/07-binary-search.md)
