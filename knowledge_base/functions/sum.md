---
canonical_id: function.sum
title: Sum
type: function
card_bucket: functions
category: aggregation
source: generated_curated_from_primer
status: active
priority: 10
supports_explorer: true
function: Sum
aliases:
- text: Sum
  type: exact
  weight: 1.0
- text: summation
  type: synonym
  weight: 0.9
- text: total over periods
  type: phrase
  weight: 0.85
- text: consecutive bars
  type: phrase
  weight: 0.9
- text: last 5 bars all true
  type: phrase
  weight: 0.9
suggests:
- canonical_id: function.if
  rationale: Sum is often used with boolean conditions or If expressions.
  priority: 30
  properties:
    formula_role: conditional_count
- canonical_id: function.mov
  rationale: Moving averages can be replicated as Sum divided by periods.
  priority: 30
  properties:
    formula_role: average_equivalent
semantic:
  concept_role: function
  mechanism: aggregation
  market_object: price
  outputs:
  - indicator_series
  supports_conditions:
  - threshold_comparison
  - crossover
  - state_filter
  does_not_cover:
  - complete_trading_pattern_by_itself
registry:
  enabled: true
  canonical_id: function.sum
  supports_explorer: true
  priority: 10
  properties:
    formula_role: aggregation
    source_path: functions/sum.md
    curation_level: upgraded_to_curated_quality
---

# Sum

## Purpose

`Sum` totals the values of a data array over the last specified number of records. It includes the current record. In Explorer generation, it is very useful for counting how many recent bars satisfied a condition, such as five consecutive closes above a moving average.

## Syntax

```metastock
Sum(DATA ARRAY, PERIODS)
```

## Parameters

| Parameter | Meaning | Common values |
|---|---|---|
| DATA ARRAY | Series or condition to total. Conditions evaluate as 1/0. | `C`, `V`, `C > Mov(C,20,S)` |
| PERIODS | Number of records to include, including the current bar. | `3`, `5`, `10`, `20` |

## Default interpretation

If the user says “for N consecutive bars”, use `Sum(condition,N)=N`. If the user says “at least M of the last N bars”, use `Sum(condition,N) >= M`.

## Common formulas

```metastock
Sum(C,20)
Sum(V,20)
Sum(C > Mov(C,20,S),5) = 5
Sum(RSI(14) < 30,10) >= 3
Sum(C > Ref(C,-1),3) = 3
Sum(C,14) / 14
```

## Natural language mappings

Use this function when the user says:

- sum
- summation
- total over 20 periods
- consecutive bars
- last five bars
- at least three of the last ten days
- all recent bars
- count days where condition is true

## Explorer column usage

Use `Sum(condition,N)=N` for consecutive-condition filters. Avoid using Explorer columns inside `Sum`; put the full formula inside `Sum` because `ColA` is not a historical data array.

## Explorer examples

### Example 1: Close above 20 MA for 5 consecutive bars

User request:

```text
Find stocks where close has been above the 20 day moving average for 5 consecutive bars
```

Explorer output:

```text
Column A: C
Column B: Mov(C,20,S)
Column C: Sum(C > Mov(C,20,S),5)
Filter: ColC = 5
```
### Example 2: At least 3 oversold days in the last 10 bars

User request:

```text
Find stocks where RSI was below 30 at least 3 times in the last 10 days
```

Explorer output:

```text
Column A: RSI(14)
Column B: Sum(RSI(14) < 30,10)
Filter: ColB >= 3
```

## Filter-only usage

If the user only needs a pass/fail condition and does not need to inspect intermediate values, the function may be used directly in the Filter. For this project, prefer columns when the value helps the result table or when a pattern has multiple logical components.

## Valid Examples

```metastock
Sum(C,20)
Sum(C > Mov(C,20,S),5) = 5
Sum(RSI(14) < 30,10) >= 3
```

## Common Mistakes

- Bad: `Sum(ColA,5)` to count prior column values. Correct: repeat the underlying formula, e.g. `Sum(C > Mov(C,20,S),5)`.
- Bad: forgetting that the current bar is included. For previous-only logic use `Ref(Sum(condition,N),-1)` or build a previous-window expression.
- Bad: using `Sum` when the user only asks for a single-bar condition.

## Assumptions

- Conditions inside `Sum` are treated as 1 when true and 0 when false.
- The current bar is included in the sum.
- Consecutive N bars means `Sum(condition,N)=N`.

## Related Patterns

- pattern.consecutive_condition
- function.if
- function.mov

## Related functions and concepts

- Explorer columns and filters
- Price fields such as `C`, `H`, `L`, `O`, and `V`
- `Cross` when the user asks for a crossing event
- `Ref` when the user asks for previous-bar or prior-event logic



## Retrieval keywords

Sum, summation, consecutive bars, count condition, last N bars, at least N days.

## Test Queries

- Find stocks above the 20 MA for 5 consecutive bars
- Find stocks where RSI was oversold at least 3 days in the last 10
