---
canonical_id: function.fml
title: Fml
type: function
card_bucket: functions
category: formula_reference
source: generated_curated_from_primer
status: active
priority: 10
supports_explorer: true
function: Fml
aliases:
- text: Fml
  type: exact
  weight: 1.0
- text: formula call
  type: exact
  weight: 0.95
- text: reference another indicator
  type: phrase
  weight: 0.9
- text: custom formula reference
  type: phrase
  weight: 0.9
suggests:
- canonical_id: reference.formula_reference_external_dependencies
  rationale: Fml depends on external formula names and installed custom indicators.
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
  canonical_id: function.fml
  supports_explorer: true
  priority: 10
  properties:
    formula_role: formula_reference
    source_path: functions/fml.md
    curation_level: upgraded_to_curated_quality
---

# Fml

## Purpose

`Fml` includes the calculated value of another named formula. It is useful when an Explorer needs to reuse a custom indicator already defined in MetaStock. It creates an external dependency on the exact formula name.

## Syntax

```metastock
Fml("FORMULA_NAME")
```

## Parameters

| Parameter | Meaning | Common values |
|---|---|---|
| `"FORMULA_NAME"` | Exact name of the formula to call. Must be quoted. | `"My Indicator"` |

## Default interpretation

Do not invent custom formula names. Use `Fml()` only when the user provides the exact indicator/formula name or when your app has stored a known formula dependency.

## Common formulas

```metastock
Fml("My Indicator")
Fml("Market Filter") > 0
Cross(C,Fml("My Moving Average"))
```

## Natural language mappings

Use this function when the user says:

- Fml
- formula call
- use my custom indicator
- reference existing indicator
- custom formula value

## Explorer column usage

In Explorer, use Fml only when the named custom formula exists in the user’s MetaStock environment. Prefer explicit formulas for portable generated Explorers.

## Explorer examples

### Example 1: Use known custom indicator

User request:

```text
Find stocks where my custom indicator Market Filter is positive
```

Explorer output:

```text
Column A: Fml("Market Filter")
Filter: ColA > 0
```

## Filter-only usage

If the user only needs a pass/fail condition and does not need to inspect intermediate values, the function may be used directly in the Filter. For this project, prefer columns when the value helps the result table or when a pattern has multiple logical components.

## Valid Examples

```metastock
Fml("My Indicator")
Fml("Market Filter") > 0
```

## Common Mistakes

- Bad: `Fml(My Indicator)` without quotes. Correct: `Fml("My Indicator")`.
- Bad: inventing a formula name that does not exist.
- Bad: forgetting that renaming the source formula breaks Fml references.
- Bad: expecting Fml to return all plotted lines of a multi-line indicator; references may only use the formula result exposed by MetaStock.

## Assumptions

- Formula name must be exact and quoted.
- The referenced formula must exist in MetaStock.
- Prefer explicit formula code when portability matters.

## Related Patterns

- function.fmlvar
- reference.formula_reference_external_dependencies

## Related functions and concepts

- Explorer columns and filters
- Price fields such as `C`, `H`, `L`, `O`, and `V`
- `Cross` when the user asks for a crossing event
- `Ref` when the user asks for previous-bar or prior-event logic



## Retrieval keywords

Fml, formula call, custom indicator, external dependency.

## Test Queries

- Use my custom indicator Market Filter in an Explorer
