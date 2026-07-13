# 26 - Bit manipulation

> **Problem shape:** "Every element appears twice except one, find it." "Count the
> 1 bits in a number." "Generate all subsets." "Add two integers without using +."
> Anything where the answer falls out of treating an integer as a bag of bits and
> reaching for `&`, `|`, `^`, and shifts instead of arithmetic.

Bit manipulation trades human-readable arithmetic for a handful of constant-time
operations on the machine word. The payoff is O(1) set operations, O(1) parity and
membership checks, and the ability to enumerate all 2^n subsets by counting. The
whole pattern is a small vocabulary of idioms: once you know what `x & (x - 1)`
and `x & -x` do, most problems are one line.

![Clearing the lowest set bit of 13 with x AND x minus 1](../assets/bit-manipulation.svg)

*x & (x - 1) clears the lowest set bit: 13 (1101) becomes 12 (1100).*

## The signal

Reach for bit manipulation when you see:

- **"Appears twice / thrice except one"** or any duplicate-cancellation phrasing.
  XOR is self-inverse (`a ^ a == 0`), so pairs annihilate and the loner survives.
- **"Count / check / toggle a specific bit"**, "number of 1 bits", "power of two",
  "is bit k set". These are single mask-and-shift operations.
- **"Generate all subsets" with n small (n <= 20 or so)**. Each subset maps to an
  n-bit integer, so iterating `0 .. 2^n - 1` enumerates every subset.
- **A set of small integers (0..63)** you want to store, union, intersect, or test
  in O(1). A single `int` becomes a set via bitmask; this is the state type for
  bitmask DP.
- **"Without using the + operator"** or other arithmetic-forbidden framings. Add,
  subtract, and multiply all decompose into XOR (sum without carry) plus AND-shift
  (the carry).

The tell is that the natural data unit is a bit or a small set, and the operation
you need is union, toggle, parity, or "isolate one bit".

## The idea

Two idioms carry most of the weight, and both are worth deriving once so you never
forget them:

- **`x & (x - 1)` clears the lowest set bit.** Subtracting 1 flips the lowest set
  bit to 0 and turns every 0 below it into 1; ANDing with the original keeps only
  the bits above that point. Loop it and count iterations to get the popcount in
  O(number of set bits), better than scanning all 32 bits (Brian Kernighan).
- **`x & -x` isolates the lowest set bit.** In two's complement `-x == ~x + 1`, so
  `-x` is `x` with everything above the lowest set bit flipped; the AND leaves
  exactly that one bit. This is the backbone of the Fenwick / binary indexed tree.

The XOR properties do the rest: `a ^ a == 0`, `a ^ 0 == a`, and XOR is commutative
and associative, so XORing a whole list cancels every value that appears an even
number of times and leaves the odd-count survivor. No sorting, no hashing, O(1)
space.

## The template

**Core idioms, memorize these:**

```python
# Time: O(1), Space: O(1) per operation
x & (x - 1)          # clear the lowest set bit
x & -x               # isolate the lowest set bit (value, not index)
x & (1 << k)         # test bit k (nonzero if set)
x | (1 << k)         # set bit k
x & ~(1 << k)        # clear bit k
x ^ (1 << k)         # toggle bit k
x & (x - 1) == 0     # true iff x is a power of two (x > 0)
```

**Single number (XOR cancellation):**

```python
# Time: O(n), Space: O(1)
def single_number(nums):
    result = 0
    for x in nums:
        result ^= x          # pairs cancel, the lone value remains
    return result
```

**Counting bits, popcount via Kernighan:**

```python
# Time: O(number of set bits), Space: O(1)
def hamming_weight(x):
    count = 0
    while x:
        x &= x - 1           # drop the lowest set bit each step
        count += 1
    return count
```

**Subsets by bitmask (iterate 0 .. 2^n - 1):**

```python
# Time: O(n * 2^n), Space: O(1) auxiliary (beyond the output list)
def subsets(nums):
    n = len(nums)
    out = []
    for mask in range(1 << n):               # every n-bit integer is one subset
        out.append([nums[i] for i in range(n) if mask & (1 << i)])
    return out
```

The rule to keep straight: `mask & (1 << i)` asks "is element i in this subset",
and `mask` ranges over exactly `2^n` values, one per subset.

