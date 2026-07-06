---
type: function
function: BBandBot
category: bollinger_bands
source: MetaStock Formula Primer
status: active
priority: 10
aliases:
  - BBandBot
  - Bollinger Band Bottom
  - lower Bollinger Band
  - bottom Bollinger Band
  - close below lower Bollinger Band
  - price below lower band
suggests:
  - function.bbandtop
  - function.mov
  - function.cross
registry:
  enabled: true
  supports_explorer: true
  properties:
    formula_role: lower_volatility_band
    default_data_array: C
    default_period: 20
    default_method: S
    default_deviations: 2
---

# BBandBot

## Purpose

`BBandBot` calculates the lower Bollinger Band of a data array.

In this project, it is mainly used for Explorer filters such as:

- close below the lower Bollinger Band
- price crossing back above the lower band
- Bollinger Band mean-reversion setups
- Bollinger Band width and squeeze calculations

## Syntax

```metastock
BBandBot(DATA ARRAY, PERIODS, METHOD, DEVIATIONS)
```

## Parameters

- `DATA ARRAY`: the price, volume, indicator, or formula series to calculate the band from. Commonly `C` for close.
- `PERIODS`: number of periods used for the band calculation. Commonly `20`.
- `METHOD`: moving average method used by the band. Common abbreviations include `S`, `E`, `W`, `T`, `TRI`, and `VAR`.
- `DEVIATIONS`: number of standard deviations the bottom band is shifted downward. Commonly `2`.

## Valid Examples

```metastock
BBandBot(C,20,S,2)
C < BBandBot(C,20,S,2)
Cross(C, BBandBot(C,20,S,2))
BBandTop(C,20,S,2) - BBandBot(C,20,S,2)
```

## Natural Language Triggers

- lower Bollinger Band
- Bollinger Band bottom
- bottom band
- price below lower band
- close below lower Bollinger Band
- lower band rebound
- lower band mean reversion

## Explorer Column Usage

Lower-band oversold condition:

```text
Column A: C
Column B: BBandBot(C,20,S,2)
Filter: ColA < ColB
```

Lower-band recovery event:

```text
Column A: C
Column B: BBandBot(C,20,S,2)
Filter: Cross(ColA, ColB)
```

## Common Mistakes

- Do not write `BollingerBottom(C,20,2)`; use `BBandBot(C,20,S,2)`.
- Do not omit the moving-average method argument.
- Do not omit the deviations argument.
- Do not use the bottom band when the user asks for an upper-band breakout.
- Do not use a broad alias such as `bottom` or `band`; those are too ambiguous for registry matching.

## Related Patterns

- pattern.bollinger_band_breakout
- pattern.bollinger_band_squeeze
- pattern.bollinger_band_mean_reversion

## Test Queries

- Find stocks where close is below the lower Bollinger Band
- Find stocks where price crosses back above the lower Bollinger Band
- Find lower Bollinger Band mean reversion setups

## Retrieval Keywords

BBandBot, Bollinger Band Bottom, lower Bollinger Band, lower band rebound, close below lower band, Bollinger mean reversion.
