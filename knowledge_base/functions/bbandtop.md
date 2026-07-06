---
canonical_id: function.bbandtop
title: BBandTop
type: function
card_bucket: functions
category: bollinger_bands
source: generated_curated_from_primer
status: active
priority: 10
supports_explorer: true
function: BBandTop
aliases:
- text: BBandTop
  type: exact
  weight: 1.0
- text: Bollinger Band Top
  type: exact
  weight: 1.0
- text: upper Bollinger Band
  type: synonym
  weight: 0.95
- text: top Bollinger Band
  type: synonym
  weight: 0.9
- text: close above upper Bollinger Band
  type: phrase
  weight: 0.95
suggests:
- canonical_id: function.bbandbot
  rationale: Band width and squeeze formulas require the lower band as comparison context.
  priority: 30
  properties:
    formula_role: paired_band
- canonical_id: function.cross
  rationale: Upper-band breakouts may be crossing events.
  priority: 30
  properties:
    formula_role: crossing_event
semantic:
  concept_role: function
  mechanism: bollinger_bands
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
  canonical_id: function.bbandtop
  supports_explorer: true
  priority: 10
  properties:
    formula_role: bollinger_bands
    source_path: functions/bbandtop.md
    curation_level: upgraded_to_curated_quality
---

# BBandTop

## Purpose

`BBandTop` calculates the upper Bollinger Band of a data array. In Explorer generation it is used for upper-band breakouts, upper-band crosses, and band-width calculations when paired with `BBandBot`.

## Syntax

```metastock
BBandTop(DATA ARRAY, PERIODS, METHOD, DEVIATIONS)
```

## Parameters

| Parameter | Meaning | Common values |
|---|---|---|
| DATA ARRAY | Series used for the band. | `C` |
| PERIODS | Band lookback period. | `20` |
| METHOD | Moving average method. | `S`, `E`, `W`, `T`, `TRI`, `VAR` |
| DEVIATIONS | Number of standard deviations. | `2` |

## Default interpretation

If the user says Bollinger Bands without settings, use close, 20 periods, simple method, and 2 deviations: `BBandTop(C,20,S,2)`.

## Common formulas

```metastock
BBandTop(C,20,S,2)
C > BBandTop(C,20,S,2)
Cross(C,BBandTop(C,20,S,2))
BBandTop(C,20,S,2) - BBandBot(C,20,S,2)
```

## Natural language mappings

Use this function when the user says:

- upper Bollinger Band
- Bollinger Band top
- top band
- close above upper band
- upper band breakout
- Bollinger breakout

## Explorer column usage

Define current close and upper band as separate columns. Use `ColA > ColB` for a continuing above-band condition and `Cross(ColA,ColB)` for the crossing event.

## Explorer examples

### Example 1: Close above upper band

User request:

```text
Find stocks where close is above the upper Bollinger Band
```

Explorer output:

```text
Column A: C
Column B: BBandTop(C,20,S,2)
Filter: ColA > ColB
```
### Example 2: Cross above upper band

User request:

```text
Find stocks where close crosses above the upper Bollinger Band
```

Explorer output:

```text
Column A: C
Column B: BBandTop(C,20,S,2)
Filter: Cross(ColA, ColB)
```

## Filter-only usage

If the user only needs a pass/fail condition and does not need to inspect intermediate values, the function may be used directly in the Filter. For this project, prefer columns when the value helps the result table or when a pattern has multiple logical components.

## Valid Examples

```metastock
BBandTop(C,20,S,2)
C > BBandTop(C,20,S,2)
Cross(C,BBandTop(C,20,S,2))
```

## Common Mistakes

- Bad: `BollingerTop(C,20,2)`. Correct: `BBandTop(C,20,S,2)`.
- Bad: omitting the method or deviations argument.
- Bad: using the top band for lower-band rebound logic.

## Assumptions

- Default band is `C,20,S,2`.
- Upper band breakout is bullish unless the user says otherwise.

## Related Patterns

- pattern.bollinger_band_breakout
- pattern.bollinger_band_squeeze

## Related functions and concepts

- Explorer columns and filters
- Price fields such as `C`, `H`, `L`, `O`, and `V`
- `Cross` when the user asks for a crossing event
- `Ref` when the user asks for previous-bar or prior-event logic



## Retrieval keywords

BBandTop, upper Bollinger Band, top band, Bollinger breakout.

## Test Queries

- Find stocks where close crosses above the upper Bollinger Band
