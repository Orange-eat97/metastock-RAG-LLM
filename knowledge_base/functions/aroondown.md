---
canonical_id: function.aroondown
title: AroonDown
type: function
card_bucket: functions
category: trend_timing
source: generated_curated_from_primer
status: active
priority: 10
supports_explorer: true
function: AroonDown
aliases:
- text: AroonDown
  type: exact
  weight: 1.0
- text: Aroon Down
  type: synonym
  weight: 1.0
- text: aroon bearish
  type: phrase
  weight: 0.9
- text: Aroon Down above Aroon Up
  type: phrase
  weight: 0.95
suggests:
- canonical_id: function.aroonup
  rationale: AroonDown is commonly compared with AroonUp.
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
  canonical_id: function.aroondown
  supports_explorer: true
  priority: 10
  properties:
    formula_role: trend_timing
    source_path: functions/aroondown.md
    curation_level: upgraded_to_curated_quality
---

# AroonDown

## Purpose

Aroon Down component of the predefined Aroon indicator. It reflects how recently a low occurred within the lookback period. It is usually compared with AroonUp for trend direction.

## Syntax

```metastock
AroonDown(PERIODS)
```

## Parameters

| `PERIODS` | Lookback period. | `14`, `25` |

## Default interpretation

Use `AroonDown(14)` by default unless the user gives a period. Bearish Aroon trend usually means `AroonDown(14) > AroonUp(14)`.

## Common formulas

```metastock
AroonDown(14)
AroonDown(14) > AroonUp(14)
Cross(AroonDown(14),AroonUp(14))
AroonDown(14) > 70
```

## Natural language mappings

Use this function when the user says:

- Aroon Down
- AroonDown
- Aroon bearish
- Aroon downtrend
- Aroon Down above Up

## Explorer column usage

Show AroonDown and AroonUp together for trend direction.

## Explorer examples

### Example 1: Aroon bearish trend

User request:

```text
Find stocks where Aroon Down is above Aroon Up
```

Explorer output:

```text
Column A: AroonDown(14)
Column B: AroonUp(14)
Filter: ColA > ColB
```

## Filter-only usage

If the user only needs a pass/fail condition and does not need to inspect intermediate values, the function may be used directly in the Filter. For this project, prefer columns when the value helps the result table or when a pattern has multiple logical components.

## Valid Examples

```metastock
AroonDown(14)>AroonUp(14)
Cross(AroonDown(14),AroonUp(14))
```

## Common Mistakes

- Bad: `Aroon(14)` if the available cards/functions are AroonUp and AroonDown.
- Bad: using AroonDown alone when the user asks for complete Aroon trend direction.

## Assumptions

- Default period is 14.
- AroonDown > AroonUp is bearish by default.

## Related Patterns

- pattern.aroon_trend

## Related functions and concepts

- Explorer columns and filters
- Price fields such as `C`, `H`, `L`, `O`, and `V`
- `Cross` when the user asks for a crossing event
- `Ref` when the user asks for previous-bar or prior-event logic



## Retrieval keywords

AroonDown, Aroon Down, Aroon trend, Aroon bearish.

## Test Queries

- Find stocks where Aroon Down crosses above Aroon Up
