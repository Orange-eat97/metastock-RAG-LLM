---
canonical_id: pattern.bollinger_band_squeeze
title: 'Pattern: Bollinger Band Squeeze'
type: pattern
card_bucket: patterns
category: volatility_squeeze
source: generated_curated_from_primer
status: active
priority: 10
supports_explorer: true
aliases:
- text: Bollinger Band squeeze
  type: exact
  weight: 1.0
- text: Bollinger squeeze
  type: synonym
  weight: 0.95
- text: narrow Bollinger Bands
  type: phrase
  weight: 0.9
- text: band width contraction
  type: phrase
  weight: 0.9
- text: squeeze breakout
  type: phrase
  weight: 0.9
requires:
- canonical_id: function.bbandtop
  rationale: The squeeze requires an upper Bollinger Band to calculate band width.
  priority: 30
  properties:
    formula_role: upper_band
- canonical_id: function.bbandbot
  rationale: The squeeze requires a lower Bollinger Band to calculate band width.
  priority: 30
  properties:
    formula_role: lower_band
suggests:
- canonical_id: function.mov
  rationale: Band width is often compared with a moving average of band width.
  priority: 30
  properties:
    formula_role: width_average
- canonical_id: pattern.bollinger_band_breakout
  rationale: A squeeze is often combined with a breakout condition.
  priority: 30
  properties:
    formula_role: breakout_confirmation
semantic:
  concept_role: pattern
  mechanism: volatility_squeeze
  market_object: price
  directions_supported:
  - bullish
  - bearish
  operations_supported:
  - screening
  - confirmation
  - threshold_filter
  required_components:
  - condition_definition
  - lookback_or_threshold
  does_not_cover:
  - unrelated_pattern
registry:
  enabled: true
  canonical_id: pattern.bollinger_band_squeeze
  supports_explorer: true
  priority: 10
  properties:
    formula_role: volatility_squeeze
    source_path: patterns/bollinger_band_squeeze.md
    curation_level: upgraded_to_curated_quality
---

# Pattern: Bollinger Band Squeeze

## Intent

Detect securities where Bollinger Bands have contracted into a narrow range. This pattern represents volatility compression. It can be used alone as a squeeze scan, or combined with price breaking above the upper band or below the lower band.

## Natural Language Triggers

- Bollinger Band squeeze
- Bollinger squeeze
- bands are narrow
- volatility squeeze
- band width contraction
- squeeze breakout
- Bollinger compression

## Keywords

- Bollinger Band squeeze
- Bollinger squeeze
- narrow bands
- band width
- volatility contraction
- BBandTop
- BBandBot

## Required Logical Components

- Calculate upper band with `BBandTop(C,20,S,2)`.
- Calculate lower band with `BBandBot(C,20,S,2)`.
- Calculate band width as upper minus lower, often normalized by middle price or moving average.
- Define “squeeze” with a threshold or by comparing current width with its own moving average.
- Optionally add breakout confirmation after squeeze.

## Optional Confirmation Components

- Trend confirmation, such as close above a moving average.
- Volume confirmation, such as `V > Mov(V,20,S)`.
- Momentum confirmation, such as RSI, MACD, or ROC improving.
- Recency confirmation using `BarsSince()` when the user asks for recent signals.

## Formula Building Blocks

```metastock
top:=BBandTop(C,20,S,2);
bot:=BBandBot(C,20,S,2);
width:=BBandTop(C,20,S,2)-BBandBot(C,20,S,2);
width / Mov(C,20,S)
(BBandTop(C,20,S,2)-BBandBot(C,20,S,2)) < Mov(BBandTop(C,20,S,2)-BBandBot(C,20,S,2),50,S)
```

## Composition Guidance

- If the user gives no Bollinger settings, use `C,20,S,2`.
- If the user says squeeze only, return a width-compression filter.
- If the user says squeeze breakout, combine width compression with `C > BBandTop(C,20,S,2)` or `Cross(C,BBandTop(C,20,S,2))`.
- Do not retrieve only the generic breakout card; this pattern requires band-width compression.

## Example Compositions

### Band width below its 50-period average

User request:

```text
Find stocks with a Bollinger Band squeeze
```

Explorer output:

```text
Column A: BBandTop(C,20,S,2) - BBandBot(C,20,S,2)
Column B: Mov(BBandTop(C,20,S,2) - BBandBot(C,20,S,2),50,S)
Filter: ColA < ColB
```
### Squeeze plus upper-band breakout

User request:

```text
Find stocks with a Bollinger Band squeeze breakout
```

Explorer output:

```text
Column A: C
Column B: BBandTop(C,20,S,2)
Column C: BBandTop(C,20,S,2) - BBandBot(C,20,S,2)
Column D: Mov(BBandTop(C,20,S,2) - BBandBot(C,20,S,2),50,S)
Filter: ColC < ColD AND ColA > ColB
```

## Observable Outputs

Useful Explorer columns:

- Current close `C`
- Upper band `BBandTop(C,20,S,2)`
- Lower band `BBandBot(C,20,S,2)`
- Band width `BBandTop(C,20,S,2)-BBandBot(C,20,S,2)`
- Average band width

## Default Assumptions

- Default Bollinger settings are `C,20,S,2`.
- Squeeze means current band width is below its own 50-period simple average if no threshold is specified.
- Bullish squeeze breakout means close above the upper band after compression.

## Pitfalls

- Do not treat a simple price breakout as a Bollinger squeeze.
- Do not compare `Mov(ColA,50,S)`; Explorer columns are last-value references, not historical arrays.
- Do not omit either upper or lower band in width calculations.

## Good outputs

```metastock
(BBandTop(C,20,S,2)-BBandBot(C,20,S,2)) < Mov(BBandTop(C,20,S,2)-BBandBot(C,20,S,2),50,S)
C > BBandTop(C,20,S,2)
```

## What not to do

- Bad: retrieve only `pattern.breakout` for Bollinger squeeze breakout.
- Bad: `Mov(ColA,50,S)` for average width.
- Bad: `BollingerSqueeze(C,20)` invented function.

## Related functions and concepts

- function.bbandtop
- function.bbandbot
- function.mov
- pattern.bollinger_band_breakout

## Retrieval keywords

Bollinger Band squeeze, Bollinger squeeze, narrow bands, band width, volatility contraction, BBandTop, BBandBot.

## Test Queries

- Find stocks with a Bollinger Band squeeze
- Find stocks with a Bollinger Band squeeze breakout
