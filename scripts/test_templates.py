#!/usr/bin/env python3
"""Execute every self-contained code template against known LeetCode answers.

`scripts/check.py` only compiles the code (syntax). This runs it: each pattern
file's python blocks are exec'd, then the resulting functions are called on the
canonical example inputs and checked against the known outputs. A logic
regression in any template fails CI here, not just a syntax error.

Nested helper functions (inner dfs/backtrack) are exercised through their public
function. Illustrative snippets that reference an undefined helper (e.g. the
sliding-window `is_valid` placeholder) are not called. No third-party deps: the
pattern templates use only the standard library.

Run: python3 scripts/test_templates.py   (exit non-zero on any failure)
"""

import os
import re
import sys
from collections import deque

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
fails = []
ran = 0


def load(rel_path):
    ns = {}
    text = open(os.path.join(ROOT, rel_path), encoding="utf-8").read()
    for m in re.finditer(r"```python\n(.*?)```", text, re.S):
        try:
            exec(m.group(1), ns)
        except Exception:
            pass
    return ns


def T(label, fn):
    global ran
    ran += 1
    try:
        if not fn():
            fails.append(f"WRONG: {label}")
    except Exception as e:
        fails.append(f"ERROR: {label}: {type(e).__name__}: {e}")


def blist(ns, arr):
    L = ns["ListNode"]
    d = c = L(0)
    for x in arr:
        c.next = L(x)
        c = c.next
    return d.next


def toa(x):
    r = []
    while x:
        r.append(x.val)
        x = x.next
    return r


def btree(ns, arr):
    TN = ns["TreeNode"]
    if not arr:
        return None
    root = TN(arr[0])
    dq = deque([root])
    i = 1
    while dq and i < len(arr):
        nd = dq.popleft()
        if i < len(arr) and arr[i] is not None:
            nd.left = TN(arr[i])
            dq.append(nd.left)
        i += 1
        if i < len(arr) and arr[i] is not None:
            nd.right = TN(arr[i])
            dq.append(nd.right)
        i += 1
    return root


P = "patterns/"

n = load(P + "01-two-pointers.md")
T("01.two_sum_sorted", lambda: n["two_sum_sorted"]([2, 7, 11, 15], 9) == [0, 1])
T("01.remove_duplicates", lambda: n["remove_duplicates"]([1, 1, 2]) == 2)

n = load(P + "02-sliding-window.md")
T("02.min_subarray_len", lambda: n["min_subarray_len"](7, [2, 3, 1, 2, 4, 3]) == 2)
T("02.max_sum_k", lambda: n["max_sum_k"]([1, 12, -5, -6, 50, 3], 4) == 51)

n = load(P + "03-prefix-sum.md")
T("03.subarray_sum", lambda: n["subarray_sum"]([1, 2, 3], 3) == 2)

n = load(P + "04-hashing.md")
T("04.contains_duplicate", lambda: n["contains_duplicate"]([1, 2, 1]) is True)
T("04.two_sum", lambda: n["two_sum"]([2, 7, 11, 15], 9) == [0, 1])
T("04.is_anagram", lambda: n["is_anagram"]("anagram", "nagaram") is True)

n = load(P + "05-intervals.md")
T("05.merge", lambda: n["merge"]([[1, 3], [2, 6], [8, 10]]) == [[1, 6], [8, 10]])
T("05.min_meeting_rooms", lambda: n["min_meeting_rooms"]([[0, 30], [5, 10], [15, 20]]) == 2)
T("05.max_concurrent", lambda: n["max_concurrent"]([[0, 30], [5, 10], [15, 20]]) == 2)

n = load(P + "06-cyclic-sort.md")
T("06.missing_number", lambda: n["missing_number"]([3, 0, 1]) == 2)
T("06.find_disappeared", lambda: sorted(n["find_disappeared"]([4, 3, 2, 7, 8, 2, 3, 1])) == [5, 6])
T("06.first_missing_positive", lambda: n["first_missing_positive"]([3, 4, -1, 1]) == 2)

n = load(P + "07-binary-search.md")
T("07.binary_search", lambda: n["binary_search"]([-1, 0, 3, 5, 9, 12], 9) == 4)
T("07.lower_bound", lambda: n["lower_bound"]([1, 2, 2, 3], 2) == 1)
T("07.upper_bound", lambda: n["upper_bound"]([1, 2, 2, 3], 2) == 3)
T("07.min_eating_speed", lambda: n["min_eating_speed"]([3, 6, 7, 11], 8) == 4)

n = load(P + "08-sorting.md")
T("08.largest_number", lambda: n["largest_number"]([10, 2]) == "210")

n = load(P + "09-top-k-quickselect.md")
T("09.kth_largest", lambda: n["kth_largest"]([3, 2, 1, 5, 6, 4], 2) == 5)

