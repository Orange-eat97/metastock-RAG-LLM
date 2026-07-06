---
canonical_id: pattern.consecutive_condition
title: 'Pattern: Consecutive Condition'
type: pattern
card_bucket: patterns
category: condition_persistence
source: MetaStock Formula Primer / Formula Primer II / internal project pattern
status: active
priority: 10
supports_explorer: true
functions:
- Sum
- Ref
- Mov
aliases:
- text: 'Pattern: Consecutive Condition'
  type: synonym
  weight: 0.85
- text: Consecutive Condition
  type: exact
  weight: 1.0
- text: condition held for N bars
  type: synonym
  weight: 0.85
- text: stayed above
  type: phrase
  weight: 0.9
- text: for five days in a row
  type: synonym
  weight: 0.85
- text: consecutive bars
  type: synonym
  weight: 0.85
- text: for N days in a row
  type: synonym
  weight: 0.85
- text: remained below
  type: phrase
  weight: 0.9
- text: held above moving average
  type: phrase
  weight: 0.9
- text: above MA for five days
  type: phrase
  weight: 0.9
- text: true for all last N bars
  type: synonym
  weight: 0.85
- text: at least three of the last five days
  type: synonym
  weight: 0.85
- text: repeated confirmation
  type: synonym
  weight: 0.85
requires:
- canonical_id: function.sum
  rationale: This card usually needs function.sum for correct formula generation.
  priority: 10
  properties:
    source: registry_ready_transform
    formula_role: requires
suggests:
- canonical_id: function.ref
  rationale: function.ref is often useful context for this card but is not always mandatory.
  priority: 40
  properties:
    source: registry_ready_transform
    formula_role: suggests
- canonical_id: template.explorer_columns_filter
  rationale: template.explorer_columns_filter is often useful context for this card but is not always mandatory.
  priority: 40
  properties:
    source: registry_ready_transform
    formula_role: suggests
semantic:
  concept_role: pattern
  mechanism: condition_persistence
  market_object: price
  directions_supported:
  - bullish
  - bearish
  operations_supported:
  - condition_persistence
  required_components:
  - sum
  does_not_cover:
  - unrelated_pattern_substitution
  - guaranteed_trade_profitability
registry:
  enabled: true
  canonical_id: pattern.consecutive_condition
  supports_explorer: true
  priority: 10
  properties:
    source_path: patterns/consecutive_condition.md
    generated_schema_version: registry_ready_v2
---

# Pattern: Consecutive Condition

## Intent

Detect stocks where a condition has remained true for several consecutive bars or has been true a minimum number of times in a recent window.

This pattern is used when the user describes persistence, stability, follow-through, or repeated confirmation.

## Natural Language Triggers

- consecutive bars
- for N days in a row
- stayed above
- remained below
- held above moving average
- above MA for five days
- true for all last N bars
- at least three of the last five days
- repeated confirmation

## Keywords

- consecutive
- stayed above
- held above
- remained below
- Sum(condition,N)=N
- at least N of last M
- condition persistence
- follow-through

## Required Logical Components

1. Define the base condition.
2. Choose the lookback window.
3. Decide whether all bars must pass or only at least K bars must pass.
4. Use `Sum(condition,N)` because true conditions contribute `1` and false conditions contribute `0`.

## Formula Building Blocks

All last 5 bars above 20 MA:

```metastock
Sum(C > Mov(C,20,S),5) = 5
```

At least 3 of last 5 bars closed higher than prior close:

```metastock
Sum(C > Ref(C,-1),5) >= 3
```

RSI rising for 3 bars:

```metastock
Sum(RSI(14) > Ref(RSI(14),-1),3) = 3
```

## Composition Guidance

- Use `= N` when the user says every bar, all bars, or N days in a row.
- Use `>= K` when the user says at least K times in the last N bars.
- Keep the base condition simple and testable.
- If the base condition contains a historical comparison, use `Ref` inside the condition.

## Example Compositions

Close stayed above 50 MA for 5 bars:

```metastock
Sum(C > Mov(C,50,S),5) = 5
```

Volume above average at least 3 times in 5 bars:

```metastock
Sum(V > Mov(V,20,S),5) >= 3
```

## Observable Outputs

Useful Explorer columns:

- Count of passing bars: `Sum(condition,N)`
- Base value being tested: e.g. `C`
- Reference value: e.g. `Mov(C,50,S)`

## Explorer examples

### Example 1: Above 20 MA for five days

User request:

```text
Find stocks that stayed above the 20 day moving average for five consecutive days
```

Explorer output:

```text
Column A: C
Column B: Mov(C,20,S)
Column C: Sum(C > Mov(C,20,S),5)
Filter: ColC = 5
```

### Example 2: Volume confirmation in recent bars

User request:

```text
Find stocks where volume was above average on at least three of the last five days
```

Explorer output:

```text
Column A: Sum(V > Mov(V,20,S),5)
Filter: ColA >= 3
```

## Pitfalls

- Do not use `BarsSince` for “all last N bars”. Use `Sum(condition,N)=N`.
- Do not use `Sum(DATA,N)` when you need an average; use `Mov`.
- If the user asks for a current-bar event only, do not add persistence unless requested.

## Default Assumptions

- “For N days in a row” means `Sum(condition,N)=N`.
- “At least K of the last N days” means `Sum(condition,N)>=K`.
- The current bar is included in the lookback.

## Related functions and concepts

- Sum: count true conditions
- Ref: previous-bar comparison
- BarsSince: recent event age
- Mov: moving average condition

## Retrieval keywords

consecutive condition, for N days in a row, stayed above, held above, remained below, at least three of last five, Sum(condition,N)=N, Sum(C > Mov(C,20,S),5)=5.

## Test Queries

- Find stocks where close has stayed above the 20 day moving average for five bars
- Find stocks where RSI has been above 50 for three consecutive bars
