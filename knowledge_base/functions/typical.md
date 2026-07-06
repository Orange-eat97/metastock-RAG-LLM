---
canonical_id: function.typical
title: Typical
type: function
card_bucket: functions
category: price_transform
source: MetaStock Formula Primer
status: active
priority: 10
supports_explorer: true
function: Typical
aliases:
- text: Typical
  type: exact
  weight: 1.0
- text: typical price
  type: synonym
  weight: 0.85
- text: Typical function
  type: synonym
  weight: 0.85
- text: average of high low close
  type: synonym
  weight: 0.85
- text: HLC average
  type: synonym
  weight: 0.85
suggests:
- canonical_id: function.mov
  rationale: function.mov is often useful context for this card but is not always mandatory.
  priority: 40
  properties:
    source: registry_ready_transform
    formula_role: suggests
- canonical_id: reference.price_fields
  rationale: reference.price_fields is often useful context for this card but is not always mandatory.
  priority: 40
  properties:
    source: registry_ready_transform
    formula_role: suggests
semantic:
  concept_role: function
  mechanism: price_transform
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
  canonical_id: function.typical
  supports_explorer: true
  priority: 10
  properties:
    formula_role: price_transform
    supports_explorer: true
    source_path: functions/typical.md
    generated_schema_version: registry_ready_v2
---

# Typical

## Purpose

`Typical` returns the typical price indicator value, commonly equivalent to averaging high, low, and close. It is useful as a data array inside moving averages or bands.

## Syntax

```metastock
Typical()
```

## Parameters

- `No parameters`: The function takes empty parentheses

## Valid Examples

```metastock
Typical()
Mov(Typical(),20,S)
Typical() > Mov(Typical(),20,S)
```

## Common Mistakes

- Do not write `Typical` without parentheses.
- Do not pass parameters to `Typical()`.
- Do not confuse typical price with close unless the user explicitly wants close.

## Related Patterns

- None yet.

## Natural Language Mappings

Use this function when the user says:

- typical price
- Typical function
- average of high low close
- HLC average

## Assumptions

- Use this function only when the user request explicitly maps to this concept.

## Retrieval keywords

typical price, Typical function, average of high low close, HLC average, Typical, Typical().

## Test Queries

- Find stocks using Typical
