---
canonical_id: pattern.volatility_expansion
title: 'Pattern: Volatility Expansion'
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
- HHV
aliases:
- text: 'Pattern: Volatility Expansion'
  type: synonym
  weight: 0.85
- text: Volatility Expansion
  type: exact
  weight: 1.0
- text: standard deviation is rising
  type: synonym
  weight: 0.85
- text: Bollinger Band width expanding
  type: synonym
  weight: 0.85
- text: price volatility increasing
  type: synonym
  weight: 0.85
- text: breakout with volatility expansion
  type: phrase
  weight: 0.9
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
- canonical_id: function.hhv
  rationale: function.hhv is often useful context for this card but is not always mandatory.
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
  canonical_id: pattern.volatility_expansion
  supports_explorer: true
  priority: 10
  properties:
    formula_role: volatility
    supports_explorer: true
    source_path: patterns/volatility_expansion.md
    generated_schema_version: registry_ready_v2
---

# Pattern: Volatility Expansion

## Intent

Detect securities where volatility is increasing, often as confirmation of a breakout or momentum move.

## Natural Language Triggers

- volatility expansion
- standard deviation is rising
- Bollinger Band width expanding
- price volatility increasing
- breakout with volatility expansion

## Required Logical Components

- Choose a volatility measure such as `Stdev(C,20)` or Bollinger Band width.
- Compare current volatility against the previous value or average.
- Optionally combine with breakout condition.

## Formula Building Blocks

```metastock
Stdev(C,20) > Ref(Stdev(C,20),-1)
BBandTop(C,20,S,2)-BBandBot(C,20,S,2)
C > Ref(HHV(C,20),-1) AND Stdev(C,20) > Ref(Stdev(C,20),-1)
```

## Example Compositions

```metastock
Stdev(C,20) > Ref(Stdev(C,20),-1)
C > Ref(HHV(C,20),-1) AND Stdev(C,20) > Ref(Stdev(C,20),-1)
```

## Default Assumptions

- Default lookback period is 20.
- Expansion is a confirmation, not a direction by itself.
- Use breakout pattern if user asks for expansion with price breakout.

## Pitfalls

- Do not use volatility expansion as a standalone bullish signal unless user asks.
- Do not confuse volatility expansion with volume above average.
- Do not omit Ref when comparing to previous value.

## Related functions and concepts

- function.stdev
- function.ref
- function.hhv
- pattern.breakout
- function.bbandtop
- function.bbandbot

## Retrieval keywords

volatility expansion, standard deviation is rising, Bollinger Band width expanding, price volatility increasing, breakout with volatility expansion, Stdev, Ref, HHV.

## Test Queries

- Find stocks with volatility expansion
- Find close breakout with standard deviation rising
