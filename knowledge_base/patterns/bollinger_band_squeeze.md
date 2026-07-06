---
type: pattern
card_bucket: patterns
category: bollinger_band_squeeze
source: MetaStock Formula Primer / internal project pattern
status: active
priority: 10
aliases:
  - Bollinger Band squeeze
  - Bollinger squeeze
  - narrow Bollinger Bands
  - Bollinger Band width contraction
  - tight Bollinger Bands
  - low Bollinger Band width
requires:
  - function.bbandtop
  - function.bbandbot
  - function.mov
suggests:
  - function.llv
  - function.cross
  - pattern.bollinger_band_breakout
registry:
  enabled: true
  supports_explorer: true
  properties:
    formula_role: volatility_contraction
    default_band_period: 20
    default_width_average_period: 50
    default_method: S
    default_deviations: 2
---

# Pattern: Bollinger Band Squeeze

## Intent

Detect stocks where Bollinger Bands have contracted, meaning the distance between the upper and lower bands is unusually narrow.

This pattern is used for volatility-contraction setups that may precede a later breakout.

## Natural Language Triggers

- Bollinger Band squeeze
- Bollinger squeeze
- narrow Bollinger Bands
- tight Bollinger Bands
- Bollinger Band width contraction
- Bollinger Bands are narrowing
- low Bollinger Band width
- volatility squeeze using Bollinger Bands

## Required Logical Components

1. Calculate the upper Bollinger Band with `BBandTop`.
2. Calculate the lower Bollinger Band with `BBandBot`.
3. Define band width as upper band minus lower band.
4. Compare current band width with a reference value:
   - average band width using `Mov(width,N,S)`, or
   - lowest band width using `LLV(width,N)` if the user asks for narrowest in a lookback.
5. Optionally combine the squeeze with a breakout condition when the user asks for squeeze breakout.

## Formula Building Blocks

Band width:

```metastock
BBandTop(C,20,S,2) - BBandBot(C,20,S,2)
```

Band width below its 50-period average:

```metastock
(BBandTop(C,20,S,2) - BBandBot(C,20,S,2)) < Mov(BBandTop(C,20,S,2) - BBandBot(C,20,S,2),50,S)
```

Narrowest band width in 50 periods:

```metastock
(BBandTop(C,20,S,2) - BBandBot(C,20,S,2)) = LLV(BBandTop(C,20,S,2) - BBandBot(C,20,S,2),50)
```

## Example Compositions

Simple squeeze filter using width below average width:

```metastock
(BBandTop(C,20,S,2) - BBandBot(C,20,S,2)) < Mov(BBandTop(C,20,S,2) - BBandBot(C,20,S,2),50,S)
```

Squeeze plus bullish upper-band breakout:

```metastock
(BBandTop(C,20,S,2) - BBandBot(C,20,S,2)) < Mov(BBandTop(C,20,S,2) - BBandBot(C,20,S,2),50,S) AND C > BBandTop(C,20,S,2)
```

Explorer columns for squeeze:

```text
Column A: BBandTop(C,20,S,2)
Column B: BBandBot(C,20,S,2)
Column C: BBandTop(C,20,S,2) - BBandBot(C,20,S,2)
Column D: Mov(BBandTop(C,20,S,2) - BBandBot(C,20,S,2),50,S)
Filter: ColC < ColD
```

## Default Assumptions

- Use close `C` as the Bollinger Band data array.
- Use 20-period simple Bollinger Bands with 2 standard deviations.
- Use 50 periods as the default comparison window for average band width.
- A basic squeeze means current band width is below its average width.
- A stricter “narrowest squeeze” can use `LLV(width,N)`.

## Pitfalls

- Do not confuse Bollinger Band squeeze with a price breakout; squeeze is about band width contraction.
- Do not use only `BBandTop` or only `BBandBot`; width requires both bands.
- Do not invent a function such as `BollingerWidth()` unless such a function exists in the local card registry.
- Be careful with Explorer column references: do not use `Ref(ColC,-1)`. Put historical logic inside the column formula if needed.
- Do not use broad aliases like `squeeze` alone because that can mean other indicators.

## Test Queries

- Find stocks with a Bollinger Band squeeze
- Find stocks where Bollinger Bands are unusually narrow
- Find stocks with Bollinger Band width below its 50 day average