n = load(P + "10-linked-list.md")
T("10.reverse_list", lambda: toa(n["reverse_list"](blist(n, [1, 2, 3]))) == [3, 2, 1])
T("10.middle", lambda: n["middle"](blist(n, [1, 2, 3, 4, 5])).val == 3)
T("10.has_cycle", lambda: n["has_cycle"](blist(n, [1, 2, 3])) is False)
T("10.merge_two_lists", lambda: toa(n["merge_two_lists"](blist(n, [1, 3]), blist(n, [2, 4]))) == [1, 2, 3, 4])

n = load(P + "11-stacks.md")
T("11.is_valid", lambda: n["is_valid"]("()[]{}") is True and n["is_valid"]("(]") is False)
T("11.max_sliding_window", lambda: n["max_sliding_window"]([1, 3, -1, -3, 5, 3, 6, 7], 3) == [3, 3, 5, 5, 6, 7])
T("11.largest_rectangle", lambda: n["largest_rectangle"]([2, 1, 5, 6, 2, 3]) == 10)

n = load(P + "12-tree-dfs.md")
T("12.max_depth", lambda: n["max_depth"](btree(n, [3, 9, 20, None, None, 15, 7])) == 3)
T("12.diameter", lambda: n["diameter"](btree(n, [1, 2, 3, 4, 5])) == 3)
T("12.has_path_sum", lambda: n["has_path_sum"](btree(n, [5, 4, 8, 11, None, 13, 4, 7, 2]), 22) is True)

n = load(P + "13-tree-bfs.md")
T("13.level_order", lambda: n["level_order"](btree(n, [3, 9, 20, None, None, 15, 7])) == [[3], [9, 20], [15, 7]])
T("13.min_depth", lambda: n["min_depth"](btree(n, [2, None, 3, None, 4])) == 3)
T("13.right_side_view", lambda: n["right_side_view"](btree(n, [1, 2, 3, None, 5, None, 4])) == [1, 3, 4])

n = load(P + "14-bst.md")
T("14.is_valid_bst", lambda: n["is_valid_bst"](btree(n, [2, 1, 3])) is True and n["is_valid_bst"](btree(n, [5, 1, 4, None, None, 3, 6])) is False)
T("14.kth_smallest", lambda: n["kth_smallest"](btree(n, [3, 1, 4, None, 2]), 1) == 1)
T("14.search_bst", lambda: n["search_bst"](btree(n, [4, 2, 7, 1, 3]), 2).val == 2)

n = load(P + "15-trie.md")


def trie_test():
    tr = n["Trie"]()
    tr.insert("apple")
    sw = getattr(tr, "startsWith", None) or getattr(tr, "starts_with", None)
    return tr.search("apple") and not tr.search("app") and sw("app")


T("15.Trie", trie_test)
T("15.Trie_has_LC_startsWith", lambda: hasattr(n["Trie"](), "startsWith"))
T("15.find_maximum_xor", lambda: n["find_maximum_xor"]([3, 10, 5, 25, 2, 8]) == 28)

n = load(P + "16-graph-traversal.md")
T("16.num_islands", lambda: n["num_islands"]([["1", "1", "0"], ["1", "0", "0"], ["0", "0", "1"]]) == 2)

n = load(P + "17-topological-sort.md")


def topo_test():
    r = n["topo_sort_kahn"](4, [(0, 1), (0, 2), (1, 3), (2, 3)])
    return bool(r) and r.index(0) < r.index(1) and r.index(1) < r.index(3) and r.index(2) < r.index(3)


T("17.topo_sort_kahn", topo_test)

n = load(P + "18-union-find.md")
T("18.count_provinces", lambda: n["count_provinces"]([[1, 1, 0], [1, 1, 0], [0, 0, 1]]) == 2)

n = load(P + "19-shortest-path.md")


def dij_test():
    adj = {0: [(1, 1), (2, 4)], 1: [(2, 2)], 2: [(3, 1)], 3: []}
    return n["dijkstra"](adj, 0, 4)[3] == 4


T("19.dijkstra", dij_test)

n = load(P + "20-backtracking.md")
T("20.subsets", lambda: len(n["subsets"]([1, 2, 3])) == 8)
T("20.permute", lambda: len(n["permute"]([1, 2, 3])) == 6)
T("20.combination_sum", lambda: sorted([sorted(x) for x in n["combination_sum"]([2, 3, 6, 7], 7)]) == [[2, 2, 3], [7]])

n = load(P + "21-dp-linear-knapsack.md")
T("21.rob", lambda: n["rob"]([1, 2, 3, 1]) == 4)
T("21.max_subarray", lambda: n["max_subarray"]([-2, 1, -3, 4, -1, 2, 1, -5, 4]) == 6)
T("21.coin_change", lambda: n["coin_change"]([1, 2, 5], 11) == 3 and n["coin_change"]([2], 3) == -1)

