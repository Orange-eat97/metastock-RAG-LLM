---
canonical_id: function.var
title: Var
type: function
card_bucket: functions
category: statistical_volatility
source: MetaStock Formula Primer
status: active
priority: 10
supports_explorer: true
function: Var
aliases:
- text: Var
  type: exact
  weight: 1.0
- text: variance
  type: exact
  weight: 1.0
- text: Var function
  type: synonym
  weight: 0.85
- text: statistical variance
  type: synonym
  weight: 0.85
- text: variance of close
  type: synonym
  weight: 0.85
suggests:
- canonical_id: function.ref
  rationale: function.ref is often useful context for this card but is not always mandatory.
  priority: 40
  properties:
    source: registry_ready_transform
    formula_role: suggests
- canonical_id: function.stdev
  rationale: function.stdev is often useful context for this card but is not always mandatory.
  priority: 40
  properties:
    source: registry_ready_transform
    formula_role: suggests
semantic:
  concept_role: function
  mechanism: statistical_volatility
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
  canonical_id: function.var
  supports_explorer: true
  priority: 10
  properties:
    formula_role: statistical_volatility
    supports_explorer: true
    source_path: functions/var.md
    generated_schema_version: registry_ready_v2
---

# Var

## Purpose

`Var` calculates statistical variance over a lookback period. It is usually less directly useful than standard deviation, but supports statistical-volatility formulas.

## Syntax

```metastock
Var(DATA ARRAY, PERIODS)
```

## Parameters

- `DATA ARRAY`: Series to measure, such as `C`
- `PERIODS`: Lookback period

## Valid Examples

```metastock
Var(C,20)
Var(C,20) > Ref(Var(C,20),-1)
```

## Common Mistakes

- Do not confuse `Var` with moving-average method `VAR` used inside `Mov`.
- Do not write `Variance(C,20)` unless a supported card defines it.
- Variance is not the same scale as price; avoid direct price comparisons.

## Related Patterns

- None yet.

## Natural Language Mappings

Use this function when the user says:

- variance
- Var function
- statistical variance
- variance of close

## Assumptions

- Use this function only when the user request explicitly maps to this concept.

## Retrieval keywords

variance, Var function, statistical variance, variance of close, Var, Var(DATA ARRAY, PERIODS).

## Test Queries

- Find stocks using Var
