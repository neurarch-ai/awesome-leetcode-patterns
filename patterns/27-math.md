# 27 - Math and number theory

> **Problem shape:** "Compute pow(x, n)." "Count the primes below n." "Reverse an
> integer without overflow." "How many trailing zeroes in n factorial." "Convert
> an Excel column title to a number." Anything where the algorithm is a known
> number-theory identity (Euclid, the Sieve, fast exponentiation) and the real
> difficulty is edge cases and overflow.

Math problems reward knowing the closed-form trick rather than deriving it under
pressure. The core toolkit is small: Euclid's gcd, the Sieve of Eratosthenes,
modular arithmetic, exponentiation by squaring, a little combinatorics, and
digit-by-digit manipulation. Most of the interview risk is not the idea, it is the
overflow, the sign of zero, and the off-by-one on boundaries.

![Sieve of Eratosthenes over 2 to 31 with primes highlighted](../assets/math.svg)

*The Sieve of Eratosthenes: cross out every multiple of each prime, and the survivors are the primes.*

## The signal

Reach for a math pattern when you see:

- **gcd / lcm / "reduce a fraction" / "simplify a ratio"**. Euclid's algorithm is
  the answer, O(log(min(a, b))).
- **"Count primes", "is prime", "prime factors below n"**. The Sieve of
  Eratosthenes precomputes all primes under n in O(n log log n); trial division is
  the fallback for a single query.
- **"Modulo 1e9 + 7", "the answer may be huge"**. You never materialize the big
  number; you carry everything mod m, using modular addition and multiplication and
  modular exponentiation.
- **"Compute x^n"** with large n. Exponentiation by squaring turns O(n) multiplies
  into O(log n).
- **"How many ways to choose k of n", Pascal's triangle, binomial coefficients**.
  Combinatorics: `nCr`, either from the multiplicative formula or the Pascal
  recurrence.
- **Digit surgery**: reverse an integer, palindrome number, sum of digits, happy
  number. You peel digits with `% 10` and `// 10`.
- **Base conversion**: Excel column titles (base 26, 1-indexed), "number to hex",
  binary and back. The general "repeated divmod by the base" loop.

The tell is that the problem is small in code but has a named identity behind it,
and the grading is really about handling the boundaries.

## The idea

Each tool is one identity applied cleanly:

- **Euclid's gcd.** `gcd(a, b) == gcd(b, a % b)`, because any common divisor of
  `a` and `b` also divides `a % b`. Recurse until the remainder is 0. Then
  `lcm(a, b) == a // gcd(a, b) * b` (divide first to avoid overflow).
- **Sieve of Eratosthenes.** Every composite has a smallest prime factor, so
  starting from each prime `p` you strike out `p*p, p*p+p, ...`; start at `p*p`
  because smaller multiples were already struck by smaller primes. What survives is
  prime.
- **Modular arithmetic.** `(a + b) % m`, `(a * b) % m`, and `(a - b) % m` all
  distribute over the operation, so you can reduce at every step and never let the
  running value grow. This keeps products inside the word (or, in Python, cheap).
- **Fast exponentiation.** `x^n = (x^(n/2))^2` for even n, times one extra `x` for
  odd n. Halving the exponent each step gives O(log n) multiplies. Same recurrence
  powers modular exponentiation.

The unifying move in digit and base problems is `divmod`: `q, r = divmod(x, base)`
peels the least-significant digit `r` and shifts the rest into `q`.

## The template

**gcd and lcm (Euclid):**

```python
# Time: O(log(min(a, b))), Space: O(1)
def gcd(a, b):
    while b:
        a, b = b, a % b      # invariant: gcd(a, b) unchanged
    return a

# Time: O(log(min(a, b))), Space: O(1)
def lcm(a, b):
    return a // gcd(a, b) * b # divide before multiply to limit growth
```

**Sieve of Eratosthenes, count primes below n:**

```python
# Time: O(n log log n), Space: O(n)
def count_primes(n):
    if n < 3:
        return 0
    is_prime = [True] * n
    is_prime[0] = is_prime[1] = False
    p = 2
    while p * p < n:
        if is_prime[p]:
            for multiple in range(p * p, n, p):   # start at p*p, earlier ones done
                is_prime[multiple] = False
        p += 1
    return sum(is_prime)
```

**Fast exponentiation (pow by squaring), with optional modulus:**

```python
# Time: O(log n), Space: O(1)
def fast_pow(x, n, mod=None):
    if n < 0:
        x, n = 1 / x, -n          # for modular pow, use modular inverse instead
    result = 1
    while n:
        if n & 1:                 # odd bit: fold in one factor of x
            result *= x
            if mod: result %= mod
        x *= x                    # square the base
        if mod: x %= mod
        n >>= 1
    return result
```

