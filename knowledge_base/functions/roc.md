---
canonical_id: function.roc
title: ROC
type: function
card_bucket: functions
category: momentum
source: generated_curated_from_primer
status: active
priority: 10
supports_explorer: true
function: ROC
aliases:
- text: ROC
  type: abbreviation
  weight: 1.0
- text: rate of change
  type: exact
  weight: 1.0
- text: percentage change
  type: phrase
  weight: 0.9
- text: point change
  type: phrase
  weight: 0.9
- text: momentum change
  type: phrase
  weight: 0.85
suggests:
- canonical_id: function.ref
  rationale: ROC can be replicated with Ref and is often used for previous-period comparisons.
  priority: 30
  properties:
    formula_role: time_reference_equivalent
semantic:
  concept_role: function
  mechanism: momentum
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
  canonical_id: function.roc
  supports_explorer: true
  priority: 10
  properties:
    formula_role: momentum
    source_path: functions/roc.md
    curation_level: upgraded_to_curated_quality
---

# ROC

## Purpose

`ROC` calculates rate of change over a number of periods. It can express the result as percent change using `%` or point change using `$`. In Explorer generation, it is used for momentum filters, price-change thresholds, and rising/falling confirmations.

## Syntax

```metastock
ROC(DATA ARRAY, PERIODS, DIFF_METHOD)
```

## Parameters

| Parameter | Meaning | Common values |
|---|---|---|
| DATA ARRAY | Series to compare against its prior value. | `C`, `V`, `Mov(C,20,S)`, `RSI(14)` |
| PERIODS | Lookback length. | `1`, `3`, `5`, `20` |
| DIFF_METHOD | Difference method. | `%` for percent, `$` for points |

## Default interpretation

If the user says “percentage change”, use `%`. If the user says “point change” or “up by points”, use `$`. If the user says “rising from previous bar”, `ROC(DATA ARRAY,1,$) > 0` is acceptable, though `DATA ARRAY > Ref(DATA ARRAY,-1)` is often clearer.

## Common formulas

```metastock
ROC(C,1,$)
ROC(C,5,%)
ROC(C,3,%) <= -5
ROC(V,1,$) > 0
ROC(Mov(C,20,S),1,$) > 0
```

## Natural language mappings

Use this function when the user says:

- rate of change
- ROC
- percentage change
- percent gain
- percent loss
- price dropped 5 percent
- momentum positive
- rising over 3 days
- falling over 5 days

## Explorer column usage

Use ROC as a displayed column when the user wants to inspect percentage or point change. Combine with thresholds directly in the filter.

## Explorer examples

### Example 1: Five-day percentage gain

User request:

```text
Find stocks up more than 10 percent over 5 days
```

Explorer output:

```text
Column A: ROC(C,5,%)
Filter: ColA > 10
```
### Example 2: Price dropped 5 percent in 3 bars

User request:

```text
Find stocks that dropped at least 5 percent over the last 3 periods
```

Explorer output:

```text
Column A: ROC(C,3,%)
Filter: ColA <= -5
```
### Example 3: Moving average rising

User request:

```text
Find stocks where the 20 day moving average is rising
```

Explorer output:

```text
Column A: Mov(C,20,S)
Column B: ROC(Mov(C,20,S),1,$)
Filter: ColB > 0
```

## Filter-only usage

If the user only needs a pass/fail condition and does not need to inspect intermediate values, the function may be used directly in the Filter. For this project, prefer columns when the value helps the result table or when a pattern has multiple logical components.

## Valid Examples

```metastock
ROC(C,5,%) > 10
ROC(C,1,$) > 0
ROC(Mov(C,20,S),1,$) > 0
```

## Common Mistakes

- Bad: `ROC(C,5)` without diff method. Correct: `ROC(C,5,%)` or `ROC(C,5,$)`.
- Bad: using `%` when the user asked for point change.
- Bad: interpreting a negative ROC as bullish unless the user explicitly asks for downside movement.

## Assumptions

- Use `%` for percent change wording.
- Use `$` for point change or simple rising/falling checks.
- Negative ROC means the series fell over the lookback.

## Related Patterns

- function.ref
- pattern.rsi_recovery
- pattern.macd_divergence

## Related functions and concepts

- Explorer columns and filters
- Price fields such as `C`, `H`, `L`, `O`, and `V`
- `Cross` when the user asks for a crossing event
- `Ref` when the user asks for previous-bar or prior-event logic



## Retrieval keywords

ROC, rate of change, percentage change, point change, momentum, price dropped.

## Test Queries

- Find stocks up more than 10 percent over 5 days
- Find stocks that dropped 5 percent over 3 days
