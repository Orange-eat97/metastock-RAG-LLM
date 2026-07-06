---
canonical_id: function.stochmomentum
title: StochMomentum
type: function
card_bucket: functions
category: momentum_oscillator
source: MetaStock Formula Primer
status: active
priority: 10
supports_explorer: true
function: StochMomentum
aliases:
- text: StochMomentum
  type: exact
  weight: 1.0
- text: stochastic momentum index
  type: synonym
  weight: 0.85
- text: SMI indicator
  type: synonym
  weight: 0.85
- text: stoch momentum
  type: synonym
  weight: 0.85
- text: stochastic momentum crosses above zero
  type: phrase
  weight: 0.9
suggests:
- canonical_id: function.cross
  rationale: function.cross is often useful context for this card but is not always mandatory.
  priority: 40
  properties:
    source: registry_ready_transform
    formula_role: suggests
semantic:
  concept_role: function
  mechanism: momentum_oscillator
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
  canonical_id: function.stochmomentum
  supports_explorer: true
  priority: 10
  properties:
    formula_role: momentum_oscillator
    supports_explorer: true
    source_path: functions/stochmomentum.md
    generated_schema_version: registry_ready_v2
---

# StochMomentum

## Purpose

`StochMomentum` returns the Stochastic Momentum Index value. It is used when the user explicitly asks for SMI or stochastic momentum.

## Syntax

```metastock
StochMomentum(PERIODS, SMOOTHING, DOUBLE SMOOTHING)
```

## Parameters

- `PERIODS`: Lookback period
- `SMOOTHING`: First smoothing period
- `DOUBLE SMOOTHING`: Second smoothing period

## Valid Examples

```metastock
StochMomentum(14,3,3)
StochMomentum(14,3,3) > 0
Cross(StochMomentum(14,3,3),0)
```

## Common Mistakes

- Do not confuse `StochMomentum` with `Stoch`.
- Do not omit smoothing parameters.
- Use only when the user asks for stochastic momentum or SMI, not ordinary stochastic oscillator.

## Related Patterns

- pattern.stochastic_oversold_recovery

## Natural Language Mappings

Use this function when the user says:

- stochastic momentum index
- SMI indicator
- stoch momentum
- stochastic momentum crosses above zero
- StochMomentum

## Assumptions

- Use this function only when the user request explicitly maps to this concept.

## Retrieval keywords

stochastic momentum index, SMI indicator, stoch momentum, stochastic momentum crosses above zero, StochMomentum, StochMomentum, StochMomentum(PERIODS, SMOOTHING, DOUBLE SMOOTHING).

## Test Queries

- Find stocks using StochMomentum
