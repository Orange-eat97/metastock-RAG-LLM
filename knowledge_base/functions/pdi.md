---
canonical_id: function.pdi
title: PDI
type: function
card_bucket: functions
category: trend_direction
source: generated_curated_from_primer
status: active
priority: 10
supports_explorer: true
function: PDI
aliases:
- text: PDI
  type: abbreviation
  weight: 1.0
- text: plus directional movement
  type: exact
  weight: 1.0
- text: positive directional indicator
  type: synonym
  weight: 0.9
- text: +DI
  type: abbreviation
  weight: 0.9
suggests:
- canonical_id: function.mdi
  rationale: PDI is commonly compared with MDI for directional trend.
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
  canonical_id: function.pdi
  supports_explorer: true
  priority: 10
  properties:
    formula_role: trend_direction
    source_path: functions/pdi.md
    curation_level: upgraded_to_curated_quality
---

# PDI

## Purpose

Plus Directional Movement indicator. In Explorer scans it is commonly compared against `MDI()` to represent bullish directional pressure.

## Syntax

```metastock
PDI(PERIODS)
```

## Parameters

| `PERIODS` | Number of periods for PDI calculation. | `14` |

## Default interpretation

Use `PDI(14)` by default. For bullish directional condition, use `PDI(14) > MDI(14)`. For a cross, use `Cross(PDI(14),MDI(14))`.

## Common formulas

```metastock
PDI(14)
PDI(14) > MDI(14)
Cross(PDI(14),MDI(14))
ADX(14) > 25 AND PDI(14) > MDI(14)
```

## Natural language mappings

Use this function when the user says:

- PDI
- +DI
- plus directional movement
- positive directional indicator
- PDI above MDI
- bullish directional movement

## Explorer column usage

Define PDI and MDI as separate columns when comparing direction.

## Explorer examples

### Example 1: PDI above MDI

User request:

```text
Find stocks where PDI is above MDI
```

Explorer output:

```text
Column A: PDI(14)
Column B: MDI(14)
Filter: ColA > ColB
```

## Filter-only usage

If the user only needs a pass/fail condition and does not need to inspect intermediate values, the function may be used directly in the Filter. For this project, prefer columns when the value helps the result table or when a pattern has multiple logical components.

## Valid Examples

```metastock
PDI(14)>MDI(14)
Cross(PDI(14),MDI(14))
```

## Common Mistakes

- Bad: using PDI alone as trend strength. Use ADX for strength.
- Bad: reversing PDI/MDI for bullish direction.

## Assumptions

- Default period is 14.
- PDI > MDI is bullish directional pressure.

## Related Patterns

- pattern.adx_trend_strength

## Related functions and concepts

- Explorer columns and filters
- Price fields such as `C`, `H`, `L`, `O`, and `V`
- `Cross` when the user asks for a crossing event
- `Ref` when the user asks for previous-bar or prior-event logic



## Retrieval keywords

PDI, plus directional movement, +DI, PDI above MDI.

## Test Queries

- Find stocks where PDI crosses above MDI
