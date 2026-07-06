---
canonical_id: function.cos
title: Cos
type: function
card_bucket: functions
category: math_trigonometry
source: MetaStock Formula Primer
status: active
priority: 10
supports_explorer: true
function: Cos
aliases:
- text: Cos
  type: exact
  weight: 1.0
- text: cosine function
  type: synonym
  weight: 0.85
- text: Cos function
  type: synonym
  weight: 0.85
- text: cycle cosine formula
  type: synonym
  weight: 0.85
- text: trigonometric cosine
  type: synonym
  weight: 0.85
semantic:
  concept_role: function
  mechanism: math_trigonometry
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
  canonical_id: function.cos
  supports_explorer: true
  priority: 10
  properties:
    formula_role: math_trigonometry
    supports_explorer: true
    source_path: functions/cos.md
    generated_schema_version: registry_ready_v2
---

# Cos

## Purpose

`Cos` calculates cosine. It is mainly for mathematical/custom cycle formulas, not standard Explorer scans.

## Syntax

```metastock
Cos(DATA ARRAY)
```

## Parameters

- `DATA ARRAY`: Angle input used by the cosine calculation

## Valid Examples

```metastock
Cos(Cum(1))
Cos(Cum(360/17))
```

## Common Mistakes

- Do not retrieve `Cos` for normal crossover queries.
- Do not confuse `Cos` with close `C`.
- Use only for explicit trigonometric or cycle formulas.

## Related Patterns

- None yet.

## Natural Language Mappings

Use this function when the user says:

- cosine function
- Cos function
- cycle cosine formula
- trigonometric cosine

## Assumptions

- Use this function only when the user request explicitly maps to this concept.

## Retrieval keywords

cosine function, Cos function, cycle cosine formula, trigonometric cosine, Cos, Cos(DATA ARRAY).

## Test Queries

- Find stocks using Cos
