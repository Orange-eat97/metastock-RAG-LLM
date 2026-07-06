---
canonical_id: function.if
title: If
type: function
card_bucket: functions
category: logic
source: generated_curated_from_primer
status: active
priority: 10
supports_explorer: true
function: If
aliases:
- text: If
  type: exact
  weight: 1.0
- text: conditional function
  type: synonym
  weight: 0.9
- text: if then else
  type: phrase
  weight: 0.9
- text: binary wave
  type: phrase
  weight: 0.8
- text: conditional output
  type: phrase
  weight: 0.85
suggests:
- canonical_id: function.sum
  rationale: If conditions are often counted with Sum.
  priority: 30
  properties:
    formula_role: conditional_count
- canonical_id: function.ref
  rationale: If is often combined with previous values.
  priority: 30
  properties:
    formula_role: previous_value_condition
semantic:
  concept_role: function
  mechanism: logic
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
  canonical_id: function.if
  supports_explorer: true
  priority: 10
  properties:
    formula_role: logic
    source_path: functions/if.md
    curation_level: upgraded_to_curated_quality
---

# If

## Purpose

`If` returns one value when a condition is true and another value when it is false. It is the main explicit conditional function in MetaStock. For Explorer filters, a bare condition such as `C > Mov(C,40,S)` is often enough, but `If` is useful when a formula must output a numeric state, score, flag, or switch.

## Syntax

```metastock
If(CONDITION, TRUE RESULT, FALSE RESULT)
```

## Parameters

| Parameter | Meaning | Common values |
|---|---|---|
| CONDITION | A comparison or logical expression. | `C > Mov(C,40,S)` |
| TRUE RESULT | Value returned if condition is true. | `1`, `C`, `RSI(14)` |
| FALSE RESULT | Value returned if condition is false. | `0`, `PREV`, `-1` |

## Default interpretation

For simple Explorer filters, prefer the condition itself. Use `If` when the user asks for a grade, score, binary flag, or a formula that must output different values under different cases.

## Common formulas

```metastock
If(C > Mov(C,40,S),1,0)
If(RSI(14) < 30,1,0)
If(C > Mov(C,50,S), RSI(14), 0)
If(MACD() > Mov(MACD(),9,E),1,If(MACD() < Mov(MACD(),9,E),-1,0))
```

## Natural language mappings

Use this function when the user says:

- if
- if then else
- conditional formula
- binary wave
- flag condition
- score when true
- return 1 otherwise 0
- state switch

## Explorer column usage

Use `If` columns when the result table should show a numeric flag or score. The filter can often use the plain condition instead of `If(condition,1,0)=1`.

## Explorer examples

### Example 1: Binary flag for close above MA

User request:

```text
Show a flag when close is above 40 day moving average
```

Explorer output:

```text
Column A: C
Column B: Mov(C,40,S)
Column C: If(ColA > ColB,1,0)
Filter: ColC = 1
```
Notes:

```text
For maximum historical safety, use `If(C > Mov(C,40,S),1,0)` directly in Column C rather than relying on ColA/ColB inside a historical function.
```
### Example 2: Filter without If

User request:

```text
Find stocks where close is above 40 day moving average
```

Explorer output:

```text
Column A: C
Column B: Mov(C,40,S)
Filter: ColA > ColB
```

## Filter-only usage

If the user only needs a pass/fail condition and does not need to inspect intermediate values, the function may be used directly in the Filter. For this project, prefer columns when the value helps the result table or when a pattern has multiple logical components.

## Valid Examples

```metastock
If(C > Mov(C,40,S),1,0)
If(RSI(14) > 70, -1, 0)
C > Mov(C,40,S)
```

## Common Mistakes

- Bad: `If(C > Mov(C,40,S),1)`. Correct: `If(C > Mov(C,40,S),1,0)`.
- Bad: using natural-language THEN/ELSE text inside a numeric formula.
- Bad: using `If` unnecessarily for simple Explorer filters when the condition itself is clearer.
- Bad: omitting parentheses around complex `AND`/`OR` conditions.

## Assumptions

- MetaStock treats a true condition as non-zero and false as zero.
- Explorer filters can use direct logical conditions without wrapping them in `If`.
- Nested `If` expressions are valid but should be kept readable.

## Related Patterns

- pattern.logical_switch_state_machine
- function.sum
- function.barssince

## Related functions and concepts

- Explorer columns and filters
- Price fields such as `C`, `H`, `L`, `O`, and `V`
- `Cross` when the user asks for a crossing event
- `Ref` when the user asks for previous-bar or prior-event logic



## Retrieval keywords

If, conditional, binary wave, if then else, logic, state flag.

## Test Queries

- Find stocks where close is above the 40 day moving average
- Create a flag for RSI below 30
