# 31 - String matching (KMP and rolling hash)

> **Problem shape:** "Find the first occurrence of a pattern in a text." "Is this
> string built by repeating a shorter block?" "What is the longest substring that
> appears twice?" "Find the shortest palindrome you can make by prepending
> characters." Anytime naive substring search (check every start, O(n*m)) is too
> slow, or the problem is really about a string's internal periodicity.

The brute force for "find pattern in text" re-checks the pattern from scratch at
every position, an O(n*m) scan that throws away everything it learned on a
mismatch. Two techniques fix this. **KMP** precomputes the pattern's self-overlap
(its prefix function) so a mismatch jumps ahead instead of restarting, giving
O(n+m). **Rolling hash** (Rabin-Karp) turns each length-m window into a number you
can update in O(1), so comparing substrings becomes comparing integers. Both are
staples of the modern interview string section, and both unlock a family of
periodicity and duplicate-detection problems that have no clean two-pointer or DP
answer.

## The signal

Reach for string matching when you see:

- **Substring search where O(n*m) is too slow**: n and m both large, "find the
  pattern", "index of first occurrence".
- **Periodicity**: "is s made of a repeated block", "longest prefix that is also a
  suffix", "shortest palindrome by prepending". These are exactly what the KMP
  prefix function measures.
- **Duplicate or repeated substrings**: "longest duplicated substring", "all
  10-letter sequences that repeat" (DNA). Rolling hash makes each window comparable
  in O(1), often combined with [binary search](07-binary-search.md) on the length.
- **Matching many patterns at once, or streaming text**: rolling hash (or
  Aho-Corasick for many patterns) beats running a separate search per pattern.

The tell is that the answer depends on how a string overlaps with itself, or on
comparing many equal-length windows cheaply.

## The idea

**KMP and the prefix function.** For each position of the pattern, precompute the
length of the longest proper prefix that is also a suffix ending there (the "lps"
or failure array). On a mismatch during the search, instead of moving the pattern
back to the start, you slide it forward by falling back to `lps[k-1]`: the already
matched prefix guarantees those characters still line up, so you never re-examine a
text character. That is what turns O(n*m) into O(n+m).

**Rolling hash (Rabin-Karp).** Treat a length-m window as a base-B number mod a
large prime. Precompute the pattern's hash and the first window's hash in O(m);
then slide the window one step by subtracting the leaving character's contribution,
multiplying by the base, and adding the entering character, all in O(1). Equal
hashes mean a likely match, which you verify with a direct compare to rule out the
rare collision. Because comparison is now O(1) amortized, rolling hash powers
duplicate detection and "binary search on the substring length" solutions.

Rule of thumb: single exact pattern or a periodicity question, reach for **KMP**.
Duplicate detection, many patterns, or a length to binary-search, reach for
**rolling hash**.

![The KMP prefix function (lps) for the pattern ababc](../assets/string-matching.svg)

*The prefix function: lps[i] is the longest proper prefix of pattern[0..i] that is also a suffix. On a mismatch, jump back to lps[k-1] instead of restarting.*

## The template

**KMP: build the prefix function, then search in O(n+m).**

```python
# Time: O(m), Space: O(m)  (m = pattern length)
def build_lps(pattern):
    lps = [0] * len(pattern)
    k = 0                                  # length of the current prefix-suffix
    for i in range(1, len(pattern)):
        while k and pattern[i] != pattern[k]:
            k = lps[k - 1]                 # fall back, do not restart
        if pattern[i] == pattern[k]:
            k += 1
        lps[i] = k
    return lps

# Time: O(n + m), Space: O(m)
def kmp_search(text, pattern):
    if not pattern:
        return 0
    lps = build_lps(pattern)
    k = 0
    for i in range(len(text)):
        while k and text[i] != pattern[k]:
            k = lps[k - 1]                 # slide the pattern, never rescan text
        if text[i] == pattern[k]:
            k += 1
        if k == len(pattern):
            return i - k + 1               # first match start index
    return -1
```

**Rolling hash (Rabin-Karp): compare windows as integers.**

