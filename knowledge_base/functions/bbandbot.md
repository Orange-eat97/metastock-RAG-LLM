---
canonical_id: function.bbandbot
title: BBandBot
type: function
card_bucket: functions
category: bollinger_bands
source: generated_curated_from_primer
status: active
priority: 10
supports_explorer: true
function: BBandBot
aliases:
- text: BBandBot
  type: exact
  weight: 1.0
- text: Bollinger Band Bottom
  type: exact
  weight: 1.0
- text: lower Bollinger Band
  type: synonym
  weight: 0.95
- text: bottom Bollinger Band
  type: synonym
  weight: 0.9
- text: close below lower Bollinger Band
  type: phrase
  weight: 0.95
suggests:
- canonical_id: function.bbandtop
  rationale: Band width and squeeze formulas require the upper band as comparison context.
  priority: 30
  properties:
    formula_role: paired_band
- canonical_id: function.cross
  rationale: Lower-band recoveries may be crossing events.
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
  canonical_id: function.bbandbot
  supports_explorer: true
  priority: 10
  properties:
    formula_role: bollinger_bands
    source_path: functions/bbandbot.md
    curation_level: upgraded_to_curated_quality
---

# BBandBot

## Purpose

`BBandBot` calculates the lower Bollinger Band of a data array. In Explorer generation it is used for lower-band oversold conditions, lower-band recovery crosses, mean-reversion setups, and band-width calculations when paired with `BBandTop`.

## Syntax

```metastock
BBandBot(DATA ARRAY, PERIODS, METHOD, DEVIATIONS)
```

## Parameters

| Parameter | Meaning | Common values |
|---|---|---|
| DATA ARRAY | Series used for the band. | `C` |
| PERIODS | Band lookback period. | `20` |
| METHOD | Moving average method. | `S`, `E`, `W`, `T`, `TRI`, `VAR` |
| DEVIATIONS | Number of standard deviations. | `2` |

## Default interpretation

If the user says Bollinger Bands without settings, use close, 20 periods, simple method, and 2 deviations: `BBandBot(C,20,S,2)`.

## Common formulas

```metastock
BBandBot(C,20,S,2)
C < BBandBot(C,20,S,2)
Cross(C,BBandBot(C,20,S,2))
BBandTop(C,20,S,2) - BBandBot(C,20,S,2)
```

## Natural language mappings

Use this function when the user says:

- lower Bollinger Band
- Bollinger Band bottom
- bottom band
- close below lower band
- lower band rebound
- Bollinger mean reversion

## Explorer column usage

Define current close and lower band as separate columns. Use `ColA < ColB` for below-band condition. Use `Cross(ColA,ColB)` for price crossing back above the lower band.

## Explorer examples

### Example 1: Close below lower band

User request:

```text
Find stocks where close is below the lower Bollinger Band
```

Explorer output:

```text
Column A: C
Column B: BBandBot(C,20,S,2)
Filter: ColA < ColB
```
### Example 2: Cross back above lower band

User request:

```text
Find stocks where close crosses back above the lower Bollinger Band
```

Explorer output:

```text
Column A: C
Column B: BBandBot(C,20,S,2)
Filter: Cross(ColA, ColB)
```

## Filter-only usage

If the user only needs a pass/fail condition and does not need to inspect intermediate values, the function may be used directly in the Filter. For this project, prefer columns when the value helps the result table or when a pattern has multiple logical components.

## Valid Examples

```metastock
BBandBot(C,20,S,2)
C < BBandBot(C,20,S,2)
Cross(C,BBandBot(C,20,S,2))
```

## Common Mistakes

- Bad: `BollingerBottom(C,20,2)`. Correct: `BBandBot(C,20,S,2)`.
- Bad: omitting the method or deviations argument.
- Bad: using the bottom band for upper-band breakout logic.

## Assumptions

- Default band is `C,20,S,2`.
- Lower band rebound means price crosses back above the lower band.

## Related Patterns

- pattern.bollinger_band_mean_reversion
- pattern.bollinger_band_squeeze

## Related functions and concepts

- Explorer columns and filters
- Price fields such as `C`, `H`, `L`, `O`, and `V`
- `Cross` when the user asks for a crossing event
- `Ref` when the user asks for previous-bar or prior-event logic



## Retrieval keywords

BBandBot, lower Bollinger Band, bottom band, Bollinger mean reversion.

## Test Queries

- Find stocks where close crosses back above the lower Bollinger Band
