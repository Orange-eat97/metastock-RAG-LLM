---
canonical_id: function.stoch
title: Stoch
type: function
card_bucket: functions
category: momentum
source: generated_curated_from_primer
status: active
priority: 10
supports_explorer: true
function: Stoch
aliases:
- text: Stoch
  type: abbreviation
  weight: 1.0
- text: stochastic oscillator
  type: exact
  weight: 1.0
- text: stochastic oversold
  type: phrase
  weight: 0.9
- text: stochastic above 80
  type: phrase
  weight: 0.9
suggests:
- canonical_id: function.mov
  rationale: The stochastic signal line is commonly represented with a moving average of Stoch().
  priority: 30
  properties:
    formula_role: signal_line
- canonical_id: function.cross
  rationale: Stoch is often used in threshold or signal-line crosses.
  priority: 30
  properties:
    formula_role: crossing_event
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
  canonical_id: function.stoch
  supports_explorer: true
  priority: 10
  properties:
    formula_role: momentum
    source_path: functions/stoch.md
    curation_level: upgraded_to_curated_quality
---

# Stoch

## Purpose

The predefined Stochastic Oscillator value. Use it for stochastic overbought/oversold filters and stochastic recovery/crossover conditions. The built-in syntax takes %K periods and %K slowing; a signal line can be built separately with `Mov(Stoch(5,3),3,S)`.

## Syntax

```metastock
Stoch(%K PERIODS, %K SLOWING)
```

## Parameters

| `%K PERIODS` | Lookback period for stochastic range. | `5`, `14` |
| `%K SLOWING` | Slowing applied to %K. | `3` |

## Default interpretation

If the user says stochastic without settings, use `Stoch(5,3)` for the common 5/3 main line. Use 80 as overbought and 20 as oversold unless the user gives thresholds.

## Common formulas

```metastock
Stoch(5,3)
Stoch(5,3) > 80
Stoch(5,3) < 20
Cross(Stoch(5,3),20)
Mov(Stoch(5,3),3,S)
```

## Natural language mappings

Use this function when the user says:

- stochastic
- stochastic oscillator
- stoch oversold
- stoch above 80
- stoch crosses above 20
- 5 3 3 stochastic

## Explorer column usage

Use Stoch as a displayed oscillator column. If the user asks for 5/3/3 stochastic, use `Stoch(5,3)` as the main line and `Mov(Stoch(5,3),3,S)` as the signal line.

## Explorer examples

### Example 1: Stochastic oversold recovery

User request:

```text
Find stocks where stochastic crosses above 20
```

Explorer output:

```text
Column A: Stoch(5,3)
Filter: Cross(ColA, 20)
```
### Example 2: Stochastic signal cross above 80

User request:

```text
Find stocks where 5 3 3 stochastic crosses below its signal line above 80
```

Explorer output:

```text
Column A: Stoch(5,3)
Column B: Mov(Stoch(5,3),3,S)
Filter: Cross(ColB, ColA) AND ColA > 80 AND ColB > 80
```

## Filter-only usage

If the user only needs a pass/fail condition and does not need to inspect intermediate values, the function may be used directly in the Filter. For this project, prefer columns when the value helps the result table or when a pattern has multiple logical components.

## Valid Examples

```metastock
Stoch(5,3)
Cross(Stoch(5,3),20)
Cross(Stoch(5,3),Mov(Stoch(5,3),3,S))
```

## Common Mistakes

- Bad: `Stoch(5,3,3)` as the built-in Stoch function. Correct: use `Stoch(5,3)` and build the signal line separately with `Mov(Stoch(5,3),3,S)`.
- Bad: using stochastic recovery when the user asked for RSI recovery.
- Bad: forgetting that overbought/oversold thresholds are assumptions if not specified.

## Assumptions

- Default main stochastic is `Stoch(5,3)`.
- Default signal line for 5/3/3 is `Mov(Stoch(5,3),3,S)`.
- Oversold defaults to below 20; overbought defaults to above 80.

## Related Patterns

- pattern.stochastic_oversold_recovery

## Related functions and concepts

- Explorer columns and filters
- Price fields such as `C`, `H`, `L`, `O`, and `V`
- `Cross` when the user asks for a crossing event
- `Ref` when the user asks for previous-bar or prior-event logic



## Retrieval keywords

Stoch, stochastic oscillator, 5 3 3 stochastic, stochastic oversold, stochastic cross.

## Test Queries

- Find stocks where stochastic crosses above 20