```python
# Time: O(n + m) average, Space: O(1)
def rabin_karp(text, pattern):
    n, m = len(text), len(pattern)
    if m == 0:
        return 0
    if m > n:
        return -1
    MOD, BASE = 1_000_000_007, 256
    high = pow(BASE, m - 1, MOD)           # value of the top digit
    ph = th = 0
    for i in range(m):                     # hash the pattern and the first window
        ph = (ph * BASE + ord(pattern[i])) % MOD
        th = (th * BASE + ord(text[i])) % MOD
    for i in range(n - m + 1):
        if ph == th and text[i:i + m] == pattern:   # verify to defuse collisions
            return i
        if i < n - m:                      # roll: drop text[i], add text[i+m]
            th = ((th - ord(text[i]) * high) * BASE + ord(text[i + m])) % MOD
    return -1
```

**Periodicity from the prefix function (repeated substring pattern).**

```python
# Time: O(n), Space: O(n)
def repeated_substring(s):
    lps = build_lps(s)
    k = lps[-1]                            # longest prefix that is also a suffix
    return k > 0 and len(s) % (len(s) - k) == 0
```

## Variations

- **Z-function.** An alternative to the prefix function: `z[i]` is the length of the
  longest substring starting at `i` that matches a prefix of the string. Solves the
  same problems; some people find it easier for "match against a prefix".
- **Shortest palindrome (214).** Build the prefix function of `s + "#" + reverse(s)`;
  `lps[-1]` is the longest palindromic prefix of `s`, so prepend the rest reversed.
- **Longest happy prefix (1392).** The answer is `s[:lps[-1]]` directly.
- **Longest duplicated substring (1044).** Binary search the length L; for each L,
  use a rolling hash to detect any repeated length-L window in O(n). This is the
  canonical rolling-hash-plus-binary-search combination.
- **Repeated DNA sequences (187).** Slide a fixed length-10 window and hash (or just
  use a set of the substrings); classic rolling-hash warmup.
- **Double hashing.** For adversarial inputs, hash with two different mods (or a
  random base) and compare both to make collisions astronomically unlikely.
- **Many patterns at once.** Aho-Corasick builds a trie of all patterns plus KMP-style
  failure links, matching them all in one pass. Worth naming even if rarely coded in
  an interview. See [trie](15-trie.md).

## Canonical problems

| # | Problem | Difficulty | What it drills |
|---|---------|-----------|----------------|
| 28 | Find the Index of the First Occurrence in a String | Easy | The base KMP or Rabin-Karp search |
| 459 | Repeated Substring Pattern | Easy | Periodicity from the prefix function |
| 686 | Repeated String Match | Medium | Search across repeated copies |
| 187 | Repeated DNA Sequences | Medium | Fixed-window rolling hash (or a set) |
| 214 | Shortest Palindrome | Hard | Prefix function of s + separator + reverse |
| 1392 | Longest Happy Prefix | Hard | The prefix function read off directly |
| 1044 | Longest Duplicate Substring | Hard | Rolling hash plus binary search on length |

## Pitfalls

- **Restarting instead of falling back.** The whole point of KMP is `k = lps[k-1]`
  on a mismatch. If you reset `k = 0` and move the text pointer back, you have
  rewritten the O(n*m) brute force.
- **Off-by-one in the prefix function.** The inner fallback is `k = lps[k - 1]`, and
  `lps[i]` is set after the comparison. Build it for a couple of patterns by hand
  (`"aabaaab"`, `"ababc"`) until the recurrence is muscle memory.
- **Trusting a hash match blindly.** Equal hashes are not equal strings. Always verify
  with a direct compare on a hit, or use double hashing if you cannot afford the
  verify. Skipping the check is a real bug on adversarial tests.
- **Overflow in other languages.** Python integers are unbounded, so the mod is only
  about keeping the number small. In C++ or Java the multiply overflows a 64-bit int
  before the mod, so you need `__int128` or careful modular multiplication. Say this.
- **Weak modulus or base.** A small prime or `BASE` smaller than the alphabet invites
  collisions. Use a large prime (around 1e9+7) and a base at least the alphabet size.

## Follow-ups and related patterns

- "Search by prefix, or match many patterns" points at the [trie](15-trie.md), and
  Aho-Corasick is a trie with KMP failure links bolted on.
- "Longest duplicate substring" and "kth ... of length L" pair rolling hash with
  [binary search on the answer](07-binary-search.md).
- "Just detect any repeat" often needs nothing fancier than
  [hashing](04-hashing.md) a fixed window into a set; reach for a full rolling hash
  only when the window is large or the length is being binary-searched.
- Periodicity and palindromic-prefix questions are pure prefix-function reads, a
  different tool from the [string DP](22-dp-strings.md) used for edit distance and
  subsequences.
