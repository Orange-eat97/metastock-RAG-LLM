---
canonical_id: function.macd
title: MACD
type: function
card_bucket: functions
category: momentum
source: generated_curated_from_primer
status: active
priority: 10
supports_explorer: true
function: MACD
aliases:
- text: MACD
  type: abbreviation
  weight: 1.0
- text: moving average convergence divergence
  type: exact
  weight: 1.0
- text: MACD line
  type: phrase
  weight: 0.9
- text: MACD histogram
  type: phrase
  weight: 0.85
- text: MACD signal line
  type: phrase
  weight: 0.85
suggests:
- canonical_id: function.mov
  rationale: The MACD signal line is commonly represented as a 9-period exponential moving average of MACD().
  priority: 30
  properties:
    formula_role: signal_smoothing
- canonical_id: function.cross
  rationale: MACD is often used in crossover conditions.
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
  canonical_id: function.macd
  supports_explorer: true
  priority: 10
  properties:
    formula_role: momentum
    source_path: functions/macd.md
    curation_level: upgraded_to_curated_quality
---

# MACD

## Purpose

`MACD` returns the predefined MACD indicator series. In Explorer generation it is usually used for momentum filters, MACD above or below zero, MACD crossing its signal line, and MACD histogram-style differences. The built-in `MACD()` function returns the MACD line itself; the signal line must be written separately, commonly as `Mov(MACD(),9,E)`.

## Syntax

```metastock
MACD()
```

## Parameters

| Parameter | Meaning | Common values |
|---|---|---|
| none | `MACD()` uses MetaStock default MACD settings. | no arguments |

## Default interpretation

If the user says “MACD” alone, use `MACD()` with parentheses. If the user says “MACD signal line”, use `Mov(MACD(),9,E)` unless a different signal period or smoothing method is specified. If the user says “MACD histogram”, use `MACD() - Mov(MACD(),9,E)`.

## Common formulas

```metastock
MACD()
MACD() > 0
MACD() < 0
Mov(MACD(),9,E)
Cross(MACD(), Mov(MACD(),9,E))
MACD() - Mov(MACD(),9,E)
```

## Natural language mappings

Use this function when the user says:

- MACD
- moving average convergence divergence
- MACD above zero
- MACD below zero
- MACD crosses above signal line
- bullish MACD cross
- bearish MACD cross
- MACD histogram positive
- MACD momentum improving

## Explorer column usage

For MACD inspection, define both the MACD line and the signal line as columns. Use `Cross(ColA,ColB)` only for a crossing event. Use `ColA > ColB` for a continuing MACD-above-signal condition. Do not write `MACD` without parentheses.

## Explorer examples

### Example 1: MACD crosses above signal line

User request:

```text
Find stocks where MACD crosses above its signal line
```

Explorer output:

```text
Column A: MACD()
Column B: Mov(MACD(),9,E)
Filter: Cross(ColA, ColB)
```
Notes:

```text
Column A is the MACD line. Column B is the signal line approximation.
```
### Example 2: MACD above zero

User request:

```text
Find stocks where MACD is above zero
```

Explorer output:

```text
Column A: MACD()
Filter: ColA > 0
```
### Example 3: Positive MACD histogram

User request:

```text
Find stocks where MACD histogram is positive
```

Explorer output:

```text
Column A: MACD()
Column B: Mov(MACD(),9,E)
Column C: ColA - ColB
Filter: ColA > ColB
```
Notes:

```text
Avoid using Column C as an input to another historical function; use it only as displayed output or final last-value comparison.
```

## Filter-only usage

If the user only needs a pass/fail condition and does not need to inspect intermediate values, the function may be used directly in the Filter. For this project, prefer columns when the value helps the result table or when a pattern has multiple logical components.

## Valid Examples

```metastock
MACD()
MACD() > 0
Cross(MACD(), Mov(MACD(),9,E))
MACD() > Mov(MACD(),9,E)
```

## Common Mistakes

- Bad: `MACD > 0`. Correct: `MACD() > 0`.
- Bad: `Cross(MACD(), signal line)`. Correct: `Cross(MACD(), Mov(MACD(),9,E))`.
- Bad: using `MACD() > Mov(MACD(),9,E)` when the user asked for “crosses above”. Correct: use `Cross(MACD(), Mov(MACD(),9,E))`.
- Bad: assuming `MACD()` returns both the MACD line and signal line. It returns the MACD line only.

## Assumptions

- MACD without parameters means MetaStock default `MACD()`.
- Signal line defaults to `Mov(MACD(),9,E)`.
- Bullish MACD cross means `Cross(MACD(), Mov(MACD(),9,E))`.
- Bearish MACD cross can be represented as `Cross(Mov(MACD(),9,E), MACD())`.

## Related Patterns

- pattern.macd_crossover
- pattern.macd_divergence
- function.mov
- function.cross

## Related functions and concepts

- Explorer columns and filters
- Price fields such as `C`, `H`, `L`, `O`, and `V`
- `Cross` when the user asks for a crossing event
- `Ref` when the user asks for previous-bar or prior-event logic



## Retrieval keywords

MACD, MACD line, signal line, MACD crossover, MACD histogram, moving average convergence divergence.

## Test Queries

- Find stocks where MACD crosses above its signal line
- Find stocks where MACD histogram is positive
- Find stocks where MACD is above zero
