---
canonical_id: reference.formula_reference_external_dependencies
title: Formula Reference External Dependencies
type: reference
card_bucket: references
category: formula_reference_external_dependencies
source: MetaStock Formula Primer / Formula Primer II / internal project rule
status: active
priority: 10
supports_explorer: true
aliases:
- text: Formula Reference External Dependencies
  type: exact
  weight: 1.0
- text: Fml external dependency
  type: synonym
  weight: 0.85
- text: FmlVar custom indicator dependency
  type: synonym
  weight: 0.85
- text: formula reference by name
  type: synonym
  weight: 0.85
- text: custom indicator must exist
  type: synonym
  weight: 0.85
requires:
- canonical_id: function.fml
  rationale: This card usually needs function.fml for correct formula generation.
  priority: 10
  properties:
    source: registry_ready_transform
    formula_role: requires
- canonical_id: function.fmlvar
  rationale: This card usually needs function.fmlvar for correct formula generation.
  priority: 10
  properties:
    source: registry_ready_transform
    formula_role: requires
semantic:
  concept_role: reference
  mechanism: formula_reference_external_dependencies
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
  canonical_id: reference.formula_reference_external_dependencies
  supports_explorer: true
  priority: 10
  properties:
    formula_role: formula_reference_external_dependencies
    supports_explorer: true
    source_path: references/formula_reference_external_dependencies.md
    generated_schema_version: registry_ready_v2
---

# Formula Reference External Dependencies

## Purpose

Explain that `Fml` and `FmlVar` depend on custom indicators and variables already existing in MetaStock.

## Rules

- `Fml("FORMULA_NAME")` requires an exact existing custom indicator name.
- `FmlVar("FORMULA_NAME","VARIABLE_NAME")` requires an exact existing formula and variable name.
- If a referenced formula or variable is renamed, all references must be updated.
- Generated Explorer formulas should avoid Fml/FmlVar unless the user explicitly names an existing custom indicator.

## Examples

```metastock
Fml("MyMACD")
FmlVar("MyIndicator","MyVariableA")
```

## What Not To Do

- Do not invent custom indicator names.
- Do not omit quotation marks.
- Do not assume built-in indicators expose FmlVar variables.

## Natural Language Mappings

- Fml external dependency
- FmlVar custom indicator dependency
- formula reference by name
- custom indicator must exist

## Retrieval keywords

Fml external dependency, FmlVar custom indicator dependency, formula reference by name, custom indicator must exist.

## Test Queries

- Fml external dependency
- FmlVar custom indicator dependency