## Variations

- **Single number II (every element thrice except one).** XOR no longer cancels
  triples. Count each bit position mod 3 (a bit that appears in a multiple of 3
  values contributes 0), or run the two-variable `ones`/`twos` state machine that
  tracks each bit's count mod 3.
- **Single number III (two singletons).** XOR everything to get `a ^ b`, isolate
  any set bit with `diff = xor & -xor` (a bit where `a` and `b` differ), then
  partition the array by that bit and XOR each half separately.
- **Counting bits 0..n as DP.** `bits[i] = bits[i >> 1] + (i & 1)`: `i` has the same
  set bits as `i >> 1` plus its own lowest bit. O(n) instead of O(n log n).
- **Submask enumeration.** To iterate every subset of a mask `m`:
  `sub = m; while sub: ...; sub = (sub - 1) & m`. Total work over all masks is
  O(3^n), the classic bitmask-DP inner loop.
- **Addition without +.** `sum_no_carry = a ^ b`, `carry = (a & b) << 1`, repeat
  until carry is 0. In Python mask to 32 bits and reinterpret the sign, because
  Python ints are unbounded.
- **Bitmask as a set.** Union is `|`, intersection is `&`, difference is `& ~`,
  membership is `& (1 << k)`, size is popcount. The state representation for
  travelling-salesman and "shortest path visiting all nodes" DP.

## Canonical problems

| # | Problem | Difficulty | What it drills |
|---|---------|-----------|----------------|
| 136 | Single Number | Easy | XOR cancellation, the base idiom |
| 191 | Number of 1 Bits | Easy | Kernighan popcount |
| 338 | Counting Bits | Easy | `bits[i] = bits[i >> 1] + (i & 1)` DP |
| 268 | Missing Number | Easy | XOR indices against values |
| 190 | Reverse Bits | Easy | Shift out, shift in, 32 iterations |
| 137 | Single Number II | Medium | Per-bit count mod 3 |
| 260 | Single Number III | Medium | Split by an isolated differing bit |
| 78 | Subsets | Medium | Enumerate 0 .. 2^n - 1 as masks |
| 371 | Sum of Two Integers | Medium | XOR sum plus AND-shift carry |

## Pitfalls

- **Python integers are unbounded and signed.** Bit tricks that assume a fixed
  32-bit word (addition-by-XOR, reverse bits, anything with `-x` overflow) need
  explicit masking with `0xFFFFFFFF` and a sign fix-up, or they loop forever or
  return a huge positive number.
- **`x & -x` gives the value of the lowest bit, not its index.** If you need the
  position, take `(x & -x).bit_length() - 1`, do not use the isolated value as an
  index directly.
- **Operator precedence.** `&`, `|`, `^` bind looser than `==` and `+` in Python.
  `x & 1 == 0` parses as `x & (1 == 0)`. Parenthesize: `(x & 1) == 0`.
- **Power-of-two check on zero.** `x & (x - 1) == 0` is also true for `x == 0`;
  guard with `x > 0` if zero should not count.
- **XOR only cancels even counts.** The "every element twice" trick breaks the
  moment duplicates come in threes; switch to the mod-3 bit counting variant.
- **Subset enumeration blows up past ~20 elements.** `2^n` is fine at n = 20
  (a million) but hopeless at n = 40. If n is large, subsets is the wrong pattern.

## Follow-ups and related patterns

- "Now do subset-sum or visit-all-nodes efficiently" pushes the bitmask from an
  enumeration trick into a DP state in
  [DP III: grids, intervals, bitmask](23-dp-grids-intervals.md).
- "Generate subsets when n is large or you need pruning" pushes to
  [backtracking](20-backtracking.md), where you build subsets incrementally
  instead of counting.
- "Find the duplicate / missing number using the values as indices" overlaps with
  [cyclic sort and index-as-hash](06-cyclic-sort.md); XOR and cyclic sort are two
  O(1)-space answers to the same family.
- The lowest-set-bit isolation `x & -x` is the mechanism behind the Fenwick tree;
  the prefix-of-bits idea shows up again in [tries](15-trie.md) for XOR-maximization
  problems.
- Number-theoretic bit questions (parity, base conversion, powers) blur into
  [math and number theory](27-math.md).
