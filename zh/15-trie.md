# 15 - 字典树 Trie

> 中文版。English: [15-trie](../patterns/15-trie.md)

> **题目形态:**「实现一个支持 insert、search 和 startsWith 的前缀树。」「设计一个支持 `.` 作为通配符的字典。」「在一个字母网格里找出所有藏着的字典单词。」「给定一个整数数组,找出其中任意两个数的最大异或值。」凡是关于共享前缀、逐字符增量匹配、或逐位贪心选择的,都属于这一类。

字典树(前缀树)通过在从根出发的路径上共享公共前缀来存储一组字符串。每条边是一个字符,所以一个长度为 L 的单词插入或查找只要 O(L),与已存了多少单词无关。正是这种前缀共享让它在前缀查询、通配符匹配和网格找词剪枝上胜过哈希集合,而它的按位版本则驱动了最大异或类问题。

## 识别信号

看到以下情况就该想到字典树:

- **大规模前缀查询**:「是否有单词以这个前缀开头」、自动补全、「统计有多少单词带某前缀」。哈希集合能回答「这个确切单词在不在」,但不扫全部就无法回答前缀问题。
- **对字典做增量匹配**:你一次消费一个字符的输入,并想在每一步知道自己是否仍在一个有效前缀上。
- **对词表做通配符或模糊搜索**:「用 `.` 匹配任意字母来搜索」。字典树让你只在需要的地方分叉 DFS,而不是测试每个已存单词。
- **在网格里找词**:一次匹配许多目标单词。为这些单词建一棵字典树,一次网格 DFS 就能在当前路径离开所有单词的前缀时立刻剪枝。
- **最大异或 / 按位贪心的成对问题**:把数字当作定宽的位串存进二进制字典树,这样你就能在每一层贪心地追逐相反的位来最大化异或值。

标志是「许多共享结构的字符串(或位模式),按前缀查询或逐符号构建」。

## 核心思想

一个字典树节点持有一个从下一个字符到子节点的映射,外加一个标志,标记是否有一个完整单词在此结束。插入沿路行走(创建缺失的孩子),每个字符一个节点;终止节点的 `is_word = True`。搜索沿同一路径行走并检查标志;`startsWith` 沿路径行走,只需到达即可,标志无关紧要。

![存储 cat、car、dog 且共享 ca 前缀的字典树](../assets/trie.svg)

*单词「cat」、「car」、「dog」。cat 和 car 的「ca」前缀作为共享主干只存一次;完整单词在其终止节点被打上标志。*

它的威力来自两个性质:

- **共享前缀只存一次。** 「app」、「apple」、「apply」共享 `a-p-p` 主干,所以空间与不同前缀的数量成正比,而任何前缀查询都是 O(L),与字典大小无关。
- **树结构会剪枝搜索。** 对通配符,一个 `.` 把 DFS 扇出到所有孩子,但每个非通配符字符仍收敛到单个孩子,所以你只探索存活的前缀。对网格找词,一旦网格路径拼出一个在字典树里没有对应孩子的字符串,你立刻放弃那条分支。

按位字典树是同样的结构,只是字母表只有 `{0, 1}`:把每个数字的位从最高位往下存,要最大化 `x XOR y`,就沿 `x` 的位贪心地在每一层优先选相反的位(相反的位异或得 1,而高位占主导)。

## 模板

**标准字典树:insert、search、startsWith。**

```python
# Space: O(1)
class TrieNode:
    # Time: O(1)
    def __init__(self):
        self.children = {}      # char -> TrieNode
        self.is_word = False

# Space: O(total chars * alphabet)
class Trie:
    # Time: O(1)
    def __init__(self):
        self.root = TrieNode()

    # Time: O(L) where L = word length
    def insert(self, word):
        node = self.root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.is_word = True

    # Time: O(L) where L = word length
    def search(self, word):
        node = self._walk(word)
        return node is not None and node.is_word

    # Time: O(L) where L = prefix length
    def startsWith(self, prefix):   # LeetCode 208 requires this exact method name
        return self._walk(prefix) is not None

    # Time: O(L) where L = length of s
    def _walk(self, s):
        node = self.root
        for ch in s:
            if ch not in node.children:
                return None
            node = node.children[ch]
        return node
```

**通配符搜索(`.` 匹配任意字母):在字典树上做 DFS。**

```python
# Space: O(total chars * alphabet)
class WordDictionary:
    # Time: O(1)
    def __init__(self):
        self.root = TrieNode()

    # Time: O(L) where L = word length
    def add_word(self, word):
        node = self.root
        for ch in word:
            node = node.children.setdefault(ch, TrieNode())
        node.is_word = True

    # Time: O(alphabet^k * L) worst, k = number of wildcards
    def search(self, word):
        def dfs(node, i):
            if i == len(word):
                return node.is_word
            ch = word[i]
            if ch == '.':
                return any(dfs(child, i + 1) for child in node.children.values())
            return ch in node.children and dfs(node.children[ch], i + 1)
        return dfs(self.root, 0)
```

**单词搜索 II:为单词建一棵字典树,DFS 网格并按字典树剪枝。**

