---
canonical_id: pattern.volatility_contraction
title: 'Pattern: Volatility Contraction'
type: pattern
card_bucket: patterns
category: volatility
source: MetaStock Formula Primer / Formula Primer II / internal project pattern
status: active
priority: 10
supports_explorer: true
functions:
- Stdev
- Ref
- BBandTop
- BBandBot
aliases:
- text: 'Pattern: Volatility Contraction'
  type: synonym
  weight: 0.85
- text: Volatility Contraction
  type: exact
  weight: 1.0
- text: standard deviation is falling
  type: synonym
  weight: 0.85
- text: Bollinger Band width contracting
  type: synonym
  weight: 0.85
- text: Bollinger squeeze by narrowing bands
  type: phrase
  weight: 0.9
- text: price volatility decreasing
  type: synonym
  weight: 0.85
requires:
- canonical_id: function.stdev
  rationale: This card usually needs function.stdev for correct formula generation.
  priority: 10
  properties:
    source: registry_ready_transform
    formula_role: requires
- canonical_id: function.ref
  rationale: This card usually needs function.ref for correct formula generation.
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
- canonical_id: pattern.bollinger_band_squeeze
  rationale: pattern.bollinger_band_squeeze is often useful context for this card but is not always mandatory.
  priority: 40
  properties:
    source: registry_ready_transform
    formula_role: suggests
- canonical_id: pattern.breakout
  rationale: pattern.breakout is often useful context for this card but is not always mandatory.
  priority: 40
  properties:
    source: registry_ready_transform
    formula_role: suggests
semantic:
  concept_role: pattern
  mechanism: volatility
  market_object: price
  directions_supported:
  - bullish
  - bearish
  operations_supported:
  - volatility
  - volatility_condition
  required_components:
  - stdev
  - ref
  does_not_cover:
  - unrelated_pattern_substitution
  - guaranteed_trade_profitability
registry:
  enabled: true
  canonical_id: pattern.volatility_contraction
  supports_explorer: true
  priority: 10
  properties:
    formula_role: volatility
    supports_explorer: true
    source_path: patterns/volatility_contraction.md
    generated_schema_version: registry_ready_v2
---

# Pattern: Volatility Contraction

## Intent

Detect securities where volatility is narrowing, using standard deviation or Bollinger Band width.

## Natural Language Triggers

- volatility contraction
- standard deviation is falling
- Bollinger Band width contracting
- Bollinger squeeze by narrowing bands
- price volatility decreasing

## Required Logical Components

- Choose volatility measure: `Stdev(C,N)` or Bollinger Band width.
- Compare current volatility with previous volatility or its average.
- Optionally combine with breakout confirmation in another pattern.

## Formula Building Blocks

```metastock
Stdev(C,20) < Ref(Stdev(C,20),-1)
BBandTop(C,20,S,2) - BBandBot(C,20,S,2)
(BBandTop(C,20,S,2)-BBandBot(C,20,S,2)) < Ref(BBandTop(C,20,S,2)-BBandBot(C,20,S,2),-1)
```

## Example Compositions

```metastock
Stdev(C,20) < Ref(Stdev(C,20),-1)
(BBandTop(C,20,S,2)-BBandBot(C,20,S,2)) < Ref(BBandTop(C,20,S,2)-BBandBot(C,20,S,2),-1)
```

## Default Assumptions

- Default lookback period is 20.
- If Bollinger cards exist, band width is top band minus bottom band.
- Contraction alone is not directional.

## Pitfalls

- Do not treat volatility contraction as bullish or bearish by itself.
- Do not confuse low volume with low volatility.
- Do not use broad alias `volatility` alone.

## Related functions and concepts

- function.stdev
- function.ref
- function.bbandtop
- function.bbandbot
- pattern.bollinger_band_squeeze
- pattern.breakout

## Retrieval keywords

volatility contraction, standard deviation is falling, Bollinger Band width contracting, Bollinger squeeze by narrowing bands, price volatility decreasing, Stdev, Ref, BBandTop, BBandBot.

## Test Queries

- Find stocks where volatility is contracting
- Find Bollinger Band width contracting
