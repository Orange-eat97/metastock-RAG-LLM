---
canonical_id: pattern.pivot_points
title: 'Pattern: Classic Pivot Points'
type: pattern
card_bucket: patterns
category: support_resistance
source: MetaStock Formula Primer / Formula Primer II / internal project pattern
status: active
priority: 10
supports_explorer: true
functions:
- Ref
aliases:
- text: 'Pattern: Classic Pivot Points'
  type: synonym
  weight: 0.85
- text: Classic Pivot Points
  type: exact
  weight: 1.0
- text: classic pivot point
  type: synonym
  weight: 0.85
- text: price above pivot point
  type: phrase
  weight: 0.9
- text: daily pivot point from previous day
  type: synonym
  weight: 0.85
- text: pivot support resistance levels
  type: phrase
  weight: 0.9
- text: floor trader pivot
  type: synonym
  weight: 0.85
requires:
- canonical_id: function.ref
  rationale: This card usually needs function.ref for correct formula generation.
  priority: 10
  properties:
    source: registry_ready_transform
    formula_role: requires
suggests:
- canonical_id: reference.price_fields
  rationale: reference.price_fields is often useful context for this card but is not always mandatory.
  priority: 40
  properties:
    source: registry_ready_transform
    formula_role: suggests
- canonical_id: reference.higher_timeframe_explorer_limitations
  rationale: reference.higher_timeframe_explorer_limitations is often useful context for this card but is not always mandatory.
  priority: 40
  properties:
    source: registry_ready_transform
    formula_role: suggests
semantic:
  concept_role: pattern
  mechanism: support_resistance
  market_object: price
  directions_supported:
  - bullish
  - bearish
  operations_supported:
  - support_resistance
  required_components:
  - ref
  does_not_cover:
  - unrelated_pattern_substitution
  - guaranteed_trade_profitability
registry:
  enabled: true
  canonical_id: pattern.pivot_points
  supports_explorer: true
  priority: 10
  properties:
    formula_role: support_resistance
    supports_explorer: true
    source_path: patterns/pivot_points.md
    generated_schema_version: registry_ready_v2
---

# Pattern: Classic Pivot Points

## Intent

Calculate classic floor-trader pivot levels from previous period high, low, and close, and scan price relative to those levels.

## Natural Language Triggers

- classic pivot point
- price above pivot point
- daily pivot point from previous day
- pivot support resistance levels
- floor trader pivot

## Required Logical Components

- Get previous high, low, and close with `Ref`.
- Calculate pivot point as average of previous high, low, and close.
- Optionally calculate support/resistance levels from the pivot.
- Compare current close against pivot or levels.

## Formula Building Blocks

```metastock
P:= (Ref(H,-1)+Ref(L,-1)+Ref(C,-1))/3;
C > (Ref(H,-1)+Ref(L,-1)+Ref(C,-1))/3
R1:= 2*P-Ref(L,-1);
S1:= 2*P-Ref(H,-1);
```

## Example Compositions

```metastock
C > (Ref(H,-1)+Ref(L,-1)+Ref(C,-1))/3
C < (Ref(H,-1)+Ref(L,-1)+Ref(C,-1))/3
```

## Default Assumptions

- Default pivot uses previous bar high, low, and close.
- For daily data this means previous trading day.
- For intraday data, true daily pivots require careful session handling.

## Pitfalls

- Do not confuse classic pivot points with swing pivots from Peak/Trough.
- Do not use current H/L/C in the pivot calculation.
- Do not use positive future references.

## Related functions and concepts

- function.ref
- reference.price_fields
- reference.higher_timeframe_explorer_limitations

## Retrieval keywords

classic pivot point, price above pivot point, daily pivot point from previous day, pivot support resistance levels, floor trader pivot, Ref.

## Test Queries

- Find stocks closing above classic pivot point
- Create a daily pivot point scan using previous high low close
