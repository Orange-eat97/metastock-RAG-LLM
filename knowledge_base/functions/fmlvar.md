---
canonical_id: function.fmlvar
title: FmlVar
type: function
card_bucket: functions
category: formula_reference
source: generated_curated_from_primer
status: active
priority: 10
supports_explorer: true
function: FmlVar
aliases:
- text: FmlVar
  type: exact
  weight: 1.0
- text: formula variable call
  type: exact
  weight: 0.95
- text: reference variable from formula
  type: phrase
  weight: 0.9
- text: custom formula variable
  type: phrase
  weight: 0.9
suggests:
- canonical_id: function.fml
  rationale: FmlVar is related to calling external formulas.
  priority: 30
  properties:
    formula_role: formula_reference
- canonical_id: reference.formula_reference_external_dependencies
  rationale: FmlVar depends on external formula and variable names.
  priority: 30
  properties:
    formula_role: external_dependency
semantic:
  concept_role: function
  mechanism: formula_reference
  market_object: price
  outputs:
  - indicator_series
  supports_conditions:
  - threshold_comparison
  - crossover
  - state_filter
  does_not_cover:
  - complete_trading_pattern_by_itself
registry:
  enabled: true
  canonical_id: function.fmlvar
  supports_explorer: true
  priority: 10
  properties:
    formula_role: formula_reference
    source_path: functions/fmlvar.md
    curation_level: upgraded_to_curated_quality
---

# FmlVar

## Purpose

`FmlVar` retrieves a named variable from another formula. It is useful for advanced modular formulas but creates a strong dependency on the exact formula name and variable name.

## Syntax

```metastock
FmlVar("FORMULA_NAME", "VARIABLE_NAME")
```

## Parameters

| Parameter | Meaning | Common values |
|---|---|---|
| `"FORMULA_NAME"` | Exact source formula name. | `"My Formula"` |
| `"VARIABLE_NAME"` | Exact variable name inside the source formula. | `"signal"` |

## Default interpretation

Use `FmlVar` only when both the formula name and variable name are known. Do not invent either field.

## Common formulas

```metastock
FmlVar("My Formula","signal")
FmlVar("Trend Model","trend") = 1
```

## Natural language mappings

Use this function when the user says:

- FmlVar
- formula variable call
- use variable from custom indicator
- reference variable from another formula

## Explorer column usage

FmlVar can make generated Explorers non-portable. Prefer explicit formulas unless the user intentionally references an existing custom formula variable.

## Explorer examples

### Example 1: Use known variable from formula

User request:

```text
Find stocks where variable trend from my formula Trend Model equals 1
```

Explorer output:

```text
Column A: FmlVar("Trend Model","trend")
Filter: ColA = 1
```

## Filter-only usage

If the user only needs a pass/fail condition and does not need to inspect intermediate values, the function may be used directly in the Filter. For this project, prefer columns when the value helps the result table or when a pattern has multiple logical components.

## Valid Examples

```metastock
FmlVar("Trend Model","trend")
FmlVar("My Formula","signal") = 1
```

## Common Mistakes

- Bad: `FmlVar(Trend Model,trend)` without quotes.
- Bad: inventing a variable name.
- Bad: renaming the source formula or variable without updating FmlVar.
- Bad: using FmlVar when the user expects a self-contained Explorer.

## Assumptions

- Both names must be exact and quoted.
- The source formula must exist and expose the variable.
- Use only when portability is less important than reuse.

## Related Patterns

- function.fml
- reference.formula_reference_external_dependencies

## Related functions and concepts

- Explorer columns and filters
- Price fields such as `C`, `H`, `L`, `O`, and `V`
- `Cross` when the user asks for a crossing event
- `Ref` when the user asks for previous-bar or prior-event logic



## Retrieval keywords

FmlVar, formula variable, custom indicator variable, external formula dependency.

## Test Queries

- Use variable signal from my custom formula in an Explorer
