---
canonical_id: function.sin
title: Sin
type: function
card_bucket: functions
category: math_trigonometry
source: MetaStock Formula Primer
status: active
priority: 10
supports_explorer: true
function: Sin
aliases:
- text: Sin
  type: exact
  weight: 1.0
- text: sine function
  type: synonym
  weight: 0.85
- text: Sin function
  type: synonym
  weight: 0.85
- text: cycle sine formula
  type: synonym
  weight: 0.85
- text: trigonometric sine
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
  canonical_id: function.sin
  supports_explorer: true
  priority: 10
  properties:
    formula_role: math_trigonometry
    supports_explorer: true
    source_path: functions/sin.md
    generated_schema_version: registry_ready_v2
---

# Sin

## Purpose

`Sin` calculates sine. It is mainly for mathematical/custom cycle formulas, not standard Explorer scans.

## Syntax

```metastock
Sin(DATA ARRAY)
```

## Parameters

- `DATA ARRAY`: Angle input used by the sine calculation

## Valid Examples

```metastock
Sin(Cum(1))
Sin(Cum(360/17))
```

## Common Mistakes

- Do not retrieve `Sin` for normal price strength queries.
- Do not confuse `Sin` with signal line.
- Use only for explicit trigonometric or cycle formulas.

## Related Patterns

- None yet.

## Natural Language Mappings

Use this function when the user says:

- sine function
- Sin function
- cycle sine formula
- trigonometric sine

## Assumptions

- Use this function only when the user request explicitly maps to this concept.

## Retrieval keywords

sine function, Sin function, cycle sine formula, trigonometric sine, Sin, Sin(DATA ARRAY).

## Test Queries

- Find stocks using Sin
