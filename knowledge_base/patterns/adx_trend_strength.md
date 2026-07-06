---
canonical_id: pattern.adx_trend_strength
title: 'Pattern: ADX Trend Strength'
type: pattern
card_bucket: patterns
category: trend_strength
source: MetaStock Formula Primer / Formula Primer II / internal project pattern
status: active
priority: 10
supports_explorer: true
functions:
- ADX
- PDI
- MDI
- Ref
aliases:
- text: 'Pattern: ADX Trend Strength'
  type: synonym
  weight: 0.85
- text: ADX Trend Strength
  type: exact
  weight: 1.0
- text: ADX above 25
  type: phrase
  weight: 0.9
- text: ADX rising trend strength
  type: synonym
  weight: 0.85
- text: bullish ADX trend
  type: synonym
  weight: 0.85
- text: bearish ADX trend
  type: synonym
  weight: 0.85
- text: PDI above MDI with ADX above 25
  type: phrase
  weight: 0.9
requires:
- canonical_id: function.adx
  rationale: This card usually needs function.adx for correct formula generation.
  priority: 10
  properties:
    source: registry_ready_transform
    formula_role: requires
suggests:
- canonical_id: function.pdi
  rationale: function.pdi is often useful context for this card but is not always mandatory.
  priority: 40
  properties:
    source: registry_ready_transform
    formula_role: suggests
- canonical_id: function.mdi
  rationale: function.mdi is often useful context for this card but is not always mandatory.
  priority: 40
  properties:
    source: registry_ready_transform
    formula_role: suggests
- canonical_id: function.ref
  rationale: function.ref is often useful context for this card but is not always mandatory.
  priority: 40
  properties:
    source: registry_ready_transform
    formula_role: suggests
semantic:
  concept_role: pattern
  mechanism: trend_strength
  market_object: price
  directions_supported:
  - bullish
  - bearish
  operations_supported:
  - trend_strength
  required_components:
  - adx
  does_not_cover:
  - unrelated_pattern_substitution
  - guaranteed_trade_profitability
registry:
  enabled: true
  canonical_id: pattern.adx_trend_strength
  supports_explorer: true
  priority: 10
  properties:
    formula_role: trend_strength
    supports_explorer: true
    source_path: patterns/adx_trend_strength.md
    generated_schema_version: registry_ready_v2
---

# Pattern: ADX Trend Strength

## Intent

Detect securities with strong trend strength using ADX, optionally adding PDI/MDI direction filters for bullish or bearish direction.

## Natural Language Triggers

- ADX trend strength
- ADX above 25
- ADX rising trend strength
- bullish ADX trend
- bearish ADX trend
- PDI above MDI with ADX above 25

## Required Logical Components

- Calculate `ADX(14)` for strength.
- For bullish direction, require `PDI(14) > MDI(14)`.
- For bearish direction, require `MDI(14) > PDI(14)`.
- Optionally require ADX rising with `ADX(14) > Ref(ADX(14),-1)`.

## Formula Building Blocks

```metastock
ADX(14) > 25
PDI(14) > MDI(14)
MDI(14) > PDI(14)
ADX(14) > Ref(ADX(14),-1)
```

## Example Compositions

```metastock
ADX(14) > 25
ADX(14) > 25 AND PDI(14) > MDI(14)
ADX(14) > 25 AND MDI(14) > PDI(14)
```

## Default Assumptions

- Default ADX period is 14.
- Default strength threshold is 25 if the user does not specify one.
- ADX alone is trend strength, not trend direction.

## Pitfalls

- Do not call `ADX(14) > 25` bullish without PDI/MDI direction.
- Do not use broad `trend` aliases that force-retrieve this card unnecessarily.
- Do not use `PDI`/`MDI` unless direction is needed.

## Related functions and concepts

- function.adx
- function.pdi
- function.mdi
- function.ref

## Retrieval keywords

ADX trend strength, ADX above 25, ADX rising trend strength, bullish ADX trend, bearish ADX trend, PDI above MDI with ADX above 25, ADX, PDI, MDI, Ref.

## Test Queries

- Find stocks with ADX above 25 and PDI above MDI
- Find strong bearish ADX trend stocks
