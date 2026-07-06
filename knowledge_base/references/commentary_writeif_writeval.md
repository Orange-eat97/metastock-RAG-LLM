---
canonical_id: reference.commentary_writeif_writeval
title: Commentary WriteIf / WriteVal Rules
type: reference
card_bucket: references
category: commentary_writeif_writeval
source: MetaStock Formula Primer / Formula Primer II / internal project rule
status: active
priority: 10
supports_explorer: false
aliases:
- text: Commentary WriteIf / WriteVal Rules
  type: exact
  weight: 1.0
- text: WriteIf commentary rule
  type: synonym
  weight: 0.85
- text: WriteVal commentary rule
  type: synonym
  weight: 0.85
- text: Expert Advisor commentary
  type: synonym
  weight: 0.85
- text: commentary text functions
  type: synonym
  weight: 0.85
requires:
- canonical_id: function.writeif
  rationale: This card usually needs function.writeif for correct formula generation.
  priority: 10
  properties:
    source: registry_ready_transform
    formula_role: requires
- canonical_id: function.writeval
  rationale: This card usually needs function.writeval for correct formula generation.
  priority: 10
  properties:
    source: registry_ready_transform
    formula_role: requires
semantic:
  concept_role: reference
  mechanism: commentary_writeif_writeval
  market_object: formula_commentary
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
  canonical_id: reference.commentary_writeif_writeval
  supports_explorer: false
  priority: 10
  properties:
    formula_role: commentary_writeif_writeval
    supports_explorer: false
    source_path: references/commentary_writeif_writeval.md
    generated_schema_version: registry_ready_v2
---

# Commentary WriteIf / WriteVal Rules

## Purpose

Keep Expert Advisor commentary functions separate from Explorer formula generation.

## Rules

- `WriteIf` displays conditional text in Expert Advisor commentary.
- `WriteVal` displays calculated numeric values as text in commentary.
- These functions are not scan/filter conditions for Explorer.
- Use numeric formulas for Explorer; use commentary functions only in Expert Advisor commentary cards.

## Examples

```metastock
WriteIf(RSI(14)>70,"Overbought","Not overbought")
WriteVal(C)
WriteVal(Mov(C,40,S))
```

## What Not To Do

- Do not use `WriteIf` in Explorer filter.
- Do not use `WriteVal` in Explorer column definitions for numeric scans.
- Do not mix commentary text output with formula conditions.

## Natural Language Mappings

- WriteIf commentary rule
- WriteVal commentary rule
- Expert Advisor commentary
- commentary text functions

## Retrieval keywords

WriteIf commentary rule, WriteVal commentary rule, Expert Advisor commentary, commentary text functions.

## Test Queries

- WriteIf commentary rule
- WriteVal commentary rule
