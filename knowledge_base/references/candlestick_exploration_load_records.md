---
canonical_id: reference.candlestick_exploration_load_records
title: Candlestick Exploration Load Records
type: reference
card_bucket: references
category: candlestick_exploration_load_records
source: MetaStock Formula Primer / Formula Primer II / internal project rule
status: active
priority: 10
supports_explorer: true
aliases:
- text: Candlestick Exploration Load Records
  type: exact
  weight: 1.0
- text: candlestick load records
  type: synonym
  weight: 0.85
- text: Load 10 records candlestick
  type: synonym
  weight: 0.85
- text: Explorer Options candlestick
  type: synonym
  weight: 0.85
- text: candlestick exploration inaccurate
  type: synonym
  weight: 0.85
semantic:
  concept_role: reference
  mechanism: candlestick_exploration_load_records
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
  canonical_id: reference.candlestick_exploration_load_records
  supports_explorer: true
  priority: 10
  properties:
    formula_role: candlestick_exploration_load_records
    supports_explorer: true
    source_path: references/candlestick_exploration_load_records.md
    generated_schema_version: registry_ready_v2
---

# Candlestick Exploration Load Records

## Purpose

Warn that MetaStock candlestick explorations need enough loaded records for accurate pattern detection.

## Rules

- When using candlestick functions in an exploration, configure Explorer Options to load enough records.
- The Primer specifically warns to specify at least 10 loaded records.
- This is an execution/runtime configuration pitfall, not a formula syntax change.
- Mention this assumption in generated Explorer descriptions for candlestick scans.

## Examples

```metastock
hammer()
engulfingbull() OR piercingline()
darkcloud() OR eveningstar()
```

## What Not To Do

- Do not run candlestick explorations with insufficient loaded records.
- Do not hide the load-record assumption from the user.
- Do not treat wrong results from insufficient records as formula syntax failure.

## Natural Language Mappings

- candlestick load records
- Load 10 records candlestick
- Explorer Options candlestick
- candlestick exploration inaccurate

## Retrieval keywords

candlestick load records, Load 10 records candlestick, Explorer Options candlestick, candlestick exploration inaccurate.

## Test Queries

- candlestick load records
- Load 10 records candlestick
