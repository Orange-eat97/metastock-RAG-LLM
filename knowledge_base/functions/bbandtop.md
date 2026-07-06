---
type: function
function: BBandTop
category: bollinger_bands
source: MetaStock Formula Primer
status: active
priority: 10
aliases:
  - BBandTop
  - Bollinger Band Top
  - upper Bollinger Band
  - top Bollinger Band
  - close above upper Bollinger Band
  - price above upper band
suggests:
  - function.bbandbot
  - function.mov
  - function.cross
registry:
  enabled: true
  supports_explorer: true
  properties:
    formula_role: upper_volatility_band
    default_data_array: C
    default_period: 20
    default_method: S
    default_deviations: 2
---

# BBandTop

## Purpose

`BBandTop` calculates the upper Bollinger Band of a data array.

In this project, it is mainly used for Explorer filters such as:

- close above the upper Bollinger Band
- price crossing above the upper band
- Bollinger Band breakout
- Bollinger Band width and squeeze calculations

## Syntax

```metastock
BBandTop(DATA ARRAY, PERIODS, METHOD, DEVIATIONS)
```

## Parameters

- `DATA ARRAY`: the price, volume, indicator, or formula series to calculate the band from. Commonly `C` for close.
- `PERIODS`: number of periods used for the band calculation. Commonly `20`.
- `METHOD`: moving average method used by the band. Common abbreviations include `S`, `E`, `W`, `T`, `TRI`, and `VAR`.
- `DEVIATIONS`: number of standard deviations the top band is shifted upward. Commonly `2`.

## Valid Examples

```metastock
BBandTop(C,20,S,2)
C > BBandTop(C,20,S,2)
Cross(C, BBandTop(C,20,S,2))
BBandTop(C,20,S,2) - BBandBot(C,20,S,2)
```

## Natural Language Triggers

- upper Bollinger Band
- Bollinger Band top
- top band
- price above upper band
- close above upper Bollinger Band
- upper band breakout

## Explorer Column Usage

Upper-band breakout:

```text
Column A: C
Column B: BBandTop(C,20,S,2)
Filter: ColA > ColB
```

Upper-band crossing event:

```text
Column A: C
Column B: BBandTop(C,20,S,2)
Filter: Cross(ColA, ColB)
```

## Common Mistakes

- Do not write `BollingerTop(C,20,2)`; use `BBandTop(C,20,S,2)`.
- Do not omit the moving-average method argument.
- Do not omit the deviations argument.
- Do not use the top band when the user asks for the lower Bollinger Band or oversold lower-band condition.
- Do not use a broad alias such as `top` or `band`; those are too ambiguous for registry matching.

## Related Patterns

- pattern.bollinger_band_breakout
- pattern.bollinger_band_squeeze
- pattern.bollinger_band_mean_reversion

## Test Queries

- Find stocks where close is above the upper Bollinger Band
- Find stocks where price crosses above the top Bollinger Band
- Find Bollinger Band breakouts

## Retrieval Keywords

BBandTop, Bollinger Band Top, upper Bollinger Band, upper band breakout, close above upper band, Bollinger breakout.
