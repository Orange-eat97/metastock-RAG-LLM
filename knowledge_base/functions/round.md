---
canonical_id: function.round
title: Round
type: function
card_bucket: functions
category: math
source: MetaStock Formula Primer
status: active
priority: 10
supports_explorer: true
function: Round
aliases:
- text: Round
  type: exact
  weight: 1.0
- text: round to nearest integer
  type: synonym
  weight: 0.85
- text: Round function
  type: synonym
  weight: 0.85
- text: rounded RSI
  type: synonym
  weight: 0.85
- text: rounded close
  type: synonym
  weight: 0.85
semantic:
  concept_role: function
  mechanism: math
  market_object: price
  outputs:
  - numeric_value
  supports_conditions:
  - threshold_comparison
  - crossover
  - state_filter
  does_not_cover:
  - complete_trading_pattern_by_itself
registry:
  enabled: true
  canonical_id: function.round
  supports_explorer: true
  priority: 10
  properties:
    formula_role: math
    supports_explorer: true
    source_path: functions/round.md
    generated_schema_version: registry_ready_v2
---

# Round

## Purpose

`Round` rounds a value to the nearest integer. It is useful for display-like calculations or formulas needing integer thresholds.

## Syntax

```metastock
Round(DATA ARRAY)
```

## Parameters

- `DATA ARRAY`: Value or formula to round

## Valid Examples

```metastock
Round(C)
Round(RSI(14))
```

## Common Mistakes

- Do not use `Round` to control Explorer sorting unless the rounded value is intended.
- Do not pass a precision argument; use a separate precision function if needed.
- Do not confuse rounding with truncation.

## Related Patterns

- None yet.

## Natural Language Mappings

Use this function when the user says:

- round to nearest integer
- Round function
- rounded RSI
- rounded close

## Assumptions

- Use this function only when the user request explicitly maps to this concept.

## Retrieval keywords

round to nearest integer, Round function, rounded RSI, rounded close, Round, Round(DATA ARRAY).

## Test Queries

- Find stocks using Round
