---
type: function
function: ROC
category: momentum
source: MetaStock Formula Primer
priority: 10
status: active
aliases:
- rate of change
- ROC
- percent change
- point change
requires:
- reference.price_fields
- function.ref
suggests:
- template.explorer_columns_filter
registry:
  supports_explorer: true
  priority: 20
  properties:
    source_notes:
    - Formula Primer: Rate of Change, roc(DATA ARRAY, PERIODS, DIFF_METHOD), percent
        and points.
  enabled: true
---

# ROC

## Purpose

`ROC` calculates the rate of change of a data array over a lookback period.

In this project, `ROC` is mainly used for Explorer filters such as:

- price momentum
- close has risen over N bars
- close has fallen by a percentage
- moving average is rising or falling
- volume or indicator rate of change

## Syntax

```metastock
ROC(DATA ARRAY, PERIODS, DIFF_METHOD)
```

## Parameters

| Parameter | Meaning | Common values |
|---|---|---|
| DATA ARRAY | Series to compare against its prior value | `C`, `V`, `Mov(C,20,S)`, `RSI(14)` |
| PERIODS | Lookback distance | `1`, `3`, `5`, `20` |
| DIFF_METHOD | Difference method | `%` for percent, `$` for points |

## Common formulas

One-bar point change in close:

```metastock
ROC(C,1,$)
```

Three-bar percentage change in close:

```metastock
ROC(C,3,%)
```

Close up more than 5 percent over 20 bars:

```metastock
ROC(C,20,%) > 5
```

20-period moving average rising from previous bar:

```metastock
ROC(Mov(C,20,S),1,$) > 0
```

## Natural language mappings

Use this function when the user says:

- rate of change
- ROC
- percent change
- price change over N days
- close has risen 5 percent
- close has dropped 5 percent
- momentum is positive
- moving average is rising
- moving average is falling
- volume increased by percent
- three day return
- one day change

## Explorer column usage

Momentum column:

```text
Column A: ROC(C,20,%)
Filter: ColA > 5
```

Moving average slope column:

```text
Column A: ROC(Mov(C,20,S),1,$)
Filter: ColA > 0
```

## Explorer examples

### Example 1: Positive 20-day momentum

User request:

```text
Find stocks up more than 5 percent over the last 20 days
```

Explorer output:

```text
Column A: ROC(C,20,%)
Filter: ColA > 5
```

### Example 2: Moving average rising

User request:

```text
Find stocks where the 20 day moving average is rising
```

Explorer output:

```text
Column A: ROC(Mov(C,20,S),1,$)
Filter: ColA > 0
```

## What not to do

Do not use `ROC(C,3,%) < -5` when the user asks for point movement. Use `$` for point difference.

Bad for point change:

```metastock
ROC(C,3,%) < -5
```

Correct:

```metastock
ROC(C,3,$) < -5
```

Do not invent `RateOfChange()`.

Correct:

```metastock
ROC(C,20,%)
```

## Assumptions

- If the user says percentage change, use `%`.
- If the user says point change, use `$`.
- If the user says rising without a percent threshold, use `ROC(DATA ARRAY,1,$) > 0`.

## Related functions and concepts

- Ref: explicit previous value comparison
- Mov: moving average slope
- RSI: momentum threshold
- Sum: repeated positive momentum

## Retrieval keywords

ROC, rate of change, percent change, percentage change, point change, return over N days, price momentum, rising moving average, falling moving average, ROC(C,20,%), ROC(C,1,$).

## Valid Examples

```metastock
ROC(C,1,$)
ROC(C,12,%)
ROC(Mov(C,20,S),1,$) > 0
```


## Common Mistakes

- Do not omit the difference method.
- Use `%` for percent change and `$` for point change.
- Do not write `RateOfChange(C,12)`; use `ROC(C,12,%)` or `ROC(C,12,$)`.


## Related Patterns

- pattern.rsi_recovery
- pattern.ma_support_bounce


## Test Queries

- Find stocks where rate of change is positive
- Find stocks where close gained more than 5 percent over 3 bars
