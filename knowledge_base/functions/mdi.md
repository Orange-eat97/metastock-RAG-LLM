---
canonical_id: function.mdi
title: MDI
type: function
card_bucket: functions
category: trend_direction
source: generated_curated_from_primer
status: active
priority: 10
supports_explorer: true
function: MDI
aliases:
- text: MDI
  type: abbreviation
  weight: 1.0
- text: minus directional movement
  type: exact
  weight: 1.0
- text: negative directional indicator
  type: synonym
  weight: 0.9
- text: -DI
  type: abbreviation
  weight: 0.9
suggests:
- canonical_id: function.pdi
  rationale: MDI is commonly compared with PDI for directional trend.
  priority: 30
  properties:
    formula_role: opposite_directional_component
- canonical_id: function.adx
  rationale: ADX is often used with PDI/MDI to require trend strength.
  priority: 30
  properties:
    formula_role: trend_strength
semantic:
  concept_role: function
  mechanism: trend_direction
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
  canonical_id: function.mdi
  supports_explorer: true
  priority: 10
  properties:
    formula_role: trend_direction
    source_path: functions/mdi.md
    curation_level: upgraded_to_curated_quality
---

# MDI

## Purpose

Minus Directional Movement indicator. In Explorer scans it is commonly compared against `PDI()` to represent bearish directional pressure.

## Syntax

```metastock
MDI(PERIODS)
```

## Parameters

| `PERIODS` | Number of periods for MDI calculation. | `14` |

## Default interpretation

Use `MDI(14)` by default. For bearish directional condition, use `MDI(14) > PDI(14)`. For a bearish cross, use `Cross(MDI(14),PDI(14))`.

## Common formulas

```metastock
MDI(14)
MDI(14) > PDI(14)
Cross(MDI(14),PDI(14))
ADX(14) > 25 AND MDI(14) > PDI(14)
```

## Natural language mappings

Use this function when the user says:

- MDI
- -DI
- minus directional movement
- negative directional indicator
- MDI above PDI
- bearish directional movement

## Explorer column usage

Define MDI and PDI as separate columns when comparing direction.

## Explorer examples

### Example 1: Bearish directional movement

User request:

```text
Find stocks where MDI is above PDI
```

Explorer output:

```text
Column A: MDI(14)
Column B: PDI(14)
Filter: ColA > ColB
```

## Filter-only usage

If the user only needs a pass/fail condition and does not need to inspect intermediate values, the function may be used directly in the Filter. For this project, prefer columns when the value helps the result table or when a pattern has multiple logical components.

## Valid Examples

```metastock
MDI(14)>PDI(14)
Cross(MDI(14),PDI(14))
```

## Common Mistakes

- Bad: using MDI alone as trend strength. Use ADX for strength.
- Bad: reversing MDI/PDI for bearish direction.

## Assumptions

- Default period is 14.
- MDI > PDI is bearish directional pressure.

## Related Patterns

- pattern.adx_trend_strength

## Related functions and concepts

- Explorer columns and filters
- Price fields such as `C`, `H`, `L`, `O`, and `V`
- `Cross` when the user asks for a crossing event
- `Ref` when the user asks for previous-bar or prior-event logic



## Retrieval keywords

MDI, minus directional movement, -DI, MDI above PDI.

## Test Queries

- Find stocks where MDI is above PDI
