---
canonical_id: pattern.aroon_trend
title: 'Pattern: Aroon Trend'
type: pattern
card_bucket: patterns
category: trend_indicator
source: MetaStock Formula Primer / Formula Primer II / internal project pattern
status: active
priority: 10
supports_explorer: true
functions:
- AroonUp
- AroonDown
- Cross
aliases:
- text: 'Pattern: Aroon Trend'
  type: synonym
  weight: 0.85
- text: Aroon Trend
  type: exact
  weight: 1.0
- text: Aroon bullish trend
  type: synonym
  weight: 0.85
- text: Aroon Up above Aroon Down
  type: phrase
  weight: 0.9
- text: Aroon Up above 70 and Aroon Down below 30
  type: phrase
  weight: 0.9
- text: Aroon bearish trend
  type: synonym
  weight: 0.85
- text: Aroon Down above Aroon Up
  type: phrase
  weight: 0.9
requires:
- canonical_id: function.aroonup
  rationale: This card usually needs function.aroonup for correct formula generation.
  priority: 10
  properties:
    source: registry_ready_transform
    formula_role: requires
- canonical_id: function.aroondown
  rationale: This card usually needs function.aroondown for correct formula generation.
  priority: 10
  properties:
    source: registry_ready_transform
    formula_role: requires
suggests:
- canonical_id: function.cross
  rationale: function.cross is often useful context for this card but is not always mandatory.
  priority: 40
  properties:
    source: registry_ready_transform
    formula_role: suggests
semantic:
  concept_role: pattern
  mechanism: trend_indicator
  market_object: price
  directions_supported:
  - bullish
  - bearish
  operations_supported:
  - trend_indicator
  required_components:
  - aroonup
  - aroondown
  does_not_cover:
  - unrelated_pattern_substitution
  - guaranteed_trade_profitability
registry:
  enabled: true
  canonical_id: pattern.aroon_trend
  supports_explorer: true
  priority: 10
  properties:
    formula_role: trend_indicator
    supports_explorer: true
    source_path: patterns/aroon_trend.md
    generated_schema_version: registry_ready_v2
---

# Pattern: Aroon Trend

## Intent

Detect bullish or bearish trend conditions using the relationship between Aroon Up and Aroon Down.

## Natural Language Triggers

- Aroon bullish trend
- Aroon Up above Aroon Down
- Aroon Up above 70 and Aroon Down below 30
- Aroon bearish trend
- Aroon Down above Aroon Up

## Required Logical Components

- Calculate `AroonUp(N)` and `AroonDown(N)`.
- For bullish trend, compare Aroon Up above Aroon Down.
- For stricter bullish trend, require Aroon Up high and Aroon Down low.
- For bearish trend, reverse the relationship.

## Formula Building Blocks

```metastock
AroonUp(14) > AroonDown(14)
AroonUp(14) > 70 AND AroonDown(14) < 30
AroonDown(14) > AroonUp(14)
```

## Example Compositions

```metastock
AroonUp(14) > AroonDown(14)
AroonUp(14) > 70 AND AroonDown(14) < 30
AroonDown(14) > AroonUp(14)
```

## Default Assumptions

- Default period is 14 unless the user specifies another period.
- Bullish means Aroon Up dominates Aroon Down.
- Bearish means Aroon Down dominates Aroon Up.

## Pitfalls

- Do not use only Aroon Up when the user asks for an Aroon trend comparison.
- Do not reverse bullish and bearish relationships.
- Do not use broad alias `trend`.

## Related functions and concepts

- function.aroonup
- function.aroondown
- function.cross

## Retrieval keywords

Aroon bullish trend, Aroon Up above Aroon Down, Aroon Up above 70 and Aroon Down below 30, Aroon bearish trend, Aroon Down above Aroon Up, AroonUp, AroonDown, Cross.

## Test Queries

- Find stocks where Aroon Up is above Aroon Down
- Find bullish Aroon trend stocks
