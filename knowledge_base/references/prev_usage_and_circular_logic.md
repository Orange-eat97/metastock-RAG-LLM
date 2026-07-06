---
canonical_id: reference.prev_usage_and_circular_logic
title: PREV Usage and Circular Logic
type: reference
card_bucket: references
category: prev_usage_and_circular_logic
source: MetaStock Formula Primer / Formula Primer II / internal project rule
status: active
priority: 10
supports_explorer: true
aliases:
- text: PREV Usage and Circular Logic
  type: exact
  weight: 1.0
- text: PREV recursive formula
  type: synonym
  weight: 0.85
- text: MetaStock PREV switch
  type: synonym
  weight: 0.85
- text: logical switch with PREV
  type: synonym
  weight: 0.85
- text: recursive smoothing with PREV
  type: synonym
  weight: 0.85
- text: circular formula warning
  type: synonym
  weight: 0.85
semantic:
  concept_role: reference
  mechanism: prev_usage_and_circular_logic
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
  canonical_id: reference.prev_usage_and_circular_logic
  supports_explorer: true
  priority: 10
  properties:
    formula_role: prev_usage_and_circular_logic
    supports_explorer: true
    source_path: references/prev_usage_and_circular_logic.md
    generated_schema_version: registry_ready_v2
---

# PREV Usage and Circular Logic

## Purpose

Define when and how to use `PREV` in MetaStock formulas, especially for recursive state logic and custom smoothing.

## Rules

- `PREV` refers to the previous value of the current formula expression.
- Use `PREV` for recursive calculations such as switches, custom smoothing, and running state.
- Initialize recursive logic with an `If` condition so the first valid value is defined.
- Keep recursive formulas simple and validate them in MetaStock.

## Examples

```metastock
If(Cross(C,Mov(C,50,S)),1,If(Cross(Mov(C,50,S),C),0,PREV))
If(Cum(1)=14,Sum(C,14)/14,PREV+((C-PREV)/14))
```

## What Not To Do

- Do not use PREV when a simple `Ref()` is enough.
- Do not create circular variables with no initialization.
- Do not assume PREV references a prior column value.

## Natural Language Mappings

- PREV recursive formula
- MetaStock PREV switch
- logical switch with PREV
- recursive smoothing with PREV
- circular formula warning

## Retrieval keywords

PREV recursive formula, MetaStock PREV switch, logical switch with PREV, recursive smoothing with PREV, circular formula warning.

## Test Queries

- PREV recursive formula
- MetaStock PREV switch
