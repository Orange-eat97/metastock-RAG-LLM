---
canonical_id: function.willr
title: WillR
type: function
card_bucket: functions
category: momentum
source: generated_curated_from_primer
status: active
priority: 10
supports_explorer: true
function: WillR
aliases:
- text: WillR
  type: abbreviation
  weight: 1.0
- text: Williams %R
  type: exact
  weight: 1.0
- text: Williams percent R
  type: synonym
  weight: 0.95
- text: Williams R oversold
  type: phrase
  weight: 0.9
suggests:
- canonical_id: function.cross
  rationale: Williams %R recovery is often expressed as a threshold cross.
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
  canonical_id: function.willr
  supports_explorer: true
  priority: 10
  properties:
    formula_role: momentum
    source_path: functions/willr.md
    curation_level: upgraded_to_curated_quality
---

# WillR

## Purpose

Williams %R oscillator. It is usually interpreted on a -100 to 0 scale, with values below -80 often treated as oversold and values above -20 often treated as overbought.

## Syntax

```metastock
WillR(PERIODS)
```

## Parameters

| `PERIODS` | Lookback period for Williams %R. | `14` |

## Default interpretation

If the user says Williams %R without a period, use `WillR(14)`. If the user says oversold recovery, use `Cross(WillR(14),-80)` by default.

## Common formulas

```metastock
WillR(14)
WillR(14) < -80
WillR(14) > -20
Cross(WillR(14),-80)
Cross(-20,WillR(14))
```

## Natural language mappings

Use this function when the user says:

- Williams %R
- Williams R
- WillR
- oversold Williams %R
- Williams %R crosses above -80
- overbought Williams %R

## Explorer column usage

Use WillR as an oscillator column. Use `Cross(WillR(14),-80)` for recovery from oversold and `Cross(-20,WillR(14))` for crossing down from overbought.

## Explorer examples

### Example 1: Williams %R oversold

User request:

```text
Find stocks where Williams %R is below -80
```

Explorer output:

```text
Column A: WillR(14)
Filter: ColA < -80
```
### Example 2: Williams %R recovery

User request:

```text
Find stocks where Williams %R crosses above -80
```

Explorer output:

```text
Column A: WillR(14)
Filter: Cross(ColA, -80)
```

## Filter-only usage

If the user only needs a pass/fail condition and does not need to inspect intermediate values, the function may be used directly in the Filter. For this project, prefer columns when the value helps the result table or when a pattern has multiple logical components.

## Valid Examples

```metastock
WillR(14)
WillR(14)<-80
Cross(WillR(14),-80)
```

## Common Mistakes

- Bad: `WilliamsR(14)`. Correct: `WillR(14)`.
- Bad: using +80/+20 thresholds for Williams %R; the common scale is negative.
- Bad: reversing the Cross arguments for recovery above -80.

## Assumptions

- Default period is 14.
- Oversold defaults to below -80.
- Overbought defaults to above -20.

## Related Patterns

- pattern.williams_r_recovery

## Related functions and concepts

- Explorer columns and filters
- Price fields such as `C`, `H`, `L`, `O`, and `V`
- `Cross` when the user asks for a crossing event
- `Ref` when the user asks for previous-bar or prior-event logic



## Retrieval keywords

WillR, Williams %R, Williams R, oversold -80, overbought -20.

## Test Queries

- Find stocks where Williams %R crosses above -80