**Digit peel (reverse integer with 32-bit overflow guard):**

```python
# Time: O(number of digits), Space: O(1)
def reverse(x):
    sign = -1 if x < 0 else 1
    x = abs(x)
    result = 0
    while x:
        x, digit = divmod(x, 10)
        result = result * 10 + digit
    result *= sign
    return result if -2**31 <= result <= 2**31 - 1 else 0   # clamp to int range
```

## Variations

- **Modular inverse and nCr mod p.** When p is prime, `a^(p-1) == 1 (mod p)`
  (Fermat), so `a^(-1) == a^(p-2) (mod p)` via fast modular pow. This is how you
  compute binomial coefficients under a prime modulus.
- **Pascal's triangle for nCr.** `C(n, k) = C(n-1, k-1) + C(n-1, k)`. Build the
  triangle row by row when you need many small coefficients; use the multiplicative
  formula `C(n, k) = prod((n-i)/(i+1))` for a single one.
- **Trailing zeroes of n!.** Zeroes come from factors of 10 = 2 * 5, and 5s are
  scarcer, so count factors of 5: `n//5 + n//25 + n//125 + ...`. No factorial
  needed.
- **Palindrome number without string conversion.** Reverse only the second half:
  build `rev` from the low digits while `x > rev`, then compare `x == rev` (even
  length) or `x == rev // 10` (odd length).
- **Base conversion, general.** Repeated `divmod(x, base)` collects digits least
  significant first, then reverse. Excel columns are base 26 but 1-indexed (A = 1,
  no zero digit), so subtract 1 before each divmod.
- **Integer sqrt (Newton or binary search).** `Sqrt(x)` floored: binary search the
  answer in `[0, x]`, or Newton's iteration `r = (r + x // r) // 2` until it stops
  decreasing.

## Canonical problems

| # | Problem | Difficulty | What it drills |
|---|---------|-----------|----------------|
| 204 | Count Primes | Medium | Sieve of Eratosthenes, start at p*p |
| 7 | Reverse Integer | Medium | Digit peel plus 32-bit overflow clamp |
| 9 | Palindrome Number | Easy | Reverse half, no string conversion |
| 50 | Pow(x, n) | Medium | Exponentiation by squaring, negative n |
| 69 | Sqrt(x) | Easy | Binary search or Newton for integer root |
| 171 | Excel Sheet Column Number | Easy | Base-26, 1-indexed conversion |
| 172 | Factorial Trailing Zeroes | Medium | Count factors of 5, not the factorial |
| 268 | Missing Number | Easy | Gauss sum n(n+1)/2 minus the array sum |

## Pitfalls

- **Overflow on the reversed or accumulated value.** In C++/Java the product
  overflows before you can check it; guard *before* multiplying (`if result > MAX/10`).
  In Python there is no overflow, but the problem still requires clamping to the
  32-bit range, so do it explicitly.
- **Multiply-before-divide in lcm.** `a * b // gcd` can overflow where
  `a // gcd * b` does not. Always divide first.
- **Sieve boundaries.** Inclusive vs exclusive of n, and remembering `0` and `1`
  are not prime. Inner loop starts at `p*p`, not `2*p`, and the outer loop only
  needs `p*p < n`.
- **Sign and zero in digit problems.** Negative numbers, trailing-zero inputs
  (1200 reverses to 21), and the single value `0` are the usual failing cases.
- **Excel is 1-indexed with no zero digit.** It is bijective base-26, not ordinary
  base-26; forgetting the `-1` shift is the classic bug on both directions.
- **Modulus of negatives.** In Python `%` already returns a non-negative result for
  a positive modulus, but in C-family languages it does not; add `m` and take `% m`
  again if you port the code.
- **Fermat inverse needs a prime modulus.** `a^(p-2)` is only the inverse when p is
  prime; for composite moduli use the extended Euclidean algorithm.

## Follow-ups and related patterns

- "n is huge and you must return it mod 1e9+7" turns most counting problems into
  modular-arithmetic versions of a [DP](23-dp-grids-intervals.md) recurrence.
- "Do it with bit tricks instead" (parity, powers of two, base-2 conversion)
  overlaps with [bit manipulation](26-bit-manipulation.md).
- "Sqrt(x) by binary search" and "find the boundary" are the monotonic-predicate
  idea from [binary search](07-binary-search.md); the math version just supplies a
  numeric answer space.
- Combinatorial counting (paths, choices) that does not have a closed form falls
  back to [DP III](23-dp-grids-intervals.md) or [backtracking](20-backtracking.md).
- "Missing / duplicate number in 1..n" has an O(1)-space companion in
  [cyclic sort and index-as-hash](06-cyclic-sort.md) alongside the Gauss-sum trick.
