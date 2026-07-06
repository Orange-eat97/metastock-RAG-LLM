---
canonical_id: function.atan
title: Atan
type: function
card_bucket: functions
category: math_trigonometry
source: MetaStock Formula Primer
status: active
priority: 10
supports_explorer: true
function: Atan
aliases:
- text: Atan
  type: exact
  weight: 1.0
- text: arctangent function
  type: synonym
  weight: 0.85
- text: Atan function
  type: synonym
  weight: 0.85
- text: angle calculation
  type: synonym
  weight: 0.85
- text: slope angle formula
  type: synonym
  weight: 0.85
suggests:
- canonical_id: function.ref
  rationale: function.ref is often useful context for this card but is not always mandatory.
  priority: 40
  properties:
    source: registry_ready_transform
    formula_role: suggests
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
  canonical_id: function.atan
  supports_explorer: true
  priority: 10
  properties:
    formula_role: math_trigonometry
    supports_explorer: true
    source_path: functions/atan.md
    generated_schema_version: registry_ready_v2
---

# Atan

## Purpose

`Atan` calculates an arctangent-style angle from two inputs. It is rare and should only be used for explicit angle/slope calculations.

## Syntax

```metastock
Atan(DATA ARRAY 1, DATA ARRAY 2)
```

## Parameters

- `DATA ARRAY 1`: Y-like component or first value
- `DATA ARRAY 2`: X-like component or second value

## Valid Examples

```metastock
Atan(10,0)
Atan(C-Ref(C,-1),1)
```

## Common Mistakes

- Do not use `Atan` for ordinary trend filters.
- Do not confuse angle with price momentum.
- Use only when the user explicitly asks for angle or trigonometric logic.

## Related Patterns

- None yet.

## Natural Language Mappings

Use this function when the user says:

- arctangent function
- Atan function
- angle calculation
- slope angle formula

## Assumptions

- Use this function only when the user request explicitly maps to this concept.

## Retrieval keywords

arctangent function, Atan function, angle calculation, slope angle formula, Atan, Atan(DATA ARRAY 1, DATA ARRAY 2).

## Test Queries

- Find stocks using Atan
