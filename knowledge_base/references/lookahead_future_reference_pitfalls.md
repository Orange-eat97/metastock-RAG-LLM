---
canonical_id: reference.lookahead_future_reference_pitfalls
title: Lookahead and Future Reference Pitfalls
type: reference
card_bucket: references
category: lookahead_future_reference_pitfalls
source: MetaStock Formula Primer / Formula Primer II / internal project rule
status: active
priority: 10
supports_explorer: true
aliases:
- text: Lookahead and Future Reference Pitfalls
  type: exact
  weight: 1.0
- text: lookahead bias
  type: synonym
  weight: 0.85
- text: future reference
  type: synonym
  weight: 0.85
- text: Ref positive number warning
  type: synonym
  weight: 0.85
- text: exclude current bar
  type: synonym
  weight: 0.85
- text: previous high with Ref HHV
  type: synonym
  weight: 0.85
requires:
- canonical_id: function.ref
  rationale: This card usually needs function.ref for correct formula generation.
  priority: 10
  properties:
    source: registry_ready_transform
    formula_role: requires
semantic:
  concept_role: reference
  mechanism: lookahead_future_reference_pitfalls
  market_object: formula_language
  operations_supported:
  - retrieval_context
  - formula_validation
  - generation_constraint
  required_components:
  - rule_application
  does_not_cover:
  - standalone_trading_signal
registry:
  enabled: true
  canonical_id: reference.lookahead_future_reference_pitfalls
  supports_explorer: true
  priority: 10
  properties:
    formula_role: lookahead_future_reference_pitfalls
    supports_explorer: true
    source_path: references/lookahead_future_reference_pitfalls.md
    generated_schema_version: registry_ready_v2
---

# Lookahead and Future Reference Pitfalls

## Purpose

Prevent generated formulas from using future data or future-looking references in Explorer scans.

## Rules

- Use negative `Ref` offsets to look backward, such as `Ref(C,-1)`.
- Avoid positive references like `Ref(C,1)` in Explorer scans because they look into future data relative to the exploration date.
- Exclude the current bar in previous-high/low logic with `Ref(HHV(...),-1)` or `Ref(LLV(...),-1)`.
- Validate current-bar inclusion/exclusion explicitly.

## Examples

```metastock
Ref(C,-1)
C > Ref(HHV(C,20),-1)
C < Ref(LLV(C,20),-1)
```

## What Not To Do

- Do not use `Ref(C,1)` for normal scans.
- Do not compare `C > HHV(C,20)` when the current bar is included; this is usually impossible.
- Do not use future bars to confirm pivots in Explorer.

## Natural Language Mappings

- lookahead bias
- future reference
- Ref positive number warning
- exclude current bar
- previous high with Ref HHV

## Retrieval keywords

lookahead bias, future reference, Ref positive number warning, exclude current bar, previous high with Ref HHV.

## Test Queries

- lookahead bias
- future reference
