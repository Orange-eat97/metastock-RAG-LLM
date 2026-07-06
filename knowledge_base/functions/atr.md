---
canonical_id: function.atr
title: ATR
type: function
card_bucket: functions
category: volatility
source: generated_curated_from_primer
status: active
priority: 10
supports_explorer: true
function: ATR
aliases:
- text: ATR
  type: abbreviation
  weight: 1.0
- text: average true range
  type: exact
  weight: 1.0
- text: volatility using ATR
  type: phrase
  weight: 0.9
- text: ATR trailing stop
  type: phrase
  weight: 0.9
- text: 2 ATR stop
  type: phrase
  weight: 0.9
suggests:
- canonical_id: function.ref
  rationale: ATR true range logic may involve previous close when customising ATR calculations.
  priority: 30
  properties:
    formula_role: previous_close_component
- canonical_id: function.mov
  rationale: ATR is often compared with its own moving average for volatility expansion.
  priority: 30
  properties:
    formula_role: volatility_average
semantic:
  concept_role: function
  mechanism: volatility
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
  canonical_id: function.atr
  supports_explorer: true
  priority: 10
  properties:
    formula_role: volatility
    source_path: functions/atr.md
    curation_level: upgraded_to_curated_quality
---

# ATR

## Purpose

`ATR` calculates Average True Range over a specified number of periods. In this project it is mainly used as a volatility gauge, as a distance unit for stops, and as a volatility confirmation condition. `ATR(14)` is the common default.

## Syntax

```metastock
ATR(PERIODS)
```

## Parameters

| Parameter | Meaning | Common values |
|---|---|---|
| PERIODS | Number of periods used for Average True Range. | `10`, `14`, `20` |

## Default interpretation

If the user says ATR without a period, use `ATR(14)`. If the user says “2 ATR stop”, interpret it as a stop distance of `2 * ATR(14)` unless another period or multiplier is provided.

## Common formulas

```metastock
ATR(14)
ATR(14) > Mov(ATR(14),20,S)
C > Mov(C,50,S) AND ATR(14) > Mov(ATR(14),20,S)
HHV(H,20) - 2 * ATR(14)
C > HHV(H,20) - 2 * ATR(14)
```

## Natural language mappings

Use this function when the user says:

- ATR
- average true range
- volatility
- volatility expansion
- volatility contraction
- ATR above average
- ATR trailing stop
- 2 ATR stop
- close above ATR stop
- price within one ATR

## Explorer column usage

Use ATR as a column when the user wants to inspect volatility or stop distance. For an ATR stop scan, define the close and stop level as columns, then compare them in the filter.

## Explorer examples

### Example 1: ATR above its average

User request:

```text
Find stocks where ATR is above its 20 day average
```

Explorer output:

```text
Column A: ATR(14)
Column B: Mov(ATR(14),20,S)
Filter: ColA > ColB
```
### Example 2: Close above a 2 ATR trailing stop proxy

User request:

```text
Find stocks where close is above a 2 ATR trailing stop
```

Explorer output:

```text
Column A: C
Column B: HHV(H,20) - 2 * ATR(14)
Filter: ColA > ColB
```
Notes:

```text
This is a simple Explorer-friendly stop proxy, not a position-aware System Tester trailing stop.
```

## Filter-only usage

If the user only needs a pass/fail condition and does not need to inspect intermediate values, the function may be used directly in the Filter. For this project, prefer columns when the value helps the result table or when a pattern has multiple logical components.

## Valid Examples

```metastock
ATR(14)
ATR(20) > Mov(ATR(20),50,S)
C > HHV(H,20) - 2 * ATR(14)
```

## Common Mistakes

- Bad: `AverageTrueRange(14)`. Correct: `ATR(14)`.
- Bad: `ATR` without parentheses. Correct: `ATR(14)`.
- Bad: treating ATR trailing stops as fully position-aware inside Explorer. Explorer formulas do not know trade entry state unless explicitly encoded.

## Assumptions

- ATR period defaults to 14.
- ATR stop multiplier defaults to 2 when the user says “2 ATR”.
- For Explorer scans, ATR trailing stop formulas are approximations unless the user supplies exact stop logic.

## Related Patterns

- pattern.atr_trailing_stop
- pattern.volatility_expansion
- pattern.volatility_contraction

## Related functions and concepts

- Explorer columns and filters
- Price fields such as `C`, `H`, `L`, `O`, and `V`
- `Cross` when the user asks for a crossing event
- `Ref` when the user asks for previous-bar or prior-event logic



## Retrieval keywords

ATR, Average True Range, volatility, ATR stop, 2 ATR, trailing stop.

## Test Queries

- Find stocks where ATR is above its 20 day average
- Find stocks where close is above a 2 ATR trailing stop
