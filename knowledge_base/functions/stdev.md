---
canonical_id: function.stdev
title: Stdev
type: function
card_bucket: functions
category: statistical_volatility
source: MetaStock Formula Primer
status: active
priority: 10
supports_explorer: true
function: Stdev
aliases:
- text: Stdev
  type: exact
  weight: 1.0
- text: standard deviation
  type: synonym
  weight: 0.85
- text: standard deviation of close
  type: synonym
  weight: 0.85
- text: price volatility by standard deviation
  type: synonym
  weight: 0.85
- text: standard deviation band
  type: synonym
  weight: 0.85
suggests:
- canonical_id: function.mov
  rationale: function.mov is often useful context for this card but is not always mandatory.
  priority: 40
  properties:
    source: registry_ready_transform
    formula_role: suggests
- canonical_id: function.ref
  rationale: function.ref is often useful context for this card but is not always mandatory.
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
  canonical_id: function.stdev
  supports_explorer: true
  priority: 10
  properties:
    formula_role: statistical_volatility
    supports_explorer: true
    source_path: functions/stdev.md
    generated_schema_version: registry_ready_v2
---

# Stdev

## Purpose

`Stdev` calculates standard deviation over a lookback period. It supports volatility contraction, volatility expansion, and standard-deviation band patterns.

## Syntax

```metastock
Stdev(DATA ARRAY, PERIODS)
```

## Parameters

- `DATA ARRAY`: Series to measure, such as `C`
- `PERIODS`: Lookback period, commonly 20

## Valid Examples

```metastock
Stdev(C,20)
Stdev(C,20) < Ref(Stdev(C,20),-1)
C > Mov(C,20,S) + 2 * Stdev(C,20)
```

## Common Mistakes

- Do not write `StdDev` unless a supported card defines that spelling.
- Do not use `Stdev` without a data array and period.
- Do not confuse statistical volatility with volume.

## Related Patterns

- pattern.volatility_contraction
- pattern.standard_deviation_breakout

## Natural Language Mappings

Use this function when the user says:

- standard deviation
- Stdev
- standard deviation of close
- price volatility by standard deviation
- standard deviation band

## Assumptions

- Use this function only when the user request explicitly maps to this concept.

## Retrieval keywords

standard deviation, Stdev, standard deviation of close, price volatility by standard deviation, standard deviation band, Stdev, Stdev(DATA ARRAY, PERIODS).

## Test Queries

- Find stocks using Stdev
