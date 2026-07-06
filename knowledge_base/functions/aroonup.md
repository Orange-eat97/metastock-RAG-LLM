---
canonical_id: function.aroonup
title: AroonUp
type: function
card_bucket: functions
category: trend_timing
source: generated_curated_from_primer
status: active
priority: 10
supports_explorer: true
function: AroonUp
aliases:
- text: AroonUp
  type: exact
  weight: 1.0
- text: Aroon Up
  type: synonym
  weight: 1.0
- text: aroon bullish
  type: phrase
  weight: 0.9
- text: Aroon Up above Aroon Down
  type: phrase
  weight: 0.95
suggests:
- canonical_id: function.aroondown
  rationale: AroonUp is commonly compared with AroonDown.
  priority: 30
  properties:
    formula_role: opposite_aroon_component
- canonical_id: function.cross
  rationale: Aroon trend signals often use crossing events.
  priority: 30
  properties:
    formula_role: crossing_event
semantic:
  concept_role: function
  mechanism: trend_timing
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
  canonical_id: function.aroonup
  supports_explorer: true
  priority: 10
  properties:
    formula_role: trend_timing
    source_path: functions/aroonup.md
    curation_level: upgraded_to_curated_quality
---

# AroonUp

## Purpose

Aroon Up component of the predefined Aroon indicator. It reflects how recently a high occurred within the lookback period. It is usually compared with AroonDown for trend direction.

## Syntax

```metastock
AroonUp(PERIODS)
```

## Parameters

| `PERIODS` | Lookback period. | `14`, `25` |

## Default interpretation

Use `AroonUp(14)` by default unless the user gives a period. Bullish Aroon trend usually means `AroonUp(14) > AroonDown(14)`, optionally with AroonUp above 70.

## Common formulas

```metastock
AroonUp(14)
AroonUp(14) > AroonDown(14)
Cross(AroonUp(14),AroonDown(14))
AroonUp(14) > 70
```

## Natural language mappings

Use this function when the user says:

- Aroon Up
- AroonUp
- Aroon bullish
- Aroon uptrend
- Aroon Up above Down

## Explorer column usage

Show AroonUp and AroonDown together. Do not use AroonUp alone if the user asks for complete trend direction.

## Explorer examples

### Example 1: Aroon bullish trend

User request:

```text
Find stocks where Aroon Up is above Aroon Down
```

Explorer output:

```text
Column A: AroonUp(14)
Column B: AroonDown(14)
Filter: ColA > ColB
```

## Filter-only usage

If the user only needs a pass/fail condition and does not need to inspect intermediate values, the function may be used directly in the Filter. For this project, prefer columns when the value helps the result table or when a pattern has multiple logical components.

## Valid Examples

```metastock
AroonUp(14)>AroonDown(14)
Cross(AroonUp(14),AroonDown(14))
```

## Common Mistakes

- Bad: `Aroon(14)` if the available cards/functions are AroonUp and AroonDown.
- Bad: using AroonUp alone when the user asks for Aroon trend direction.

## Assumptions

- Default period is 14.
- AroonUp > AroonDown is bullish by default.

## Related Patterns

- pattern.aroon_trend

## Related functions and concepts

- Explorer columns and filters
- Price fields such as `C`, `H`, `L`, `O`, and `V`
- `Cross` when the user asks for a crossing event
- `Ref` when the user asks for previous-bar or prior-event logic



## Retrieval keywords

AroonUp, Aroon Up, Aroon trend, Aroon bullish.

## Test Queries

- Find stocks where Aroon Up crosses above Aroon Down
