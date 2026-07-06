---
canonical_id: function.wilders
title: Wilders
type: function
card_bucket: functions
category: smoothing
source: MetaStock Formula Primer / Formula Primer II
status: active
priority: 10
supports_explorer: true
function: Wilders
aliases:
- text: Wilders
  type: exact
  weight: 1.0
- text: Wilder smoothing
  type: synonym
  weight: 0.85
- text: Wilder's smoothing
  type: synonym
  weight: 0.85
- text: Wilder average
  type: synonym
  weight: 0.85
- text: Wilder style average
  type: synonym
  weight: 0.85
- text: custom RSI calculation
  type: synonym
  weight: 0.85
- text: custom ATR calculation
  type: synonym
  weight: 0.85
- text: smooth using Wilder method
  type: synonym
  weight: 0.85
suggests:
- canonical_id: function.atr
  rationale: function.atr is often useful context for this card but is not always mandatory.
  priority: 40
  properties:
    source: registry_ready_transform
    formula_role: suggests
- canonical_id: function.rsi
  rationale: function.rsi is often useful context for this card but is not always mandatory.
  priority: 40
  properties:
    source: registry_ready_transform
    formula_role: suggests
- canonical_id: reference.price_fields
  rationale: reference.price_fields is optional helper context for examples involving this function.
  priority: 40
  properties:
    source: converted_from_old_function_requires
    formula_role: suggests
semantic:
  concept_role: function
  mechanism: smoothing
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
  canonical_id: function.wilders
  supports_explorer: true
  priority: 10
  properties:
    source_notes:
    - Formula Primer: Wilders(DATA ARRAY, PERIODS) calculates Wilder's Smoothing.
    - Formula Primer II: Wilder smoothing starts with a simple average and then uses prior average plus current contribution.
    source_path: functions/wilders.md
    generated_schema_version: registry_ready_v2
---

# Wilders

## Purpose

`Wilders` calculates Wilder's Smoothing of a data array.

In this project, `Wilders` is mainly used for advanced formulas that recreate or customize Wilder-style indicators, including ATR-like and RSI-like calculations.

## Syntax

```metastock
Wilders(DATA ARRAY, PERIODS)
```

## Common formulas

Wilder smoothing of close:

```metastock
Wilders(C,14)
```

Wilder smoothing of positive one-bar changes:

```metastock
Wilders(If(ROC(C,1,$)>0, ROC(C,1,$), 0), 14)
```

## Natural language mappings

Use this function when the user says:

- Wilder smoothing
- Wilder's smoothing
- Wilder average
- Wilder style average
- custom RSI calculation
- custom ATR calculation
- smooth using Wilder method

## Explorer column usage

Wilder smoothed close:

```text
Column A: Wilders(C,14)
Filter: ColA > Ref(ColA,-1)
```

Better Explorer-safe version avoiding historical `ColA` reference:

```text
Column A: Wilders(C,14)
Column B: Ref(Wilders(C,14),-1)
Filter: ColA > ColB
```

## What not to do

Do not use `Wilders` when the user simply asks for a normal moving average.

Use this for simple moving average:

```metastock
Mov(C,14,S)
```

Use this for exponential moving average:

```metastock
Mov(C,14,E)
```

Do not reference `Ref(ColA,-1)` in Explorer filters. Put the `Ref` inside a column.

## Assumptions

- Use `Wilders` only when the user explicitly asks for Wilder smoothing or when recreating Wilder-style indicators.
- For common user queries, prefer built-in `RSI(14)` or `ATR(14)` over manually rebuilding the indicator.

## Related functions and concepts

- ATR: Wilder-style volatility indicator
- RSI: Wilder-style momentum indicator
- If: separating positive and negative changes
- ROC: price change input
- PREV: manual smoothing logic

## Retrieval keywords

Wilders, Wilder's smoothing, Wilder smoothing, Wilder average, custom RSI, custom ATR, smooth using Wilder method, Wilders(C,14), Wilders(If(ROC(C,1,$)>0,ROC(C,1,$),0),14).

## Parameters

- `DATA ARRAY`: the series to smooth.
- `PERIODS`: number of periods for Wilder smoothing.


## Valid Examples

```metastock
Wilders(C,14)
Wilders(If(ROC(C,1,$)>0,ROC(C,1,$),0),14)
```


## Common Mistakes

- Do not confuse `Wilders` with a simple moving average.
- Do not write `Wilder(C,14)`; use `Wilders(C,14)`.
- Do not use it when the user specifically asks for SMA or EMA.


## Related Patterns

- pattern.rsi_recovery


## Test Queries

- Calculate Wilder smoothing of close
- Build a custom RSI style formula with Wilders
