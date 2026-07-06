---
type: function
function: Wilders
category: smoothing
source: MetaStock Formula Primer / Formula Primer II
priority: 10
status: active
aliases:
- Wilder smoothing
- Wilder's smoothing
- Wilders
- Wilder average
requires:
- reference.price_fields
suggests:
- function.atr
- function.rsi
registry:
  supports_explorer: true
  priority: 35
  properties:
    source_notes:
    - Formula Primer: Wilders(DATA ARRAY, PERIODS) calculates Wilder's Smoothing.
    - Formula Primer II: Wilder smoothing starts with a simple average and then uses
        prior average plus current contribution.
  enabled: true
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
