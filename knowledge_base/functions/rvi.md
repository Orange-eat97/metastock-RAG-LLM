---
canonical_id: function.rvi
title: RVI
type: function
card_bucket: functions
category: volatility_momentum
source: MetaStock Formula Primer
status: active
priority: 10
supports_explorer: true
function: RVI
aliases:
- text: RVI
  type: abbreviation
  weight: 1.0
- text: Relative Volatility Index
  type: synonym
  weight: 0.85
- text: RVI indicator
  type: synonym
  weight: 0.85
- text: RVI above 50
  type: phrase
  weight: 0.9
- text: RVI rising
  type: synonym
  weight: 0.85
- text: relative volatility confirmation
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
  mechanism: volatility_momentum
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
  canonical_id: function.rvi
  supports_explorer: true
  priority: 10
  properties:
    formula_role: volatility_momentum
    supports_explorer: true
    source_path: functions/rvi.md
    generated_schema_version: registry_ready_v2
---

# RVI

## Purpose

`RVI` returns the Relative Volatility Index. It is used when the user explicitly asks for RVI or relative volatility confirmation.

## Syntax

```metastock
RVI(PERIODS)
```

## Parameters

- `PERIODS`: Lookback period, commonly 14

## Valid Examples

```metastock
RVI(14)
RVI(14) > 50
RVI(14) > Ref(RVI(14),-1)
```

## Common Mistakes

- Do not confuse `RVI` with RSI.
- Do not use RVI for volume; it is a volatility index.
- Do not use broad volatility aliases that should retrieve ATR or Stdev instead.

## Related Patterns

- None yet.

## Natural Language Mappings

Use this function when the user says:

- Relative Volatility Index
- RVI indicator
- RVI above 50
- RVI rising
- relative volatility confirmation

## Assumptions

- Use this function only when the user request explicitly maps to this concept.

## Retrieval keywords

Relative Volatility Index, RVI indicator, RVI above 50, RVI rising, relative volatility confirmation, RVI, RVI(PERIODS).

## Test Queries

- Find stocks using RVI
