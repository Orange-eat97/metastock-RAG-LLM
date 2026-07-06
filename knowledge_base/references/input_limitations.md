---
canonical_id: reference.input_limitations
title: Input() Limitations
type: reference
card_bucket: references
category: input_limitations
source: MetaStock Formula Primer / Formula Primer II / internal project rule
status: active
priority: 10
supports_explorer: false
aliases:
- text: Input() Limitations
  type: exact
  weight: 1.0
- text: Input limitation
  type: synonym
  weight: 0.85
- text: Input not Explorer
  type: synonym
  weight: 0.85
- text: custom indicator prompt
  type: synonym
  weight: 0.85
- text: six inputs limit
  type: synonym
  weight: 0.85
- text: Fml Input default value
  type: synonym
  weight: 0.85
requires:
- canonical_id: function.input
  rationale: This card usually needs function.input for correct formula generation.
  priority: 10
  properties:
    source: registry_ready_transform
    formula_role: requires
semantic:
  concept_role: reference
  mechanism: input_limitations
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
  canonical_id: reference.input_limitations
  supports_explorer: false
  priority: 10
  properties:
    formula_role: input_limitations
    supports_explorer: false
    source_path: references/input_limitations.md
    generated_schema_version: registry_ready_v2
---

# Input() Limitations

## Purpose

Explain why `Input()` should generally not be generated for Explorer formulas in this project.

## Rules

- `Input()` is supported by the Custom Indicator Builder, not normal Explorer generation.
- A custom indicator can have up to six inputs.
- When a formula containing Input is referenced by Fml, the default value is used.
- Prefer fixed constants in generated Explorer formulas unless the user is explicitly creating a custom indicator.

## Examples

```metastock
periods:=Input("periods",1,100,14);
Mov(C,periods,S)
Mov(C,50,S) {preferred fixed Explorer version}
```

## What Not To Do

- Do not place `Input()` directly into Explorer filters generated for automation.
- Do not assume the Explorer will prompt the user for Input values.
- Do not exceed six inputs in custom indicators.

## Natural Language Mappings

- Input limitation
- Input not Explorer
- custom indicator prompt
- six inputs limit
- Fml Input default value

## Retrieval keywords

Input limitation, Input not Explorer, custom indicator prompt, six inputs limit, Fml Input default value.

## Test Queries

- Input limitation
- Input not Explorer
