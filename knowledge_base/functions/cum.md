---
type: function
function: Cum
category: cumulative
source: MetaStock Formula Primer / Formula Primer II
priority: 10
status: active
aliases:
- cum
- cumulate
- running total
- bar count
requires:
- reference.price_fields
suggests:
- function.sum
registry:
  supports_explorer: true
  priority: 30
  properties:
    source_notes:
    - Formula Primer: Cum(DATA ARRAY) keeps a running total; Cum(1) counts loaded
        records.
  enabled: true
---

# Cum

## Purpose

`Cum` keeps a running cumulative total of a data array.

In this project, `Cum` is mainly used for advanced formulas such as:

- counting loaded bars with `Cum(1)`
- building stateful or date-aware calculations
- starting a custom calculation only after enough bars exist
- supporting advanced indicator formulas before they are simplified into Explorer-safe logic

## Syntax

```metastock
Cum(DATA ARRAY)
```

## Common formulas

Count loaded bars:

```metastock
Cum(1)
```

Cumulative volume:

```metastock
Cum(V)
```

Only signal after at least 50 bars are loaded:

```metastock
Cum(1) >= 50 AND C > Mov(C,50,S)
```

## Natural language mappings

Use this function when the user says:

- cumulative
- running total
- total since chart start
- count bars loaded
- bar number
- after enough bars
- only after N bars
- cumulative volume

## Explorer column usage

`Cum` can be shown as a column, but it is usually not useful as a result-table value unless the scan explicitly needs a running total.

Example:

```text
Column A: Cum(V)
Filter: ColA > 0
```

## Explorer examples

### Example 1: Require enough history before a 50-period MA condition

User request:

```text
Find stocks above the 50 day moving average only when enough bars are loaded
```

Explorer output:

```text
Column A: C
Column B: Mov(C,50,S)
Column C: Cum(1)
Filter: ColC >= 50 AND ColA > ColB
```

## What not to do

Do not use `Cum` as a substitute for `Sum` when the user asks for a rolling lookback.

Bad for last 5 bars:

```metastock
Cum(V)
```

Correct:

```metastock
Sum(V,5)
```

Do not use `Cum(1)` as a universal fix for missing data unless the condition actually requires a minimum bar count.

## Assumptions

- `Cum(1)` counts records loaded in the chart or exploration data context.
- Use `Sum(DATA ARRAY,N)` for rolling window totals.
- Use `Cum(DATA ARRAY)` for running totals from the first loaded bar.

## Related functions and concepts

- Sum: rolling sum
- BarsSince: time since an event
- ValueWhen: value at event occurrence
- PREV: previous calculated value

## Retrieval keywords

Cum, cumulate, cumulative total, running total, bar count, count loaded bars, Cum(1), cumulative volume, enough data, enough bars.

## Parameters

- `DATA ARRAY`: the value or condition to cumulate from the start of loaded data.


## Valid Examples

```metastock
Cum(1)
Cum(C > Mov(C,50,S))
Cum(V)
```


## Common Mistakes

- Do not use `Cum` when a fixed rolling window is needed; use `Sum(DATA ARRAY, PERIODS)` instead.
- Do not assume `Cum(1)` counts all history outside the loaded records.
- Do not write `CountBars()`; use `Cum(1)` for a running bar count.


## Related Patterns

- pattern.consecutive_condition


## Test Queries

- Create a bar count using Cum
- Count cumulative days where close is above moving average
