---
type: function
function: Sum
category: aggregation
source: MetaStock Formula Primer
priority: 10
status: active
aliases:
- summation
- total over periods
- count consecutive conditions
requires:
- reference.price_fields
suggests:
- template.explorer_columns_filter
registry:
  supports_explorer: true
  priority: 20
  properties:
    source_notes:
    - Formula Primer: Summation, Sum(DATA ARRAY, PERIODS), consecutive values, includes
        current period.
  enabled: true
---

# Sum

## Purpose

`Sum` calculates the cumulative sum of a data array over a fixed lookback period.

In this project, `Sum` is mainly used for Explorer filters such as:

- total volume over several bars
- count how many times a condition was true over the last N bars
- require a condition to hold for several consecutive bars
- measure confirmation frequency before a breakout or crossover

## Syntax

```metastock
Sum(DATA ARRAY, PERIODS)
```

## Parameters

| Parameter | Meaning | Common values |
|---|---|---|
| DATA ARRAY | Numeric series or logical condition to sum | `V`, `C > Mov(C,20,S)`, `RSI(14) > Ref(RSI(14),-1)` |
| PERIODS | Number of periods to include, including the current period | `3`, `5`, `10`, `20` |

## Common formulas

Five-period total volume:

```metastock
Sum(V,5)
```

Close above 20-period moving average for five consecutive bars:

```metastock
Sum(C > Mov(C,20,S),5) = 5
```

At least three up closes in the last five bars:

```metastock
Sum(C > Ref(C,-1),5) >= 3
```

RSI rising for three bars:

```metastock
Sum(RSI(14) > Ref(RSI(14),-1),3) = 3
```

## Natural language mappings

Use this function when the user says:

- sum
- total
- cumulative sum
- total volume over five days
- last N bars all true
- for five consecutive bars
- for at least three of the last five days
- condition has been true for N periods
- close above moving average for five days
- count how many times a condition occurred
- confirmation over the last N bars

## Explorer column usage

For a consecutive-condition scan, define the summed condition as an Explorer column when the count is useful to inspect.

Example:

```text
Column A: Sum(C > Mov(C,20,S),5)
Filter: ColA = 5
```

For a pure filter, the direct formula is also acceptable:

```metastock
Sum(C > Mov(C,20,S),5) = 5
```

## Explorer examples

### Example 1: Close above 20 MA for five consecutive bars

User request:

```text
Find stocks where close has stayed above the 20 day moving average for five days
```

Explorer output:

```text
Column A: Sum(C > Mov(C,20,S),5)
Filter: ColA = 5
```

### Example 2: At least three up closes in the last five bars

User request:

```text
Find stocks that closed higher than yesterday on at least three of the last five days
```

Explorer output:

```text
Column A: Sum(C > Ref(C,-1),5)
Filter: ColA >= 3
```

## What not to do

Do not use `Sum` when the user asks for a moving average unless the formula intentionally computes an average.

Bad:

```metastock
Sum(C,20)
```

Correct for 20-period average close:

```metastock
Mov(C,20,S)
```

Do not forget that logical expressions contribute `1` when true and `0` when false.

## Assumptions

- `Sum(condition,N)=N` means the condition is true for all N bars.
- `Sum(condition,N)>=K` means the condition is true at least K times in the last N bars.
- The lookback includes the current bar.

## Related functions and concepts

- Mov: average over periods
- Ref: previous bar comparisons
- If: explicit conditional values
- BarsSince: time since an event occurred
- Consecutive Condition pattern

## Retrieval keywords

Sum, summation, total volume, cumulative sum, consecutive bars, condition true for N bars, at least N days, count condition, confirmation count, Sum(C > Mov(C,20,S),5)=5.

## Valid Examples

```metastock
Sum(C > Mov(C,20,S),5) = 5
Sum(V > Mov(V,20,S),10) >= 7
Sum(C,14) / 14
```


## Common Mistakes

- Do not use `Sum` as a cumulative total; use `Cum` for cumulative-from-start logic.
- Do not forget that summing true/false conditions counts true bars.
- Do not write `Count(condition,N)`; use `Sum(condition,N)`.


## Related Patterns

- pattern.consecutive_condition
- pattern.ma_support_bounce


## Test Queries

- Find stocks above the 20 day moving average for five consecutive bars
- Count how many of the last ten bars had volume above average
