---
canonical_id: function.adx
title: ADX
type: function
card_bucket: functions
category: trend_strength
source: generated_curated_from_primer
status: active
priority: 10
supports_explorer: true
function: ADX
aliases:
- text: ADX
  type: abbreviation
  weight: 1.0
- text: average directional movement
  type: exact
  weight: 1.0
- text: trend strength
  type: phrase
  weight: 0.85
- text: ADX above 25
  type: phrase
  weight: 0.95
suggests:
- canonical_id: function.pdi
  rationale: ADX trend direction often needs PDI for bullish direction.
  priority: 30
  properties:
    formula_role: directional_component
- canonical_id: function.mdi
  rationale: ADX trend direction often needs MDI for bearish direction.
  priority: 30
  properties:
    formula_role: directional_component
semantic:
  concept_role: function
  mechanism: trend_strength
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
  canonical_id: function.adx
  supports_explorer: true
  priority: 10
  properties:
    formula_role: trend_strength
    source_path: functions/adx.md
    curation_level: upgraded_to_curated_quality
---

# ADX

## Purpose

Average Directional Movement indicator. ADX measures trend strength, not bullish or bearish direction by itself. Direction usually requires comparing `PDI()` and `MDI()`.

## Syntax

```metastock
ADX(PERIODS)
```

## Parameters

| `PERIODS` | Number of periods for ADX calculation. | `14` |

## Default interpretation

If the user says strong trend without a threshold, use `ADX(14) > 25` as a conventional assumption and state it. Use PDI/MDI for direction.

## Common formulas

```metastock
ADX(14)
ADX(14) > 25
ADX(14) > Ref(ADX(14),-1)
ADX(14) > 25 AND PDI(14) > MDI(14)
```

## Natural language mappings

Use this function when the user says:

- ADX
- average directional movement
- trend strength
- strong trend
- ADX above 25
- ADX rising
- directional movement

## Explorer column usage

Show ADX as a column when the user wants to inspect trend strength. For bullish trend scans, combine ADX with `PDI(14) > MDI(14)`.

## Explorer examples

### Example 1: Strong trend

User request:

```text
Find stocks with ADX above 25
```

Explorer output:

```text
Column A: ADX(14)
Filter: ColA > 25
```
### Example 2: Strong bullish trend

User request:

```text
Find stocks in a strong bullish ADX trend
```

Explorer output:

```text
Column A: ADX(14)
Column B: PDI(14)
Column C: MDI(14)
Filter: ColA > 25 AND ColB > ColC
```

## Filter-only usage

If the user only needs a pass/fail condition and does not need to inspect intermediate values, the function may be used directly in the Filter. For this project, prefer columns when the value helps the result table or when a pattern has multiple logical components.

## Valid Examples

```metastock
ADX(14)>25
ADX(14)>Ref(ADX(14),-1)
ADX(14)>25 AND PDI(14)>MDI(14)
```

## Common Mistakes

- Bad: assuming `ADX(14)>25` means bullish. ADX measures strength, not direction.
- Bad: `ADX` without parentheses.
- Bad: inventing `ADXRising(14)`; use `ADX(14)>Ref(ADX(14),-1)`.

## Assumptions

- Default period is 14.
- Strong trend default threshold is 25 if unspecified.
- Direction requires PDI/MDI or another directional condition.

## Related Patterns

- pattern.adx_trend_strength

## Related functions and concepts

- Explorer columns and filters
- Price fields such as `C`, `H`, `L`, `O`, and `V`
- `Cross` when the user asks for a crossing event
- `Ref` when the user asks for previous-bar or prior-event logic



## Retrieval keywords

ADX, trend strength, PDI, MDI, directional movement.

## Test Queries

- Find stocks where ADX is above 25 and PDI is above MDI