```python
# Time: O(total chars in words + M * N * 4 * 3^(L - 1)) where L = max word length, Space: O(total chars in words)
def find_words(board, words):
    root = TrieNode()
    for w in words:                     # build the trie of targets
        node = root
        for ch in w:
            node = node.children.setdefault(ch, TrieNode())
        node.word = w                   # stash the full word at its end node

    rows, cols = len(board), len(board[0])
    found = []

    def dfs(r, c, node):
        ch = board[r][c]
        nxt = node.children.get(ch)
        if not nxt:                     # this prefix is in no word: prune
            return
        if getattr(nxt, 'word', None):
            found.append(nxt.word)
            nxt.word = None             # de-dup: do not report twice
        board[r][c] = '#'               # mark visited
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] != '#':
                dfs(nr, nc, nxt)
        board[r][c] = ch                # restore (backtrack)

    for r in range(rows):
        for c in range(cols):
            dfs(r, c, root)
    return found
```

**求两数最大异或的二进制字典树。**

```python
# Time: O(n * 32), Space: O(n * 32)
def find_maximum_xor(nums, bits=31):
    root = {}
    for x in nums:                      # insert each number's bits, MSB first
        node = root
        for i in range(bits, -1, -1):
            b = (x >> i) & 1
            node = node.setdefault(b, {})

    best = 0
    for x in nums:
        node, cur = root, 0
        for i in range(bits, -1, -1):
            b = (x >> i) & 1
            want = 1 - b                # greedily chase the opposite bit
            if want in node:
                cur |= (1 << i)         # that bit of the XOR is 1
                node = node[want]
            else:
                node = node[b]
        best = max(best, cur)
    return best
```

## 变体

- **终止标志 vs 存储单词。** 用布尔 `is_word` 表示成员关系,或者当你需要产出它时,在终止节点存下整个字符串 / 一个载荷(单词搜索 II、自动补全结果列表)。
- **用数组孩子代替字典。** 对固定的小写字母表,一个长度为 26 的子指针数组比哈希表更快、更缓存友好。字典对稀疏或未知的字母表更简洁。
- **在节点上计数 / 记频。** 在每个节点存一个 `prefix_count` 来在 O(L) 内回答「有多少单词共享这个前缀」,或者为多重集字典树存一个单词计数。
- **删除。** 取消终止标志;可选地在回溯途中剪掉那些变得既无孩子又非终止的节点。
- **后缀 / 反向字典树。** 插入反转后的单词来回答后缀查询,或者组合一棵正向和一棵反向字典树来「按前缀和后缀搜索单词」。
- **按位字典树扩展。** 加上每节点计数以支持删除,从而实现「在元素增删下求最大异或」或「限制下求最大异或」等查询变体。

## 经典题目

| # | 题目 | 难度 | 训练点 |
|---|---------|-----------|----------------|
| 208 | Implement Trie (Prefix Tree) | 中等 | insert、search、startsWith 核心 |
| 211 | Design Add and Search Words Data Structure | 中等 | 在字典树上做通配符 DFS |
| 212 | Word Search II | 困难 | 字典树加网格回溯,按前缀剪枝 |
| 421 | Maximum XOR of Two Numbers in an Array | 中等 | 二进制字典树,贪心追相反位 |
| 648 | Replace Words | 中等 | 扫描时查最短前缀 |
| 677 | Map Sum Pairs | 中等 | 在字典树节点上做前缀和聚合 |
| 1268 | Search Suggestions System | 中等 | 前缀自动补全,每个前缀取最优匹配 |
| 720 | Longest Word in Dictionary | 中等 | 能逐字符构建出来的单词 |

## 常见坑

- **混淆 search 与 startsWith。** `search` 必须在终止节点检查 `is_word`;`startsWith` 一定不能。前缀查询返回该标志会把缺失单词误报,而 `search` 忽略它会把前缀误报成完整单词。
- **通配符搜索不剪枝。** 用测试每个已存单词的方式来实现 `.` 就失去意义了。只在 `node.children` 上分叉 DFS,这样非通配符字符仍收敛到单个孩子。
- **网格找词忘了回溯。** DFS 返回后要恢复 `board[r][c]`,否则该格子一直被标记,其他单词无法复用它。
- **单词搜索 II 里报了重复。** 找到后把存下的单词置空(或用一个集合),这样同一个单词不会为多条网格路径重复产出。
- **异或字典树里位序错了。** 从最高位往下插入和查询;高位主导异或值,所以贪心选择只在自顶向下时成立。同时把位宽固定到能覆盖最大输入。
- **内存爆炸。** 在巨大字母表或数百万长单词上用每节点一字典的字典树很重;改用数组、压缩单孩子链(基数树),或者当你只需要精确查找时重新考虑哈希集合是否够用。

## 延伸与相关模式

- 「我只需要精确成员关系,不需要前缀」意味着朴素哈希集合胜过字典树;只有在查询*前缀*结构时才专门用字典树。
- 单词搜索 II 是字典树与 [回溯](20-backtracking.md) 的融合:网格 DFS 是标准回溯,而字典树是剪枝的判定器。
- 带已访问标记和恢复的网格行走,是在隐式网格图上的 [图遍历](16-graph-traversal.md)。
- 二进制字典树的贪心取位技巧就在 [位运算](26-bit-manipulation.md) 旁边;同样的「最高位优先、高位主导」的推理在异或和子集问题里也会出现。
- 「在一趟文本扫描里匹配许多模式」把字典树推广到 Aho-Corasick(带失配链接的字典树),即字符串匹配的多模式表亲。
