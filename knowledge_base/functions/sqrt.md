---
canonical_id: function.sqrt
title: Sqrt
type: function
card_bucket: functions
category: math
source: MetaStock Formula Primer
status: active
priority: 10
supports_explorer: true
function: Sqrt
aliases:
- text: Sqrt
  type: exact
  weight: 1.0
- text: square root
  type: synonym
  weight: 0.85
- text: Sqrt function
  type: synonym
  weight: 0.85
- text: root of variance
  type: synonym
  weight: 0.85
suggests:
- canonical_id: function.var
  rationale: function.var is often useful context for this card but is not always mandatory.
  priority: 40
  properties:
    source: registry_ready_transform
    formula_role: suggests
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
  canonical_id: function.sqrt
  supports_explorer: true
  priority: 10
  properties:
    formula_role: math
    supports_explorer: true
    source_path: functions/sqrt.md
    generated_schema_version: registry_ready_v2
---

# Sqrt

## Purpose

`Sqrt` calculates the square root of a data array. It is mainly used in custom mathematical formulas.

## Syntax

```metastock
Sqrt(DATA ARRAY)
```

## Parameters

- `DATA ARRAY`: Value or formula whose square root is needed

## Valid Examples

```metastock
Sqrt(C)
Sqrt(Var(C,20))
```

## Common Mistakes

- Do not take square root of negative values without guarding logic.
- Do not use `Sqrt` for percent changes unless mathematically intended.
- Do not write `SquareRoot()` unless a card defines it.

## Related Patterns

- None yet.

## Natural Language Mappings

Use this function when the user says:

- square root
- Sqrt function
- root of variance
- sqrt

## Assumptions

- Use this function only when the user request explicitly maps to this concept.

## Retrieval keywords

square root, Sqrt function, root of variance, sqrt, Sqrt, Sqrt(DATA ARRAY).

## Test Queries

- Find stocks using Sqrt