n = load(P + "22-dp-strings.md")
T("22.lis_quadratic", lambda: n["lis_quadratic"]([10, 9, 2, 5, 3, 7, 101, 18]) == 4)
T("22.lis_nlogn", lambda: n["lis_nlogn"]([10, 9, 2, 5, 3, 7, 101, 18]) == 4)
T("22.lcs", lambda: n["lcs"]("abcde", "ace") == 3)
T("22.edit_distance", lambda: n["edit_distance"]("horse", "ros") == 3)
T("22.longest_palindrome_subseq", lambda: n["longest_palindrome_subseq"]("bbbab") == 4)

n = load(P + "23-dp-grids-intervals.md")
T("23.unique_paths", lambda: n["unique_paths"](3, 7) == 28)
T("23.min_path_sum", lambda: n["min_path_sum"]([[1, 3, 1], [1, 5, 1], [4, 2, 1]]) == 7)
T("23.max_coins", lambda: n["max_coins"]([3, 1, 5, 8]) == 167)

n = load(P + "24-heap.md")
T("24.k_largest", lambda: sorted(n["k_largest"]([3, 2, 1, 5, 6, 4], 2)) == [5, 6])


def median_test():
    mf = n["MedianFinder"]()
    for x in [1, 2, 3]:
        mf.addNum(x)
    return mf.findMedian() == 2


T("24.MedianFinder", median_test)

n = load(P + "25-greedy.md")
T("25.can_reach_end", lambda: n["can_reach_end"]([2, 3, 1, 1, 4]) is True and n["can_reach_end"]([3, 2, 1, 0, 4]) is False)
T("25.min_jumps", lambda: n["min_jumps"]([2, 3, 1, 1, 4]) == 2)

n = load(P + "26-bit-manipulation.md")
T("26.single_number", lambda: n["single_number"]([2, 2, 1]) == 1)
T("26.hamming_weight", lambda: n["hamming_weight"](11) == 3)
T("26.subsets", lambda: len(n["subsets"]([1, 2, 3])) == 8)

n = load(P + "27-math.md")
T("27.gcd", lambda: n["gcd"](12, 18) == 6)
T("27.lcm", lambda: n["lcm"](4, 6) == 12)
T("27.count_primes", lambda: n["count_primes"](10) == 4)
T("27.fast_pow", lambda: n["fast_pow"](2, 10) == 1024)

n = load(P + "28-design.md")


def lru_test():
    c = n["LRUCache"](2)
    c.put(1, 1)
    c.put(2, 2)
    if c.get(1) != 1:
        return False
    c.put(3, 3)
    if c.get(2) != -1:
        return False
    c.put(4, 4)
    return c.get(1) == -1 and c.get(3) == 3 and c.get(4) == 4


T("28.LRUCache", lru_test)

n = load(P + "29-segment-tree-fenwick.md")


def bit_test():
    bit = n["BIT"](5)
    for i, v in enumerate([1, 2, 3, 4, 5], 1):
        bit.update(i, v)
    return bit.query(3) == 6 and bit.range_query(2, 4) == 9


T("29.BIT", bit_test)
T("29.SegTree", lambda: n["SegTree"]([1, 2, 3, 4, 5]).query(1, 4) == 9)
T("29.count_smaller", lambda: n["count_smaller"]([5, 2, 6, 1]) == [2, 1, 1, 0])

n = load(P + "30-state-machine-dp.md")
T("30.max_profit_unlimited", lambda: n["max_profit_unlimited"]([7, 1, 5, 3, 6, 4]) == 7)
T("30.max_profit_k", lambda: n["max_profit_k"](2, [3, 2, 6, 5, 0, 3]) == 7)
T("30.max_profit_cooldown", lambda: n["max_profit_cooldown"]([1, 2, 3, 0, 2]) == 3)
T("30.max_profit_fee", lambda: n["max_profit_fee"]([1, 3, 2, 8, 4, 9], 2) == 8)


n = load(P + "31-string-matching.md")
T("31.build_lps", lambda: n["build_lps"]("ababc") == [0, 0, 1, 2, 0])
T("31.kmp_search", lambda: n["kmp_search"]("mississippi", "issip") == 4 and n["kmp_search"]("abc", "xyz") == -1)
T("31.rabin_karp", lambda: n["rabin_karp"]("sadbutsad", "sad") == 0 and n["rabin_karp"]("leetcode", "leeto") == -1)
T("31.repeated_substring", lambda: n["repeated_substring"]("abab") is True and n["repeated_substring"]("aba") is False)


if fails:
    print(f"FAIL: {len(fails)} of {ran} template checks failed\n")
    for f in fails:
        print("  " + f)
    sys.exit(1)
print(f"OK: all {ran} code templates run correctly against known LeetCode answers")
