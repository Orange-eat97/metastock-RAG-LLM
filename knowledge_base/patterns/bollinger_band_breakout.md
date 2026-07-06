---
canonical_id: pattern.bollinger_band_breakout
title: 'Pattern: Bollinger Band Breakout'
type: pattern
card_bucket: patterns
category: volatility_breakout
source: generated_curated_from_primer
status: active
priority: 10
supports_explorer: true
aliases:
- text: Bollinger Band breakout
  type: exact
  weight: 1.0
- text: upper Bollinger Band breakout
  type: phrase
  weight: 0.95
- text: close above upper band
  type: phrase
  weight: 0.95
- text: lower Bollinger Band breakdown
  type: phrase
  weight: 0.9
requires:
- canonical_id: function.bbandtop
  rationale: Upper-band breakout requires BBandTop.
  priority: 30
  properties:
    formula_role: upper_band
suggests:
- canonical_id: function.bbandbot
  rationale: Lower-band breakdown and full band context use BBandBot.
  priority: 30
  properties:
    formula_role: lower_band
- canonical_id: function.cross
  rationale: A breakout may be expressed as a crossing event.
  priority: 30
  properties:
    formula_role: crossing_event
semantic:
  concept_role: pattern
  mechanism: volatility_breakout
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
  canonical_id: pattern.bollinger_band_breakout
  supports_explorer: true
  priority: 10
  properties:
    formula_role: volatility_breakout
    source_path: patterns/bollinger_band_breakout.md
    curation_level: upgraded_to_curated_quality
---

# Pattern: Bollinger Band Breakout

## Intent

Detect securities where price breaks outside a Bollinger Band. Upper-band breakouts are usually bullish volatility expansion signals; lower-band breakdowns are usually bearish or oversold signals depending on strategy wording.

## Natural Language Triggers

- Bollinger Band breakout
- close above upper Bollinger Band
- price crosses above upper band
- break below lower Bollinger Band
- Bollinger volatility breakout

## Keywords

- Bollinger breakout
- upper band breakout
- lower band breakdown
- BBandTop
- BBandBot
- Cross(C,BBandTop)

## Required Logical Components

- Choose direction: upper breakout or lower breakdown.
- Calculate the relevant Bollinger Band.
- Compare current close to the band or use Cross for a one-bar event.
- Optionally require squeeze or volume confirmation.

## Optional Confirmation Components

- Trend confirmation, such as close above a moving average.
- Volume confirmation, such as `V > Mov(V,20,S)`.
- Momentum confirmation, such as RSI, MACD, or ROC improving.
- Recency confirmation using `BarsSince()` when the user asks for recent signals.

## Formula Building Blocks

```metastock
C > BBandTop(C,20,S,2)
Cross(C,BBandTop(C,20,S,2))
C < BBandBot(C,20,S,2)
Cross(BBandBot(C,20,S,2),C)
```

## Composition Guidance

- If user says breakout without lower/upper, assume bullish upper-band breakout.
- Use `C > BBandTop(...)` for continuing above-band condition.
- Use `Cross(C,BBandTop(...))` when the user says crosses/breaks today.
- For lower-band breakdown, use `C < BBandBot(...)`.

## Example Compositions

### Upper-band breakout

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
### Upper-band crossing event

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
### Lower-band breakdown

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

## Observable Outputs

Useful Explorer columns:

- Current close
- Upper Bollinger Band
- Lower Bollinger Band
- Band breakout flag

## Default Assumptions

- Default Bollinger settings are `C,20,S,2`.
- Breakout means close-based confirmation unless high/low is specified.
- Crossing language means use `Cross`.

## Pitfalls

- Do not use `Cross` for a continuing above-band condition.
- Do not use lower band when user asks for upper breakout.
- Do not invent `BollingerBreakout()` function.

## Good outputs

```metastock
C > BBandTop(C,20,S,2)
Cross(C,BBandTop(C,20,S,2))
C < BBandBot(C,20,S,2)
```

## What not to do

- Bad: `C > BollingerTop(C,20,2)`.
- Bad: `Cross(BBandTop(C,20,S,2),C)` for bullish upper-band cross.
- Bad: assuming breakout includes squeeze unless user says squeeze.

## Related functions and concepts

- function.bbandtop
- function.bbandbot
- function.cross
- pattern.bollinger_band_squeeze

## Retrieval keywords

Bollinger breakout, upper band breakout, lower band breakdown, BBandTop, BBandBot, Cross(C,BBandTop).

## Test Queries

- Find stocks where close crosses above the upper Bollinger Band
