---
canonical_id: reference.explorer_environment_limitations
title: Explorer Environment Limitations
type: reference
card_bucket: references
category: explorer_environment
source: generated_curated_from_primer
status: active
priority: 10
supports_explorer: true
aliases:
- text: Explorer limitations
  type: exact
  weight: 1.0
- text: MetaStock Explorer columns limitation
  type: phrase
  weight: 0.95
- text: ColA historical values
  type: phrase
  weight: 0.9
- text: Explorer cannot use future values
  type: phrase
  weight: 0.9
suggests:
- canonical_id: reference.lookahead_future_reference_pitfalls
  rationale: Explorer formulas must avoid future-looking references.
  priority: 30
  properties:
    formula_role: lookahead_validation
semantic:
  concept_role: reference
  mechanism: explorer_environment
  market_object: formula_environment
  outputs:
  - generation_rule
  - validation_rule
  supports_conditions:
  - environment_validation
  - syntax_validation
  does_not_cover:
  - specific_trading_signal_by_itself
registry:
  enabled: true
  canonical_id: reference.explorer_environment_limitations
  supports_explorer: true
  priority: 10
  properties:
    formula_role: explorer_environment
    source_path: references/explorer_environment_limitations.md
    curation_level: upgraded_to_curated_quality
---

# Explorer Environment Limitations

## Purpose

This card defines environment rules for generating MetaStock Explorer formulas. It prevents invalid column references, future-looking formulas, and System Tester-only constructs from entering Explorer output.

## Rules

- Explorer columns such as `ColA`, `ColB`, and `ColC` are last-value references for the exploration date.
- Do not treat `ColA` as a historical data array; avoid `Ref(ColA,-1)`, `Mov(ColA,20,S)`, and `Sum(ColA,5)`.
- Put historical logic inside the column formula itself, such as `Ref(C,-1)` or `Mov(C,20,S)`.
- Explorer formulas should not reference values after the exploration date.
- Define columns before referencing them in the filter.
- Use `AND` and `OR`, not programming operators such as `&&` or `||`.
- Use `=` for equality, not `==`.

## Examples

```metastock
Column A: C
Column B: Ref(C,-1)
Filter: ColA > ColB
Column A: Mov(C,20,S)
Column B: Ref(Mov(C,20,S),-1)
Filter: ColA > ColB
Column A: C
Column B: Mov(C,50,S)
Filter: ColA > ColB
```

## What Not To Do

- Bad: `Filter: Ref(ColA,-1) > ColB`.
- Bad: `Column A: C` then `Filter: ColB > 0` when Column B is undefined.
- Bad: `Filter: C > Ref(C,1)` for live Explorer scans.
- Bad: using `OPT1` or simulation functions in Explorer.

## Validation checklist

- Every `ColX` in the filter has a matching column definition.
- No historical function wraps a `ColX` reference.
- No positive `Ref(...,1)` unless explicitly marked as historical hindsight.
- No System Tester-only function appears in Explorer output.
- All formulas use MetaStock syntax, not Python/C syntax.

## Related functions and concepts

- template.explorer_columns_filter
- reference.lookahead_future_reference_pitfalls
- reference.system_tester_vs_explorer_limits



## Test Queries

- Why is Ref(ColA,-1) invalid in Explorer?
- Generate an Explorer filter using previous close safely.
