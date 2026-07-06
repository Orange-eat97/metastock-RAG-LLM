---
canonical_id: pattern.stochastic_oversold_recovery
title: 'Pattern: Stochastic Oversold Recovery'
type: pattern
card_bucket: patterns
category: momentum_recovery
source: MetaStock Formula Primer / Formula Primer II / internal project pattern
status: active
priority: 10
supports_explorer: true
functions:
- Stoch
- Cross
aliases:
- text: 'Pattern: Stochastic Oversold Recovery'
  type: phrase
  weight: 0.9
- text: Stochastic Oversold Recovery
  type: exact
  weight: 1.0
- text: stochastic crosses above 20
  type: phrase
  weight: 0.9
- text: stochastic turns up from oversold
  type: phrase
  weight: 0.9
- text: Stoch(14,3) crosses above 20
  type: phrase
  weight: 0.9
- text: stochastic buy signal
  type: synonym
  weight: 0.85
requires:
- canonical_id: function.stoch
  rationale: This card usually needs function.stoch for correct formula generation.
  priority: 10
  properties:
    source: registry_ready_transform
    formula_role: requires
- canonical_id: function.cross
  rationale: This card usually needs function.cross for correct formula generation.
  priority: 10
  properties:
    source: registry_ready_transform
    formula_role: requires
suggests:
- canonical_id: function.mov
  rationale: function.mov is often useful context for this card but is not always mandatory.
  priority: 40
  properties:
    source: registry_ready_transform
    formula_role: suggests
- canonical_id: template.explorer_columns_filter
  rationale: template.explorer_columns_filter is often useful context for this card but is not always mandatory.
  priority: 40
  properties:
    source: registry_ready_transform
    formula_role: suggests
semantic:
  concept_role: pattern
  mechanism: momentum_recovery
  market_object: price
  directions_supported:
  - bullish
  - bearish
  operations_supported:
  - momentum_recovery
  required_components:
  - stoch
  - cross
  does_not_cover:
  - unrelated_pattern_substitution
  - guaranteed_trade_profitability
registry:
  enabled: true
  canonical_id: pattern.stochastic_oversold_recovery
  supports_explorer: true
  priority: 10
  properties:
    formula_role: momentum_recovery
    supports_explorer: true
    source_path: patterns/stochastic_oversold_recovery.md
    generated_schema_version: registry_ready_v2
---

# Pattern: Stochastic Oversold Recovery

## Intent

Detect securities where the stochastic oscillator recovers upward from an oversold zone, usually by crossing above 20.

## Natural Language Triggers

- stochastic oversold recovery
- stochastic crosses above 20
- stochastic turns up from oversold
- Stoch(14,3) crosses above 20
- stochastic buy signal

## Required Logical Components

- Calculate stochastic oscillator with a default period and slowing value.
- Define the oversold threshold, usually 20.
- Use `Cross(Stoch(14,3),20)` for the recovery event.
- Use `Stoch(14,3) < 20` only when the user asks for still-oversold securities.

## Formula Building Blocks

```metastock
Stoch(14,3)
Cross(Stoch(14,3),20)
Stoch(14,3) < 20
```

## Example Compositions

```metastock
Cross(Stoch(14,3),20)
Cross(Stoch(14,3),20) AND C > Mov(C,50,S)
```

## Default Assumptions

- Default stochastic settings are 14 periods and 3 slowing if unspecified.
- Oversold threshold defaults to 20.
- Recovery means a crossing above 20, not merely being below 20.

## Pitfalls

- Do not use RSI thresholds for stochastic unless the user asks for RSI.
- Do not use `Cross(20,Stoch(14,3))` for bullish recovery; that represents a cross below 20.
- Do not invent `Stochastic()` if `Stoch()` is the supported function.

## Related functions and concepts

- function.stoch
- function.cross
- function.mov
- template.explorer_columns_filter

## Retrieval keywords

stochastic oversold recovery, stochastic crosses above 20, stochastic turns up from oversold, Stoch(14,3) crosses above 20, stochastic buy signal, Stoch, Cross.

## Test Queries

- Find stocks where stochastic crosses above 20
- Find stocks with stochastic oversold recovery and close above 50 day moving average
