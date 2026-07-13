# 30 - State-machine DP (stock series)

> **Problem shape:** "Best time to buy and sell stock, at most k transactions."
> "...with a cooldown after selling." "...with a transaction fee." Any problem
> where you move through a sequence and at each step you are in one of a few
> **states** (holding, not holding, in cooldown), with fixed rules for moving
> between them. The stock series is the canonical family, but paint-house and
> similar problems share the shape.

This is [dynamic programming](21-dp-linear-knapsack.md) where the state is not just
"position i" but "position i **and** which mode am I in". Once you name the modes
and the legal transitions between them, the recurrence writes itself and the six
stock problems become one template with small tweaks. Interviewers love this
family because it looks like six problems and is really one idea.

## The signal

Reach for state-machine DP when:

- At each step you are in one of a **small, fixed set of states**, and your options
  depend on which state you are in. For stocks: "holding a share" vs "holding
  cash" are two states; a cooldown adds a third.
- There is a **cost or reward on each transition** (buy pays the price, sell earns
  it, maybe minus a fee), and you want to maximize or minimize the total over the
  whole sequence.
- The problem is a **variation on a base problem** by adding a rule (a cooldown, a
  fee, a cap on the number of transactions). That "base plus a twist" smell is the
  giveaway that one state machine covers all the variants.
- Phrases like "at most k times", "cannot buy again until", "you may complete as
  many transactions as you like".

## The idea

Draw the states as nodes and the legal moves as arrows, then keep one DP value per
state and update them left to right across the sequence. For the stock problems the
core machine has two states:

- **cash**: you hold no share. You can stay in cash, or buy (pay `price`, move to
  hold).
- **hold**: you hold one share. You can stay in hold, or sell (earn `price`, move
  to cash).

`cash = max(cash, hold + price)` and `hold = max(hold, cash - price)`, applied for
each price, is the entire unlimited-transactions solution. Every variant is this
machine with an edit:

- **One transaction** (121): buy resets from 0, not from prior cash.
- **At most k** (188, 123 is k = 2): index every state by the transaction count.
- **Cooldown** (309): add a **sold** state that must pass through a rest day before
  buying again.
- **Fee** (714): subtract the fee on the sell transition.

The number of states stays tiny, so the DP is O(n) or O(n * k) time and O(1) or
O(k) space.

## The template

**Unlimited transactions (122), the two-state core:**

```python
def max_profit_unlimited(prices):
    cash, hold = 0, float('-inf')
    for p in prices:
        cash = max(cash, hold + p)     # sell, or stay in cash
        hold = max(hold, cash - p)     # buy, or stay holding
    return cash
```

**At most k transactions (188, and 123 with k = 2):**

```python
def max_profit_k(k, prices):
    n = len(prices)
    if n == 0 or k == 0:
        return 0
    if k >= n // 2:                    # k is effectively unlimited
        return sum(max(0, prices[i + 1] - prices[i]) for i in range(n - 1))
    cash = [0] * (k + 1)
    hold = [float('-inf')] * (k + 1)
    for p in prices:
        for t in range(1, k + 1):
            hold[t] = max(hold[t], cash[t - 1] - p)   # buying opens transaction t
            cash[t] = max(cash[t], hold[t] + p)       # selling closes it
    return cash[k]
```

**Cooldown (309), a three-state machine:**

```python
def max_profit_cooldown(prices):
    hold, sold, rest = float('-inf'), 0, 0
    for p in prices:
        prev_sold = sold
        sold = hold + p                # sell today, enter the sold state
        hold = max(hold, rest - p)     # keep holding, or buy from a rested state
        rest = max(rest, prev_sold)    # rest, or come off the cooldown
    return max(sold, rest)
```

**Transaction fee (714):** the unlimited core with the fee on the sell edge:

```python
def max_profit_fee(prices, fee):
    cash, hold = 0, float('-inf')
    for p in prices:
        cash = max(cash, hold + p - fee)
        hold = max(hold, cash - p)
    return cash
```

## Variations

- **The whole stock ladder**: 121 (one transaction), 122 (unlimited), 123 (two),
  188 (k), 309 (cooldown), 714 (fee). Solve 122 first, then add each rule and watch
  one line change.
- **Paint house / paint fence** (256, 265): the state is "which color did I paint
  the last house", transitions forbid repeating a color. Same machine, different
  states.
- **Delete and earn** (740): reduces to house-robber after a counting step, which
  is itself a two-state (take / skip) machine.
- **General finite-state DP**: whenever you can enumerate a handful of modes and the
  legal transitions among them, this pattern applies beyond stocks.

## Canonical problems

| # | Problem | Difficulty | What it drills |
|---|---------|-----------|----------------|
| 121 | Best Time to Buy and Sell Stock | Easy | One transaction, track min-so-far or one state |
| 122 | Best Time to Buy and Sell Stock II | Medium | The two-state unlimited core |
| 123 | Best Time to Buy and Sell Stock III | Hard | At most two transactions |
| 188 | Best Time to Buy and Sell Stock IV | Hard | At most k transactions, state indexed by count |
| 309 | Best Time to Buy and Sell Stock with Cooldown | Medium | A third state for the cooldown |
| 714 | Best Time to Buy and Sell Stock with Transaction Fee | Medium | Fee on the sell transition |
| 256 | Paint House | Medium | State is the last color chosen |
| 740 | Delete and Earn | Medium | Reduces to a take/skip state machine |

## Pitfalls

- **Initializing `hold` to 0 instead of negative infinity.** Before you have
  bought anything, "holding" is impossible; seed it to `float('-inf')` so a phantom
  free share cannot leak into the answer.
- **Overwriting a state you still need this step.** In the cooldown machine, save
  `prev_sold` before you overwrite `sold`, or the `rest` update reads the wrong
  value. Update order matters when states depend on each other's old values.
- **Missing the k >= n/2 shortcut.** With k large enough, the cap never binds and
  the O(n * k) table can blow up (188 has k up to 10^9). Fall back to the unlimited
  formula when `k >= n // 2`.
- **Modeling too many states.** The stock machine needs two or three states, not
  one per day times per price. If your state space is huge, you have mis-modeled;
  find the small set of modes.

## Follow-ups and related patterns

- "There is no state, just a 1D choice" pulls back to plain
  [DP I: linear and knapsack](21-dp-linear-knapsack.md); house-robber is the
  simplest take/skip machine.
- "The transitions depend on two sequences" points at
  [DP II: subsequences and strings](22-dp-strings.md).
- "A greedy pick works" (122 can also be solved by summing every positive
  price step) points at [greedy](25-greedy.md); state-machine DP is the safe
  general form when greedy is not obviously correct.
- The general technique (enumerate states, define transitions) is the same modeling
  skill behind [bitmask DP](23-dp-grids-intervals.md), where the state is a subset.
