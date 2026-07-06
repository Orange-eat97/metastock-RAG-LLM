---
canonical_id: pattern.standard_deviation_breakout
title: 'Pattern: Standard Deviation Breakout'
type: pattern
card_bucket: patterns
category: volatility_breakout
source: MetaStock Formula Primer / Formula Primer II / internal project pattern
status: active
priority: 10
supports_explorer: true
functions:
- Stdev
- Mov
aliases:
- text: 'Pattern: Standard Deviation Breakout'
  type: phrase
  weight: 0.9
- text: Standard Deviation Breakout
  type: exact
  weight: 1.0
- text: close above two standard deviations
  type: phrase
  weight: 0.9
- text: price above moving average plus 2 standard deviations
  type: phrase
  weight: 0.9
- text: standard deviation band breakout
  type: phrase
  weight: 0.9
- text: close below lower standard deviation band
  type: phrase
  weight: 0.9
requires:
- canonical_id: function.stdev
  rationale: This card usually needs function.stdev for correct formula generation.
  priority: 10
  properties:
    source: registry_ready_transform
    formula_role: requires
- canonical_id: function.mov
  rationale: This card usually needs function.mov for correct formula generation.
  priority: 10
  properties:
    source: registry_ready_transform
    formula_role: requires
suggests:
- canonical_id: function.bbandtop
  rationale: function.bbandtop is often useful context for this card but is not always mandatory.
  priority: 40
  properties:
    source: registry_ready_transform
    formula_role: suggests
- canonical_id: function.bbandbot
  rationale: function.bbandbot is often useful context for this card but is not always mandatory.
  priority: 40
  properties:
    source: registry_ready_transform
    formula_role: suggests
- canonical_id: pattern.bollinger_band_breakout
  rationale: pattern.bollinger_band_breakout is often useful context for this card but is not always mandatory.
  priority: 40
  properties:
    source: registry_ready_transform
    formula_role: suggests
semantic:
  concept_role: pattern
  mechanism: volatility_breakout
  market_object: price
  directions_supported:
  - bullish
  - bearish
  operations_supported:
  - breakout_detection
  - volatility_breakout
  - volatility_condition
  required_components:
  - stdev
  - mov
  does_not_cover:
  - unrelated_pattern_substitution
  - guaranteed_trade_profitability
registry:
  enabled: true
  canonical_id: pattern.standard_deviation_breakout
  supports_explorer: true
  priority: 10
  properties:
    formula_role: volatility_breakout
    supports_explorer: true
    source_path: patterns/standard_deviation_breakout.md
    generated_schema_version: registry_ready_v2
---

# Pattern: Standard Deviation Breakout

## Intent

Detect price breaking beyond a moving average by a standard-deviation band, similar to a manually constructed band breakout.

## Natural Language Triggers

- standard deviation breakout
- close above two standard deviations
- price above moving average plus 2 standard deviations
- standard deviation band breakout
- close below lower standard deviation band

## Required Logical Components

- Calculate moving average baseline.
- Calculate standard deviation over the same lookback period.
- Build upper/lower band using multiplier.
- Compare close against the band.

## Formula Building Blocks

```metastock
Mov(C,20,S) + 2 * Stdev(C,20)
Mov(C,20,S) - 2 * Stdev(C,20)
C > Mov(C,20,S) + 2 * Stdev(C,20)
C < Mov(C,20,S) - 2 * Stdev(C,20)
```

## Example Compositions

```metastock
C > Mov(C,20,S) + 2 * Stdev(C,20)
C < Mov(C,20,S) - 2 * Stdev(C,20)
```

## Default Assumptions

- Default period is 20.
- Default standard deviation multiplier is 2.
- Use Bollinger Band cards if the user explicitly says Bollinger.

## Pitfalls

- Do not use `Stdev(C,20)` alone as the breakout level.
- Do not confuse upper and lower band logic.
- Do not invent `StdDevBandTop()` unless supported.

## Related functions and concepts

- function.stdev
- function.mov
- function.bbandtop
- function.bbandbot
- pattern.bollinger_band_breakout

## Retrieval keywords

standard deviation breakout, close above two standard deviations, price above moving average plus 2 standard deviations, standard deviation band breakout, close below lower standard deviation band, Stdev, Mov.

## Test Queries

- Find stocks closing above two standard deviations
- Find standard deviation band breakout stocks
