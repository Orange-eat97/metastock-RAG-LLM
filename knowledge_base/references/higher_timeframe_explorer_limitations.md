---
canonical_id: reference.higher_timeframe_explorer_limitations
title: Higher Timeframe Explorer Limitations
type: reference
card_bucket: references
category: higher_timeframe_explorer_limitations
source: MetaStock Formula Primer / Formula Primer II / internal project rule
status: active
priority: 10
supports_explorer: true
aliases:
- text: Higher Timeframe Explorer Limitations
  type: exact
  weight: 1.0
- text: higher timeframe limitation
  type: synonym
  weight: 0.85
- text: weekly approximation daily data
  type: synonym
  weight: 0.85
- text: monthly approximation daily data
  type: synonym
  weight: 0.85
- text: multi timeframe Explorer caveat
  type: synonym
  weight: 0.85
requires:
- canonical_id: function.mov
  rationale: This card usually needs function.mov for correct formula generation.
  priority: 10
  properties:
    source: registry_ready_transform
    formula_role: requires
semantic:
  concept_role: reference
  mechanism: higher_timeframe_explorer_limitations
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
  canonical_id: reference.higher_timeframe_explorer_limitations
  supports_explorer: true
  priority: 10
  properties:
    formula_role: higher_timeframe_explorer_limitations
    supports_explorer: true
    source_path: references/higher_timeframe_explorer_limitations.md
    generated_schema_version: registry_ready_v2
---

# Higher Timeframe Explorer Limitations

## Purpose

State the limitations of approximating higher-timeframe logic in Explorer formulas.

## Rules

- A daily formula that multiplies periods is only an approximation of weekly/monthly logic.
- True higher-timeframe calculations require data prepared at that timeframe or careful custom construction.
- If approximation is used, document the conversion assumption.
- Do not use future bars or incomplete periods to force a higher-timeframe signal.

## Examples

```metastock
Mov(C,50,S) {approximate 10-week moving average on daily data}
Mov(C,100,S) {approximate 20-week moving average on daily data}
```

## What Not To Do

- Do not claim a daily 50-period moving average is exactly a weekly 10-period moving average.
- Do not mix intraday and daily logic without defining session boundaries.
- Do not use positive Ref to complete a higher timeframe bar.

## Natural Language Mappings

- higher timeframe limitation
- weekly approximation daily data
- monthly approximation daily data
- multi timeframe Explorer caveat

## Retrieval keywords

higher timeframe limitation, weekly approximation daily data, monthly approximation daily data, multi timeframe Explorer caveat.

## Test Queries

- higher timeframe limitation
- weekly approximation daily data
